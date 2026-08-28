from BaseClasses import Region
from worlds.AutoWorld import World
from .Locations import AE2Location, location_id_from_name, location_name_from_id
from .Items import AE2Item
from BaseClasses import ItemClassification, LocationProgressType
from .Levels import levels
from .Monkeys import monkey_from_name
import copy

def can_reach_connection(state, world, player, requirements):
    if state.has("Glitched Item", player):
        hard = True
        expert = True
        air_crawl = (state.has("Catapult", player) and state.has("Air Crawl", player)) or state.has("Progressive Catapult", player, 2)
        long_jump = state.has("Dash Hoop", player)
        boost_fly = state.has("Sky Flyer", player)
        damage_boost = True
        boost_jump = state.has("Monkey Net", player) and (state.has("Stun Club", player) or state.has("Monkey Radar", player) or state.has("Dash Hoop", player) or state.has(world.get_catapult_item_name(), player) or state.has("Sky Flyer", player) or state.has("R.C. Car", player) or state.has("Bananarang", player) or state.has("Water Cannon", player) or state.has("Electro Magnet", player) or state.has("Power Punch", player))
        hidden_monkey_logic = False
    else:
        hard = world.options.logic_difficulty.value > 0
        expert = world.options.logic_difficulty.value > 1
        air_crawl = ((state.has("Catapult", player) and state.has("Air Crawl", player)) or state.has("Progressive Catapult", player, 2)) and world.options.air_crawl_logic.value
        long_jump = state.has("Dash Hoop", player) and world.options.long_jump_logic.value
        boost_fly = state.has("Sky Flyer", player) and world.options.boost_fly_logic.value and (state.has("Monkey Net", player) or state.has("Electro Magnet", player) or state.has("Stun Club", player) or state.has("Power Punch", player))
        damage_boost = world.options.damage_boost_logic.value
        boost_jump = state.has("Monkey Net", player) and world.options.boost_jump_logic.value and (state.has("Stun Club", player) or state.has("Monkey Radar", player) or state.has("Dash Hoop", player) or state.has(world.get_catapult_item_name(), player) or state.has("Sky Flyer", player) or state.has("R.C. Car", player) or state.has("Bananarang", player) or state.has("Water Cannon", player) or state.has("Electro Magnet", player) or state.has("Power Punch", player))
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

        while "*Bull Fight" in item_group and (state.has(world.get_catapult_item_name(), player) or state.has("Stun Club", player) or state.has("Power Punch", player) or state.has("Dash Hoop", player) or (state.has("Sky Flyer", player) and expert)): #To attack the monkeys that get in bulls
            item_group.remove("*Bull Fight")

        while "*UFO" in item_group and (hard or state.has(world.get_catapult_item_name(), player) or state.has("Stun Club", player) or state.has("Power Punch", player)): #To attack the monkeys that get in UFOs
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

        while "*Non-Net" in item_group and (state.has("Stun Club", player) or state.has("Monkey Radar", player) or state.has("Dash Hoop", player) or state.has(world.get_catapult_item_name(), player) or state.has("Sky Flyer", player) or state.has("R.C. Car", player) or state.has("Bananarang", player) or state.has("Water Cannon", player) or state.has("Electro Magnet", player) or state.has("Power Punch", player)):
            item_group.remove("*Non-Net")

        #Lookout Valley
        while "*Valley Gap" in item_group and ((state.has("Sky Flyer", player) and state.has(world.get_catapult_item_name(), player)) or
                                            (expert and ((((state.has("Power Punch", player) or state.has("Sky Flyer", player)) and state.has("Water Net", player))) or state.has(world.get_catapult_item_name(), player))) or 
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

        while "*Valley Button" in item_group and (state.has(world.get_catapult_item_name(), player) or
                                            (hard and state.has("Water Net", player) and (state.has("Sky Flyer", player) or state.has("Stun Club", player))) or 
                                            (air_crawl)):
            item_group.remove("*Valley Button")

        while "*Valley Stalag" in item_group and (state.has("R.C. Car", player) or
                                            (hard and state.has("Sky Flyer", player)) or 
                                            (air_crawl)):
            item_group.remove("*Valley Stalag")

        #Panic Pyramid
        while "*Pyramid Sarcophagus" in item_group and (state.has(world.get_catapult_item_name(), player) or
                                            (boost_fly and state.has("Sky Flyer", player) and hard)):
            item_group.remove("*Pyramid Sarcophagus")

        #Moon Base
        while "*Moon Fire" in item_group and (state.has("Water Cannon", player) or
                                            (damage_boost) or
                                            (air_crawl)):
            item_group.remove("*Moon Fire")

        if "Catapult" in item_group and "Catapult" != world.get_catapult_item_name():
            item_group.remove("Catapult")
            item_group.append(world.get_catapult_item_name())

    return any(all(state.has(item, player) for item in item_group) for item_group in requirements)

def can_catch_all_monkeys(state, world, player):
    for level in [level for level in levels if level.name != "Final Showdown with Specter!"]:
        for monkey in level.monkeys:
            if not state.can_reach_location(monkey.get_location_name(), player):
                return False
    return True

def count_catchable_monkeys(state, world, player):
    catchable_count = 0
    for level in [level for level in levels if level.name != "Final Showdown with Specter!"]:
        catchable_count += len([monkey for monkey in level.monkeys if state.can_reach_location(monkey.get_location_name(), player)])
    return catchable_count

def can_obtain_gotcha_box_location(state, world, player, gotcha_box_location_number):
    unlocked_level_count = sum(world_key_requirement <= state.count("World Key", player) for world_key_requirement in world.world_key_requirements.values())
    gotcha_box_location_number_percentage = gotcha_box_location_number / world.options.gotcha_box_locations.value #How far into the Gotcha Box you have to progress in order to reach this location

    #Check if location is accessible
    can_access = False
    if world.options.gotcha_box_gating.value == 1: #Levels
        required_levels = int((len(levels) - 2) * gotcha_box_location_number_percentage)
        if unlocked_level_count < required_levels:
            return False
    elif world.options.gotcha_box_gating.value == 2: #Item
        required_restock_items = int((gotcha_box_location_number) / 10)
        if state.count("Gotcha Box Restock", player) < required_restock_items:
            return False

    #Chcek if location is logically expected
    if state.has("Glitched Item", player):
        return True
    else:
        level_curve = gotcha_box_location_number_percentage ** 0.5 #End game levels put more into logic than early game ones
        logical_level_unlock_expectation = int(level_curve * (len(levels) - 2)) #Specter fights don't add logical Gotcha Box locations
        return unlocked_level_count > logical_level_unlock_expectation and count_catchable_monkeys(state, world, player) > (300 * (gotcha_box_location_number_percentage - 0.05))
    return False

def create_regions(world: World) -> None:
    player = world.player
    multiworld = world.multiworld
    
    menu_region = Region("Menu", player, multiworld)
    multiworld.regions.append(menu_region)

    #Create Gotcha Box region
    gotcha_box_region = Region("Gotcha Box", player, multiworld)
    multiworld.regions.append(gotcha_box_region)
    menu_region.connect(connecting_region = gotcha_box_region)

    #Create Gotcha Box locations
    for x in range(0, world.options.gotcha_box_locations.value):
        gotcha_box_location = AE2Location(player, f"Gotcha Box: Item #{x + 1}", 2001 + x, gotcha_box_region)
        gotcha_box_location.access_rule = lambda state, x = x:can_obtain_gotcha_box_location(state, world, player, x)
        gotcha_box_region.locations += [gotcha_box_location]

    #Gotcha Box forced filler
    if world.options.gotcha_box_forced_filler_percentage.value > 0 and not hasattr(multiworld, "re_gen_passthrough"):
        number_of_forced_filler_locations = int(world.options.gotcha_box_locations.value * (world.options.gotcha_box_forced_filler_percentage.value / 100))
        possible_locations = [f"Gotcha Box: Item #{x + 1}" for x in range(0, world.options.gotcha_box_locations.value)]
        for x in range(0, number_of_forced_filler_locations):
            chosen_location = world.random.choices(possible_locations, weights = range(1, len(possible_locations) + 1))[0] #Weight the forced filler locations to be the later ones to reduce grinding
            multiworld.get_location(chosen_location, player).progress_type = LocationProgressType.EXCLUDED
            possible_locations.remove(chosen_location)

    #Create level regions and locations
    for level in levels:
        if not (world.options.goal.value == 0 and level.name == "Final Showdown with Specter!"):
            #Create regions
            for room_entrance in level.room_entrances:
                room_entrance_region = Region(f"{room_entrance.name} - {level.name}", player, multiworld)
                multiworld.regions.append(room_entrance_region)

            #Add locations
            level_locations = [] + level.monkeys
            if world.options.message_phone_locations.value:
                level_locations += level.phones

            for location in level_locations:
                location_region = Region(f"{location.name} - {level.name}", player, multiworld)
                location_region.locations += [AE2Location(player, location.get_location_name(), location.id, location_region)]
                multiworld.regions.append(location_region)

                for connection in location.connection_requirements:
                    connection_region_name = f"{connection} - {level.name}"
                    connection_region = multiworld.get_region(connection_region_name, player)
                    connection_region.connect(connecting_region = location_region, rule = lambda state, location = location, connection = connection: can_reach_connection(state, world, player, location.connection_requirements[connection]))

    #Build connections
    for level in levels:
        if not (world.options.goal.value == 0 and level.name == "Final Showdown with Specter!"):        
            #Connect room entrances
            for room_entrance in level.room_entrances:
                room_entrance_region = multiworld.get_region(f"{room_entrance.name} - {level.name}", player)

                for connection in room_entrance.connection_requirements:
                    region_name = f"{connection} - {level.name}"
                    if region_name in world.randomised_gates:
                        region_name = world.randomised_gates[region_name]
                    connection_region = multiworld.get_region(region_name, player)
                    room_entrance_region.connect(connecting_region = connection_region, rule = lambda state, room_entrance = room_entrance, connection = connection: can_reach_connection(state, world, player, room_entrance.connection_requirements[connection]))

            starting_entrance = "Entry from Spawn"
            if level.name in world.randomised_starting_rooms:
                starting_entrance = level.room_entrances[world.randomised_starting_rooms[level.name]].name
            if level.name == "Final Showdown with Specter!":
                menu_region.connect(connecting_region = multiworld.get_region(f"{starting_entrance} - {level.name}", player), rule = lambda state, level = level: state.has("World Key", player, world.world_key_requirements[level.name]) and can_catch_all_monkeys(state, world, player))
            else:
                menu_region.connect(connecting_region = multiworld.get_region(f"{starting_entrance} - {level.name}", player), rule = lambda state, level = level: state.has("World Key", player, world.world_key_requirements[level.name]))