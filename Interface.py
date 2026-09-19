import socket, struct, platform, os, datetime
from .Monkeys import monkeys, monkey_from_name, monkey_from_id
from .Levels import level_from_name, levels, gate_from_name
from .Phones import phone_from_name
from .Music import music_table
from .Addresses import gadget_addresses, equipped_gadget_addresses, gadget_ids, gadget_from_id, gadget_tutorial_addresses, misc_addresses, kakeru_addresses, gotcha_box_collectibles

class AE2Interface:

    def __init__(self, logger) -> None:
        self.logger = logger
        self.socket = None
        self.connected = False
        self.game_region = None
        self.reset()

    def reset(self) -> None:
        self.world_key_requirements = {}
        self.randomised_starting_rooms = {}
        self.randomised_gates = {}
        self.current_level_name = None
        self.caught_monkeys_in_current_level = 0
        self.music_map = {}

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

        self.used_message_info_pointers = []
        self.activated_phones = set()
        self.message_phone_locations = False

        self.transition_state = "default"
        self.target_room_to_load = 0x71
        self.transition_pointer = -1

        self.natsumi_introduced = False
        self.applied_custom_music_map = False
        self.empty_hands = True

        self.gotcha_box_state = "unknown"
        self.obtained_gotcha_box_checks = set()
        self.missing_gotcha_box_checks = []
        self.gotcha_box_locations = -1
        self.gotcha_box_gating = -1
        self.unlocked_collectibles = set()

        self.tracker_level_name = "Travel Station"

        self.active_traps = {}

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

    def read_u64(self, address): #Read a 64-bit value
        self.socket.sendall((9).to_bytes(4, "little") + (3).to_bytes(1, "little") + address.to_bytes(4, "little"))
        data = self.recv_full()
        if len(data) < 8:
            self.disconnected()
        else:
            return int.from_bytes(data[-8:], "little")

    def write_u8(self, address, value): #Write an 8-bit value
        self.socket.sendall((10).to_bytes(4, "little") + (4).to_bytes(1, "little") + address.to_bytes(4, "little") + value.to_bytes(1, "little"))
        self.recv_full()

    def write_u32(self, address, value): #Write a 32-bit value
        self.socket.sendall((13).to_bytes(4, "little") + (6).to_bytes(1, "little") + address.to_bytes(4, "little") + value.to_bytes(4, "little"))
        self.recv_full()

    def write_string_at(self, address, value) -> None: #Writes a string of arbitrary length
        encoded = value.encode("utf-8") + b"\x00"
        for i, byte in enumerate(encoded):
            self.write_u8(address + i, byte)

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
            if self.current_level_name in self.randomised_starting_rooms:
                room_index = self.randomised_starting_rooms[self.current_level_name]
            else:
                room_index = 0
            self.target_room_to_load = level_from_name[self.current_level_name].room_entrances[room_index].target_room
            self.write_u8(misc_addresses["level_to_be_loaded"][self.game_region], self.target_room_to_load) #Change area to be loaded when select confirms
            self.previous_level_select_location = selected_level #Remember level selector position

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
        legal_face_buttons = []
        illegal_face_buttons = []

        for face_button in equipped_gadget_addresses:
            currently_equipped[face_button] = self.read_u8(equipped_gadget_addresses[face_button][self.game_region])
            if currently_equipped[face_button] in gadget_from_id and not gadget_from_id[currently_equipped[face_button]] in self.unlocked_gadgets: #You have a gadget equipped that you shouldn't
                illegal_face_buttons.append(face_button)
            else:
                legal_face_buttons.append(face_button)

        try:
            selected_face_button = ["triangle", "circle", "cross", "square"][self.read_u8(misc_addresses["selected_face_button"][self.game_region])]
        except:
            selected_face_button = None

        for illegal_face_button in illegal_face_buttons:
            if selected_face_button == illegal_face_button: #Selecting the illegal button
                if len(legal_face_buttons) > 0: #We can swap you to another gadget
                    selected_face_button = legal_face_buttons[0]
                    self.write_u8(misc_addresses["selected_face_button"][self.game_region], {"triangle": 0, "circle": 1, "cross": 2, "square": 3}[selected_face_button]) #Highlight a legal button
                    self.write_u8(misc_addresses["equipped"][self.game_region], currently_equipped[selected_face_button]) #Put the chosen gadget in your hand
                    self.write_u8(equipped_gadget_addresses[illegal_face_button][self.game_region], 0) #Set the illegal face button to nothing
                    currently_equipped[illegal_face_button] = 0
                else: #We can't swap you to another gadget right now, so just put nothing there
                    self.write_u8(equipped_gadget_addresses[illegal_face_button][self.game_region], 0) #Set the illegal face button to nothing
                    self.write_u8(misc_addresses["equipped"][self.game_region], 0) #Put nothing in your hands
                    currently_equipped[illegal_face_button] = 0
            else:
                self.write_u8(equipped_gadget_addresses[illegal_face_button][self.game_region], 0) #Put nothing there

        for gadget_name in [gadget_name for gadget_name in self.unlocked_gadgets if gadget_name in gadget_ids]:
            if any(equipped_gadget_id == 0 for equipped_gadget_id in currently_equipped.values()): #Empty space available
                newly_received_gadget_id = gadget_ids[gadget_name]
                if all(equipped_gadget_id != newly_received_gadget_id for equipped_gadget_id in currently_equipped.values()): #Gadget not currently equipped
                    face_button_to_use = next((face_button for face_button, equipped_gadget_id in currently_equipped.items() if equipped_gadget_id == 0), None)
                    self.write_u8(equipped_gadget_addresses[face_button_to_use][self.game_region], newly_received_gadget_id)
                    currently_equipped[face_button_to_use] = newly_received_gadget_id

        if selected_face_button == None or currently_equipped[selected_face_button] == 0: #Nothing
            self.write_u8(misc_addresses["gadget_visible"][self.game_region], 0) #Hide your gadget
            self.write_u8(misc_addresses["selected_face_button"][self.game_region], 4)
            self.write_u8(misc_addresses["equipped"][self.game_region], 0) #Put nothing in your hands
            self.write_u32(misc_addresses["invisible_hoop_giver"][self.game_region], 0x00000000) #nop out the instruction that gives you an invisible Dash Hoop
            self.empty_hands = True
        elif self.empty_hands:
            self.write_u8(misc_addresses["gadget_visible"][self.game_region], 1) #Show your gadget
            self.empty_hands = False
            self.write_u32(misc_addresses["invisible_hoop_giver"][self.game_region], 0xAE220B14) #Restore the function that spawns your gadget in

    def trigger_falloff(self) -> None:
        self.write_u8(misc_addresses["in_first_person"][self.game_region], 0x00) #Take you out of first person
        self.write_u8(misc_addresses["camera_state"][self.game_region], 0x00) #Freeze camera in place
        self.write_u32(misc_addresses["y_position"][self.game_region], 0xFFFFFFFF) #Teleport you below the death barrier

    def to_float(self, value) -> int:
        return struct.unpack('<f', struct.pack('<I', value))[0]

    def get_player_position(self) -> list[float]:
        return [self.to_float(self.read_u32(misc_addresses["x_position"][self.game_region])), self.to_float(self.read_u32(misc_addresses["y_position"][self.game_region])), self.to_float(self.read_u32(misc_addresses["z_position"][self.game_region]))]

    def teleport_player_to_position(self, x, y, z) -> None:
        self.write_u32(misc_addresses["x_position"][self.game_region], x) 
        self.write_u32(misc_addresses["y_position"][self.game_region], y)
        self.write_u32(misc_addresses["z_position"][self.game_region], z)

    def get_closest_gate(self) -> str:
        level = level_from_name[self.current_level_name]
        available_gates = [room_entrance for room_entrance in level.room_entrances if room_entrance.source_room == self.read_u8(misc_addresses["room_to_be_loaded"][self.game_region])]
        if len(available_gates) == 1:
            return available_gates[0]
        elif len(available_gates) > 1:
            player_position = self.get_player_position()
            return min(available_gates, key=lambda location: sum((a - self.to_float(b)) ** 2 for a, b in zip(player_position, location.trigger_pos)))
        else:
            return None

    def set_gotcha_box_enabled(self, enabled) -> None:
        if enabled:
            self.write_u8(misc_addresses["gotcha_box_enabled"][self.game_region], 0x01)
            self.gotcha_box_state = "enabled"
        else:
            self.write_u8(misc_addresses["gotcha_box_enabled"][self.game_region], 0x00)
            self.gotcha_box_state = "disabled"

    def unlock_collectible(self, collectible_name) -> None:
        if collectible_name in gotcha_box_collectibles:
            self.write_u8(gotcha_box_collectibles[collectible_name][self.game_region], 0xFF)
            self.unlocked_collectibles.add(collectible_name)

    def restore_collectibles(self) -> None:
        for collectible_name in self.unlocked_collectibles:
            self.write_u8(gotcha_box_collectibles[collectible_name][self.game_region], 0xFF)

    def update_gotcha_box(self) -> None:
        if self.gotcha_box_state == "unknown": #Patches the Gotcha Box to disable itself after each item dispensed, this is so we can see the gotcha box has disabled itself, send a location and then manually re-enable it
            self.write_u32(misc_addresses["dispense_gotcha_box_capsule"][self.game_region], 0x00000000) #nop
            self.write_u32(misc_addresses["gotcha_box_patch_a"][self.game_region], 0x3C0201F5) #lui v0,0x01F5
            self.write_u32(misc_addresses["gotcha_box_patch_b"][self.game_region], 0x3442924C) #ori v0,v0,0x924C
            self.write_u32(misc_addresses["gotcha_box_patch_c"][self.game_region], 0xAC400000) #sw zero,0x0(v0)
            self.restore_collectibles() #Restores collectible state when loading into the Travel Station
        elif self.gotcha_box_state == "enabled" and self.read_u8(misc_addresses["gotcha_box_enabled"][self.game_region]) == 0x00:
            self.obtained_gotcha_box_checks.add(self.missing_gotcha_box_checks.pop(0))

        if len(self.missing_gotcha_box_checks) > 0 and self.gotcha_box_gating == 1: #Level based gating
            required_levels = int((len(levels) - 2) * ((self.missing_gotcha_box_checks[0] - 2001) / self.gotcha_box_locations))
            unlocked_level_count = sum(world_key_requirement <= self.world_keys for world_key_requirement in self.world_key_requirements.values())
            if unlocked_level_count >= required_levels:
                self.set_gotcha_box_enabled(True)
            else:
                self.set_gotcha_box_enabled(False)
        elif len(self.missing_gotcha_box_checks) > 0 and ((self.gotcha_box_gating == 0) or #No gating
            (self.gotcha_box_gating == 2 and self.gotcha_box_restocks >= int((self.missing_gotcha_box_checks[0] - 2001) / 10))): #Restock based gating
            self.set_gotcha_box_enabled(True)
        else:
            self.set_gotcha_box_enabled(False)            

    def activate_trap(self, trap_id) -> None:
        self.active_traps[trap_id] = datetime.datetime.now() + datetime.timedelta(seconds = 5)
        if trap_id == 400: #Lazy Camera Trap
            self.write_u8(misc_addresses["in_first_person"][self.game_region], 0x00)
            self.write_u8(misc_addresses["camera_state"][self.game_region], 0x00)
        elif trap_id == 401: #Rocket Boots Trap
            self.write_u32(misc_addresses["hikaru_max_speed"][self.game_region], 0x50000000)
        elif trap_id == 402: #Slowness Trap
            self.write_u32(misc_addresses["hikaru_max_speed"][self.game_region], 0x3F200000)

    def update_traps(self) -> None:
        completed_traps = []
        for trap in self.active_traps:
            if self.active_traps[trap] < datetime.datetime.now(): #Trap expired
                completed_traps.append(trap)
        for trap in completed_traps:
            if trap == 400: #Lazy Camera Trap
                self.write_u8(misc_addresses["in_first_person"][self.game_region], 0x00)
                self.write_u8(misc_addresses["camera_state"][self.game_region], 0x02)                
            elif trap in [401, 402]: #Speed Traps
                self.write_u32(misc_addresses["hikaru_max_speed"][self.game_region], 0x3FC7AE12)
            del self.active_traps[trap]

    def set_transitions_enabled(self, enabled) -> None:
        if enabled:
            self.write_u32(misc_addresses["transition_function_a"][self.game_region], 0xAC620004)
            self.write_u32(misc_addresses["transition_function_b"][self.game_region], 0xB2060007)
        else:
            self.write_u32(misc_addresses["transition_function_a"][self.game_region], 0x00000000)
            self.write_u32(misc_addresses["transition_function_b"][self.game_region], 0x00000000)

    def set_gate_destination_room(self, room_name) -> None:
        self.write_string_at(self.transition_pointer + 0x54, room_name)

    def set_gate_destination_spawn(self, spawn_name) -> None:
        self.write_string_at(self.transition_pointer + 0x8C, spawn_name)

    def update_active_gate(self) -> None:
        if self.read_u8(misc_addresses["in_transition"][self.game_region]) != 2: #Not already in an active transition
            closest_gate = self.get_closest_gate()
            if closest_gate != None and f"{closest_gate.name} - {self.current_level_name}" in self.randomised_gates:
                print(f"{closest_gate.name} found: {self.randomised_gates[f"{closest_gate.name} - {self.current_level_name}"]}")
                self.set_gate_destination_room(self.randomised_gates[f"{closest_gate.name} - {self.current_level_name}"]["room"])
                self.set_gate_destination_spawn(self.randomised_gates[f"{closest_gate.name} - {self.current_level_name}"]["spawn"])

    def apply_custom_music_map(self) -> None:
        for room in self.music_map:
            self.write_u8(music_table[int(room)]["address"][self.game_region], self.music_map[room])
        self.applied_custom_music_map = True

    def interpret_randomised_gates(self, gate_mapping) -> None:
        self.randomised_gates = {}
        for source_gate, target_gate in gate_mapping.items():
            self.randomised_gates[source_gate] = {"room": gate_from_name[target_gate].dest_room, "spawn": gate_from_name[target_gate].dest_spawn}

    def enforce_game_state(self) -> None:
        current_screen = self.read_u8(misc_addresses["screen"][self.game_region])

        if self.read_u8(misc_addresses["natsumi_introduced"][self.game_region]) == 0: #Starting a new game (haven't heard Natsumi's introduction), so force you to the Travel Station instead of Liberty Island
            self.natsumi_introduced = False
            self.write_u8(misc_addresses["level_to_be_loaded"][self.game_region], 0x71) #Force to Travel Station
        elif current_screen == 1: #In the Travel Station
            #Update Natsumi introduction state tracking
            self.natsumi_introduced = True

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
            else:
                self.current_level_name = "Travel Station"
                self.tracker_level_name = self.current_level_name
                if self.previous_level_select_location != -1:
                    self.write_u8(misc_addresses["selected"][self.game_region], self.previous_level_select_location)

            if not self.applied_custom_music_map:
                self.apply_custom_music_map()

            if self.randomised_gates != {}: #Re-enable level transitions in preparation for next stage
                self.set_transitions_enabled(True)
                self.transition_state = "default"

            self.auto_equip()

            if self.gotcha_box_gating != -1:
                self.update_gotcha_box()

        elif current_screen != 31: #Not in the title screen and not in the Travel Station

            #Update level name
            if self.transition_state != "teleporting_to_door" and current_screen - 2 < len(levels):
                self.current_level_name = levels[current_screen - 2].name
                self.tracker_level_name = self.current_level_name
            self.write_u8(misc_addresses["cleared"][self.game_region], 255) #Sets 255 levels to cleared - stops you getting taken to boss fights

            #Check message phones
            if self.message_phone_locations:
                message_info_pointer = self.read_u32(misc_addresses["message_info_pointer"][self.game_region])
                if message_info_pointer != None and message_info_pointer != 0 and not message_info_pointer in self.used_message_info_pointers:
                    message_name_pointer = self.read_u32(message_info_pointer + 0x8)
                    self.used_message_info_pointers.append(message_info_pointer)
                    phone_name = self.read_u64(message_name_pointer).to_bytes(8, "little").decode("ascii").rstrip("\x00")
                    print(f"Phone Detected: {phone_name}")
                    if phone_name.strip() in phone_from_name:
                        self.activated_phones.add(phone_from_name[phone_name].id)

            #Swimming Prevention
            if self.can_swim == False and self.read_u8(misc_addresses["air_meter_showing"][self.game_region]) != 0:
                self.trigger_falloff()

            if current_screen != 30: #Not in the Gadget Trainer
                 self.auto_equip()
            self.gotcha_box_state = "unknown" 

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

        if current_screen == 33: #"Catch Monkeys!" screen
            if self.randomised_gates != {} and self.transition_state == "default" and self.current_level_name != None and len(level_from_name[self.current_level_name].room_entrances) > 1:
                self.write_u8(misc_addresses["level_to_be_loaded"][self.game_region], 0x54) #Load you into Moon Base (before Magnetic Panels)
                if str(int(self.target_room_to_load)) in self.music_map:
                    music_value = self.music_map[str(int(self.target_room_to_load))]
                else:
                    music_value = music_table[self.target_room_to_load]["value"]
                self.write_u8(music_table[0x54]["address"][self.game_region], music_value) #Replace Moon Base Moving Platforms music with desired level's music
                self.transition_state = "teleporting_to_door"

        if (current_screen >= 1 and current_screen < 30): #In the hub or in a level
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
            self.update_traps()

            #Air Crawl Prevention
            hikaru_state = self.read_u8(misc_addresses["hikaru_state"][self.game_region])
            if (not self.air_crawl_allowed) and hikaru_state in [7, 8, 9] and self.read_u8(misc_addresses["y_velocity"][self.game_region]) != 0:
                self.write_u8(misc_addresses["hikaru_state"][self.game_region], 0)

            #Transition randomisation
            if self.randomised_gates != {}:
                #Teleport to known door in Moon Base, record details, lock transitions and then warp you back to desired room
                if current_screen == 0x1B and self.transition_state == "teleporting_to_door":
                    self.write_u8(misc_addresses["in_first_person"][self.game_region], 2) #Turn off camera
                    self.teleport_player_to_position(0xC33D34DD, 0x41DF3F4F, 0xC1BA0349) #Teleport you to the door 
                    self.transition_pointer = self.read_u32(misc_addresses["gate_pointer"][self.game_region]) #Check transition pointer
                    if self.read_u64(self.transition_pointer + 0x54) == 0x31435f4f4f4d: #MOO_D identifier for target room
                        if '84' in self.music_map:
                            music_value = self.music_map['84']
                        else:
                            music_value = music_table[0x54]["value"]
                        self.write_u8(music_table[0x54]["address"][self.game_region], music_value) #Restore the Moon Base music
                        self.set_transitions_enabled(False) #Lock transitions from updating
                        self.write_u8(misc_addresses["room_to_be_loaded"][self.game_region], self.target_room_to_load) #Set room to be loaded
                        self.write_u8(misc_addresses["reload_room"][self.game_region], 4) #Reload the room
                        self.transition_state = "transitions_locked" #Update state

                #Game is paused or exiting level or Hikaru is celebrating, so unlock transitions
                if self.transition_state == "transitions_locked" and (self.read_u8(misc_addresses["game_paused"][self.game_region]) == 0x03 or self.read_u8(misc_addresses["game_paused"][self.game_region]) == 0x01 or hikaru_state == 49):
                    self.set_transitions_enabled(True)
                    self.transition_state = "transitions_temporarily_available"
                #Game is unpaused and not exiting level and Hikaru is not celebrating, so lock transitions again           
                elif self.transition_state == "transitions_temporarily_available" and self.read_u8(misc_addresses["game_paused"][self.game_region]) != 0x03 and self.read_u8(misc_addresses["game_paused"][self.game_region]) != 0x01 and hikaru_state != 49: 
                    self.set_transitions_enabled(False)
                    self.transition_state = "transitions_locked"
                #Transitions are locked and ready to be messed with
                elif self.transition_state == "transitions_locked":
                    self.update_active_gate()

            #Double Jump Prevention - future item?
            #if hikaru_state == 4: #Jumping
            #    self.write_u8(misc_addresses["jump_state"][self.game_region], 3) #Double jumped

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