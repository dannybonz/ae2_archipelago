from BaseClasses import Region
from worlds.AutoWorld import World
from .Locations import AE2Location, location_id_from_name, location_name_from_id
from .Items import AE2Item
from BaseClasses import ItemClassification
from .Levels import levels
from .Monkeys import monkey_from_name
import copy

def can_reach_connection(state, world, player, requirements):

    if state.has("Glitched Item", player):
        hard = True
        expert = True
        air_crawl = state.has("Catapult", player) and state.has("Air Crawl", player)
        long_jump = state.has("Dash Hoop", player)
        boost_fly = state.has("Sky Flyer", player)
        damage_boost = True
        boost_jump = state.has("Monkey Net", player) and (state.has("Stun Club", player) or state.has("Monkey Radar", player) or state.has("Dash Hoop", player) or state.has("Catapult", player) or state.has("Sky Flyer", player) or state.has("R.C. Car", player) or state.has("Bananarang", player) or state.has("Water Cannon", player) or state.has("Electro Magnet", player) or state.has("Power Punch", player))
        hidden_monkey_logic = False
    else:
        hard = world.options.logic_difficulty.value > 0
        expert = world.options.logic_difficulty.value > 1
        air_crawl = state.has("Catapult", player) and state.has("Air Crawl", player) and world.options.air_crawl_logic.value
        long_jump = state.has("Dash Hoop", player) and world.options.long_jump_logic.value
        boost_fly = state.has("Sky Flyer", player) and world.options.boost_fly_logic.value and (state.has("Monkey Net", player) or state.has("Electro Magnet", player) or state.has("Stun Club", player) or state.has("Power Punch", player))
        damage_boost = world.options.damage_boost_logic.value
        boost_jump = state.has("Monkey Net", player) and world.options.boost_jump_logic.value and (state.has("Stun Club", player) or state.has("Monkey Radar", player) or state.has("Dash Hoop", player) or state.has("Catapult", player) or state.has("Sky Flyer", player) or state.has("R.C. Car", player) or state.has("Bananarang", player) or state.has("Water Cannon", player) or state.has("Electro Magnet", player) or state.has("Power Punch", player))
        hidden_monkey_logic = world.options.hidden_monkey_logic.value

    requirements = copy.deepcopy(requirements) #Fixes a UT oddity

    for item_group in requirements:
        while "*Air Crawl" in item_group and air_crawl:
            item_group.remove("*Air Crawl")

        while "*Damage Boost" in item_group and damage_boost:
            item_group.remove("*Damage Boost")

        while "*Boost Fly" in item_group and boost_fly:
            item_group.remove("*Boost Fly")

        while "*Boost Jump" in item_group and boost_jump:
            item_group.remove("*Boost Jump")

        while "*Bull Fight" in item_group and (state.has("Catapult", player) or state.has("Stun Club", player) or state.has("Power Punch", player) or state.has("Dash Hoop", player) or (state.has("Sky Flyer", player) and expert)): #To attack the monkeys that get in bulls
            item_group.remove("*Bull Fight")

        while "*UFO" in item_group and (hard or state.has("Catapult", player) or state.has("Stun Club", player) or state.has("Power Punch", player)): #To attack the monkeys that get in UFOs
            item_group.remove("*UFO")

        while "*Gear" in item_group and (state.has("Stun Club", player) or state.has("Power Punch", player)): #To spin gears
            item_group.remove("*Gear")

        while "*Punch" in item_group and (state.has("Power Punch", player) and (state.has("See-All Scope", player) or not hidden_monkey_logic)): #To find hidden Power Punch monkeys
            item_group.remove("*Punch")

        while "*Radar" in item_group and (state.has("Monkey Radar", player) or not hidden_monkey_logic): #To find hidden monkeys
            item_group.remove("*Radar")

        while "*Attack" in item_group and (state.has("Stun Club", player) or state.has("Power Punch", player) or state.has("Dash Hoop", player)):
            item_group.remove("*Attack")

        while "*Hard" in item_group and hard:
            item_group.remove("*Hard")

        while "*Expert" in item_group and expert:
            item_group.remove("*Expert")

        while "*Non-Net" in item_group and (state.has("Stun Club", player) or state.has("Monkey Radar", player) or state.has("Dash Hoop", player) or state.has("Catapult", player) or state.has("Sky Flyer", player) or state.has("R.C. Car", player) or state.has("Bananarang", player) or state.has("Water Cannon", player) or state.has("Electro Magnet", player) or state.has("Power Punch", player)):
            item_group.remove("*Non-Net")

        #Lookout Valley
        while "*Valley Gap" in item_group and ((state.has("Sky Flyer", player) and state.has("Catapult", player)) or
                                            (expert and ((((state.has("Power Punch", player) or state.has("Sky Flyer", player)) and state.has("Water Net", player))) or state.has("Catapult", player))) or 
                                            (air_crawl) or 
                                            (expert and long_jump and (state.has("Pipotchi", player) or state.has("Stun Club", player)))):
            item_group.remove("*Valley Gap")

        while "*Valley Island" in item_group and (state.has("Water Net", player) or
                                            (hard and state.has("Sky Flyer", player)) or 
                                            (air_crawl) or 
                                            (expert and long_jump)):
            item_group.remove("*Valley Island")

        while "*Valley Boat" in item_group and (state.has("Water Net", player) or
                                            (hard and state.has("Sky Flyer", player)) or 
                                            (air_crawl)):
            item_group.remove("*Valley Boat")

        while "*Valley Button" in item_group and (state.has("Catapult", player) or
                                            (hard and state.has("Water Net", player) and (state.has("Sky Flyer", player) or state.has("Stun Club", player))) or 
                                            (air_crawl)):
            item_group.remove("*Valley Button")

        while "*Valley Stalag" in item_group and (state.has("R.C. Car", player) or
                                            (hard and state.has("Sky Flyer", player)) or 
                                            (air_crawl)):
            item_group.remove("*Valley Stalag")

        #Panic Pyramid
        while "*Pyramid Sarcophagus" in item_group and (state.has("Catapult", player) or
                                            (boost_fly and state.has("Sky Flyer", player) and hard)):
            item_group.remove("*Pyramid Sarcophagus")

        #Moon Base
        while "*Moon Fire" in item_group and (state.has("Water Cannon", player) or
                                            (damage_boost) or
                                            (air_crawl)):
            item_group.remove("*Moon Fire")

    return any(all(state.has(item, player) for item in item_group) for item_group in requirements)

def can_catch_all_monkeys(state, world, player):
    for level in [level for level in levels if level.name != "Final Showdown with Specter!"]:
        for monkey in level.monkeys:
            if not state.can_reach_location(monkey.get_location_name(), player):
                return False
    return True         

def create_regions(world: World) -> None:
    player = world.player
    multiworld = world.multiworld
    
    menu_region = Region("Menu", player, multiworld)
    multiworld.regions.append(menu_region)

    for level in levels:
        if not (world.options.goal.value == 0 and level.name == "Final Showdown with Specter!"):
            #Create regions
            for room_entrance in level.room_entrances:
                room_entrance_region = Region(f"{level.name} ({room_entrance.name})", player, multiworld)
                multiworld.regions.append(room_entrance_region)
        
            #Connect room entrances
            for room_entrance in level.room_entrances:
                room_entrance_region = multiworld.get_region(f"{level.name} ({room_entrance.name})", player)
                for connection in room_entrance.connection_requirements:
                    connection_region = multiworld.get_region(f"{level.name} ({connection})", player)
                    room_entrance_region.connect(connecting_region = connection_region, rule = lambda state, room_entrance = room_entrance, connection = connection: can_reach_connection(state, world, player, room_entrance.connection_requirements[connection]))

            level_locations = [] + level.monkeys
            if world.options.message_phone_locations.value:
                level_locations += level.phones

            for location in level_locations:
                location_region = Region(f"{level.name} ({location.name})", player, multiworld)
                location_region.locations += [AE2Location(player, location.get_location_name(), location.id, location_region)]
                multiworld.regions.append(location_region)

                for connection in location.connection_requirements:
                    connection_region_name = f"{level.name} ({connection})"
                    connection_region = multiworld.get_region(connection_region_name, player)
                    connection_region.connect(connecting_region = location_region, rule = lambda state, location = location, connection = connection: can_reach_connection(state, world, player, location.connection_requirements[connection]))

            starting_entrance = "Entry from Spawn" #Random starting room will go here
            if level.name == "Final Showdown with Specter!":
                menu_region.connect(connecting_region = multiworld.get_region(f"{level.name} ({starting_entrance})", player), rule = lambda state, level = level: state.has("World Key", player, world.world_key_requirements[level.name]) and can_catch_all_monkeys(state, world, player))
            else:
                menu_region.connect(connecting_region = multiworld.get_region(f"{level.name} ({starting_entrance})", player), rule = lambda state, level = level: state.has("World Key", player, world.world_key_requirements[level.name]))

    location_ids: Dict[str, int] = {}    
