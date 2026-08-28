client_ver = "1.3"

from typing import Optional, Set, Dict, Any
import asyncio, multiprocessing, traceback

from CommonClient import ClientCommandProcessor, get_base_parser, logger, server_loop, gui_enabled
from NetUtils import ClientStatus
import Utils

from .Interface import AE2Interface
from .Items import item_name_from_id
from .Levels import level_from_name, levels
from .Phones import phone_from_name

from kvui import MDLabel, MDFloatLayout, MDDivider, MDBoxLayout, MDLinearProgressIndicator
from kivymd.uix.card import MDCard
from kivy.metrics import dp
from kivy.animation import Animation

tracker_loaded = False
try:
    from worlds.tracker.TrackerClient import TrackerGameContext as SuperContext
    tracker_loaded = True
except ModuleNotFoundError:
    from CommonClient import CommonContext as SuperContext

class AE2CommandProcessor(ClientCommandProcessor):
    def __init__(self, ctx: SuperContext) -> None:
        super().__init__(ctx)

    def _cmd_set_room(self, value: str) -> None:
        if isinstance(self.ctx, AE2Context):
            self.ctx.interface.set_gate_destination_room(value)

    def _cmd_set_spawn(self, value: str) -> None:
        if isinstance(self.ctx, AE2Context):
            self.ctx.interface.set_gate_destination_spawn(value)

    def _cmd_pos(self):
        if isinstance(self.ctx, AE2Context):
            logger.info(self.ctx.interface.get_position_str())

class AE2Context(SuperContext):
    client_version: str = "v1.3.0"
    game: str = "Ape Escape 2"

    command_processor = AE2CommandProcessor
    items_handling = 0b111

    interface_sync_task : asyncio.tasks = None
    last_error_message : Optional[str] = None

    slot_data: Dict[str, Any]
    tags = {"AP"}

    def __init__(self, address, password: str) -> None:
        super().__init__(address, password)
        Utils.init_logging(f"Ape Escape 2 Archipelago Client {self.client_version}")
        self.interface = AE2Interface(logger)
        self.most_recent_instruction = None
        self.connection_state = "none"

        self.travel_station_status_card = None
        self.level_status_card = None

    def on_package(self, cmd: str, args: Dict[str, Any]) -> None:
        super().on_package(cmd, args) #UT

        #Connected to server
        if cmd == "Connected":
            #Init
            self.slot_data = args["slot_data"]  
            try:
                self.previously_checked_locations = set(args["checked_locations"])
            except:
                self.previously_checked_locations = set()

            if (not "gen_ver" in self.slot_data) or self.slot_data["gen_ver"] != client_ver:
                logger.info(f"Version Mismatch: You are using version {client_ver}. The server expects version {self.slot_data["gen_ver"]}.")
                logger.info(f"To connect to this world, you need to install a compatible ae2.apworld.")
                Utils.async_start(self.disconnect(), name="disconnecting")
            else:
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
                self.interface.randomised_starting_rooms = self.slot_data["randomised_starting_rooms"]
                self.interface.interpret_randomised_gates(self.slot_data["randomised_gates"])
                self.interface.music_map = self.slot_data["music_map"]
                self.interface.gotcha_box_restocks = 0
                if self.slot_data["gotcha_box_locations"] > 0:
                    self.interface.gotcha_box_locations = self.slot_data["gotcha_box_locations"]
                    self.interface.gotcha_box_gating = self.slot_data["gotcha_box_gating"]
                self.interface.message_phone_locations = self.slot_data["message_phone_locations"]
                update_connection_status_card(self)

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
            update_connection_status_card(self)
            create_travel_station_status_card(self)
            create_level_status_card(self)

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

    def make_gui(self):
        ui = super().make_gui()
        ui.base_title = "Ape Escape 2 Archipelago"
        ui.logging_pairs = [("Client", "Archipelago")]

        return ui

    def player_instruction(self, instruction) -> None:
        if self.most_recent_instruction != instruction:
            logger.info(instruction)
            self.most_recent_instruction = instruction

def create_connection_status_card(ctx) -> None: #Card to display Archipelago and PCSX2 connection statuses
    ctx.connection_status_card = MDCard(orientation = "vertical", size_hint = (None, None), size = (dp(600), dp(100)), padding = dp(8), pos_hint = {"center_x": 0.5, "top": 0.95}, radius = [dp(15)], focus_behavior = False)

    connection_status_bar = MDBoxLayout(orientation = "horizontal")

    ctx.connection_status_archipelago = MDLabel(halign = "center", markup = True)
    connection_status_bar.add_widget(ctx.connection_status_archipelago)

    divider = MDDivider(orientation = "vertical")
    connection_status_bar.add_widget(divider)

    ctx.connection_status_emulator = MDLabel(halign = "center", markup = True)
    connection_status_bar.add_widget(ctx.connection_status_emulator)

    connection_status_title = MDLabel(text = "Connection Status", halign = "center", bold = True)
    ctx.connection_status_card.add_widget(connection_status_title)

    ctx.connection_status_card.add_widget(connection_status_bar)

def create_progress_container(include_vertical_divider) -> None: #Creates a container with a label and progress bar, to be used by Travel Station and Level status cards
    outer_container = MDBoxLayout(orientation = "horizontal") #Contains divider and inner_container side-by-side
    inner_container = MDBoxLayout(orientation = "vertical", spacing = dp(8)) #Contains text label and progress bar, one atop the other

    text_label = MDLabel(halign = "center", markup = True)
    inner_container.add_widget(text_label)

    progress_bar = MDLinearProgressIndicator(value = 50, size_hint_x = 0.5, size_hint_y = 0.2, pos_hint={"center_x": 0.5}, radius=[dp(5)])
    inner_container.add_widget(progress_bar)

    if include_vertical_divider:
        divider = MDDivider(orientation = "vertical")
        outer_container.add_widget(divider)

    outer_container.add_widget(inner_container)

    return outer_container, text_label, progress_bar

def update_progress_bar(progress_bar_element, value) -> None: #Smoothly animates the given progress bar to the target width
    if int(value) != int(progress_bar_element.value):
        Animation(value = int(value), duration = 0.1).start(progress_bar_element)

def create_travel_station_status_card(ctx) -> None: #Shown in the Travel Station, displays total counts and Gotcha Box availability
    if ctx.interface.gotcha_box_locations > 0:
        card_height = 150
    else:
        card_height = 100

    ctx.travel_station_status_card = MDCard(orientation = "vertical", size_hint = (None, None), size = (dp(600), dp(card_height)), padding = dp(8), pos_hint = {"center_x": 0.5, "top": 0.95}, radius = [dp(15)], focus_behavior = False)

    ctx.travel_station_status_title = MDLabel(text = "Travel Station", halign = "center", bold = True)
    ctx.travel_station_status_card.add_widget(ctx.travel_station_status_title)

    ctx.travel_station_status_bar = MDBoxLayout(orientation = "horizontal", padding = (0, 0, 0, dp(8)))

    ctx.travel_station_status_monkeys_container, ctx.travel_station_status_monkeys_label, ctx.travel_station_status_monkeys_bar = create_progress_container(False)
    ctx.travel_station_status_bar.add_widget(ctx.travel_station_status_monkeys_container)

    if ctx.interface.message_phone_locations:
        ctx.travel_station_status_phones_container, ctx.travel_station_status_phones_label, ctx.travel_station_status_phones_bar = create_progress_container(True)
        ctx.travel_station_status_bar.add_widget(ctx.travel_station_status_phones_container)

    ctx.travel_station_status_world_keys_container, ctx.travel_station_status_world_keys_label, ctx.travel_station_status_world_keys_bar = create_progress_container(True)
    ctx.travel_station_status_bar.add_widget(ctx.travel_station_status_world_keys_container)

    ctx.travel_station_status_card.add_widget(ctx.travel_station_status_bar)    

    if ctx.interface.gotcha_box_locations > 0:
        ctx.travel_station_status_card_gotcha_box_title = MDLabel(text = "Gotcha Box", halign = "center", bold = True)
        ctx.travel_station_status_card.add_widget(ctx.travel_station_status_card_gotcha_box_title)

        ctx.travel_station_gotcha_box_bar = MDBoxLayout(orientation = "horizontal", padding = (0, 0, 0, dp(8)))

        ctx.travel_station_status_gotcha_box_container, ctx.travel_station_status_gotcha_box_label, ctx.travel_station_status_gotcha_box_bar = create_progress_container(False)
        ctx.travel_station_gotcha_box_bar.add_widget(ctx.travel_station_status_gotcha_box_container)

        ctx.travel_station_status_card.add_widget(ctx.travel_station_gotcha_box_bar)

def create_level_status_card(ctx) -> None: #Shown in gameplay and on the level select, shows level title along with location counts/availability
    ctx.level_status_card = MDCard(orientation = "vertical", size_hint = (None, None), size = (dp(600), dp(100)), padding = dp(8), pos_hint = {"center_x": 0.5, "top": 0.95}, radius = [dp(15)], focus_behavior = False)

    ctx.level_status_title = MDLabel(halign = "center", bold = True)
    ctx.level_status_card.add_widget(ctx.level_status_title)

    ctx.level_status_bar = MDBoxLayout(padding = (0, 0, 0, dp(8)))

    ctx.level_status_monkeys_container, ctx.level_status_monkeys_label, ctx.level_status_monkeys_bar = create_progress_container(False)
    ctx.level_status_bar.add_widget(ctx.level_status_monkeys_container)

    if ctx.interface.message_phone_locations:
        ctx.level_status_phones_container, ctx.level_status_phones_label, ctx.level_status_phones_bar = create_progress_container(True)
        ctx.level_status_bar.add_widget(ctx.level_status_phones_container)

    ctx.level_status_card.add_widget(ctx.level_status_bar)   

def update_connection_status_card(ctx) -> None:
    #AP Connection
    if ctx.slot:
        if ctx.connection_state == "ready":
            ctx.connection_status_archipelago.text = "[color=00ff00]Connected to Archipelago[/color]"
        else:
            ctx.connection_status_archipelago.text = "[color=ffff00]Archipelago connection waiting...[/color]"
    else:
        ctx.connection_status_archipelago.text = "[color=ff0000]Not connected to Archipelago[/color]"

    #PCSX2 Connection
    if ctx.interface.connected:
        ctx.connection_status_emulator.text = "[color=00ff00]Connected to PCSX2[/color]"
    else:
        ctx.connection_status_emulator.text = "[color=ff0000]Not connected to PCSX2[/color]"

    if ctx.slot and ctx.interface.connected:
        if ctx.connection_status_card in ctx.cards_layout.children:
            ctx.cards_layout.remove_widget(ctx.connection_status_card)
    elif not ctx.connection_status_card in ctx.cards_layout.children:
        ctx.cards_layout.add_widget(ctx.connection_status_card)
        if ctx.level_status_card in ctx.cards_layout.children:
            ctx.cards_layout.remove_widget(ctx.level_status_card)
        elif ctx.travel_station_status_card in ctx.cards_layout.children:
            ctx.cards_layout.remove_widget(ctx.travel_station_status_card)

def update_level_status_card(ctx) -> None: #Displays and updates the information on the Travel Station or Level status card
    if ctx.interface.current_level_name == "Travel Station":
        if tracker_loaded:
            if any(location_id < 1000 for location_id in ctx.tracker_core.locations_available):
                monkey_checks_indicator = "[color=00ff00]•[/color] "
            elif any(location_id < 1000 for location_id in ctx.tracker_core.glitched_locations):
                monkey_checks_indicator = "[color=ffff00]•[/color] "
            elif any(location_id < 1000 for location_id in ctx.missing_locations):
                monkey_checks_indicator = "[color=ff0000]•[/color] "
            else:
                monkey_checks_indicator = "• "
        else:
            monkey_checks_indicator = ""

        ctx.travel_station_status_monkeys_label.text = f"{monkey_checks_indicator}{len(ctx.interface.caught_monkeys)}/308 Monkeys" #300 Monkeys + 8 Boss Fights (Blue, Yellow, Pink, White, Red, Giant Yellow, Specter 1, Specter 2)
        update_progress_bar(ctx.travel_station_status_monkeys_bar, (len(ctx.interface.caught_monkeys)/308) * 100)

        ctx.travel_station_status_world_keys_label.text = f"{ctx.interface.world_keys}/{max(ctx.interface.world_key_requirements.values())} World Keys"
        update_progress_bar(ctx.travel_station_status_world_keys_bar, min(100, (ctx.interface.world_keys/max(ctx.interface.world_key_requirements.values())) * 100))

        if ctx.interface.message_phone_locations:
            if tracker_loaded:
                if any(location_id < 2000 and location_id >= 1000 for location_id in ctx.tracker_core.locations_available):
                    phone_checks_indicator = "[color=00ff00]•[/color] "
                elif any(location_id < 2000 and location_id >= 1000 for location_id in ctx.tracker_core.glitched_locations):
                    phone_checks_indicator = "[color=ffff00]•[/color] "
                elif any(location_id < 2000 and location_id >= 1000 for location_id in ctx.missing_locations):
                    phone_checks_indicator = "[color=ff0000]•[/color] "
                else:
                    phone_checks_indicator = "• "
            else:
                phone_checks_indicator = ""

            activated_phones = len([phone_from_name[phone_name] for phone_name in phone_from_name if not phone_from_name[phone_name].id in ctx.missing_locations])
            ctx.travel_station_status_phones_label.text = f"{phone_checks_indicator}{activated_phones}/30 Phones"
            update_progress_bar(ctx.travel_station_status_phones_bar, (activated_phones/30) * 100)

        if ctx.interface.gotcha_box_gating != -1:
            if tracker_loaded:
                if len(ctx.interface.missing_gotcha_box_checks) == 0:
                    gotcha_box_checks_indicator = "• "
                elif any(location_id in ctx.tracker_core.locations_available for location_id in ctx.interface.missing_gotcha_box_checks):
                    gotcha_box_checks_indicator = "[color=00ff00]•[/color] "
                elif any(location_id in ctx.tracker_core.glitched_locations for location_id in ctx.interface.missing_gotcha_box_checks):
                    gotcha_box_checks_indicator = "[color=ffff00]•[/color] "
                else:
                    gotcha_box_checks_indicator = "[color=ff0000]•[/color] "
            else:
                gotcha_box_checks_indicator = ""

            claimed_gotcha_box_locations = ctx.interface.gotcha_box_locations - len(ctx.interface.missing_gotcha_box_checks)
            ctx.travel_station_status_gotcha_box_label.text = f"{gotcha_box_checks_indicator}{claimed_gotcha_box_locations}/{ctx.interface.gotcha_box_locations} Items Claimed"
            ctx.travel_station_status_gotcha_box_bar.value = (claimed_gotcha_box_locations/ctx.interface.gotcha_box_locations) * 100
            update_progress_bar(ctx.travel_station_status_gotcha_box_bar, (claimed_gotcha_box_locations/ctx.interface.gotcha_box_locations) * 100)

        if not ctx.travel_station_status_card in ctx.cards_layout.children:
            ctx.cards_layout.add_widget(ctx.travel_station_status_card)
            if ctx.level_status_card in ctx.cards_layout.children:
                ctx.cards_layout.remove_widget(ctx.level_status_card)
    else:
        current_level = level_from_name[ctx.interface.current_level_name]
        ctx.level_status_title.text = current_level.name

        caught_monkeys_in_current_level = len([monkey for monkey in current_level.monkeys if monkey.id in ctx.interface.caught_monkeys])

        if tracker_loaded:
            if any(monkey.id in ctx.tracker_core.locations_available for monkey in current_level.monkeys):
                monkey_checks_indicator = "[color=00ff00]•[/color] "
            elif any(monkey.id in ctx.tracker_core.glitched_locations for monkey in current_level.monkeys):
                monkey_checks_indicator = "[color=ffff00]•[/color] "
            elif any(monkey.id in ctx.missing_locations for monkey in current_level.monkeys):
                monkey_checks_indicator = "[color=ff0000]•[/color] "
            else:
                monkey_checks_indicator = "• "
        else:
            monkey_checks_indicator = ""

        ctx.level_status_monkeys_label.text = f"{monkey_checks_indicator}{caught_monkeys_in_current_level}/{len(current_level.monkeys)} Monkeys"
        update_progress_bar(ctx.level_status_monkeys_bar, (caught_monkeys_in_current_level/len(current_level.monkeys)) * 100)

        if ctx.interface.message_phone_locations:
            if (len(current_level.phones)) > 0:
                activated_phones_in_current_level = len([phone for phone in current_level.phones if not phone.id in ctx.missing_locations])
                if tracker_loaded:
                    if activated_phones_in_current_level == len(current_level.phones):
                        phone_checks_indicator = "• "
                    elif any(phone.id in ctx.tracker_core.locations_available for phone in current_level.phones):
                        phone_checks_indicator = "[color=00ff00]•[/color] "
                    elif any(phone.id in ctx.tracker_core.glitched_locations for phone in current_level.phones):
                        phone_checks_indicator = "[color=ffff00]•[/color] "
                    else:
                        phone_checks_indicator = "[color=ff0000]•[/color] "
                else:
                    phone_checks_indicator = ""

                ctx.level_status_phones_label.text = f"{phone_checks_indicator}{activated_phones_in_current_level}/{len(current_level.phones)} Phones"
                update_progress_bar(ctx.level_status_phones_bar, (activated_phones_in_current_level/len(current_level.phones)) * 100)
                ctx.level_status_phones_container.disabled = False
            else:
                if tracker_loaded:
                    ctx.level_status_phones_label.text = "• 0/0 Phones"
                    
                else:
                    ctx.level_status_phones_label.text = "0/0 Phones"
                update_progress_bar(ctx.level_status_phones_bar, 0)
                ctx.level_status_phones_container.disabled = True

        if not ctx.level_status_card in ctx.cards_layout.children:
            ctx.cards_layout.add_widget(ctx.level_status_card)
            if ctx.travel_station_status_card in ctx.cards_layout.children:
                ctx.cards_layout.remove_widget(ctx.travel_station_status_card)

async def interface_sync_task(ctx) -> None:

    ctx.cards_layout = MDFloatLayout()
    ctx.ui.screens.get_screen("Archipelago").add_widget(ctx.cards_layout)
    create_connection_status_card(ctx)
    update_connection_status_card(ctx)            

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

            update_connection_status_card(ctx)
            await asyncio.sleep(1)      
            return

        ctx.player_instruction("You are now connected and ready to play. Go ape!")

        #Check for unsent locations
        new_locations = (ctx.interface.caught_monkeys.union(ctx.interface.activated_phones).union(ctx.interface.obtained_gotcha_box_checks)).difference(ctx.previously_checked_locations)

        #If there are unsent locations, send them now
        if new_locations:
            await ctx.send_msgs([{"cmd" : "LocationChecks", "locations" : new_locations}])
            await ctx.send_msgs([{"cmd": "Set", "key": f"ae2_caught_{ctx.team}_{ctx.slot}", "default": {}, "want_reply": False, "operations": [{"operation": "replace", "value": ctx.interface.caught_monkeys}]}])

        ctx.previously_checked_locations.update(new_locations)
        ctx.interface.missing_gotcha_box_checks = sorted([location_id for location_id in ctx.missing_locations if location_id >= 2000 and location_id < 3000])

        #Receive items from server
        for i in range (0, len(ctx.items_received)):
            if i >= ctx.processed_items:
                server_item = ctx.items_received[i]
                if server_item.item == 102: #Victory item
                    await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
                elif server_item.item <= 14:
                    ctx.interface.unlock_gadget(item_name_from_id[server_item.item])
                elif server_item.item == 15: #Progressive Catapult
                    if "Catapult" in ctx.interface.unlocked_gadgets:
                        ctx.interface.air_crawl_allowed = True
                    else:
                        ctx.interface.unlock_gadget("Catapult")
                elif server_item.item == 101: #World Key
                    ctx.interface.world_keys += 1
                elif server_item.item == 300:
                    ctx.interface.air_crawl_allowed = True
                elif server_item.item == 103:
                    ctx.interface.gotcha_box_restocks += 1
                elif server_item.item >= 1000 and server_item.item <= 1248: #Gotcha Box collectible
                    ctx.interface.unlock_collectible(item_name_from_id[server_item.item])

                if ctx.previously_processed_items != -1 and ctx.previously_processed_items < i:
                    sending_one_use_item = True
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
                    elif server_item.item == 206: #1 Coin
                        ctx.interface.queued_up_coins += 1
                    elif server_item.item == 207: #10 Coins
                        ctx.interface.queued_up_coins += 10
                    elif server_item.item == 208: #20 Coins
                        ctx.interface.queued_up_coins += 20
                    elif server_item.item == 209:
                        ctx.interface.queued_up_explosive_pellets += 3
                    elif server_item.item == 210:
                        ctx.interface.queued_up_guided_pellets += 3
                    elif server_item.item >= 400 and server_item.item < 500:
                        ctx.interface.activate_trap(server_item.item)
                    else:
                        sending_one_use_item = False

                    ctx.previously_processed_items = i

                    if sending_one_use_item: #Prevent traps/filler being re-sent on reconnection
                        await ctx.send_msgs([{"cmd": "Set", "key": f"ae2_processed_{ctx.team}_{ctx.slot}", "default": 0, "want_reply": False, "operations": [{"operation": "replace", "value": ctx.previously_processed_items}]}])

                ctx.processed_items += 1

        if ctx.interface.current_level_name != None:
            update_level_status_card(ctx)

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
        update_connection_status_card(ctx)
        
async def reconnect_game(ctx) -> None:
    ctx.player_instruction("Communication with PCSX2 failed. Please ensure that PCSX2 is open and Ape Escape 2 is loaded.")
    update_connection_status_card(ctx)
    await asyncio.sleep(5)
    ctx.interface.connect_to_pcsx2()
    update_connection_status_card(ctx)

def launch() -> None:
    async def main() -> None:
        multiprocessing.freeze_support()

        parser = get_base_parser()
        args = parser.parse_args()

        ctx = AE2Context(args.connect, args.password)
        ctx.server_task = asyncio.create_task(server_loop(ctx), name="Server Loop")

        if tracker_loaded:
            ctx.run_generator()
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