gen_ver = "1.3"

from BaseClasses import Item, ItemClassification
from worlds.AutoWorld import WebWorld, World
from worlds.LauncherComponents import Component, components, launch_subprocess, Type
from .Items import AE2Item, item_id_from_name, gadget_aliases
from .Locations import location_id_from_name, location_groups
from .Options import AE2Options, option_groups
from .Regions import create_regions
from Options import OptionError
import copy, math
from .Monkeys import monkeys
from .Levels import levels, level_from_name, build_randomised_maps
from .Music import music_table, randomised_music_pool

#Identifier for Archipelago to recognize and run the client
def run_client() -> None:
    from .Client import launch
    launch_subprocess(launch, name="AE2Client")

components.append(Component("Ape Escape 2 Client", func=run_client, component_type=Type.CLIENT))

class AE2WebWorld(WebWorld):
    theme = "jungle"
    
    '''
    setup = Tutorial(
        tutorial_name = "Setup Guide",
        description = "A guide to setting up the Ape Escape 2 Archipelago Multiworld",
        language = "English",
        file_name = "setup.md",
        link = "setup/en",
        authors = ["Bonzorio"]
    )
    tutorials = [setup]
    '''

    option_groups = option_groups

class AE2World(World):
    """
    Ape Escape 2
    """
    game = "Ape Escape 2"
    web = AE2WebWorld()
    options_dataclass = AE2Options
    options: AE2Options

    topology_present = False

    item_name_to_id = item_id_from_name
    location_name_to_id = location_id_from_name

    #Aliases
    item_name_groups = {
        #Monkey Net
        "Net": {"Monkey Net"},
        "Time Net": {"Monkey Net"},

        #Stun Club
        "Club": {"Stun Club"},

        #Monkey Radar
        "Radar": {"Monkey Radar"},

        #Dash Hoop
        "Super Hoop": {"Dash Hoop"},
        "Hoop": {"Dash Hoop"},

        #Catapult
        "Slingshot": {"Catapult", "Progressive Catapult"},
        "Slingback Shooter": {"Catapult", "Progressive Catapult"},
        "Sling": {"Catapult", "Progressive Catapult"},
        "Slingback": {"Catapult", "Progressive Catapult"},

        #Sky Flyer
        "Flyer": {"Sky Flyer"},

        #R.C. Car
        "RC Car": {"R.C. Car"},
        "Car": {"R.C. Car"},

        #Electro Magnet
        "Magnet": {"Electro Magnet"},

        #Power Punch
        "Magic Punch": {"Power Punch"},
        "Punch": {"Power Punch"}
    }

    location_name_groups = location_groups

    #Universal Tracker
    ut_can_gen_without_yaml = True
    glitches_item_name = "Glitched Item"

    explicit_indirect_conditions = False

    def get_catapult_item_name(self) -> str:
        if self.options.air_crawl_behaviour.value == 3:
            return "Progressive Catapult"
        else:
            return "Catapult"

    def pick_progression_items(self) -> list[str]:
        progression_items = [gadget for gadget in ["Monkey Net", "Stun Club", "Dash Hoop", self.get_catapult_item_name(), "Sky Flyer", "R.C. Car", "Bananarang", "Water Cannon", "Electro Magnet", "Power Punch", "Monkey Radar", "See-All Scope"] if not gadget in self.starting_items]
        progression_items += ["World Key"] * (max(self.world_key_requirements.values()) + self.options.extra_world_keys.value)
        if self.options.air_crawl_behaviour.value == 2:
            progression_items.append("Air Crawl")
        elif self.options.air_crawl_behaviour.value == 3:
            progression_items.append("Progressive Catapult")
        if self.options.shuffle_water_net.value:
            progression_items.append("Water Net")
        if self.options.gotcha_box_gating.value == 2:
            progression_items += ["Gotcha Box Restock"] * int((self.options.gotcha_box_locations.value - 1) / 10) #Each Gotcha Box Restock item adds 10 locations
        return sorted(progression_items)

    def pick_useful_items(self) -> list[str]:
        useful_items = ["Dance, Monkey, Dance!", "Monkey Football", "Monkey Climber", "Tissues R.C. Car Body", "Sushi R.C. Car Body", "Black R.C. Car Body", "Pudding R.C. Car Body"]
        return sorted(useful_items)

    def pick_filler_items(self, remaining_locations) -> list[str]:
        filler_items = []
        if self.options.shuffle_collectible_filler.value:
            all_filler_collectibles = [item_name for item_name, item_id in item_id_from_name.items() if item_id >= 1007 and item_id <= 1248]
            self.random.shuffle(all_filler_collectibles)
            number_of_collectibles_to_include = min(int(remaining_locations * 0.5), len(all_filler_collectibles))
            filler_items += all_filler_collectibles[:number_of_collectibles_to_include]

        while len(filler_items) < remaining_locations:
            filler_items.append(self.get_filler_item_name())
        return sorted(filler_items)

    def pick_trap_items(self, number_of_traps) -> list[str]:
        trap_items = []
        trap_weights = {"Lazy Camera Trap": self.options.lazy_camera_trap_weight.value, "Rocket Boots Trap": self.options.rocket_boots_trap_weight.value, "Slowness Trap": self.options.slowness_trap_weight.value}
        if sum(list(trap_weights.values())) != 0:
            for i in range(0, number_of_traps):
                trap_items.append(self.random.choices(list(trap_weights.keys()), weights=list(trap_weights.values()), k=1)[0])
        return sorted(trap_items)

    def create_items(self) -> None:
        item_pool: list[AE2Item] = []
        self.filler_item_names: list[str] = []
        self.trap_item_names: list[str] = []

        if self.options.goal.value == 0:
            self.multiworld.get_location("Showdown with Specter!: Specter", self.player).place_locked_item(self.create_item("Victory")) 
        else:
            self.multiworld.get_location("Final Showdown with Specter!: Specter", self.player).place_locked_item(self.create_item("Victory")) 

        #Starting inventory
        for starting_item in self.starting_items:
            self.multiworld.push_precollected(self.create_item(starting_item))

        total_locations = len(self.multiworld.get_unfilled_locations(self.player))
        remaining_locations = total_locations - len(self.progression_item_names + self.useful_item_names)

        number_of_traps = int(remaining_locations * (self.options.trap_percentage.value/100)) #Determines the number of traps based on the number of filler items left and the desired trap percentage, rounding down
        if number_of_traps > 0:
            self.trap_item_names = self.pick_trap_items(number_of_traps)
        else:
            self.trap_item_names = []

        self.filler_item_names = self.pick_filler_items(total_locations - len(self.progression_item_names + self.useful_item_names + self.trap_item_names))

        for item in self.progression_item_names + self.useful_item_names + self.filler_item_names + self.trap_item_names:
            item_pool.append(self.create_item(item))

        self.multiworld.itempool += item_pool

    def generate_early(self) -> None: 
        self.starting_items = []
        if hasattr(self.multiworld, "re_gen_passthrough"): #If generated through Universal Tracker passthrough
            slot_data: dict = self.multiworld.re_gen_passthrough[self.game]
            self.world_key_requirements = slot_data["world_key_requirements"]
            self.options.logic_difficulty.value = slot_data["logic_difficulty"]
            self.options.air_crawl_logic.value = slot_data["air_crawl_logic"]
            self.options.boost_fly_logic.value = slot_data["boost_fly_logic"]
            self.options.boost_jump_logic.value = slot_data["boost_jump_logic"]
            self.options.long_jump_logic.value = slot_data["long_jump_logic"]
            self.options.damage_boost_logic.value = slot_data["damage_boost_logic"]
            self.options.hidden_monkey_logic.value = slot_data["hidden_monkey_logic"]
            self.randomised_starting_rooms = slot_data["randomised_starting_rooms"]
            self.options.gotcha_box_locations.value = slot_data["gotcha_box_locations"]
            self.options.gotcha_box_gating.value = slot_data["gotcha_box_gating"]
            self.options.message_phone_locations.value = slot_data["message_phone_locations"]
            self.randomised_gates = {}
        else:
            if self.options.playable_character.value == 0: #playing as Hikaru
                self.starting_items.append("Pipotchi")
            else: #playing as Kakeru
                self.options.message_phone_locations.value = False
            if self.options.shuffle_water_net.value == False:
                self.starting_items.append("Water Net")
            if self.options.air_crawl_behaviour.value == 0:
                self.starting_items.append("Air Crawl")

            for entry in self.options.starting_gadgets.value:
                entry = entry.lower()
                the_gadget = None

                if entry == "random":
                    possible_gadgets = [gadget for gadget in ["Monkey Net", "Stun Club", "Monkey Radar", "Dash Hoop", self.get_catapult_item_name(), "Sky Flyer", "R.C. Car", "Bananarang", "Water Cannon", "Electro Magnet", "Power Punch"] if not gadget in self.starting_items]
                    if len(possible_gadgets) > 0:
                        the_gadget = self.random.choice(possible_gadgets)
                elif entry in ["monkey net", "stun club", "monkey radar", "dash hoop", "catapult", "sky flyer", "r.c. car", "bananarang", "water cannon", "electro magnet", "power punch"]:
                    the_gadget = next((gadget for gadget in ["Monkey Net", "Stun Club", "Monkey Radar", "Dash Hoop", "Catapult", "Sky Flyer", "R.C. Car", "Bananarang", "Water Cannon", "Electro Magnet", "Power Punch"] if gadget.lower() == entry.lower()), None)
                else:
                    the_gadget = next((gadget for alias, gadget in gadget_aliases.items() if alias.lower() == entry), None)
                if the_gadget == "Catapult" and the_gadget != self.get_catapult_item_name():
                    the_gadget = self.get_catapult_item_name()

                if the_gadget != None and not the_gadget in self.starting_items:
                    self.starting_items.append(the_gadget)

            if self.options.message_phone_locations.value == False and self.options.gotcha_box_locations.value == 0 and not "Monkey Net" in self.starting_items:
                self.starting_items.append("Monkey Net")

            if self.options.level_shuffle.value:
                level_order = []

                if self.options.goal.value == 0:
                    levels[-2].keep_at_end = True #Don't shuffle "Showdown with Specter!" if it's your goal

                bosses = [level.name for level in levels if level.is_boss and not level.keep_at_end] #Shuffle order of boss levels
                self.random.shuffle(bosses)
                not_bosses = [level.name for level in levels if not level.is_boss and not level.keep_at_end] #Shuffle order of non-boss levels
                self.random.shuffle(not_bosses)

                if self.options.level_shuffle.value == 1: #Separate - slot them back in 
                    for level in levels:
                        if level.is_boss:
                            if len(bosses) > 0:
                                level_order.append(bosses.pop())
                        else:
                            level_order.append(not_bosses.pop())
                else: #Mixed - combine them
                    level_order = not_bosses[:3] #First three levels won't be bosses
                    to_be_added = bosses + not_bosses[3:]
                    self.random.shuffle(to_be_added)
                    level_order += to_be_added
                level_order += [level.name for level in levels if level.keep_at_end]
            else: #Level shuffle disabled
                level_order = [level.name for level in levels]

            if self.options.goal.value == 0: #Remove final showdown if not playing with that goal
                level_order.remove("Final Showdown with Specter!")

            self.world_key_requirements = {}

            current_key_requirement = 0
            was_boss = False
            for level_name in level_order:
                if level_name != "Final Showdown with Specter!": #You don't need a World Key to access the Final Showdown - just catch the monkeys
                    if self.options.world_key_behaviour.value == 0 and (level_order.index(level_name) >= 3):
                        current_key_requirement += 1
                    elif self.options.world_key_behaviour.value == 1 and was_boss:
                        current_key_requirement += 1
                    elif self.options.world_key_behaviour.value == 2 and ((levels[level_order.index(level_name)].is_boss) or (was_boss)):
                        current_key_requirement += 1
                self.world_key_requirements[level_name] = current_key_requirement
                was_boss = levels[level_order.index(level_name)].is_boss

            self.randomised_starting_rooms = {}
            if self.options.randomise_starting_room.value:
                for level in levels:
                    self.randomised_starting_rooms[level.name] = level.room_entrances.index(self.random.choice([entrance for entrance in level.room_entrances if entrance.can_start]))

            self.randomised_gates = {}
            if False:#self.options.randomise_area_transitions.value:
                shuffles = 1
                print("Ape Escape 2: Shuffling transitions...")
                while True:
                    try:
                        self.randomised_gates = build_randomised_maps(self)
                        print(f"Ape Escape 2: Transitions shuffled {shuffles} times.")
                        break
                    except Exception as e:
                        shuffles += 1
                        if shuffles > 5000:
                            print("Ape Escape 2: Exceeded 5000 shuffles and unable to generate valid transitions.")
                            break
                
            self.music_map = {}
            if self.options.music_randomisation.value:
                song_replacements = {}
                for music_entry in music_table:
                    if self.options.music_randomisation.value == 1 and music_table[music_entry]["value"] in song_replacements:
                        self.music_map[music_entry] = song_replacements[music_table[music_entry]["value"]]
                    else:
                        self.music_map[music_entry] = self.random.choice(randomised_music_pool)
                        song_replacements[music_table[music_entry]["value"]] = self.music_map[music_entry]

        self.preplaced_progression = ["Victory"] + self.starting_items
        self.progression_item_names = self.pick_progression_items()
        self.useful_item_names = self.pick_useful_items()

    def fill_slot_data(self) -> dict[str, object]:
        return {"world_key_requirements": self.world_key_requirements, "deathlink_enabled": self.options.death_link.value, "logic_difficulty": self.options.logic_difficulty.value, "damage_boost_logic": self.options.damage_boost_logic.value, "air_crawl_logic": self.options.air_crawl_logic.value, "boost_jump_logic": self.options.boost_jump_logic.value, "boost_fly_logic": self.options.boost_fly_logic.value, "long_jump_logic": self.options.long_jump_logic.value, "character": self.options.playable_character.value, "hidden_monkey_logic": self.options.hidden_monkey_logic.value, "randomised_starting_rooms": self.randomised_starting_rooms, "randomised_gates": self.randomised_gates, "music_map": self.music_map, "gen_ver": gen_ver, "gotcha_box_locations": self.options.gotcha_box_locations.value, "gotcha_box_gating": self.options.gotcha_box_gating.value, "message_phone_locations": self.options.message_phone_locations.value, "level_order": list(self.world_key_requirements.keys())}

    def get_filler_item_name(self) -> str:
        items = ["Gold Coin", "10 Gold Coins", "20 Gold Coins", "Jacket", "Explosive Pellet", "Guided Pellet", "Cookie", "Deluxe Cookie", "3 Explosive Pellets", "3 Guided Pellets"]
        weights = [5, 4, 3, 3, 2, 2, 5, 3, 1, 1]
        return self.random.choices(items, weights=weights, k=1)[0]
    
    def create_item(self, name: str) -> AE2Item:
        try:
            if name == self.glitches_item_name or name in self.starting_items or name in self.preplaced_progression or name in self.progression_item_names:
                item_classification = ItemClassification.progression
            elif name in self.useful_item_names:
                item_classification = ItemClassification.useful
            elif name in self.trap_item_names:
                item_classification = ItemClassification.trap
            else:
                item_classification = ItemClassification.filler
        except:
            item_classification = ItemClassification.progression

        return AE2Item(name, item_classification, item_id_from_name[name], self.player)

    def set_rules(self) -> None:
        self.multiworld.completion_condition[self.player] = lambda state: state.has("Victory", self.player)

    def create_regions(self) -> None:
        create_regions(self)

    def write_spoiler(self, spoiler_handle: object) -> None:
        spoiler_string = f"\nApe Escape 2 Spoiler ({self.multiworld.player_name[self.player]}):\n"
        
        spoiler_string += "\nWorld Key Requirements:"
        for level in self.world_key_requirements:
            if level in self.randomised_starting_rooms and self.randomised_starting_rooms[level] != 0:
                spoiler_string += f"\n{level} ({level_from_name[level].room_entrances[self.randomised_starting_rooms[level]].name.split(" from ")[0]}): {self.world_key_requirements[level]}"
            else:
                spoiler_string += f"\n{level}: {self.world_key_requirements[level]}"

        if self.randomised_gates != {}:
            spoiler_string += "\n\nRandomised Transitions:"
            for gate in self.randomised_gates:
                spoiler_string += f"\n{gate} = {self.randomised_gates[gate]}"

        spoiler_handle.write(spoiler_string)       