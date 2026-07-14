import socket, struct, platform
from .Monkeys import monkeys, monkey_from_name, monkey_from_id
from .Levels import level_from_name, levels

gadget_addresses = {
    "Stun Club": {"PAL": 0x4D2533, "NTSC": 0x4D1333},
    "Monkey Net": {"PAL": 0x4D2593, "NTSC": 0x4D1393},
    "Monkey Radar": {"PAL": 0x4D25F3, "NTSC": 0x4D13F3},
    "Dash Hoop": {"PAL": 0x4D2653, "NTSC": 0x4D1453},
    "Catapult": {"PAL": 0x4D26B3, "NTSC": 0x4D14B3},
    "R.C. Car": {"PAL": 0x4D2713, "NTSC": 0x4D1513},
    "Sky Flyer": {"PAL": 0x4D2773, "NTSC": 0x4D1573},
    "Bananarang": {"PAL": 0x4D27D3, "NTSC": 0x4D15D3},
    "Water Cannon": {"PAL": 0x4D2833, "NTSC": 0x4D1633},
    "Electro Magnet": {"PAL": 0x4D2893, "NTSC": 0x4D1693},
    "Power Punch": {"PAL": 0x4D28F3, "NTSC": 0x4D16F3},
}

gadget_tutorial_addresses = { #Putting these to 1 prevents the gadget tutorial from playing (the game thinks you've already seen it)
    "Monkey Radar": {"PAL": 0x3E19DB, "NTSC": 0x3E06CB},
    "Water Net": {"PAL": 0x3E19E4, "NTSC": 0x3E06D4},
    "R.C. Car": {"PAL": 0x3E19DE, "NTSC": 0x3E06CE},
    "Power Punch": {"PAL": 0x3E19E3, "NTSC": 0x3E06D3},
    "See-All Scope": {"PAL": 0x3E1EBD, "NTSC": 0x3E0BAD},
    "Dash Hoop": {"PAL": 0x3E19DC, "NTSC": 0x3E06CC},
    "Sky Flyer": {"PAL": 0x3E19DF, "NTSC": 0x3E06CF},
    "Water Cannon": {"PAL": 0x3E19E1, "NTSC": 0x3E06D1},
    "Catapult": {"PAL": 0x3E19DD, "NTSC": 0x3E06CD},
    "Bananarang": {"PAL": 0x3E19E0, "NTSC": 0x3E06D0},
    "Electro Magnet": {"PAL": 0x3E19E2, "NTSC": 0x3E06D2},
    "Blue Baboon": {"PAL": 0x3E1A07, "NTSC": 0x3E06F7},
    "Enter the Monkey": {"PAL": 0x3E1A08, "NTSC": 0x3E06F8},
    "Specter": {"PAL": 0x3E1EBE, "NTSC": 0x3E0BAE} #We've finally located Specter!
}

gadget_ids = {"Stun Club": 1, "Monkey Net": 2, "Monkey Radar": 3, "Dash Hoop": 4, "Catapult": 5, "R.C. Car": 6, "Sky Flyer": 7, "Bananarang": 8, "Water Cannon": 9, "Electro Magnet": 10, "Power Punch": 11}

equipped_gadget_addresses = {
    "cross": {"PAL": 0x4D5F24, "NTSC": 0x4D4D24},
    "triangle": {"PAL": 0x4D5F1C, "NTSC": 0x4D4D1C},
    "square": {"PAL": 0x4D5F28, "NTSC": 0x4D4D28},
    "circle": {"PAL": 0x4D5F20, "NTSC": 0x4D4D20}
}

misc_addresses = {
    "selected": {"PAL": 0x1F5D80C, "NTSC": 0x1F5D80C}, #Current level hovered on level select screen (addresses are the same)
    "coins": {"PAL": 0x3E1980, "NTSC": 0x3E0670}, #How many coins you have right now
    "lives": {"PAL": 0x3E1978, "NTSC": 0x3E0668}, #How many lives you have right now
    "levels": {"PAL": 0x3E1984, "NTSC": 0x3E0674}, #How many levels you can select from,
    "character": {"PAL": 0x3E1974, "NTSC": 0x3E0664}, #01 = Hikaru, 02 = Hikaru (+See-All Scope), 03 = Kakeru, 04 = Kakeru (+See-All Scope)
    "equipped": {"PAL": 0x4D5F34, "NTSC": 0x4D4D34}, #Current held gadget
    "selected_face_button": {"PAL": 0x4D5F2C, "NTSC": 0x4D4D2C}, 
    "screen": {"PAL": 0x3B3618, "NTSC": 0x3B2118}, #Current stage/screen/area,
    "level_to_be_loaded": {"PAL": 0x3B3624, "NTSC": 0x3B2124}, #Room we're going to 
    "health": {"PAL": 0x3E197C, "NTSC": 0x3E066C}, #Current cookie count
    "visited": {"PAL": 0x3E198C, "NTSC": 0x3E067C}, #Number of levels visited (updates your unlocked gadgets) - just keep it at 255
    "cleared": {"PAL": 0x3E1988, "NTSC": 0x3E0678}, #How many levels are cleared,
    "hikaru_state": {"PAL": 0x4D5784, "NTSC": 0x4D4584}, #7 = crouched, 8 = crawling, 9 = hidden, 17 = submerged, 18 = floating, 49 = celebrating
    "y_position": {"PAL": 0x4D5CC7, "NTSC": 0x4D4AC7}, #Y position
    "air_meter_showing": {"PAL": 0x53D058, "NTSC": 0x53C0D4}, #1 = air meter visible (so check for water net unlock)
    "in_first_person": {"PAL": 0x4D1AF4, "NTSC": 0x4D08F4}, #0 = normal, 1 = first person, other numbers are different camera angles
    "camera_state": {"PAL": 0x4CCD40, "NTSC": 0x4CBB40}, #0 = frozen, 2 = active
    "natsumi_introduced": {"PAL": 0x3B366D, "NTSC": 0x3B216D}, #0 = Natsumi hasn't done her introduction, 1 = Natsumi has done her introduction
    "explosive_pellets": {"PAL": 0x3E19A9, "NTSC": 0x3E0699},
    "guided_pellets": {"PAL": 0x3E19AA, "NTSC": 0x3E069A},
    "y_velocity": {"PAL": 0x4D5D14, "NTSC": 0x4D4BC7}
}

kakeru_addresses = [  # Set these all to 1 if playing as Kakeru
    {"PAL": 0x3E1E9E, "NTSC": 0x3E0B8E},
    {"PAL": 0x3E1E9F, "NTSC": 0x3E0B8F},
    {"PAL": 0x3E1EA0, "NTSC": 0x3E0B90},
    {"PAL": 0x3E1EA1, "NTSC": 0x3E0B91},
    {"PAL": 0x3E1EA2, "NTSC": 0x3E0B92},
    {"PAL": 0x3E1EA3, "NTSC": 0x3E0B93},
    {"PAL": 0x3E1EA4, "NTSC": 0x3E0B94},
    {"PAL": 0x3E1EA5, "NTSC": 0x3E0B95},
    {"PAL": 0x3E1EA6, "NTSC": 0x3E0B96},
    {"PAL": 0x3E1EA7, "NTSC": 0x3E0B97},
    {"PAL": 0x3E1EA8, "NTSC": 0x3E0B98},
    {"PAL": 0x3E1EA9, "NTSC": 0x3E0B99},
    {"PAL": 0x3E1EAA, "NTSC": 0x3E0B9A},
    {"PAL": 0x3E1EAB, "NTSC": 0x3E0B9B},
    {"PAL": 0x3E1EAC, "NTSC": 0x3E0B9C},
    {"PAL": 0x3E1EAD, "NTSC": 0x3E0B9D},
    {"PAL": 0x3E1EAE, "NTSC": 0x3E0B9E},
    {"PAL": 0x3E1EAF, "NTSC": 0x3E0B9F},
    {"PAL": 0x3E1EB0, "NTSC": 0x3E0BA0},
    {"PAL": 0x3E1EB1, "NTSC": 0x3E0BA1},
    {"PAL": 0x3E1EB2, "NTSC": 0x3E0BA2},
    {"PAL": 0x3E1EB3, "NTSC": 0x3E0BA3},
    {"PAL": 0x3E1EB4, "NTSC": 0x3E0BA4},
    {"PAL": 0x3E1EB5, "NTSC": 0x3E0BA5},
    {"PAL": 0x3E1EB6, "NTSC": 0x3E0BA6},
    {"PAL": 0x3E1EB7, "NTSC": 0x3E0BA7},
    {"PAL": 0x3E1EB8, "NTSC": 0x3E0BA8},
    {"PAL": 0x3E1EB9, "NTSC": 0x3E0BA9},
    {"PAL": 0x3E1EBA, "NTSC": 0x3E0BAA},
    {"PAL": 0x3E1EBB, "NTSC": 0x3E0BAB},
    {"PAL": 0x3E1EBC, "NTSC": 0x3E0BAC},
    {"PAL": 0x3E1EBD, "NTSC": 0x3E0BAD},
    {"PAL": 0x3E1EBF, "NTSC": 0x3E0BAF},
    {"PAL": 0x3E1EC0, "NTSC": 0x3E0BB0},
    {"PAL": 0x3E1EC1, "NTSC": 0x3E0BB1},
    {"PAL": 0x3E1EC2, "NTSC": 0x3E0BB2},
    {"PAL": 0x3E1EC3, "NTSC": 0x3E0BB3},
    {"PAL": 0x3E1EC4, "NTSC": 0x3E0BB4},
    {"PAL": 0x3E1EC5, "NTSC": 0x3E0BB5},
    {"PAL": 0x3E1EC6, "NTSC": 0x3E0BB6},
    {"PAL": 0x3E1EC7, "NTSC": 0x3E0BB7},
    {"PAL": 0x3E1EC8, "NTSC": 0x3E0BB8},
    {"PAL": 0x3E1EC9, "NTSC": 0x3E0BB9},
    {"PAL": 0x3E1ECA, "NTSC": 0x3E0BBA},
    {"PAL": 0x3E1ECB, "NTSC": 0x3E0BBB},
    {"PAL": 0x3E1ECC, "NTSC": 0x3E0BBC},
    {"PAL": 0x3E1ECD, "NTSC": 0x3E0BBD},
]

#4D5D9C (PAL) 4D4B9C (NTSC) - tracks jump state, could use for future Double Jump item

class AE2Interface:

    def __init__(self, logger) -> None:
        self.logger = logger
        self.socket = None
        self.connected = False
        self.game_region = None
        self.reset()

    def reset(self) -> None:
        self.world_key_requirements = {}
        self.current_level_name = None
        self.caught_monkeys_in_current_level = 0

        self.caught_monkeys = set()
        self.unlocked_gadgets = set()
        self.world_keys = 0
        self.can_swim = False
        self.queued_up_coins = 0
        self.queued_up_lives = 0
        self.queued_up_cookies = 0
        self.queued_up_explosive_pellets = 0
        self.queued_up_guided_pellets = 0

        self.deathlink_enabled = False
        self.deathlink_blocked = False
        self.deathlink_queued = False
        self.deaths = 0
        self.previous_lives = -1

        self.air_crawl_allowed = False

        self.all_monkeys_caught = False
        self.character = 0 #0 = Hikaru, 1 = Kakeru

        self.previous_level_select_location = -1
        self.unlocked_levels = 0

    def connect_to_pcsx2(self) -> bool:
        try:
            if platform.system() == "Linux":
                self.socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
                socket_name = os.environ.get("XDG_RUNTIME_DIR", "/tmp")
                if os.access(socket_name + "/pcsx2.sock", os.R_OK): #Default/AppImage Socket Path
                    socket_name += "/pcsx2.sock"                
                else: #Flatpak Socket Path
                    socket_name += "/.flatpak/net.pcsx2.PCSX2/xdg-run"
                    socket_name += "/pcsx2.sock"
            elif platform.system() == "Darwin":
                self.socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
                socket_name = os.environ.get("TMPDIR", "/tmp")
                socket_name += "/pcsx2.sock"
            else:
                self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                socket_name = ("127.0.0.1", 28011)
            self.socket.connect(socket_name)
            return True
        except Exception as e:
            print(f"PCSX2 connection failed with error: {e}")
            self.connected = False
            return False

    def connected_to_ae2(self) -> bool:
        if not self.connected:
            try:
                request = struct.pack("<I", 5) + struct.pack("<B", 0xC)
                self.socket.sendall(request)
                response = self.socket.recv(64)

                game_id = response[9:-1].decode("ascii", errors="ignore")
                print(f"Detected Game ID: {game_id}")
                if game_id == "SCES-50885":
                    self.game_region = "PAL"
                    self.connected = True
                elif game_id == "SLUS-20685":
                    self.game_region = "NTSC"
                    self.connected = True
                else:
                    self.connected = False
            except:
                self.connected = False
        return self.connected

    def disconnected(self) -> None:
        self.connected = False

    def read_u8(self, address): #Read an 8-bit value
        self.socket.sendall((9).to_bytes(4, "little") + (0).to_bytes(1, "little") + address.to_bytes(4, "little"))
        data = self.recv_full()
        if not data:
            self.disconnected()
        else:
            return data[-1]

    def read_u32(self, address): #Read a 32-bit value
        self.socket.sendall((9).to_bytes(4, "little") + (2).to_bytes(1, "little") + address.to_bytes(4, "little"))
        data = self.recv_full()
        if len(data) < 4:
            self.disconnected()
        else:
            return int.from_bytes(data[-4:], "little")

    def write_u8(self, address, value): #Write an 8-bit value
        self.socket.sendall((10).to_bytes(4, "little") + (4).to_bytes(1, "little") + address.to_bytes(4, "little") + value.to_bytes(1, "little"))
        self.recv_full()

    def write_u32(self, address, value): #Write a 32-bit value
        self.socket.sendall((13).to_bytes(4, "little") + (6).to_bytes(1, "little") + address.to_bytes(4, "little") + value.to_bytes(4, "little"))
        self.recv_full()

    def recv_full(self):
        header = self.socket.recv(4)
        if not header:
            self.disconnected()
        total_size = int.from_bytes(header, "little")
        data = b""
        while len(data) < total_size - 4:
            chunk = self.socket.recv(4096)
            if not chunk:
                self.disconnected()
            data += chunk
        return data

    def check_captured_monkeys(self) -> None:
        all_monkeys_caught = True
        for monkey in [monkey for monkey in monkeys if ((not monkey.id in self.caught_monkeys) and (self.game_region in monkey.address))]:
            monkey_caught = self.read_u8(monkey.address[self.game_region])
            if monkey_caught == 1:
                self.caught_monkeys.add(monkey.id)
            elif monkey.level != "Final Showdown with Specter!":
                all_monkeys_caught = False
        if not (monkey_from_name["Yellow Monkey"].id in self.caught_monkeys and monkey_from_name["Specter"].id in self.caught_monkeys): #Monkeys with unusual check methods
            all_monkeys_caught = False
        self.all_monkeys_caught = all_monkeys_caught

    def update_unlocked_gadgets(self) -> None:
        for gadget in gadget_addresses:
            if gadget in self.unlocked_gadgets:
                self.write_u8(gadget_addresses[gadget][self.game_region], 1)
            else:
                self.write_u8(gadget_addresses[gadget][self.game_region], 0)
        
    def update_level_select(self) -> None:
        selected_level = self.read_u8(misc_addresses["selected"][self.game_region]) #Find selected level index
        if selected_level < self.unlocked_levels and selected_level > -1:
            if self.current_level_name != level_from_name[list(self.world_key_requirements.keys())[selected_level]].name:
                self.current_level_name = level_from_name[list(self.world_key_requirements.keys())[selected_level]].name #Update current level name
            self.write_u8(misc_addresses["level_to_be_loaded"][self.game_region], level_from_name[self.current_level_name].room_entrances[0].value) #Change area to be loaded when select confirms
            self.previous_level_select_location = selected_level #Remember level selector position

    def update_monkey_count(self) -> None:
        if self.current_level_name != None:
            self.caught_monkeys_in_current_level = len([monkey for monkey in level_from_name[self.current_level_name].monkeys if monkey.id in self.caught_monkeys]) #Count captured monkeys in level, to be displayed on client

    def update_coins(self) -> None:
        new_coins = min(999, self.read_u32(misc_addresses["coins"][self.game_region]) + self.queued_up_coins)
        self.write_u32(misc_addresses["coins"][self.game_region], new_coins)
        self.queued_up_coins = 0

    def update_cookies(self) -> None:
        new_health = min(50, self.read_u32(misc_addresses["health"][self.game_region]) + (self.queued_up_cookies * 10))
        self.write_u32(misc_addresses["health"][self.game_region], new_health)
        self.queued_up_cookies = 0

    def update_lives(self) -> None:
        new_lives = min(99, self.read_u32(misc_addresses["lives"][self.game_region]) + self.queued_up_lives)
        self.write_u32(misc_addresses["lives"][self.game_region], new_lives)
        self.queued_up_lives = 0

    def update_explosive_pellets(self) -> None:
        new_explosive_pellets = min(99, self.read_u8(misc_addresses["explosive_pellets"][self.game_region]) + self.queued_up_explosive_pellets)
        self.write_u8(misc_addresses["explosive_pellets"][self.game_region], new_explosive_pellets)
        self.queued_up_explosive_pellets = 0

    def update_guided_pellets(self) -> None:
        new_guided_pellets = min(99, self.read_u8(misc_addresses["guided_pellets"][self.game_region]) + self.queued_up_guided_pellets)
        self.write_u8(misc_addresses["guided_pellets"][self.game_region], new_guided_pellets)
        self.queued_up_guided_pellets = 0

    def unlock_gadget(self, gadget_name) -> None:
        self.unlocked_gadgets.add(gadget_name)
        if gadget_name == "Water Net":
            self.can_swim = True
            
    def auto_equip(self) -> None:
        currently_equipped = {}
        for face_button in equipped_gadget_addresses:
            currently_equipped[face_button] = self.read_u8(equipped_gadget_addresses[face_button][self.game_region])
            if currently_equipped[face_button] == 1 and not "Stun Club" in self.unlocked_gadgets:
                if self.read_u8(misc_addresses["equipped"][self.game_region]) == 1: #Holding the Stun Club
                    self.write_u8(misc_addresses["selected_face_button"][self.game_region], 2) #Highlight the X button
                    self.write_u8(misc_addresses["equipped"][self.game_region], 2) #Put the net in your hand
                self.write_u8(equipped_gadget_addresses[face_button][self.game_region], 0) #Set this face button to nothing
                currently_equipped[face_button] = 0

        for gadget_name in [gadget_name for gadget_name in self.unlocked_gadgets if gadget_name in gadget_ids]:
            if any(equipped_gadget_id == 0 for equipped_gadget_id in currently_equipped.values()): #Empty space available
                newly_received_gadget_id = gadget_ids[gadget_name]
                if all(equipped_gadget_id != newly_received_gadget_id for equipped_gadget_id in currently_equipped.values()): #Gadget not currently equipped
                    face_button_to_use = next((face_button for face_button, equipped_gadget_id in currently_equipped.items() if equipped_gadget_id == 0), None)
                    self.write_u8(equipped_gadget_addresses[face_button_to_use][self.game_region], newly_received_gadget_id)
                    currently_equipped[face_button_to_use] = newly_received_gadget_id

    def trigger_falloff(self) -> None:
        self.write_u8(misc_addresses["camera_state"][self.game_region], 0) #Freeze camera in place
        self.write_u8(misc_addresses["y_position"][self.game_region], 255) #Teleport you below the death barrier

    def enforce_game_state(self) -> None:
        current_screen = self.read_u8(misc_addresses["screen"][self.game_region])

        if self.read_u8(misc_addresses["natsumi_introduced"][self.game_region]) == 0: #Starting a new game (haven't heard Natsumi's introduction), so force you to the Travel Station instead of Liberty Island
            self.write_u8(misc_addresses["level_to_be_loaded"][self.game_region], 0x71) #Force to Travel Station
        elif current_screen == 1: #In the Travel Station
            #Update level select
            if (self.all_monkeys_caught):
                self.write_u8(misc_addresses["cleared"][self.game_region], 28) #Sets 28 levels to cleared - unlocks final Specter
            else:
                self.write_u8(misc_addresses["cleared"][self.game_region], 0) #Sets 0 levels to cleared - keeps the level select looking nice

            #Update level targets
            for level in levels: 
                if self.game_region in level.target_address:
                    self.write_u8(level.target_address[self.game_region], len(level.monkeys))

            for monkey_id in self.caught_monkeys: #While in the hub, update monkeys to match server state
                monkey = monkey_from_id[monkey_id]
                if self.game_region in monkey.address:
                    self.write_u8(monkey.address[self.game_region], 1) #Mark as captured

            self.unlocked_levels = 0
            for key_requirement in self.world_key_requirements.values():
                if key_requirement <= self.world_keys:
                    self.unlocked_levels += 1
            self.write_u8(misc_addresses["levels"][self.game_region], self.unlocked_levels + 1) #Update number of unlocked levels

            if self.read_u8(misc_addresses["in_first_person"][self.game_region]) == 0x0A: #Viewing the level selector
                self.update_level_select() #Update level select 
            elif self.previous_level_select_location != -1:
                self.write_u8(misc_addresses["selected"][self.game_region], self.previous_level_select_location)

            self.auto_equip()

        elif current_screen != 31: #In a level
            self.write_u8(misc_addresses["cleared"][self.game_region], 255) #Sets 255 levels to cleared - stops you getting taken to boss fights

            #Swimming Prevention
            if self.can_swim == False and self.read_u8(misc_addresses["air_meter_showing"][self.game_region]) != 0:
                self.trigger_falloff()

            self.auto_equip()

            if self.deathlink_queued:
                self.write_u8(misc_addresses["health"][self.game_region], 0) #Set health to 0
                self.trigger_falloff()
                self.deathlink_blocked = True
        self.deathlink_queued = False

        #Update character state
        self.write_u8(misc_addresses["visited"][self.game_region], 255) #Stops gadgets being taken away from you (except Power Punch - you need to be post game for that)
        self.update_unlocked_gadgets()       
        if ((not "See-All Scope" in self.unlocked_gadgets) and self.read_u8(misc_addresses["in_first_person"][self.game_region]) == 1):
            self.write_u8(misc_addresses["character"][self.game_region], 1 + (self.character * 2)) #In first person without See-All Scope unlocked; revert to normal Hikaru for now, we'll evolve into the post-game form as soon as you leave first person
        else:
            self.write_u8(misc_addresses["character"][self.game_region], 2 + (self.character * 2)) #Play as post-game Hikaru - equips the See-All Scope, spawns extra monkeys and stops the Power Punch being taken away
        if self.character == 1: #playing as Kakeru
            if self.read_u8(kakeru_addresses[0][self.game_region]) == 0:
                for address in kakeru_addresses:
                    self.write_u8(address[self.game_region], 1)

        if (current_screen >= 1 and current_screen < 30): #In gameplay/credits
            #Check lives for deathlink
            if self.deathlink_enabled:
                new_lives = self.read_u32(misc_addresses["lives"][self.game_region])
                if new_lives != None and new_lives < self.previous_lives: #Lost a life
                    if current_screen < 31 and current_screen > 1 and not self.deathlink_blocked:
                        self.deaths += 1
                    else:
                        self.deathlink_blocked = False
                self.previous_lives = new_lives

            #Update monkeys
            self.check_captured_monkeys()
            self.update_monkey_count() #Continuously update monkey count to be shown on client

            #Tutorial/Cutscene Block
            for address in gadget_tutorial_addresses.values():
                self.write_u8(address[self.game_region], 1) #Tutorial/Cutscene already seen

            #Update filler
            if self.queued_up_coins:
                self.update_coins()
            if self.queued_up_lives:
                self.update_lives()
            if self.queued_up_cookies:
                self.update_cookies()
            if self.queued_up_explosive_pellets:
                self.update_explosive_pellets() 
            if self.queued_up_guided_pellets:
                self.update_guided_pellets() 

            #Air Crawl Prevention
            hikaru_state = self.read_u8(misc_addresses["hikaru_state"][self.game_region])
            if (not self.air_crawl_allowed) and hikaru_state in [7, 8, 9] and self.read_u8(misc_addresses["y_velocity"][self.game_region]) != 0:
                self.write_u8(misc_addresses["hikaru_state"][self.game_region], 0)

            #Yellow Monkey check functions off victory
            if current_screen == 11 and hikaru_state == 49:
                self.caught_monkeys.add(monkey_from_name["Yellow Monkey"].id)                                

            #Update level target
            if self.current_level_name in level_from_name:
                level = level_from_name[self.current_level_name]
                if self.game_region in level.target_address:
                    self.write_u8(level.target_address[self.game_region], len(level.monkeys))
        elif current_screen == 46: #Credits
            self.caught_monkeys.add(monkey_from_name["Specter"].id) #If you're in the credits, you must have beaten Specter