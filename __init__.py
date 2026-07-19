GEN_VERSION = "1.0" #Used to match with client
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
from .Levels import levels

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
        "Slingshot": {"Catapult"},
        "Slingback Shooter": {"Catapult"},
        "Sling": {"Catapult"},
        "Slingback": {"Catapult"},

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

    def pick_progression_items(self) -> list[str]:
        progression_items = [gadget for gadget in ["Monkey Net", "Stun Club", "Dash Hoop", "Catapult", "Sky Flyer", "R.C. Car", "Bananarang", "Water Cannon", "Electro Magnet", "Power Punch", "Monkey Radar", "See-All Scope"] if not gadget in self.starting_items]
        progression_items += ["World Key"] * max(self.world_key_requirements.values())
        if self.options.shuffle_air_crawl.value:
            progression_items.append("Air Crawl")
        if self.options.shuffle_water_net.value:
            progression_items.append("Water Net")
        return sorted(progression_items)

    def pick_useful_items(self) -> list[str]:
        useful_items = [] #No useful items yet
        return sorted(useful_items)

    def pick_filler_items(self, remaining_locations) -> list[str]:
        filler_items = []
        while len(filler_items) < remaining_locations:
            filler_items.append(self.get_filler_item_name())
        return sorted(filler_items)

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

        self.filler_item_names = self.pick_filler_items(total_locations - len(self.progression_item_names + self.useful_item_names))

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
            self.options.message_phone_locations.value = True
        else:
            if self.options.playable_character.value == 0:
                self.starting_items.append("Pipotchi")
            if self.options.shuffle_water_net.value == False:
                self.starting_items.append("Water Net")
            if self.options.shuffle_air_crawl.value == False:
                self.starting_items.append("Air Crawl")

            for entry in self.options.starting_gadgets.value:
                entry = entry.lower()
                the_gadget = None

                if entry == "random":
                    possible_gadgets = [gadget for gadget in ["Monkey Net", "Stun Club", "Monkey Radar", "Dash Hoop", "Catapult", "Sky Flyer", "R.C. Car", "Bananarang", "Water Cannon", "Electro Magnet", "Power Punch"] if not gadget in self.starting_items]
                    if len(possible_gadgets) > 0:
                        the_gadget = self.random.choice(possible_gadgets)
                elif entry in ["monkey net", "stun club", "monkey radar", "dash hoop", "catapult", "sky flyer", "r.c. car", "bananarang", "water cannon", "electro magnet", "power punch"]:
                    the_gadget = next((gadget for gadget in ["Monkey Net", "Stun Club", "Monkey Radar", "Dash Hoop", "Catapult", "Sky Flyer", "R.C. Car", "Bananarang", "Water Cannon", "Electro Magnet", "Power Punch"] if gadget.lower() == entry.lower()), None)
                else:
                    the_gadget = next((gadget for alias, gadget in gadget_aliases.items() if alias.lower() == entry), None)

                if the_gadget != None and not the_gadget in self.starting_items:
                    self.starting_items.append(the_gadget)

            if self.options.message_phone_locations.value == False and not "Monkey Net" in self.starting_items:
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

                if not "Monkey Net" in self.starting_items: #Ensure there is at least one level in sphere 1 with an available phone                
                    levels_with_free_phones = ["Liberty Island", "Breezy Village", "Viva Apespania", "Castle Frightmare", "Vita-Z Factory", "Casino City", "Ninja Hideout", "Snowball Mountain", "The Blue Baboon", "The Lost World"]
                    if "Water Net" in self.starting_items:
                        levels_with_free_phones.append("Port Calm")
                    free_phone_level = self.random.choice(levels_with_free_phones)
                    early_level_index, free_phone_level_index = self.random.randint(0, 2), level_order.index(free_phone_level)
                    level_order[free_phone_level_index], level_order[early_level_index] = level_order[early_level_index], level_order[free_phone_level_index]
                    print(free_phone_level)

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

        self.preplaced_progression = ["Victory"] + self.starting_items
        self.progression_item_names = self.pick_progression_items()
        self.useful_item_names = self.pick_useful_items()

    def fill_slot_data(self) -> dict[str, object]:
        return {"world_key_requirements": self.world_key_requirements, "deathlink_enabled": self.options.death_link.value, "logic_difficulty": self.options.logic_difficulty.value, "damage_boost_logic": self.options.damage_boost_logic.value, "air_crawl_logic": self.options.air_crawl_logic.value, "boost_jump_logic": self.options.boost_jump_logic.value, "boost_fly_logic": self.options.boost_fly_logic.value, "long_jump_logic": self.options.long_jump_logic.value, "character": self.options.playable_character.value, "hidden_monkey_logic": self.options.hidden_monkey_logic.value}

    def get_filler_item_name(self) -> str:
        random = self.random.random()

        items = ["Gold Coin", "10 Gold Coins", "20 Gold Coins", "Jacket", "Explosive Pellet", "Guided Pellet", "Cookie", "Deluxe Cookie", "Case of Explosive Pellets", "Case of Guided Pellets"]
        weights = [5, 4, 3, 3, 2, 2, 5, 3, 1, 1]

        return self.random.choices(items, weights=weights, k=1)[0]
    
    def create_item(self, name: str) -> AE2Item:
        try:
            if name == self.glitches_item_name or name in self.starting_items or name in self.preplaced_progression or name in self.progression_item_names:
                item_classification = ItemClassification.progression
            elif name in self.useful_item_names:
                item_classification = ItemClassification.useful
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
            spoiler_string += f"\n{level}: {self.world_key_requirements[level]}"
        
        spoiler_handle.write(spoiler_string)       