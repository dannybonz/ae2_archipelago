from typing import Optional, Set, Dict, Any
import asyncio, multiprocessing, traceback

from CommonClient import ClientCommandProcessor, CommonContext, get_base_parser, logger, server_loop, gui_enabled
from NetUtils import ClientStatus
import Utils

from .Interface import AE2Interface
from .Items import item_name_from_id
from .Levels import level_from_name

from kvui import MDLabel, MDGridLayout
from kivy.metrics import dp

class AE2CommandProcessor(ClientCommandProcessor):
    def __init__(self, ctx: CommonContext) -> None:
        super().__init__(ctx)

class AE2Context(CommonContext):
    client_version: str = "v1.0.0"

    game: str = "Ape Escape 2"

    command_processor = AE2CommandProcessor
    items_handling = 0b111

    interface_sync_task : asyncio.tasks = None
    last_error_message : Optional[str] = None

    slot_data: Dict[str, Any]

    def __init__(self, address, password: str) -> None:
        super().__init__(address, password)
        Utils.init_logging(f"Ape Escape 2 Archipelago Client {self.client_version}")
        self.interface = AE2Interface(logger)
        self.most_recent_instruction = None
        self.connection_state = "none"

    def on_package(self, cmd: str, args: Dict[str, Any]) -> None:
        #Connected to server
        if cmd == "Connected":
            #Init
            self.slot_data = args["slot_data"]  
            self.previously_checked_locations = args["checked_locations"]
            self.processed_items = 0
            self.previously_processed_items = -1
            self.sent_deaths = 0
            self.deathlink_pending = False
            self.connection_state = "request"
            self.reported_all_monkeys = False

            #Set up game
            self.interface.reset()
            self.interface.world_key_requirements = self.slot_data["world_key_requirements"]
            self.interface.character = self.slot_data["character"]
            self.deathlink_enabled = self.slot_data["deathlink_enabled"]
            self.interface.deathlink_enabled = self.deathlink_enabled

            display_connection_status_labels(self)

        #Data Storage retrieved
        if cmd == "Retrieved" and self.connection_state == "requested":
            if "keys" in args:
                if f"ae2_processed_{self.team}_{self.slot}" in args["keys"]:
                    self.previously_processed_items = args["keys"].get(f"ae2_processed_{self.team}_{self.slot}", 0)
                    if self.previously_processed_items == None:
                        self.previously_processed_items = 0
                else:
                    self.previously_processed_items = 0

                if f"ae2_caught_{self.team}_{self.slot}" in args["keys"]:
                    caught_monkeys = args["keys"].get(f"ae2_caught_{self.team}_{self.slot}", {})
                    if caught_monkeys != None:
                        self.interface.caught_monkeys = set(caught_monkeys)

            self.connection_state = "ready"
            display_connection_status_labels(self)

    async def server_auth(self, password_requested : bool = False) -> None:
        if password_requested and not self.password:
            await super().server_auth(password_requested)
        await self.get_username()
        await self.send_connect()

    def on_deathlink(self, data: dict):
        if self.deathlink_enabled:
            self.deathlink_pending = True
            text = data.get("cause", "")
            if text:
                logger.info(f"DeathLink: {text}")
            else:
                logger.info(f"DeathLink: Received from {data['source']}")

    def run_gui(self) -> None:
        from kvui import GameManager

        class AE2Manager(GameManager):
            logging_pairs = [("Client", "Archipelago")]
            base_title = "Ape Escape 2 Archipelago"

        self.ui = AE2Manager(self)
        self.ui_task = asyncio.create_task(self.ui.async_run(), name = "ui")

    def player_instruction(self, instruction) -> None:
        if self.most_recent_instruction != instruction:
            logger.info(instruction)
            self.most_recent_instruction = instruction

async def interface_sync_task(ctx) -> None:

    ctx.status_bar = MDGridLayout(rows=1, size_hint_y = None, height = dp(50), spacing = dp(5), padding = dp(5),)
    ctx.ui.grid.add_widget(ctx.status_bar)
    
    ctx.level_label = MDLabel(halign="center", role="large", markup = True)
    ctx.monkey_label = MDLabel(halign="center", role="large", markup = True)

    ctx.status_bar.add_widget(ctx.level_label)
    ctx.status_bar.add_widget(ctx.monkey_label)

    display_connection_status_labels(ctx)
    ctx.player_instruction("Beginning communication with PCSX2...")
    ctx.interface.connect_to_pcsx2()

    while not ctx.exit_event.is_set():
        await asyncio.sleep(0.1) #Poll rate
        try:
            if ctx.interface.connected_to_ae2():
                await check_game(ctx)
            else:
                await reconnect_game(ctx)
        except ConnectionError:
            ctx.interface.disconnected()
        except Exception as e:
            if isinstance(e, RuntimeError):
                logger.error(str(e))
            else:
                logger.error(traceback.format_exc())
            await asyncio.sleep(3)
            continue

async def check_game(ctx) -> None:
    if ctx.server:
        if not (ctx.slot and ctx.connection_state == "ready"):
            if ctx.connection_state == "request":
                #Update death link
                await ctx.update_death_link(ctx.deathlink_enabled)

                #Request Data Storage
                ctx.connection_state = "requested"
                await ctx.send_msgs([{"cmd": "Get", "keys": [f"ae2_processed_{ctx.team}_{ctx.slot}", f"ae2_caught_{ctx.team}_{ctx.slot}"]}])
            display_connection_status_labels(ctx)
            await asyncio.sleep(1)      
            return

        ctx.player_instruction("You are now connected and ready to play. Go ape!")

        #Check for unsent locations
        new_locations = ctx.interface.caught_monkeys.difference(ctx.previously_checked_locations)

        #If there are unsent locations, send them now
        if new_locations:
            await ctx.send_msgs([{"cmd" : "LocationChecks", "locations" : new_locations}])
            await ctx.send_msgs([{"cmd": "Set", "key": f"ae2_caught_{ctx.team}_{ctx.slot}", "default": {}, "want_reply": False, "operations": [{"operation": "replace", "value": ctx.interface.caught_monkeys}]}])

        #Receive items from server
        for i in range (0, len(ctx.items_received)):
            if i >= ctx.processed_items:
                server_item = ctx.items_received[i]
                if server_item.item == 102: #Victory item
                    await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
                elif server_item.item <= 14:
                    ctx.interface.unlock_gadget(item_name_from_id[server_item.item])
                elif server_item.item == 101:
                    ctx.interface.world_keys += 1
                elif server_item.item == 300:
                    ctx.interface.air_crawl_allowed = True

                if ctx.previously_processed_items != -1 and ctx.previously_processed_items < i:
                    if server_item.item == 201: #Jacket
                        ctx.interface.queued_up_lives += 1
                    elif server_item.item == 202: #Cookie
                        ctx.interface.queued_up_cookies += 1
                    elif server_item.item == 203: #Deluxe Cookie
                        ctx.interface.queued_up_cookies += 5
                    elif server_item.item == 204:
                        ctx.interface.queued_up_explosive_pellets += 1
                    elif server_item.item == 205:
                        ctx.interface.queued_up_guided_pellets += 1
                    if server_item.item == 206: #1 Coin
                        ctx.interface.queued_up_coins += 1
                    elif server_item.item == 207: #10 Coins
                        ctx.interface.queued_up_coins += 10
                    elif server_item.item == 208: #20 Coins
                        ctx.interface.queued_up_coins += 20
                    elif server_item.item == 209:
                        ctx.interface.queued_up_explosive_pellets += 3
                    elif server_item.item == 210:
                        ctx.interface.queued_up_guided_pellets += 3

                    ctx.previously_processed_items = i
                    if ctx.interface.queued_up_lives + ctx.interface.queued_up_coins + ctx.interface.queued_up_cookies + ctx.interface.queued_up_explosive_pellets + ctx.interface.queued_up_guided_pellets > 0:
                        await ctx.send_msgs([{"cmd": "Set", "key": f"ae2_processed_{ctx.team}_{ctx.slot}", "default": 0, "want_reply": False, "operations": [{"operation": "replace", "value": ctx.previously_processed_items}]}])

                ctx.processed_items += 1

        if ctx.interface.current_level_name != None:
            ctx.level_label.text = ctx.interface.current_level_name
            ctx.monkey_label.text = f"{ctx.interface.caught_monkeys_in_current_level}/{len(level_from_name[ctx.interface.current_level_name].monkeys)} Monkeys"

        ctx.interface.enforce_game_state()

        if ctx.deathlink_pending == True:
            ctx.interface.deathlink_queued = True
            ctx.deathlink_pending = False
        elif ctx.deathlink_enabled and ctx.interface.deaths > ctx.sent_deaths:
            ctx.sent_deaths = ctx.interface.deaths
            await ctx.send_death()

        if (ctx.interface.all_monkeys_caught and not ctx.reported_all_monkeys):
            ctx.reported_all_monkeys = True
            logger.info("You have unlocked the Final Showdown with Specter! Go get him!")
    else:
        ctx.player_instruction("You are not currently connected to an Archipelago server. Connect to an Archipelago server now!")
        ctx.connection_state = "none"
        display_connection_status_labels(ctx)

def display_connection_status_labels(ctx) -> None:
    #AP Connection
    if ctx.slot:
        if ctx.connection_state == "ready":
            ctx.level_label.text = "[color=00ff00]Connected to Archipelago[/color]"
        else:
            ctx.level_label.text = "[color=ffff00]Archipelago connection waiting...[/color]"
    else:
        ctx.level_label.text = "[color=ff0000]Not connected to Archipelago[/color]"

    #PCSX2 Connection
    if ctx.interface.connected:
        ctx.monkey_label.text = "[color=00ff00]Connected to PCSX2[/color]"
    else:
        ctx.monkey_label.text = "[color=ff0000]Not connected to PCSX2[/color]"


async def reconnect_game(ctx) -> None:
    ctx.player_instruction("Communication with PCSX2 failed. Please ensure that PCSX2 is open and Ape Escape 2 is loaded.")
    display_connection_status_labels(ctx)
    await asyncio.sleep(5)
    ctx.interface.connect_to_pcsx2()
    display_connection_status_labels(ctx)

def launch() -> None:
    async def main() -> None:
        multiprocessing.freeze_support()

        parser = get_base_parser()
        args = parser.parse_args()

        ctx = AE2Context(args.connect, args.password)
        ctx.server_task = asyncio.create_task(server_loop(ctx), name="Server Loop")

        if gui_enabled:
            ctx.run_gui()
        ctx.run_cli()

        ctx.interface_sync_task = asyncio.create_task(interface_sync_task(ctx), name="PCSX2 Sync")

        await ctx.exit_event.wait()
        ctx.server_address = None

        await ctx.shutdown()

        if ctx.interface_sync_task:
            await asyncio.sleep(3)
            await ctx.interface_sync_task

    #Run Client
    import colorama

    colorama.init()
    asyncio.run(main())
    colorama.deinit()

if __name__ == '__main__':
    launch()