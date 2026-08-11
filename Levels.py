from dataclasses import dataclass, field
from .Monkeys import monkeys, Monkey    
from .Phones import phones, Phone

@dataclass
class RoomEntrance:
    name: str
    connection_requirements: dict[str, list[str]] = field(default_factory = dict)
    source_room: int = -1
    target_room: int = -1
    room_name: str = ""
    spawn_name: str = ""
    position_to_trigger: list = field(default_factory = list)
    can_start: bool = False #Whether this is applicable as a potential starting room

@dataclass
class Level:
    name: str
    world_key_requirement: int = 0
    monkeys: list[Monkey] = field(default_factory = list)
    phones: list[Phone] = field(default_factory = list)

    room_entrances: list[RoomEntrance] = field(default_factory = lambda: [RoomEntrance(name = "Entry from Spawn")])
    target_address: dict = field(default_factory = dict)
    is_boss: bool = False
    keep_at_end: bool = False
    
levels = [
    #Liberty Island
    Level(name = "Liberty Island", target_address = {"PAL": 0xC636E0, "NTSC": 0xC63960}, room_entrances = [
        #Entry
        RoomEntrance(name = "Entry from Spawn", can_start = True, target_room = 0xA)
    ]),

    #Breezy Village
    Level(name = "Breezy Village", target_address = {"PAL": 0xC63710, "NTSC": 0xC63990}, room_entrances = [
        #Entry
        RoomEntrance(name = "Entry from Spawn", can_start = True, target_room = 0xB)
    ]),

    #Port Calm
    Level(name = "Port Calm", target_address = {"PAL": 0xC63740, "NTSC": 0xC639C0}, room_entrances = [
        #Entry
        RoomEntrance(name = "Entry from Spawn", can_start = True, target_room = 0xC, connection_requirements = {"Indoors from Entry": [["Water Net"]]}), 
        RoomEntrance(name = "Entry from Indoors", source_room = 0xD, target_room = 0xC, connection_requirements = {"Indoors from Entry": [["Water Net"]]}), 

        #Indoors
        RoomEntrance(name = "Indoors from Entry", source_room = 0xC, target_room = 0xD, connection_requirements = {"Entry from Indoors": [["Water Net"]]})
    ]),

    #Viva Apespania
    Level(name = "Viva Apespania", target_address = {"PAL": 0xC63770, "NTSC": 0xC639F0}, room_entrances = [
        #Entry
        RoomEntrance(name = "Entry from Spawn", can_start = True, target_room = 0xE, connection_requirements = {"Village from Entry": [[]]}), 
        RoomEntrance(name = "Entry from Village", source_room = 0xF, target_room = 0xE, room_name = "VEN_A", spawn_name = "spawn_a_1", connection_requirements = {"Village from Entry": [[]]}), 

        #Village
        RoomEntrance(name = "Village from Entry", can_start = True, source_room = 0xE, target_room = 0xF, room_name = "VEN_B", spawn_name = "spawn_b_1", position_to_trigger = [0x43C2079F, 0xC03FE3F4, 0xC03FE3F4], connection_requirements = {"Entry from Village": [[]], "Bullring from Village": [[]]}),
        RoomEntrance(name = "Village from Bullring", source_room = 0x10, target_room = 0xF, room_name = "VEN_B", spawn_name = "spawn_b_2", connection_requirements = {"Entry from Village": [[]], "Bullring from Village": [[]]}),

        #Bullring
        RoomEntrance(name = "Bullring from Village", can_start = True, source_room = 0xF, target_room = 0x10, room_name = "VEN_C", spawn_name = "spawn_c_1", connection_requirements = {"Village from Bullring": [[]]})
    ]),

    #Blue Monkey Battle!
    Level(name = "Blue Monkey Battle!", is_boss = True, room_entrances = [
        #Entry
        RoomEntrance(name = "Entry from Spawn", can_start = True, target_room = 0x59)
    ]),

    #Castle Frightmare
    Level(name = "Castle Frightmare", target_address = {"PAL": 0xC637D0, "NTSC": 0xC63A50}, room_entrances = [
        #Entry
        RoomEntrance(name = "Entry from Spawn", can_start = True, target_room = 0x14, connection_requirements = {"House from Entry": [[]]}),
        RoomEntrance(name = "Entry from House", source_room = 0x15, target_room = 0x14, connection_requirements = {"House from Entry": [[]]}),

        #House
        RoomEntrance(name = "House from Entry", can_start = True, target_room = 0x15, connection_requirements = {"Entry from House": [[]], "Dungeon from House": [[]]}),
        RoomEntrance(name = "House from Dungeon", source_room = 0x16, target_room = 0x15, connection_requirements = {"Entry from House": [[]], "Dungeon from House": [[]]}),

        #Dungeon
        RoomEntrance(name = "Dungeon from House", can_start = True, source_room = 0x15, target_room = 0x16, connection_requirements = {"House from Dungeon": [[]]})
    ]),

    #Vita-Z Factory
    Level(name = "Vita-Z Factory", target_address = {"PAL": 0xC63800, "NTSC": 0xC63A80}, room_entrances = [
        #Entry
        RoomEntrance(name = "Entry from Spawn", can_start = True, target_room = 0x17, connection_requirements = {"Tunnel from Entry": [["Sky Flyer"], ["*Gear"], ["*Air Crawl"]], "Arena from Entry": [["Power Punch"], ["*Air Crawl", "*Hard"]]}),
        RoomEntrance(name = "Entry from Tunnel", source_room = 0x18, target_room = 0x17, connection_requirements = {"Tunnel from Entry": [["Sky Flyer"], ["*Gear"], ["*Air Crawl"]], "Arena from Entry": [["Power Punch"], ["*Air Crawl", "*Hard"]]}),
        RoomEntrance(name = "Entry from Arena", source_room = 0x19, target_room = 0x17, connection_requirements = {"Tunnel from Entry": [["Sky Flyer"], ["*Gear"], ["*Air Crawl"]], "Arena from Entry": [[]]}),
        
        #Tunnel
        RoomEntrance(name = "Tunnel from Entry", can_start = True, source_room = 0x17, target_room = 0x18, connection_requirements = {"Entry from Tunnel": [[]], "Arena from Tunnel": [[]]}),
        RoomEntrance(name = "Tunnel from Arena", source_room = 0x19, target_room = 0x18, connection_requirements = {"Entry from Tunnel": [[]], "Arena from Tunnel": [[]]}),

        #Arena
        RoomEntrance(name = "Arena from Tunnel", can_start = True, source_room = 0x18, target_room = 0x19, connection_requirements = {"Tunnel from Arena": [[]], "Entry from Arena": [[]]}),
        RoomEntrance(name = "Arena from Entry", source_room = 0x17, target_room = 0x19, connection_requirements = {"Tunnel from Arena": [[]], "Entry from Arena": [[]]})
    ]),

    #Casino City
    Level(name = "Casino City", target_address = {"PAL": 0xC63830, "NTSC": 0xC63AB0}, room_entrances = [
        #Entry
        RoomEntrance(name = "Entry from Spawn", can_start = True, target_room = 0x1A, connection_requirements = {"Bar from Entry": [["*Attack"], ["Catapult"], ["*Hard"]], "Circus from Entry": [["Catapult"], ["Stun Club", "*Hard"], ["Power Punch", "*Hard"], ["Sky Flyer", "*Hard"], ["*Expert", "Pipotchi"]]}),
        RoomEntrance(name = "Entry from Circus", source_room = 0x1C, target_room = 0x1A, connection_requirements = {"Bar from Entry": [["*Attack"], ["Catapult"], ["*Hard"]], "Circus from Entry": [[]]}),
        RoomEntrance(name = "Entry from Bar", source_room = 0x1B, target_room = 0x1A, connection_requirements = {"Bar from Entry": [[]], "Circus from Entry": [["Catapult"], ["Stun Club", "*Hard"], ["Power Punch", "*Hard"], ["Sky Flyer", "*Hard"], ["*Expert", "Pipotchi"]]}),

        #Bar
        RoomEntrance(name = "Bar from Entry", can_start = True, source_room = 0x1A, target_room = 0x1B, connection_requirements = {"Entry from Bar": [[]]}),

        #Circus
        RoomEntrance(name = "Circus from Entry", can_start = True, source_room = 0x1A, target_room = 0x1C, connection_requirements = {"Entry from Circus": [[]]})
    ]),   
    
    #Ninja Hideout
    Level(name = "Ninja Hideout", target_address = {"PAL": 0xC63860, "NTSC": 0xC63AE0}, room_entrances = [
        #Entry
        RoomEntrance(name = "Entry from Spawn", can_start = True, target_room = 0x11, connection_requirements = {"Second Room from Entry": [["Water Net", "R.C. Car", "*Hard"], ["Water Net", "R.C. Car", "*Attack"], ["*Air Crawl"], ["R.C. Car", "*Boost Fly", "*Expert"]]}),
        RoomEntrance(name = "Entry from Second Room", source_room = 0x12, target_room = 0x11, connection_requirements = {"Second Room from Entry": [["Water Net", "R.C. Car", "*Hard"], ["Water Net", "R.C. Car", "*Attack"], ["*Air Crawl"], ["R.C. Car", "*Boost Fly", "*Expert"]]}),

        #Second Room
        RoomEntrance(name = "Second Room from Entry", source_room = 0x11, target_room = 0x12, connection_requirements = {"Entry from Second Room": [[]], "Third Room Start from Second Room": [["R.C. Car"], ["Sky Flyer", "*Hard"], ["*Air Crawl"], ["Dash Hoop", "*Hard", "*Long Jump"]]}), #value = 0x12
        RoomEntrance(name = "Second Room from Third Room Start", source_room = 0x13, target_room = 0x12, connection_requirements = {"Entry from Second Room": [[]], "Third Room Start from Second Room": [[]]}),
        RoomEntrance(name = "Second Room from Third Room End", source_room = 0x13, target_room = 0x12, connection_requirements = {"Entry from Second Room": [[]], "Third Room Start from Second Room": [["R.C. Car"], ["Sky Flyer", "*Hard"], ["*Air Crawl"], ["Dash Hoop", "*Hard", "*Long Jump"]]}),

        #Third Room
        RoomEntrance(name = "Third Room Start from Second Room", source_room = 0x12, target_room = 0x13, connection_requirements = {"Second Room from Third Room End": [[]], "Second Room from Third Room Start": [[]]}), #value = 0x13
        RoomEntrance(name = "Third Room End from Second Room", source_room = 0x12, target_room = 0x13, connection_requirements = {"Second Room from Third Room End": [[]], "Second Room from Third Room Start": [[]]}),
    ]),

    #Yellow Monkey Battle!
    Level(name = "Yellow Monkey Battle!", is_boss = True, room_entrances = [
        #Entry
        RoomEntrance(name = "Entry from Spawn", can_start = True, target_room = 0x5A)
    ]),

    #Snowball Mountain
    Level(name = "Snowball Mountain", target_address = {"PAL": 0xC638C0, "NTSC": 0xC63B40}, room_entrances = [
        #Entry
        RoomEntrance(name = "Entry from Spawn", can_start = True, target_room = 0x25, connection_requirements = {"Christmas Tree from Entry": [[]], "Ski Hill from Entry": [["*Air Crawl", "*Hard"], ["Sky Flyer", "*Hard"]]}),
        RoomEntrance(name = "Entry from Christmas Tree", source_room = 0x26, target_room = 0x25, connection_requirements = {"Christmas Tree from Entry": [[]], "Ski Hill from Entry": [["*Air Crawl", "*Hard"], ["Sky Flyer", "*Hard"]]}),
        RoomEntrance(name = "Entry from Ski Hill", source_room = 0x27, target_room = 0x25, connection_requirements = {"Christmas Tree from Entry": [[]], "Ski Hill from Entry": [[]]}),

        #Christmas Tree
        RoomEntrance(name = "Christmas Tree from Entry", can_start = True, source_room = 0x25, target_room = 0x26, connection_requirements = {"Entry from Christmas Tree": [[]], "Ski Hill from Christmas Tree": [["*Air Crawl"], ["Dash Hoop"], ["*Hard"]]}),
        RoomEntrance(name = "Christmas Tree from Ski Hill", source_room = 0x27, target_room = 0x26, connection_requirements = {"Entry from Christmas Tree": [[]], "Ski Hill from Christmas Tree": [[]]}),

        #Ski Hill
        RoomEntrance(name = "Ski Hill from Entry", can_start = True, source_room = 0x25, target_room = 0x27, connection_requirements = {"Entry from Ski Hill": [[]], "Christmas Tree from Ski Hill": [[]]}),
        RoomEntrance(name = "Ski Hill from Christmas Tree", source_room = 0x26, target_room = 0x27, connection_requirements = {"Entry from Ski Hill": [[]], "Christmas Tree from Ski Hill": [[]]})
    ]),

    #Lookout Valley
    Level(name = "Lookout Valley", target_address = {"PAL": 0xC638F0, "NTSC": 0xC63B70}, room_entrances = [
        #Entry
        RoomEntrance(name = "Entry from Spawn", can_start = True, target_room = 0x22, connection_requirements = {"Cave Start from Entry": [["*Valley Gap", "*Valley Island", "*Valley Boat"]], "Cave End from Entry": [["*Boost Fly", "*Hard"], ["*Air Crawl", "*Hard"]], "Jungle Start from Entry": [["*Valley Gap", "*Valley Island"]], "Jungle End from Entry": [["*Air Crawl", "*Hard"]]}),
        RoomEntrance(name = "Entry from Cave End", source_room = 0x24, target_room = 0x22, connection_requirements = {"Cave Start from Entry": [["*Valley Boat"]], "Cave End from Entry": [[]], "Jungle Start from Entry": [["*Valley Island"]], "Jungle End from Entry": [["*Air Crawl", "*Hard"]]}),
        RoomEntrance(name = "Entry from Cave Start", source_room = 0x24, target_room = 0x22, connection_requirements = {"Cave Start from Entry": [[]], "Cave End from Entry": [["*Boost Fly", "*Hard"], ["*Air Crawl", "*Hard"]], "Jungle Start from Entry": [["*Valley Island"]], "Jungle End from Entry": [["*Air Crawl", "*Hard"]]}),
        RoomEntrance(name = "Entry from Jungle Start", source_room = 0x23, target_room = 0x22, connection_requirements = {"Cave Start from Entry": [["*Valley Island", "*Valley Boat"]], "Cave End from Entry": [["*Boost Fly", "*Hard"], ["*Air Crawl", "*Hard"]], "Jungle Start from Entry": [[]], "Jungle End from Entry": [["*Air Crawl", "*Hard"]]}),
        RoomEntrance(name = "Entry from Jungle End", source_room = 0x23, target_room = 0x22, connection_requirements = {"Cave Start from Entry": [["*Valley Island", "*Valley Boat"]], "Cave End from Entry": [["*Boost Fly", "*Hard"], ["*Air Crawl", "*Hard"]], "Jungle Start from Entry": [[]], "Jungle End from Entry": [[]]}),

        #Jungle
        RoomEntrance(name = "Jungle Start from Entry", can_start = True, source_room = 0x22, target_room = 0x23, connection_requirements = {"Entry from Jungle Start": [[]], "Entry from Jungle End": [[]]}),
        RoomEntrance(name = "Jungle End from Entry", source_room = 0x22, target_room = 0x23,connection_requirements = {"Entry from Jungle Start": [[]], "Entry from Jungle End": [[]]}),

        #Cave
        RoomEntrance(name = "Cave Start from Entry", can_start = True, source_room = 0x22, target_room = 0x24, connection_requirements = {"Entry from Cave Start": [[]], "Entry from Cave End": [["*Valley Button", "*Valley Stalag", "Water Net"], ["*Valley Button", "*Valley Stalag", "Sky Flyer", "*Hard"], ["*Valley Button", "*Valley Stalag", "*Expert"]]}),
        RoomEntrance(name = "Cave End from Entry", source_room = 0x22, target_room = 0x24, connection_requirements = {"Entry from Cave Start": [["*Air Crawl"], ["Sky Flyer"], ["Water Net"]], "Entry from Cave End": [[]]})
    ]),

    #The Blue Baboon
    Level(name = "The Blue Baboon", target_address = {"PAL": 0xC63920, "NTSC": 0xC63BA0}, room_entrances = [
        #Entry
        RoomEntrance(name = "Entry from Spawn", can_start = True, target_room = 0x1D, connection_requirements = {"Ship from Entry": [[]], "Bananarang Room from Entry": [["Water Net"], ["*Air Crawl"]], "Changing Hut from Entry": [[]]}),
        RoomEntrance(name = "Entry from Ship", source_room = 0x21, target_room = 0x1D, connection_requirements = {"Ship from Entry": [[]], "Bananarang Room from Entry": [["Water Net"], ["*Air Crawl"]], "Changing Hut from Entry": [[]]}),
        RoomEntrance(name = "Entry from Bananarang Room", source_room = 0x1F, target_room = 0x1D, connection_requirements = {"Ship from Entry": [["Water Net"], ["*Air Crawl"]], "Bananarang Room from Entry": [["Water Net"], ["*Air Crawl"]], "Changing Hut from Entry": [["Water Net"], ["*Air Crawl"]]}),
        RoomEntrance(name = "Entry from Changing Hut", source_room = 0x1E, target_room = 0x1D, connection_requirements = {"Ship from Entry": [[]], "Bananarang Room from Entry": [["Water Net"], ["*Air Crawl"]], "Changing Hut from Entry": [[]]}),

        #Hut
        RoomEntrance(name = "Changing Hut from Entry", can_start = True, source_room = 0x1D, target_room = 0x1E, connection_requirements = {"Entry from Changing Hut": [[]]}),

        #Ship
        RoomEntrance(name = "Ship from Entry", can_start = True, source_room = 0x1D, target_room = 0x21, connection_requirements = {"Entry from Ship": [[]]}),

        #Bananarang Room
        RoomEntrance(name = "Bananarang Room from Entry", can_start = True, source_room = 0x1D, target_room = 0x1F, connection_requirements = {"Entry from Bananarang Room": [[]]})
    ]),

    #Pink Monkey Battle!
    Level(name = "Pink Monkey Battle!", is_boss = True, room_entrances = [
        #Entry
        RoomEntrance(name = "Entry from Spawn", can_start = True, target_room = 0x5B)
    ]),

    #Enter the Monkey
    Level(name = "Enter the Monkey", target_address = {"PAL": 0xC63980, "NTSC": 0xC63C00}, room_entrances = [
        #Entry
        RoomEntrance(name = "Entry from Spawn", can_start = True, target_room = 0x28, connection_requirements = {"Inside Start from Entry": [[]], "Wall Start from Entry": [[]]}), 
        RoomEntrance(name = "Entry from Inside Start", source_room = 0x29, target_room = 0x28, connection_requirements = {"Inside Start from Entry": [[]], "Wall Start from Entry": [[]]}), 
        RoomEntrance(name = "Entry from Inside End", source_room = 0x29, target_room = 0x28, connection_requirements = {"Inside Start from Entry": [[]], "Wall Start from Entry": [[]]}), 
        RoomEntrance(name = "Entry from Wall Start", source_room = 0x2A, target_room = 0x28, connection_requirements = {"Inside Start from Entry": [[]], "Wall Start from Entry": [[]]}), 
        RoomEntrance(name = "Entry from Wall End", source_room = 0x2A, target_room = 0x28, connection_requirements = {"Inside Start from Entry": [[]], "Wall Start from Entry": [[]]}), 

        #Inside
        RoomEntrance(name = "Inside Start from Entry", can_start = True, source_room = 0x28, target_room = 0x29, connection_requirements = {"Entry from Inside Start": [[]], "Entry from Inside End": [["*Gear"]]}), 
        RoomEntrance(name = "Inside End from Entry", source_room = 0x28, target_room = 0x29, connection_requirements = {}), 

        #Wall
        RoomEntrance(name = "Wall Start from Entry", can_start = True, source_room = 0x28, target_room = 0x2A, connection_requirements = {"Entry from Wall Start": [[]], "Entry from Wall End": [["R.C. Car"], ["*Air Crawl"], ["*Boost Fly", "*Hard"]]}), 
        RoomEntrance(name = "Wall End from Entry", source_room = 0x28, target_room = 0x2A, connection_requirements = {"Entry from Wall Start": [[]], "Entry from Wall End": [[]]})
    ]),

    #Simian Citadel
    Level(name = "Simian Citadel", target_address = {"PAL": 0xC639B0, "NTSC": 0xC63C30}, room_entrances = [
        #Entry
        RoomEntrance(name = "Entry from Spawn", can_start = True, target_room = 0x2C, connection_requirements = {"Bullring from Entry": [["*Gear", "Water Net"]], "Fountain from Entry": [["*Air Crawl", "*Hard"], ["*Boost Fly", "*Hard"]]}), 
        RoomEntrance(name = "Entry from Bullring", source_room = 0x2D, target_room=0x2C, connection_requirements = {"Bullring from Entry": [[]], "Fountain from Entry": [["*Gear", "Water Net", "*Boost Fly", "*Hard"], ["*Gear", "Water Net", "*Air Crawl", "*Hard"]]}), 
        RoomEntrance(name = "Entry from Fountain", source_room = 0x30, target_room=0x2C, connection_requirements = {"Bullring from Entry": [["*Gear", "Water Net"]], "Fountain from Entry": [[]]}), 

        #Bullring
        RoomEntrance(name = "Bullring from Entry", can_start = True, source_room = 0x2C, target_room = 0x2D, connection_requirements = {"Entry from Bullring": [[]], "Whale from Bullring": [["Dash Hoop", "*Bull Fight"], ["*Bull Fight", "*Hard"], ["*Air Crawl", "*Hard"]]}), 
        RoomEntrance(name = "Bullring from Whale", source_room = 0x2E, target_room = 0x2D, connection_requirements = {"Entry from Bullring": [["Dash Hoop", "*Bull Fight"], ["*Bull Fight", "*Hard"], ["*Air Crawl", "*Hard"]], "Whale from Bullring": [[]]}), 

        #Whale
        RoomEntrance(name = "Whale from Bullring", can_start = True, source_room = 0x2D, target_room = 0x2E, connection_requirements = {"Submarine from Whale": [["Sky Flyer", "Water Net", "*Attack"], ["Sky Flyer", "*Hard"], ["*Air Crawl"]], "Bullring from Whale": [[]]}), 
        RoomEntrance(name = "Whale from Submarine", source_room = 0x2F, target_room = 0x2E, connection_requirements = {}), 

        #Submarine
        RoomEntrance(name = "Submarine from Whale", can_start = True, source_room = 0x2E, target_room = 0x2F, connection_requirements = {"Fountain from Submarine": [[]], "Whale from Submarine": [[]]}), 
        RoomEntrance(name = "Submarine from Fountain", source_room = 0x30, target_room = 0x2F, connection_requirements = {"Fountain from Submarine": [[]], "Whale from Submarine": [[]]}), 

        #Fountain
        RoomEntrance(name = "Fountain from Submarine", can_start = True, source_room = 0x2F, target_room = 0x30, connection_requirements = {"Submarine from Fountain": [[]], "Entry from Fountain": [[]]}), 
        RoomEntrance(name = "Fountain from Entry", source_room = 0x2C, target_room = 0x30, connection_requirements = {"Submarine from Fountain": [[]], "Entry from Fountain": [[]]})
    ]),

    #Panic Pyramid
    Level(name = "Panic Pyramid", target_address = {"PAL": 0xC639E0, "NTSC": 0xC63C60}, room_entrances = [
        #Entry
        RoomEntrance(name = "Entry from Spawn", can_start = True, target_room = 0x31, connection_requirements = {"Booby Traps from Entry": [[]], "Moving Platforms #2 from Entry": [["*Air Crawl"], ["*Boost Fly", "*Expert"]], "Boulders Start from Entry": [["R.C. Car"], ["Dash Hoop"]], "Boulders End from Entry": [["*Air Crawl"]]}), 
        RoomEntrance(name = "Entry from Booby Traps", source_room = 0x32, target_room = 0x31, connection_requirements = {"Booby Traps from Entry": [[]], "Moving Platforms #2 from Entry": [["*Air Crawl"], ["*Boost Fly", "*Expert"]], "Boulders Start from Entry": [["R.C. Car"], ["Dash Hoop"]], "Boulders End from Entry": [["*Air Crawl"]]}),
        RoomEntrance(name = "Entry from Moving Platforms #2", source_room = 0x35, target_room = 0x31, connection_requirements = {"Booby Traps from Entry": [[]], "Moving Platforms #2 from Entry": [["*Air Crawl"], ["*Boost Fly", "*Expert"]], "Boulders Start from Entry": [["R.C. Car"], ["Dash Hoop"]], "Boulders End from Entry": [["*Air Crawl"]]}), 
        RoomEntrance(name = "Entry from Boulders Start", source_room = 0x34, target_room = 0x31, connection_requirements = {"Booby Traps from Entry": [[]], "Moving Platforms #2 from Entry": [["*Air Crawl"], ["*Boost Fly", "*Expert"]], "Boulders Start from Entry": [["R.C. Car"], ["Dash Hoop"]], "Boulders End from Entry": [["*Air Crawl"]]}), 
        RoomEntrance(name = "Entry from Boulders End", source_room = 0x34, target_room = 0x31, connection_requirements = {"Booby Traps from Entry": [[]], "Moving Platforms #2 from Entry": [["*Air Crawl"], ["*Boost Fly", "*Expert"]], "Boulders Start from Entry": [["R.C. Car"], ["Dash Hoop"]], "Boulders End from Entry": [["*Air Crawl"]]}), 

        #Booby Traps
        RoomEntrance(name = "Booby Traps from Entry", can_start = True, source_room = 0x31, target_room = 0x32, connection_requirements = {"Moving Platforms #1 from Booby Traps": [["Water Net", "R.C. Car", "*Gear", "*Pyramid Sarcophagus"], ["Water Net", "*Air Crawl", "*Gear", "*Pyramid Sarcophagus"]], "Entry from Booby Traps": [[]]}), 
        RoomEntrance(name = "Booby Traps from Moving Platforms #1", source_room = 0x33, target_room = 0x32, connection_requirements = {"Moving Platforms #1 from Booby Traps": [[]], "Entry from Booby Traps": [["*Gear", "*Air Crawl"]]}), 

        #Moving Platforms #1
        RoomEntrance(name = "Moving Platforms #1 from Booby Traps", can_start = True, source_room = 0x32, target_room = 0x33, connection_requirements = {"Booby Traps from Moving Platforms #1": [[]], "Moving Platforms #2 from Moving Platforms #1": [["R.C. Car"], ["Water Cannon"], ["*Air Crawl"]]}), 
        RoomEntrance(name = "Moving Platforms #1 from Moving Platforms #2", source_room = 0x35, target_room = 0x33, connection_requirements = {"Booby Traps from Moving Platforms #1": [["R.C. Car"], ["Water Cannon"], ["*Air Crawl"]], "Moving Platforms #2 from Moving Platforms #1": [[]]}), 

        #Moving Platforms #2
        RoomEntrance(name = "Moving Platforms #2 from Moving Platforms #1", can_start = True, source_room = 0x33, target_room = 0x35, connection_requirements = {"Entry from Moving Platforms #2": [["Dash Hoop"], ["*Air Crawl"]], "Moving Platforms #1 from Moving Platforms #2": [[]]}), 
        RoomEntrance(name = "Moving Platforms #2 from Entry", source_room = 0x31, target_room = 0x35, connection_requirements = {"Entry from Moving Platforms #2": [[]], "Moving Platforms #1 from Moving Platforms #2": [["Dash Hoop"], ["*Air Crawl"]]}), 

        #Boulders
        RoomEntrance(name = "Boulders Start from Entry", can_start = True, source_room = 0x31, target_room = 0x34, connection_requirements = {"Entry from Boulders Start": [[]], "Entry from Boulders End": [["R.C. Car"], ["*Air Crawl"]]}),
        RoomEntrance(name = "Boulders End from Entry", source_room = 0x31, target_room = 0x34, connection_requirements = {"Entry from Boulders Start": [[]], "Entry from Boulders End": [[]]})
    ]),

    #White Monkey Battle!
    Level(name = "White Monkey Battle!", is_boss = True, room_entrances = [
        #Entry
        RoomEntrance(name = "Entry from Spawn", can_start = True, target_room = 0x5D)
    ]),

    #Pirate Isle
    Level(name = "Pirate Isle", target_address = {"PAL": 0xC63A40, "NTSC": 0xC63CC0}, room_entrances = [
        #Entry
        RoomEntrance(name = "Entry from Spawn", can_start = True, target_room = 0x36, connection_requirements = {"Cave Entrance from Entry": [["Water Cannon"], ["*Damage Boost"]], "Mine from Entry": [["*Air Crawl"]]}), 
        RoomEntrance(name = "Entry from Cave Entrance", source_room = 0x37, target_room = 0x36, connection_requirements = {"Cave Entrance from Entry": [["Water Cannon"], ["*Damage Boost"]], "Mine from Entry": [["*Air Crawl"]]}), 
        RoomEntrance(name = "Entry from Mine", source_room = 0x3A, target_room = 0x36, connection_requirements = {"Cave Entrance from Entry": [["Water Cannon"], ["*Damage Boost"]], "Mine from Entry": [[]]}),

        #Cave Entrance
        RoomEntrance(name = "Cave Entrance from Entry", can_start = True, source_room = 0x36, target_room = 0x37, connection_requirements = {"Entry from Cave Entrance": [[]], "Boat from Cave Entrance": [["*Air Crawl"], ["Stun Club", "*Expert"], ["Water Cannon"], ["Sky Flyer", "*Boost Fly", "*Hard"]]}), 
        RoomEntrance(name = "Cave Entrance from Boat", source_room = 0x38, target_room = 0x37, connection_requirements = {"Entry from Cave Entrance": [[]], "Boat from Cave Entrance": [[]]}),

        #Boat
        RoomEntrance(name = "Boat from Cave Entrance", can_start = True, source_room = 0x37, target_room = 0x38, connection_requirements = {"Cell from Boat": [["Water Cannon", "Sky Flyer"], ["Sky Flyer", "*Damage Boost"], ["*Air Crawl"], ["Sky Flyer", "*Hard"]], "Treasure from Boat": [[]], "Mine from Boat": [["Water Cannon"], ["*Damage Boost", "*Expert"]], "Cave Entrance from Boat": [[]]}), 
        RoomEntrance(name = "Boat from Cell", source_room = 0x39, target_room = 0x38, connection_requirements = {"Cell from Boat": [["Water Cannon", "Sky Flyer"], ["Sky Flyer", "*Damage Boost"], ["*Air Crawl"], ["Sky Flyer", "*Hard"]], "Treasure from Boat": [[]], "Mine from Boat": [["Water Cannon"], ["*Damage Boost", "*Expert"]], "Cave Entrance from Boat": [[]]}), 
        RoomEntrance(name = "Boat from Treasure", source_room = 0x39, target_room = 0x38, connection_requirements = {"Cell from Boat": [["Water Cannon", "Sky Flyer"], ["Sky Flyer", "*Damage Boost"], ["*Air Crawl"], ["Sky Flyer", "*Hard"]], "Treasure from Boat": [[]], "Mine from Boat": [["Water Cannon"], ["*Damage Boost", "*Expert"]], "Cave Entrance from Boat": [[]]}), 
        RoomEntrance(name = "Boat from Mine", source_room = 0x3A, target_room = 0x38, connection_requirements = {"Cell from Boat": [["Water Cannon", "Sky Flyer"], ["Water Cannon", "Sky Flyer", "*Damage Boost"], ["*Air Crawl"]], "Treasure from Boat": [["Water Cannon"], ["*Air Crawl"]], "Mine from Boat": [["Water Cannon"], ["*Air Crawl"]], "Cave Entrance from Boat": [["Water Cannon"], ["*Air Crawl"]]}), 

        #Cell
        RoomEntrance(name = "Cell from Boat", source_room = 0x38, target_room = 0x39, connection_requirements = {"Boat from Cell": [[]]}), 

        #Treasure
        RoomEntrance(name = "Treasure from Boat", can_start = True, source_room = 0x38, target_room = 0x39, connection_requirements = {"Boat from Treasure": [[]]}), 

        #Mine
        RoomEntrance(name = "Mine from Boat", can_start = True, source_room = 0x38, target_room = 0x3A, connection_requirements = {"Boat from Mine": [[]], "Entry from Mine": [[]]}), 
        RoomEntrance(name = "Mine from Entry", source_room = 0x36, target_room = 0x3A, connection_requirements = {"Boat from Mine": [[]], "Entry from Mine": [[]]})
    ]),

    #Land of the Apes
    Level(name = "Land of the Apes", target_address = {"PAL": 0xC63A70, "NTSC": 0xC63CF0}, room_entrances = [
        #Entry
        RoomEntrance(name = "Entry from Spawn", can_start = True, target_room = 0x3B, connection_requirements = {"Icicles from Entry": [[]]}),
        RoomEntrance(name = "Entry from Icicles", source_room = 0x3C, target_room = 0x3B, connection_requirements = {"Icicles from Entry": [[]]}),

        #Icicles
        RoomEntrance(name = "Icicles from Entry", can_start = True, source_room = 0x3B, target_room = 0x3C, connection_requirements = {"Entry from Icicles": [[]], "Spa from Icicles": [[]], "Ski Hill from Icicles": [[]]}),
        RoomEntrance(name = "Icicles from Spa", source_room = 0x3D, target_room = 0x3C, connection_requirements = {"Entry from Icicles": [[]], "Spa from Icicles": [[]], "Ski Hill from Icicles": [[]]}),
        RoomEntrance(name = "Icicles from Ski Hill", source_room = 0x3E, target_room = 0x3C, connection_requirements = {"Entry from Icicles": [[]], "Spa from Icicles": [[]], "Ski Hill from Icicles": [[]]}),

        #Spa
        RoomEntrance(name = "Spa from Icicles", can_start = True, source_room = 0x3C, target_room = 0x3D, connection_requirements = {"Icicles from Spa": [[]]}),

        #Ski Hill
        RoomEntrance(name = "Ski Hill from Icicles", can_start = True, source_room = 0x3C, target_room = 0x3E, connection_requirements = {"Icicles from Ski Hill": [[]]})
    ]),

    #The Lost World
    Level(name = "The Lost World", target_address = {"PAL": 0xC63AA0, "NTSC": 0xC63D20}, room_entrances = [
        #Entry
        RoomEntrance(name = "Entry from Spawn", can_start = True, target_room = 0x3F, connection_requirements = {"Trees from Entry": [["Water Net"], ["*Air Crawl"]], "Pterodactyls from Entry": [[]]}),
        RoomEntrance(name = "Entry from Trees", source_room = 0x41, target_room = 0x3F, connection_requirements = {"Trees from Entry": [[]], "Pterodactyls from Entry": [["Water Net"], ["*Air Crawl"], ["Sky Flyer", "*Hard"]]}),
        RoomEntrance(name = "Entry from Pterodactyls", source_room = 0x40, target_room = 0x3F, connection_requirements = {"Trees from Entry": [["Water Net"], ["*Air Crawl"]], "Pterodactyls from Entry": [[]]}),

        #Trees
        RoomEntrance(name = "Trees from Entry", can_start = True, source_room = 0x3F, target_room = 0x41, connection_requirements = {"Entry from Trees": [[]], "T-Rex from Trees": [["Water Cannon", "Water Net"], ["Water Cannon", "*Hard"], ["*Air Crawl"]]}),
        RoomEntrance(name = "Trees from T-Rex", source_room = 0x42, target_room = 0x41, connection_requirements = {"Entry from Trees": [["Water Net"], ["*Hard"]], "T-Rex from Trees": [[]]}),

        #T-Rex
        RoomEntrance(name = "T-Rex from Trees", source_room = 0x41, target_room = 0x42, connection_requirements = {"Trees from T-Rex": [[]], "Pterodactyls from T-Rex": [["Water Net"], ["*Hard"]]}),
        RoomEntrance(name = "T-Rex from Pterodactyls", can_start = True, source_room = 0x40, target_room = 0x42, connection_requirements = {"Trees from T-Rex": [["Water Net"], ["*Hard"]], "Pterodactyls from T-Rex": [[]]}),

        #Pterodactyls
        RoomEntrance(name = "Pterodactyls from T-Rex", source_room = 0x42, target_room = 0x40, connection_requirements = {"T-Rex from Pterodactyls": [[]], "Entry from Pterodactyls": [[]]}),
        RoomEntrance(name = "Pterodactyls from Entry", can_start = True, source_room = 0x3F, target_room = 0x40, connection_requirements = {"T-Rex from Pterodactyls": [[]], "Entry from Pterodactyls": [[]]})
    ]),

    #Red Monkey Battle!
    Level(name = "Red Monkey Battle!", is_boss = True, room_entrances = [
        #Entry
        RoomEntrance(name = "Entry from Spawn", can_start = True, target_room = 0x5E)
    ]),

    #Skyscraper City
    Level(name = "Skyscraper City", target_address = {"PAL": 0xC63B00, "NTSC": 0xC63D80}, room_entrances = [
        #Entry
        RoomEntrance(name = "Entry from Spawn", can_start = True, target_room = 0x43, connection_requirements = {"Lobby from Entry": [["Electro Magnet"], ["*Air Crawl"], ["Sky Flyer", "*Hard"]]}),
        RoomEntrance(name = "Entry from Lobby", source_room = 0x44, target_room = 0x43, connection_requirements = {"Lobby from Entry": [[]]}),

        #Lobby
        RoomEntrance(name = "Lobby from Entry", can_start = True, source_room = 0x43, target_room = 0x44, connection_requirements = {"Sewer Start from Lobby": [[]], "Entry from Lobby": [[]]}),
        RoomEntrance(name = "Lobby from Sewer Start", source_room = 0x45, target_room = 0x44, connection_requirements = {"Sewer Start from Lobby": [[]], "Entry from Lobby": [[]]}),
        RoomEntrance(name = "Lobby from Sewer End", source_room = 0x45, target_room = 0x44, connection_requirements = {"Sewer End from Lobby": [[]], "Entry from Lobby": [[]], "Sewer Start from Lobby": [[]], "Tank from Lobby": [[]]}),
        RoomEntrance(name = "Lobby from Tank", source_room = 0x46, target_room = 0x44, connection_requirements = {"Sewer Start from Lobby": [[]], "Entry from Lobby": [[]], "Tank from Lobby": [[]], "Sewer End from Lobby": [[]]}),
        RoomEntrance(name = "Lobby from Final Room", source_room = 0x47, target_room = 0x44, connection_requirements = {"Sewer Start from Lobby": [[]], "Entry from Lobby": [[]]}),

        #Sewer
        RoomEntrance(name = "Sewer Start from Lobby", can_start = True, source_room = 0x44, target_room = 0x45, connection_requirements = {"Lobby from Sewer Start": [[]], "Lobby from Sewer End": [["R.C. Car", "Electro Magnet"]]}),
        RoomEntrance(name = "Sewer End from Lobby", source_room = 0x44, target_room = 0x45, connection_requirements = {"Lobby from Sewer End": [[]]}),

        #Tank Room
        RoomEntrance(name = "Tank from Lobby", can_start = True, source_room = 0x44, target_room = 0x46, connection_requirements = {"Lobby from Tank": [[]], "Final Room from Tank": [[]]}),
        RoomEntrance(name = "Tank from Final Room", source_room = 0x47, target_room = 0x46, connection_requirements = {"Lobby from Tank": [[]], "Final Room from Tank": [[]]}),

        #Final Room
        RoomEntrance(name = "Final Room from Tank", can_start = True, source_room = 0x46, target_room = 0x47, connection_requirements = {"Tank from Final Room": [[]], "Lobby from Final Room": [["Electro Magnet", "Catapult", "R.C. Car"], ["*Air Crawl"], ["Electro Magnet", "Catapult", "Sky Flyer", "*Boost Jump", "*Expert"]]}),
        RoomEntrance(name = "Final Room from Lobby", source_room = 0x44, target_room = 0x47, connection_requirements = {}) #THIS HAS NO LOGIC RIGHT NOW
    ]),

    #Code C.H.I.M.P.
    Level(name = "Code C.H.I.M.P.", target_address = {"PAL": 0xC63B30, "NTSC": 0xC63DB0}, room_entrances = [
        #Entry
        RoomEntrance(name = "Entry from Spawn", can_start = True, target_room = 0x48, connection_requirements = {"Base Entrance from Entry": [["*Air Crawl"], ["*Gear"]], "Moving Platforms from Entry": [["*Air Crawl"]]}),
        RoomEntrance(name = "Entry from Base Entrance", source_room = 0x49, target_room = 0x48, connection_requirements = {"Base Entrance from Entry": [[]], "Moving Platforms from Entry": [["*Air Crawl"]]}),
        RoomEntrance(name = "Entry from Moving Platforms", source_room = 0x4C, target_room = 0x48, connection_requirements = {"Base Entrance from Entry": [["*Air Crawl"], ["*Gear"]], "Moving Platforms from Entry": [[]]}),

        #Base Entrance
        RoomEntrance(name = "Base Entrance from Entry", can_start = True, source_room = 0x48, target_room = 0x49, connection_requirements = {"Entry from Base Entrance": [[]], "Tank from Base Entrance": [["*Air Crawl"], ["Electro Magnet", "Water Cannon"], ["Electro Magnet", "*Damage Boost"], ["*Boost Fly", "*Expert", "*Damage Boost"], ["*Boost Fly", "*Expert", "Water Cannon"]]}),
        RoomEntrance(name = "Base Entrance from Tank", source_room = 0x4A, target_room = 0x49, connection_requirements = {"Entry from Base Entrance": [[]], "Tank from Base Entrance": [[]]}),

        #Tank
        RoomEntrance(name = "Tank from Base Entrance", can_start = True, source_room = 0x49, target_room = 0x4A, connection_requirements = {"Treadmills from Tank": [[]], "Base Entrance from Tank": [[]]}),
        RoomEntrance(name = "Tank from Treadmills", source_room = 0x4B, target_room = 0x4A, connection_requirements = {"Treadmills from Tank": [[]], "Base Entrance from Tank": [[]]}),

        #Treadmills
        RoomEntrance(name = "Treadmills from Tank", can_start = True, source_room = 0x4A, target_room = 0x4B, connection_requirements = {"Moving Platforms from Treadmills": [["Electro Magnet"], ["Sky Flyer", "*Boost Fly", "*Expert"], ["*Air Crawl", "*Hard"]], "Tank from Treadmills": [[]]}),
        RoomEntrance(name = "Treadmills from Moving Platforms", source_room = 0x4C, target_room = 0x4B, connection_requirements = {"Moving Platforms from Treadmills": [[]]}),

        #Moving Platforms
        RoomEntrance(name = "Moving Platforms from Treadmills", can_start = True, source_room = 0x4B, target_room = 0x4C, connection_requirements = {"Treadmills from Moving Platforms": [[]], "Magnetic Panels Start from Moving Platforms": [[]]}),
        RoomEntrance(name = "Moving Platforms from Magnetic Panels Start", source_room = 0x4D, target_room = 0x4C, connection_requirements = {"Treadmills from Moving Platforms": [[]], "Magnetic Panels Start from Moving Platforms": [[]]}),
        RoomEntrance(name = "Moving Platforms from Magnetic Panels End", source_room = 0x4D, target_room = 0x4C, connection_requirements = {"Treadmills from Moving Platforms": [["*Attack"], ["*Hard"]], "Magnetic Panels Start from Moving Platforms": [["*Attack"], ["*Hard"]], "Magnetic Panels End from Moving Platforms": [[]], "Entry from Moving Platforms": [["*Attack"], ["*Hard"]]}),
        RoomEntrance(name = "Moving Platforms from Entry", source_room = 0x48, target_room = 0x4C, connection_requirements = {"Treadmills from Moving Platforms": [[]], "Magnetic Panels Start from Moving Platforms": [[]], "Entry from Moving Platforms": [[]]}),

        #Magnetic Panels
        RoomEntrance(name = "Magnetic Panels Start from Moving Platforms", can_start = True, source_room = 0x4C, target_room = 0x4D, connection_requirements = {"Moving Platforms from Magnetic Panels End": [["Electro Magnet", "Sky Flyer"], ["Electro Magnet", "*Hard", "Pipotchi"], ["*Boost Fly", "*Hard", "Power Punch"]], "Moving Platforms from Magnetic Panels Start": [[]]}),
        RoomEntrance(name = "Magnetic Panels End from Moving Platforms", source_room = 0x4C, target_room = 0x4D, connection_requirements = {"Moving Platforms from Magnetic Panels End": [[]], "Moving Platforms from Magnetic Panels Start": [["Electro Magnet", "Sky Flyer"], ["Electro Magnet", "*Hard", "Pipotchi"], ["*Boost Fly", "*Hard"]]})
    ]),

    #Giant Yellow Monkey Battle!
    Level(name = "Giant Yellow Monkey Battle!", target_address = {"PAL": 0xC63B60, "NTSC": 0xC63DE0}, is_boss = True, room_entrances = [
        #Entry
        RoomEntrance(name = "Entry from Spawn", can_start = True, target_room = 0x5F)
    ]),

    #Moon Base
    Level(name = "Moon Base", target_address = {"PAL": 0xC63BB0, "NTSC": 0xC63E30}, room_entrances = [
        #Entry
        RoomEntrance(name = "Entry from Spawn", can_start = True, target_room = 0x4E, connection_requirements = {"Wheel from Entry": [[]], "UFO Arena from Entry": [[]], "Armoured Monkey Arena from Entry": [["*Air Crawl"]], "Robot from Entry": [["*Air Crawl"]], "Moving Platforms from Entry": [["*Air Crawl"]], "Mech Arena from Entry": [["*Air Crawl"], ["*Boost Fly", "*Hard"]], "Inside Climb from Entry": [["*Air Crawl"]], "Bomb from Entry": [["*Air Crawl"]]}),
        RoomEntrance(name = "Entry from Wheel", source_room = 0x4F, target_room = 0x4E, connection_requirements = {"Wheel from Entry": [[]], "UFO Arena from Entry": [[]], "Armoured Monkey Arena from Entry": [["*Air Crawl"]], "Robot from Entry": [["*Air Crawl"]], "Moving Platforms from Entry": [["*Air Crawl"]], "Mech Arena from Entry": [["*Air Crawl"], ["*Boost Fly", "*Hard"]], "Inside Climb from Entry": [["*Air Crawl"]], "Bomb from Entry": [["*Air Crawl"]]}),
        RoomEntrance(name = "Entry from UFO Arena", source_room = 0x52, target_room = 0x4E, connection_requirements = {"Wheel from Entry": [[]], "UFO Arena from Entry": [[]], "Armoured Monkey Arena from Entry": [["*Air Crawl"]], "Robot from Entry": [["*Air Crawl"]], "Moving Platforms from Entry": [["*Air Crawl"]], "Mech Arena from Entry": [["*Air Crawl"], ["*Boost Fly", "*Hard"]], "Inside Climb from Entry": [["*Air Crawl"]], "Bomb from Entry": [["*Air Crawl"]]}),

        RoomEntrance(name = "Entry from Armoured Monkey Arena", source_room = 0x53, target_room = 0x4E, connection_requirements = {"Wheel from Entry": [["*Air Crawl"]], "UFO Arena from Entry": [["*Air Crawl"]], "Armoured Monkey Arena from Entry": [[]], "Robot from Entry": [[]], "Moving Platforms from Entry": [[]], "Mech Arena from Entry": [["*Air Crawl"], ["*Boost Fly", "*Hard"]], "Inside Climb from Entry": [["*Air Crawl"]], "Bomb from Entry": [["*Air Crawl"]]}),
        RoomEntrance(name = "Entry from Robot", source_room = 0x50, target_room = 0x4E, connection_requirements = {"Wheel from Entry": [["*Air Crawl"]], "UFO Arena from Entry": [["*Air Crawl"]], "Armoured Monkey Arena from Entry": [[]], "Robot from Entry": [[]], "Moving Platforms from Entry": [[]], "Mech Arena from Entry": [["*Air Crawl"], ["*Boost Fly", "*Hard"]], "Inside Climb from Entry": [["*Air Crawl"]], "Bomb from Entry": [["*Air Crawl"]]}),
        RoomEntrance(name = "Entry from Moving Platforms", source_room = 0x54, target_room = 0x4E, connection_requirements = {"Wheel from Entry": [["*Air Crawl"]], "UFO Arena from Entry": [["*Air Crawl"]], "Armoured Monkey Arena from Entry": [[]], "Robot from Entry": [[]], "Moving Platforms from Entry": [[]], "Mech Arena from Entry": [["*Air Crawl"], ["*Boost Fly", "*Hard"]], "Inside Climb from Entry": [["*Air Crawl"]], "Bomb from Entry": [["*Air Crawl"]]}),

        RoomEntrance(name = "Entry from Mech Arena", source_room = 0x56, target_room = 0x4E, connection_requirements = {"Wheel from Entry": [["*Air Crawl"]], "UFO Arena from Entry": [["*Air Crawl"]], "Armoured Monkey Arena from Entry": [["*Air Crawl"]], "Robot from Entry": [["*Air Crawl"]], "Moving Platforms from Entry": [["*Air Crawl"]], "Mech Arena from Entry": [[]], "Inside Climb from Entry": [[]], "Bomb from Entry": [["*Air Crawl"]]}),
        RoomEntrance(name = "Entry from Inside Climb", source_room = 0x57, target_room = 0x4E, connection_requirements = {"Wheel from Entry": [["*Air Crawl"]], "UFO Arena from Entry": [["*Air Crawl"]], "Armoured Monkey Arena from Entry": [["*Air Crawl"]], "Robot from Entry": [["*Air Crawl"]], "Moving Platforms from Entry": [["*Air Crawl"]], "Mech Arena from Entry": [[]], "Inside Climb from Entry": [[]], "Bomb from Entry": [["*Air Crawl"]]}),

        RoomEntrance(name = "Entry from Bomb", source_room = 0x58, target_room = 0x4E, connection_requirements = {"Wheel from Entry": [[]], "UFO Arena from Entry": [[]], "Armoured Monkey Arena from Entry": [["*Air Crawl"]], "Robot from Entry": [["*Air Crawl"]], "Moving Platforms from Entry": [["*Air Crawl"]], "Mech Arena from Entry": [["*Air Crawl"]], "Inside Climb from Entry": [["*Air Crawl"]], "Bomb from Entry": [[]]}),

        #Wheel
        RoomEntrance(name = "Wheel from Entry", can_start = True, source_room = 0x4E, target_room = 0x4F, connection_requirements = {"Entry from Wheel": [[]]}),

        #UFO Arena
        RoomEntrance(name = "UFO Arena from Entry", can_start = True, source_room = 0x4E, target_room = 0x52, connection_requirements = {"Entry from UFO Arena": [[]], "Rotating Magnets from UFO Arena": [[]]}),
        RoomEntrance(name = "UFO Arena from Rotating Magnets", source_room = 0x51, target_room = 0x52, connection_requirements = {"Entry from UFO Arena": [[]], "Rotating Magnets from UFO Arena": [[]]}),

        #Rotating Magnets
        RoomEntrance(name = "Rotating Magnets from UFO Arena", can_start = True, source_room = 0x52, target_room = 0x51, connection_requirements = {"UFO Arena from Rotating Magnets": [[]], "Armoured Monkey Arena from Rotating Magnets": [["Electro Magnet", "Sky Flyer"], ["Electro Magnet", "*Hard"], ["*Air Crawl"]]}),
        RoomEntrance(name = "Rotating Magnets from Armoured Monkey Arena", source_room = 0x53, target_room = 0x51, connection_requirements = {"UFO Arena from Rotating Magnets": [["Electro Magnet", "Sky Flyer"], ["Electro Magnet", "*Hard"], ["*Air Crawl"]], "Armoured Monkey Arena from Rotating Magnets": [[]]}),

        #Arena
        RoomEntrance(name = "Armoured Monkey Arena from Rotating Magnets", source_room = 0x51, target_room = 0x53, connection_requirements = {"Rotating Magnets from Armoured Monkey Arena": [[]], "Entry from Armoured Monkey Arena": [[]]}),
        RoomEntrance(name = "Armoured Monkey Arena from Entry", can_start = True, source_room = 0x4E, target_room = 0x53, connection_requirements = {"Rotating Magnets from Armoured Monkey Arena": [[]], "Entry from Armoured Monkey Arena": [[]]}),

        #Robot
        RoomEntrance(name = "Robot from Entry", can_start = True, source_room = 0x4E, target_room = 0x50, connection_requirements = {"Entry from Robot": [[]]}),

        #Moving Platforms
        RoomEntrance(name = "Moving Platforms from Entry", can_start = True, source_room = 0x4E, target_room = 0x54, connection_requirements = {"Entry from Moving Platforms": [[]], "Magnetic Panels from Moving Platforms": [["Electro Magnet", "*Moon Fire"], ["*Moon Fire", "*Boost Fly", "*Expert", "Power Punch"], ["*Air Crawl", "Power Punch"]]}),
        RoomEntrance(name = "Moving Platforms from Magnetic Panels", source_room = 0x55, target_room = 0x54, connection_requirements = {"Entry from Moving Platforms": [["Electro Magnet", "Water Cannon", "Sky Flyer", "Power Punch"], ["Electro Magnet", "*Damage Boost", "Sky Flyer", "Power Punch"], ["Electro Magnet", "Water Cannon", "*Air Crawl", "Power Punch"], ["Electro Magnet", "*Damage Boost", "*Air Crawl", "Power Punch"]], "Magnetic Panels from Moving Platforms": [[]]}),
        
        #Magnetic Panels
        RoomEntrance(name = "Magnetic Panels from Moving Platforms", can_start = True, source_room = 0x54, target_room = 0x55, connection_requirements = {"Moving Platforms from Magnetic Panels": [[]], "Mech Arena from Magnetic Panels": [["Electro Magnet"], ["*Boost Fly", "*Expert"], ["*Air Crawl"]]}),
        RoomEntrance(name = "Magnetic Panels from Mech Arena", source_room = 0x56, target_room = 0x55, connection_requirements = {"Moving Platforms from Magnetic Panels": [["Electro Magnet"], ["*Boost Fly", "*Expert"], ["*Air Crawl"]], "Mech Arena from Magnetic Panels": [[]]}),

        #Mech Arena
        RoomEntrance(name = "Mech Arena from Magnetic Panels", can_start = True, source_room = 0x55, target_room = 0x56, connection_requirements = {"Magnetic Panels from Mech Arena": [[]], "Entry from Mech Arena": [[]]}),
        RoomEntrance(name = "Mech Arena from Entry", source_room = 0x4E, target_room = 0x56, connection_requirements = {"Magnetic Panels from Mech Arena": [[]], "Entry from Mech Arena": [[]]}),

        #Inside Climb
        RoomEntrance(name = "Inside Climb from Entry", can_start = True, source_room = 0x4E, target_room = 0x57, connection_requirements = {"Outside Climb Start from Inside Climb": [["R.C. Car", "Sky Flyer", "Catapult", "Electro Magnet", "*Attack"], ["*Boost Fly", "*Expert"], ["Sky Flyer", "Electro Magnet", "*Hard"], ["*Air Crawl"]], "Outside Climb End from Inside Climb": [["*Air Crawl"]], "Entry from Inside Climb": [[]], "Bomb from Inside Climb": [["*Air Crawl"]]}),
        RoomEntrance(name = "Inside Climb from Outside Climb Start", source_room = 0x58, target_room = 0x57, connection_requirements = {"Outside Climb Start from Inside Climb": [[]], "Outside Climb End from Inside Climb": [["*Air Crawl"]], "Entry from Inside Climb": [[]], "Bomb from Inside Climb": [["*Air Crawl"]]}),
        RoomEntrance(name = "Inside Climb from Outside Climb End", source_room = 0x58, target_room = 0x57, connection_requirements = {"Outside Climb Start from Inside Climb": [[]], "Outside Climb End from Inside Climb": [[]], "Entry from Inside Climb": [[]], "Bomb from Inside Climb": [[]]}),
        RoomEntrance(name = "Inside Climb from Bomb", source_room = 0x58, target_room = 0x57, connection_requirements = {"Outside Climb Start from Inside Climb": [[]], "Outside Climb End from Inside Climb": [[]], "Entry from Inside Climb": [[]], "Bomb from Inside Climb": [[]]}),

        #Outside Climb
        RoomEntrance(name = "Outside Climb Start from Inside Climb", can_start = True, source_room = 0x57, target_room = 0x58, connection_requirements = {"Inside Climb from Outside Climb End": [[]], "Inside Climb from Outside Climb Start": [[]]}),
        RoomEntrance(name = "Outside Climb End from Inside Climb", source_room = 0x57, target_room = 0x58, connection_requirements = {"Inside Climb from Outside Climb End": [[]], "Inside Climb from Outside Climb Start": [[]]}),

        #Bomb
        RoomEntrance(name = "Bomb from Entry", source_room = 0x4E, target_room = 0x58, connection_requirements = {"Entry from Bomb": [["Electro Magnet"], ["*Air Crawl", "Sky Flyer", "*Expert"], ["Power Punch", "*Hard"]], "Inside Climb from Bomb": [[]]}),
        RoomEntrance(name = "Bomb from Inside Climb", source_room = 0x57, target_room = 0x58, connection_requirements = {"Entry from Bomb": [["Electro Magnet"], ["*Air Crawl", "Sky Flyer", "*Expert"], ["Power Punch", "*Hard"]], "Inside Climb from Bomb": [[]]})
    ]),

    #Showdown with Specter!
    Level(name = "Showdown with Specter!", is_boss = True, room_entrances = [
        #Entry
        RoomEntrance(name = "Entry from Spawn", can_start = True, target_room = 0x60)
    ]),

    #Final Showdown with Specter!
    Level(name = "Final Showdown with Specter!", is_boss = True, keep_at_end = True, room_entrances = [
        #Entry
        RoomEntrance(name = "Entry from Spawn", can_start = True, target_room = 0x61)
    ])
]

level_from_name: dict[str, Level] = {level.name: level for level in levels}

for monkey in monkeys:
    level_from_name[monkey.level].monkeys.append(monkey)
for phone in phones:
    level_from_name[phone.level].phones.append(phone)

def build_randomised_maps(world):
    available_rooms = []
    all_rooms = {}
    room_definitions = {}

    for level in levels:
        starting_room = level.room_entrances[0]
        for entrance in level.room_entrances:
            if not entrance.name == starting_room.name:
                available_rooms.append(f"{entrance.name} - {level.name}")
            all_rooms[f"{entrance.name} - {level.name}"] = entrance

        room_definition = {}
        for connection_requirement in starting_room.connection_requirements:
            room_definition[f"{connection_requirement} - {level.name}"] = None
        room_definitions[level.name] = room_definition

    world.random.shuffle(available_rooms)

    shuffle_blacklist = ["Final Room from Lobby - Skyscraper City", "Inside End from Entry - Enter the Monkey", "Third Room End from Second Room - Ninja Hideout", "Wall End from Entry - Ninja Hideout", "Boulders End from Entry - Panic Pyramid", "Moving Platforms #2 from Entry - Panic Pyramid"]
    available_rooms = [room for room in available_rooms if not room in shuffle_blacklist]

    while any(None in room_definition.values() for room_definition in room_definitions.values()):
        for level in levels:
            room_definition = room_definitions[level.name]
            if None in room_definition.values():
                for room_connection in list(room_definition.keys()):
                    if room_definition[room_connection] == None: #No target given to this transition

                        connection_already_chosen = False
                        for entry in room_definitions:
                            if room_connection in room_definitions[entry] and not room_definitions[entry][room_connection] == None:
                                new_destination = room_definitions[entry][room_connection]
                                connection_already_chosen = True
                        if not connection_already_chosen:
                            new_destination = available_rooms.pop() #Get a new destination
                        room_definition[room_connection] = new_destination #Assign it

                        #Create the reverse of this transition
                        entrance_level = room_connection.split(" - ")[1]
                        entrance_parts = room_connection.split(" - ")[0].split(" from ")
                        entrance_parts.reverse() 
                        reversed_entrance = f"{" from ".join(entrance_parts)} - {entrance_level}"

                        destination_level = new_destination.split(" - ")[1]
                        destination_parts = new_destination.split(" - ")[0].split(" from ")
                        destination_parts.reverse()
                        reversed_destination = f"{" from ".join(destination_parts)} - {destination_level}"

                        room_definition[reversed_destination] = reversed_entrance #Assign the reverse
                        if reversed_entrance in available_rooms:
                            available_rooms.remove(reversed_entrance) #Remove reversed variant from pool
                for connection_requirement in list(room_definition.keys()):
                    for connection in all_rooms[room_definition[connection_requirement]].connection_requirements:
                        if not f"{connection} - {room_definition[connection_requirement].split(" - ")[1]}" in room_definition:
                            room_definition[f"{connection} - {room_definition[connection_requirement].split(" - ")[1]}"] = None
                room_definitions[level.name] = room_definition

    if len(available_rooms) > 0:
        raise Exception("Not all rooms allocated.")

    randomised_gates = {}
    for level in room_definitions:
        randomised_gates.update(room_definitions[level])

    return randomised_gates

music_table = {
    0xA: {"value": 0x02, "address": {"PAL": 0x3B1A58, "NTSC": 0x3B0558}}, #Liberty Island
    0xB: {"value": 0x03, "address": {"PAL": 0x3B1A98, "NTSC": 0x3B0598}}, #Breezy Village
    0xC: {"value": 0x04, "address": {"PAL": 0x3B1AD8, "NTSC": 0x3B05D8}}, #Port Calm
    0xD: {"value": 0x04, "address": {"PAL": 0x3B1B18, "NTSC": 0x3B0618}}, #Port Calm (Inside)
    0xE: {"value": 0x05, "address": {"PAL": 0x3B1B58, "NTSC": 0x3B0658}}, #Viva Apespania
    0xF: {"value": 0x05, "address": {"PAL": 0x3B1B98, "NTSC": 0x3B0698}}, #Viva Apespania (Village)
    0x10: {"value": 0x05, "address": {"PAL": 0x3B1BD8, "NTSC": 0x3B06D8}}, #Viva Apespania (Bullring)
    0x11: {"value": 0x06, "address": {"PAL": 0x3B1C18, "NTSC": 0x3B0718}}, #Ninja Hideout
    0x12: {"value": 0x06, "address": {"PAL": 0x3B1C58, "NTSC": 0x3B0758}}, #Ninja Hideout (Second Room)
    0x13: {"value": 0x06, "address": {"PAL": 0x3B1C98, "NTSC": 0x3B0798}}, #Ninja Hideout (Third Room)
    0x14: {"value": 0x07, "address": {"PAL": 0x3B1CD8, "NTSC": 0x3B07D8}}, #Castle Frightmare
    0x15: {"value": 0x07, "address": {"PAL": 0x3B1D18, "NTSC": 0x3B0818}}, #Castle Frightmare (House)
    0x16: {"value": 0x07, "address": {"PAL": 0x3B1D58, "NTSC": 0x3B0858}}, #Castle Frightmare (Dungeon)
    0x17: {"value": 0x16, "address": {"PAL": 0x3B1D98, "NTSC": 0x3B0898}}, #Vita-Z Factory
    0x18: {"value": 0x16, "address": {"PAL": 0x3B1DD8, "NTSC": 0x3B08D8}}, #Vita-Z Factory (Mech Tunnel)
    0x19: {"value": 0x16, "address": {"PAL": 0x3B1E18, "NTSC": 0x3B0918}}, #Vita-Z Factory (Mech Arena)
    0x1A: {"value": 0x08, "address": {"PAL": 0x3B1E58, "NTSC": 0x3B0958}}, #Casino City
    0x1B: {"value": 0x08, "address": {"PAL": 0x3B1E98, "NTSC": 0x3B0998}}, #Casino City (Bar)
    0x1C: {"value": 0x08, "address": {"PAL": 0x3B1ED8, "NTSC": 0x3B09D8}}, #Casino City (Circus)
    0x1D: {"value": 0x09, "address": {"PAL": 0x3B1F18, "NTSC": 0x3B0A18}}, #The Blue Baboon
    0x1E: {"value": 0x09, "address": {"PAL": 0x3B1F58, "NTSC": 0x3B0A58}}, #The Blue Baboon (Changing Hut)
    0x1F: {"value": 0x09, "address": {"PAL": 0x3B1FD8, "NTSC": 0x3B0AD8}}, #The Blue Baboon (Bananarang)
    0x21: {"value": 0x09, "address": {"PAL": 0x3B1F98, "NTSC": 0x3B0A98}}, #The Blue Baboon (Ship)
    0x22: {"value": 0x0A, "address": {"PAL": 0x3B2058, "NTSC": 0x3B0B58}}, #Lookout Valley
    0x23: {"value": 0x0A, "address": {"PAL": 0x3B2098, "NTSC": 0x3B0B98}}, #Lookout Valley (Jungle)
    0x24: {"value": 0x0A, "address": {"PAL": 0x3B20D8, "NTSC": 0x3B0BD8}}, #Lookout Valley (Cave)
    0x25: {"value": 0x0B, "address": {"PAL": 0x3B2118, "NTSC": 0x3B0C18}}, #Snowball Mountain
    0x26: {"value": 0x0B, "address": {"PAL": 0x3B2158, "NTSC": 0x3B0C58}}, #Snowball Mountain (Christmas Tree)
    0x27: {"value": 0x0C, "address": {"PAL": 0x3B2198, "NTSC": 0x3B0C98}}, #Snowball Mountain (Ski Hill)
    0x28: {"value": 0x0D, "address": {"PAL": 0x3B21D8, "NTSC": 0x3B0CD8}}, #Enter The Monkey
    0x29: {"value": 0x0D, "address": {"PAL": 0x3B21D8, "NTSC": 0x3B0CD8}}, #Enter The Monkey (Inside)
    0x2A: {"value": 0x0D, "address": {"PAL": 0x3B2258, "NTSC": 0x3B0D58}}, #Enter The Monkey (Wall)
    0x2C: {"value": 0x0E, "address": {"PAL": 0x3B22D8, "NTSC": 0x3B0DD8}}, #Simian Citadel
    0x2D: {"value": 0x0E, "address": {"PAL": 0x3B2318, "NTSC": 0x3B0E18}}, #Simian Citadel (Bullring)
    0x2E: {"value": 0x0E, "address": {"PAL": 0x3B2358, "NTSC": 0x3B0E58}}, #Simian Citadel (Whale)
    0x2F: {"value": 0x0E, "address": {"PAL": 0x3B2398, "NTSC": 0x3B0E98}}, #Simian Citadel (Submarine)
    0x30: {"value": 0x0E, "address": {"PAL": 0x3B23D8, "NTSC": 0x3B0ED8}}, #Simian Citadel (Fountain)
    0x31: {"value": 0x0F, "address": {"PAL": 0x3B2418, "NTSC": 0x3B0F18}}, #Panic Pyramid
    0x32: {"value": 0x0F, "address": {"PAL": 0x3B2458, "NTSC": 0x3B0F58}}, #Panic Pyramid (Booby Traps)
    0x33: {"value": 0x0F, "address": {"PAL": 0x3B2498, "NTSC": 0x3B0F98}}, #Panic Pyramid (Moving Platforms #1)
    0x34: {"value": 0x0F, "address": {"PAL": 0x3B24D8, "NTSC": 0x3B0FD8}}, #Panic Pyramid (Boulders)
    0x35: {"value": 0x0F, "address": {"PAL": 0x3B2518, "NTSC": 0x3B1018}}, #Panic Pyramid (Moving Platforms #2)
    0x36: {"value": 0x10, "address": {"PAL": 0x3B2558, "NTSC": 0x3B1058}}, #Pirate Isle
    0x37: {"value": 0x10, "address": {"PAL": 0x3B2598, "NTSC": 0x3B1098}}, #Pirate Isle (Volcano)
    0x38: {"value": 0x10, "address": {"PAL": 0x3B25D8, "NTSC": 0x3B10D8}}, #Pirate Isle (Boat)
    0x39: {"value": 0x10, "address": {"PAL": 0x3B2618, "NTSC": 0x3B1118}}, #Pirate Isle (Treasure)
    0x3A: {"value": 0x10, "address": {"PAL": 0x3B2658, "NTSC": 0x3B1158}}, #Pirate Isle (Mine)
    0x3B: {"value": 0x11, "address": {"PAL": 0x3B2698, "NTSC": 0x3B1198}}, #Land of the Apes
    0x3C: {"value": 0x11, "address": {"PAL": 0x3B26D8, "NTSC": 0x3B11D8}}, #Land of the Apes (Icicles)
    0x3D: {"value": 0x12, "address": {"PAL": 0x3B2718, "NTSC": 0x3B1218}}, #Land of the Apes (Ski Hill)
    0x3E: {"value": 0x13, "address": {"PAL": 0x3B2758, "NTSC": 0x3B1258}}, #Land of the Apes (Spa)
    0x3F: {"value": 0x14, "address": {"PAL": 0x3B2798, "NTSC": 0x3B1298}}, #The Lost World
    0x40: {"value": 0x14, "address": {"PAL": 0x3B27D8, "NTSC": 0x3B12D8}}, #The Lost World (Pterodactyls)
    0x41: {"value": 0x14, "address": {"PAL": 0x3B2818, "NTSC": 0x3B1318}}, #The Lost World (T-Rex)
    0x42: {"value": 0x14, "address": {"PAL": 0x3B2858, "NTSC": 0x3B1358}}, #The Lost World (Trees)
    0x43: {"value": 0x15, "address": {"PAL": 0x3B2898, "NTSC": 0x3B1398}}, #Skyscraper City
    0x44: {"value": 0x15, "address": {"PAL": 0x3B28D8, "NTSC": 0x3B13D8}}, #Skyscraper City (Lobby)
    0x45: {"value": 0x15, "address": {"PAL": 0x3B2918, "NTSC": 0x3B1418}}, #Skyscraper City (Sewer)
    0x46: {"value": 0x15, "address": {"PAL": 0x3B2958, "NTSC": 0x3B1458}}, #Skyscraper City (Tank)
    0x47: {"value": 0x15, "address": {"PAL": 0x3B2998, "NTSC": 0x3B1498}}, #Skyscraper City (Final Room)
    0x48: {"value": 0x17, "address": {"PAL": 0x3B29D8, "NTSC": 0x3B14D8}}, #Code C.H.I.M.P.
    0x49: {"value": 0x17, "address": {"PAL": 0x3B2A18, "NTSC": 0x3B1518}}, #Code C.H.I.M.P. (Base Entrance)
    0x4A: {"value": 0x17, "address": {"PAL": 0x3B2A58, "NTSC": 0x3B1558}}, #Code C.H.I.M.P. (Tank)
    0x4B: {"value": 0x17, "address": {"PAL": 0x3B2A98, "NTSC": 0x3B1598}}, #Code C.H.I.M.P. (Treadmills)
    0x4C: {"value": 0x18, "address": {"PAL": 0x3B2AD8, "NTSC": 0x3B15D8}}, #Code C.H.I.M.P. (Moving Platforms)
    0x4D: {"value": 0x18, "address": {"PAL": 0x3B2B18, "NTSC": 0x3B1618}}, #Code C.H.I.M.P. (Magnetic Panels)
    0x4E: {"value": 0x19, "address": {"PAL": 0x3B2B58, "NTSC": 0x3B1658}}, #Moon Base
    0x4F: {"value": 0x19, "address": {"PAL": 0x3B2B98, "NTSC": 0x3B1698}}, #Moon Base (Wheel)
    0x50: {"value": 0x19, "address": {"PAL": 0x3B2C18, "NTSC": 0x3B1718}}, #Moon Base (Robot)
    0x51: {"value": 0x19, "address": {"PAL": 0x3B2C58, "NTSC": 0x3B1758}}, #Moon Base (Rotating Magnets)
    0x52: {"value": 0x19, "address": {"PAL": 0x3B2C98, "NTSC": 0x3B1798}}, #Moon Base (UFO Arena)
    0x53: {"value": 0x19, "address": {"PAL": 0x3B2CD8, "NTSC": 0x3B17D8}}, #Moon Base (Armoured Monkey Arena)
    0x54: {"value": 0x19, "address": {"PAL": 0x3B2D18, "NTSC": 0x3B1818}}, #Moon Base (Moving Platforms)
    0x55: {"value": 0x19, "address": {"PAL": 0x3B2D58, "NTSC": 0x3B1858}}, #Moon Base (Magnetic Panels)
    0x56: {"value": 0x19, "address": {"PAL": 0x3B2D58, "NTSC": 0x3B1858}}, #Moon Base (Mech Arena)
    0x57: {"value": 0x1A, "address": {"PAL": 0x3B2D98, "NTSC": 0x3B1898}}, #Moon Base (Inside Climb)
    0x58: {"value": 0x1A, "address": {"PAL": 0x3B2DD8, "NTSC": 0x3B18D8}}, #Moon Base (Outside Climb)
    0x59: {"value": 0x1B, "address": {"PAL": 0x3B2E18, "NTSC": 0x3B1918}}, #Blue Monkey Battle
    0x5A: {"value": 0x1C, "address": {"PAL": 0x3B2E58, "NTSC": 0x3B1958}}, #Yellow Monkey Battle
    0x5B: {"value": 0x1D, "address": {"PAL": 0x3B2E98, "NTSC": 0x3B1998}}, #Pink Monkey Battle
    0x5C: {"value": 0x1D, "address": {"PAL": 0x3B2ED8, "NTSC": 0x3B19D8}}, #Pink Monkey Battle - Phase 2
    0x5D: {"value": 0x1E, "address": {"PAL": 0x3B2F18, "NTSC": 0x3B1A18}}, #White Monkey Battle
    0x5E: {"value": 0x1F, "address": {"PAL": 0x3B2F58, "NTSC": 0x3B1A58}}, #Red Monkey Battle
    0x5F: {"value": 0x20, "address": {"PAL": 0x3B2F98, "NTSC": 0x3B1A98}}, #Giant Yellow Monkey
    0x60: {"value": 0x21, "address": {"PAL": 0x3B2FD8, "NTSC": 0x3B1AD8}}, #Specter Battle #1
    0x61: {"value": 0x22, "address": {"PAL": 0x3B3018, "NTSC": 0x3B1B18}}, #Specter Battle #2
}

randomised_music_pool = [ #Only includes looping tracks that aren't annoyingly short
    0x02, #Liberty Island
    0x03, #Breezy Village
    0x04, #Port Calm
    0x05, #Viva Apespania
    0x06, #Ninja Hideout
    0x07, #Castle Frightmare
    0x08, #Casino City
    0x09, #Blue Baboon
    0x0A, #Lookout Valley
    0x0B, #Snowball Mountain
    0x0C, #Snowball Mountain (Ski Hill)
    0x0D, #Enter The Monkey
    0x0E, #Simian Citadel
    0x0F, #Panic Pyramid
    0x10, #Pirate Isle
    0x11, #Land of the Apes
    0x13, #Land of the Apes (Spa)
    0x14, #The Lost World
    0x15, #Skyscraper City
    0x16, #Vita-Z Factory
    0x17, #Code C.H.I.M.P.
    0x18, #Code C.H.I.M.P. #2
    0x19, #Moon Base
    0x1A, #Moon Base #2

    0x1B, #Freaky Monkey Five Battle!
    0x20, #Giant Yellow Monkey Battle
    0x21, #Specter Battle #1
    0x22, #Specter Battle #2

    0x00, #Ape Escape 1 Title Theme
    0x23, #Gadget Trainer
    0x27, #Let's Play Monkey Football!!
    0x28, #Kick Off!!
    0x32 #Monkey Climber    
]