from dataclasses import dataclass, field
from .Monkeys import monkeys, Monkey    

@dataclass
class RoomEntrance:
    name: str
    connection_requirements: dict[str, list[str]] = field(default_factory = dict)
    value: int = 0xa

@dataclass
class Level:
    name: str
    world_key_requirement: int = 0
    monkeys: list[Monkey] = field(default_factory = list)
    room_entrances: list[RoomEntrance] = field(default_factory = lambda: [RoomEntrance(name = "Entry from Spawn")])
    target_address: dict = field(default_factory = dict)
    is_boss: bool = False
    keep_at_end: bool = False
    
levels = [
    #Liberty Island
    Level(name = "Liberty Island", target_address = {"PAL": 0xC636E0, "NTSC": 0xC63960}, room_entrances = [
        #Entry
        RoomEntrance(name = "Entry from Spawn", value = 0xA)
    ]),

    #Breezy Village
    Level(name = "Breezy Village", target_address = {"PAL": 0xC63710, "NTSC": 0xC63990}, room_entrances = [
        #Entry
        RoomEntrance(name = "Entry from Spawn", value = 0xB)
    ]),

    #Port Calm
    Level(name = "Port Calm", target_address = {"PAL": 0xC63740, "NTSC": 0xC639C0}, room_entrances = [
        #Entry
        RoomEntrance(name = "Entry from Spawn", value = 0xC, connection_requirements = {"Indoors from Entry": [["Water Net"]]}), 
        RoomEntrance(name = "Entry from Indoors", connection_requirements = {"Indoors from Entry": [["Water Net"]]}), 

        #Indoors
        RoomEntrance(name = "Indoors from Entry", connection_requirements = {"Entry from Indoors": [["Water Net"]]})
    ]),

    #Viva Apespania
    Level(name = "Viva Apespania", target_address = {"PAL": 0xC63770, "NTSC": 0xC639F0}, room_entrances = [
        #Entry
        RoomEntrance(name = "Entry from Spawn", value = 0xE, connection_requirements = {"Village from Entry": [[]]}), 
        RoomEntrance(name = "Entry from Village", connection_requirements = {"Village from Entry": [[]]}), 

        #Village
        RoomEntrance(name = "Village from Entry", value = 0xF, connection_requirements = {"Entry from Village": [[]], "Bullring from Village": [[]]}),
        RoomEntrance(name = "Village from Bullring", connection_requirements = {"Entry from Village": [[]], "Bullring from Village": [[]]}),

        #Bullring
        RoomEntrance(name = "Bullring from Village", value = 0x10, connection_requirements = {"Village from Bullring": [[]]})
    ]),

    #Blue Monkey Battle!
    Level(name = "Blue Monkey Battle!", is_boss = True, room_entrances = [
        #Entry
        RoomEntrance(name = "Entry from Spawn", value = 0x59)
    ]),

    #Castle Frightmare
    Level(name = "Castle Frightmare", target_address = {"PAL": 0xC637D0, "NTSC": 0xC63A50}, room_entrances = [
        #Entry
        RoomEntrance(name = "Entry from Spawn", value = 0x14, connection_requirements = {"House from Entry": [[]]}),
        RoomEntrance(name = "Entry from House", connection_requirements = {"House from Entry": [[]]}),

        #House
        RoomEntrance(name = "House from Entry", value = 0x15, connection_requirements = {"Entry from House": [[]], "Dungeon from House": [[]]}),
        RoomEntrance(name = "House from Dungeon", connection_requirements = {"Entry from House": [[]], "Dungeon from House": [[]]}),

        #Dungeon
        RoomEntrance(name = "Dungeon from House", value = 0x16, connection_requirements = {"House from Dungeon": [[]]})
    ]),

    #Vita-Z Factory
    Level(name = "Vita-Z Factory", target_address = {"PAL": 0xC63800, "NTSC": 0xC63A80}, room_entrances = [
        #Entry
        RoomEntrance(name = "Entry from Spawn", value = 0x17, connection_requirements = {"Tunnel from Entry": [["Sky Flyer"], ["*Gear"], ["*Air Crawl"]], "Arena from Entry": [["Power Punch"], ["*Air Crawl", "*Hard"]]}),
        RoomEntrance(name = "Entry from Tunnel", connection_requirements = {"Tunnel from Entry": [["Sky Flyer"], ["*Gear"], ["*Air Crawl"]], "Arena from Entry": [["Power Punch"], ["*Air Crawl", "*Hard"]]}),
        RoomEntrance(name = "Entry from Arena", connection_requirements = {"Tunnel from Entry": [["Sky Flyer"], ["*Gear"], ["*Air Crawl"]], "Arena from Entry": [["Power Punch"], ["*Air Crawl", "*Hard"]]}),
        
        #Tunnel
        RoomEntrance(name = "Tunnel from Entry", value = 0x18, connection_requirements = {"Entry from Tunnel": [[]], "Arena from Tunnel": [[]]}),
        RoomEntrance(name = "Tunnel from Arena", connection_requirements = {"Entry from Tunnel": [[]], "Arena from Tunnel": [[]]}),

        #Arena
        RoomEntrance(name = "Arena from Tunnel", value = 0x19, connection_requirements = {"Tunnel from Arena": [[]], "Entry from Arena": [[]]}),
        RoomEntrance(name = "Arena from Entry", connection_requirements = {"Tunnel from Arena": [[]], "Entry from Arena": [[]]})
    ]),

    #Casino City
    Level(name = "Casino City", target_address = {"PAL": 0xC63830, "NTSC": 0xC63AB0}, room_entrances = [
        #Entry
        RoomEntrance(name = "Entry from Spawn", value = 0x1A, connection_requirements = {"Bar from Entry": [["*Attack"], ["Catapult"], ["*Hard"]], "Circus from Entry": [["Catapult"], ["Stun Club", "*Hard"], ["Power Punch", "*Hard"], ["Sky Flyer", "*Hard"], ["*Expert", "Pipotchi"]]}),
        RoomEntrance(name = "Entry from Circus", connection_requirements = {"Bar from Entry": [["*Attack"], ["Catapult"], ["*Hard"]], "Circus from Entry": [[]]}),
        RoomEntrance(name = "Entry from Bar", connection_requirements = {"Bar from Entry": [[]], "Circus from Entry": [["Catapult"], ["Stun Club", "*Hard"], ["Power Punch", "*Hard"], ["Sky Flyer", "*Hard"], ["*Expert", "Pipotchi"]]}),

        #Bar
        RoomEntrance(name = "Bar from Entry", value = 0x1B, connection_requirements = {"Entry from Bar": [[]]}),

        #Circus
        RoomEntrance(name = "Circus from Entry", value = 0x1C, connection_requirements = {"Entry from Circus": [[]]})
    ]),   
    
    #Ninja Hideout
    Level(name = "Ninja Hideout", target_address = {"PAL": 0xC63860, "NTSC": 0xC63AE0}, room_entrances = [
        #Entry
        RoomEntrance(name = "Entry from Spawn", value = 0x11, connection_requirements = {"Second Room from Entry": [["Water Net", "R.C. Car", "*Hard"], ["Water Net", "R.C. Car", "*Attack"], ["*Air Crawl"], ["R.C. Car", "*Boost Fly", "*Expert"]]}),
        RoomEntrance(name = "Entry from Second Room", connection_requirements = {"Second Room from Entry": [["Water Net", "R.C. Car", "*Hard"], ["Water Net", "R.C. Car", "*Attack"], ["*Air Crawl"], ["R.C. Car", "*Boost Fly", "*Expert"]]}),

        #Second Room
        RoomEntrance(name = "Second Room from Entry", value = 0x12, connection_requirements = {"Entry from Second Room": [[]], "Third Room Start from Second Room": [["R.C. Car"], ["Sky Flyer", "*Hard"], ["*Air Crawl"], ["Dash Hoop", "*Hard", "*Long Jump"]]}),
        RoomEntrance(name = "Second Room from Third Room Start", connection_requirements = {"Entry from Second Room": [[]], "Third Room Start from Second Room": [[]]}),
        RoomEntrance(name = "Second Room from Third Room End", connection_requirements = {"Entry from Second Room": [[]], "Third Room Start from Second Room": [["R.C. Car"], ["Sky Flyer", "*Hard"], ["*Air Crawl"], ["Dash Hoop", "*Hard", "*Long Jump"]]}),

        #Third Room
        RoomEntrance(name = "Third Room Start from Second Room", value = 0x13, connection_requirements = {"Second Room from Third Room End": [[]], "Second Room from Third Room Start": [[]]}),
        RoomEntrance(name = "Third Room End from Second Room", connection_requirements = {"Second Room from Third Room End": [[]], "Second Room from Third Room Start": [[]]}),
    ]),

    #Yellow Monkey Battle!
    Level(name = "Yellow Monkey Battle!", is_boss = True, room_entrances = [
        #Entry
        RoomEntrance(name = "Entry from Spawn", value = 0x5A)
    ]),

    #Snowball Mountain
    Level(name = "Snowball Mountain", target_address = {"PAL": 0xC638C0, "NTSC": 0xC63B40}, room_entrances = [
        #Entry
        RoomEntrance(name = "Entry from Spawn", value = 0x25, connection_requirements = {"Christmas Tree from Entry": [[]], "Ski Hill from Entry": [["*Air Crawl", "*Hard"], ["Sky Flyer", "*Hard"]]}),
        RoomEntrance(name = "Entry from Christmas Tree", connection_requirements = {"Christmas Tree from Entry": [[]], "Ski Hill from Entry": [["*Air Crawl", "*Hard"], ["Sky Flyer", "*Hard"]]}),
        RoomEntrance(name = "Entry from Ski Hill", connection_requirements = {"Christmas Tree from Entry": [[]], "Ski Hill from Entry": [[]]}),

        #Christmas Tree
        RoomEntrance(name = "Christmas Tree from Entry", value = 0x26, connection_requirements = {"Entry from Christmas Tree": [[]], "Ski Hill from Christmas Tree": [["*Air Crawl"], ["Dash Hoop"], ["*Hard"]]}),
        RoomEntrance(name = "Christmas Tree from Ski Hill", connection_requirements = {"Entry from Christmas Tree": [[]], "Ski Hill from Christmas Tree": [[]]}),

        #Ski Hill
        RoomEntrance(name = "Ski Hill from Entry", value = 0x27, connection_requirements = {"Entry from Ski Hill": [[]], "Christmas Tree from Ski Hill": [[]]}),
        RoomEntrance(name = "Ski Hill from Christmas Tree", connection_requirements = {"Entry from Ski Hill": [[]], "Christmas Tree from Ski Hill": [[]]})
    ]),

    #Lookout Valley
    Level(name = "Lookout Valley", target_address = {"PAL": 0xC638F0, "NTSC": 0xC63B70}, room_entrances = [
        #Entry
        RoomEntrance(name = "Entry from Spawn", value = 0x22, connection_requirements = {"Cave Start from Entry": [["*Valley Gap", "*Valley Island", "*Valley Boat"]], "Cave End from Entry": [["*Boost Fly", "*Hard"], ["*Air Crawl", "*Hard"]], "Jungle Start from Entry": [["*Valley Gap", "*Valley Island"]], "Jungle End from Entry": [["*Air Crawl", "*Hard"]]}),
        RoomEntrance(name = "Entry from Cave End", connection_requirements = {"Cave Start from Entry": [["*Valley Boat"]], "Cave End from Entry": [[]], "Jungle Start from Entry": [["*Valley Island"]], "Jungle End from Entry": [["*Air Crawl", "*Hard"]]}),
        RoomEntrance(name = "Entry from Cave Start", connection_requirements = {"Cave Start from Entry": [[]], "Cave End from Entry": [["*Boost Fly", "*Hard"], ["*Air Crawl", "*Hard"]], "Jungle Start from Entry": [["*Valley Island"]], "Jungle End from Entry": [["*Air Crawl", "*Hard"]]}),
        RoomEntrance(name = "Entry from Jungle Start", connection_requirements = {"Cave Start from Entry": [["*Valley Island", "*Valley Boat"]], "Cave End from Entry": [["*Boost Fly", "*Hard"], ["*Air Crawl", "*Hard"]], "Jungle Start from Entry": [[]], "Jungle End from Entry": [["*Air Crawl", "*Hard"]]}),
        RoomEntrance(name = "Entry from Jungle End", connection_requirements = {"Cave Start from Entry": [["*Valley Island", "*Valley Boat"]], "Cave End from Entry": [["*Boost Fly", "*Hard"], ["*Air Crawl", "*Hard"]], "Jungle Start from Entry": [[]], "Jungle End from Entry": [[]]}),

        #Jungle
        RoomEntrance(name = "Jungle Start from Entry", value = 0x23, connection_requirements = {"Entry from Jungle Start": [[]], "Entry from Jungle End": [[]]}),
        RoomEntrance(name = "Jungle End from Entry", connection_requirements = {"Entry from Jungle Start": [[]], "Entry from Jungle End": [[]]}),

        #Cave
        RoomEntrance(name = "Cave Start from Entry", value = 0x24, connection_requirements = {"Entry from Cave Start": [[]], "Entry from Cave End": [["*Valley Button", "*Valley Stalag", "Water Net"], ["*Valley Button", "*Valley Stalag", "Sky Flyer", "*Hard"], ["*Valley Button", "*Valley Stalag", "*Expert"]]}),
        RoomEntrance(name = "Cave End from Entry", connection_requirements = {"Entry from Cave Start": [["*Air Crawl"], ["Sky Flyer"], ["Water Net"]], "Entry from Cave End": [[]]})
    ]),

    #The Blue Baboon
    Level(name = "The Blue Baboon", target_address = {"PAL": 0xC63920, "NTSC": 0xC63BA0}, room_entrances = [
        #Entry
        RoomEntrance(name = "Entry from Spawn", value = 0x1D, connection_requirements = {"Ship from Entry": [[]], "Bananarang Room from Entry": [["Water Net"], ["*Air Crawl"]], "Changing Hut from Entry": [[]]}),
        RoomEntrance(name = "Entry from Ship", connection_requirements = {"Ship from Entry": [[]], "Bananarang Room from Entry": [["Water Net"], ["*Air Crawl"]], "Changing Hut from Entry": [[]]}),
        RoomEntrance(name = "Entry from Bananarang Room", connection_requirements = {"Ship from Entry": [["Water Net"], ["*Air Crawl"]], "Bananarang Room from Entry": [["Water Net"], ["*Air Crawl"]], "Changing Hut from Entry": [["Water Net"], ["*Air Crawl"]]}),
        RoomEntrance(name = "Entry from Changing Hut", connection_requirements = {"Ship from Entry": [[]], "Bananarang Room from Entry": [[]], "Changing Hut from Entry": [[]]}),

        #Hut
        RoomEntrance(name = "Changing Hut from Entry", value = 0x1E, connection_requirements = {"Entry from Changing Hut": [[]]}),

        #Ship
        RoomEntrance(name = "Ship from Entry", value = 0x21, connection_requirements = {"Entry from Ship": [[]]}),

        #Bananarang Room
        RoomEntrance(name = "Bananarang Room from Entry", value = 0x1F, connection_requirements = {"Entry from Bananarang Room": [[]]})
    ]),

    #Pink Monkey Battle!
    Level(name = "Pink Monkey Battle!", is_boss = True, room_entrances = [
        #Entry
        RoomEntrance(name = "Entry from Spawn", value = 0x5B)
    ]),

    #Enter the Monkey
    Level(name = "Enter the Monkey", target_address = {"PAL": 0xC63980, "NTSC": 0xC63C00}, room_entrances = [
        #Entry
        RoomEntrance(name = "Entry from Spawn", value = 0x28, connection_requirements = {"Inside Start from Entry": [[]], "Wall Start from Entry": [[]]}), 
        RoomEntrance(name = "Entry from Inside Start", connection_requirements = {"Inside Start from Entry": [[]], "Wall Start from Entry": [[]]}), 
        RoomEntrance(name = "Entry from Inside End", connection_requirements = {"Inside Start from Entry": [[]], "Wall Start from Entry": [[]]}), 
        RoomEntrance(name = "Entry from Wall Start", connection_requirements = {"Inside Start from Entry": [[]], "Wall Start from Entry": [[]]}), 
        RoomEntrance(name = "Entry from Wall End", connection_requirements = {"Inside Start from Entry": [[]], "Wall Start from Entry": [[]]}), 

        #Inside
        RoomEntrance(name = "Inside Start from Entry", value = 0x29, connection_requirements = {"Entry from Inside Start": [[]], "Entry from Inside End": [["*Gear"]]}), 
        RoomEntrance(name = "Inside End from Entry", connection_requirements = {}), 

        #Wall
        RoomEntrance(name = "Wall Start from Entry", value = 0x2A, connection_requirements = {"Entry from Wall Start": [[]], "Entry from Wall End": [["R.C. Car"], ["*Air Crawl"], ["*Boost Fly", "*Hard"]]}), 
        RoomEntrance(name = "Wall End from Entry", connection_requirements = {"Entry from Wall Start": [[]], "Entry from Wall End": [[]]})
    ]),

    #Simian Citadel
    Level(name = "Simian Citadel", target_address = {"PAL": 0xC639B0, "NTSC": 0xC63C30}, room_entrances = [
        #Entry
        RoomEntrance(name = "Entry from Spawn", value = 0x2C, connection_requirements = {"Bullring from Entry": [["*Gear", "Water Net"]], "Fountain from Entry": [["*Air Crawl", "*Hard"], ["*Boost Fly", "*Hard"]]}), 
        RoomEntrance(name = "Entry from Bullring", connection_requirements = {"Bullring from Entry": [[]], "Fountain from Entry": [["*Gear", "Water Net", "*Boost Fly", "*Hard"], ["*Gear", "Water Net", "*Air Crawl", "*Hard"]]}), 
        RoomEntrance(name = "Entry from Fountain", connection_requirements = {"Bullring from Entry": [["*Gear", "Water Net"]], "Fountain from Entry": [[]]}), 

        #Bullring
        RoomEntrance(name = "Bullring from Entry", value = 0x2D, connection_requirements = {"Entry from Bullring": [[]], "Whale from Bullring": [["Dash Hoop", "*Bull Fight"], ["*Bull Fight", "*Hard"], ["*Air Crawl", "*Hard"]]}), 
        RoomEntrance(name = "Bullring from Whale", connection_requirements = {"Entry from Bullring": [["Dash Hoop", "*Bull Fight"], ["*Bull Fight", "*Hard"], ["*Air Crawl", "*Hard"]], "Whale from Bullring": [[]]}), 

        #Whale
        RoomEntrance(name = "Whale from Bullring", value = 0x2E, connection_requirements = {"Submarine from Whale": [["Sky Flyer", "Water Net", "*Attack"], ["Sky Flyer", "*Hard"], ["*Air Crawl"]], "Bullring from Whale": [[]]}), 

        #Submarine
        RoomEntrance(name = "Submarine from Whale", value = 0x2F, connection_requirements = {"Fountain from Submarine": [[]]}), 
        RoomEntrance(name = "Submarine from Fountain", connection_requirements = {"Fountain from Submarine": [[]]}), 

        #Fountain
        RoomEntrance(name = "Fountain from Submarine", value = 0x30, connection_requirements = {"Submarine from Fountain": [[]], "Entry from Fountain": [[]]}), 
        RoomEntrance(name = "Fountain from Entry", connection_requirements = {"Submarine from Fountain": [[]], "Entry from Fountain": [[]]})
    ]),

    #Panic Pyramid
    Level(name = "Panic Pyramid", target_address = {"PAL": 0xC639E0, "NTSC": 0xC63C60}, room_entrances = [
        #Entry
        RoomEntrance(name = "Entry from Spawn", value = 0x31, connection_requirements = {"Booby Traps from Entry": [[]], "Moving Platforms #2 from Entry": [["*Air Crawl"], ["*Boost Fly", "*Expert"]], "Boulders Start from Entry": [["R.C. Car"], ["Dash Hoop"]], "Boulders End from Entry": [["*Air Crawl"]]}), 
        RoomEntrance(name = "Entry from Booby Traps", connection_requirements = {"Booby Traps from Entry": [[]], "Moving Platforms #2 from Entry": [["*Air Crawl"], ["*Boost Fly", "*Expert"]], "Boulders Start from Entry": [["R.C. Car"], ["Dash Hoop"]], "Boulders End from Entry": [["*Air Crawl"]]}),
        RoomEntrance(name = "Entry from Moving Platforms #2", connection_requirements = {"Booby Traps from Entry": [[]], "Moving Platforms #2 from Entry": [["*Air Crawl"], ["*Boost Fly", "*Expert"]], "Boulders Start from Entry": [["R.C. Car"], ["Dash Hoop"]], "Boulders End from Entry": [["*Air Crawl"]]}), 
        RoomEntrance(name = "Entry from Boulders Start", connection_requirements = {"Booby Traps from Entry": [[]], "Moving Platforms #2 from Entry": [["*Air Crawl"], ["*Boost Fly", "*Expert"]], "Boulders Start from Entry": [["R.C. Car"], ["Dash Hoop"]], "Boulders End from Entry": [["*Air Crawl"]]}), 
        RoomEntrance(name = "Entry from Boulders End", connection_requirements = {"Booby Traps from Entry": [[]], "Moving Platforms #2 from Entry": [["*Air Crawl"], ["*Boost Fly", "*Expert"]], "Boulders Start from Entry": [["R.C. Car"], ["Dash Hoop"]], "Boulders End from Entry": [["*Air Crawl"]]}), 

        #Booby Traps
        RoomEntrance(name = "Booby Traps from Entry", value = 0x32, connection_requirements = {"Moving Platforms #1 from Booby Traps": [["Water Net", "R.C. Car", "*Gear", "*Pyramid Sarcophagus"], ["Water Net", "*Air Crawl", "*Gear", "*Pyramid Sarcophagus"]], "Entry from Booby Traps": [[]]}), 
        RoomEntrance(name = "Booby Traps from Moving Platforms #1", connection_requirements = {"Moving Platforms #1 from Booby Traps": [[]], "Entry from Booby Traps": [["*Gear", "*Air Crawl"]]}), 

        #Moving Platforms #1
        RoomEntrance(name = "Moving Platforms #1 from Booby Traps", value = 0x33, connection_requirements = {"Booby Traps from Moving Platforms #1": [[]], "Moving Platforms #2 from Moving Platforms #1": [["R.C. Car"], ["Water Cannon"], ["*Air Crawl"]]}), 
        RoomEntrance(name = "Moving Platforms #1 from Moving Platforms #2", connection_requirements = {"Booby Traps from Moving Platforms #1": [["R.C. Car"], ["Water Cannon"], ["*Air Crawl"]], "Moving Platforms #2 from Moving Platforms #1": [[]]}), 

        #Moving Platforms #2
        RoomEntrance(name = "Moving Platforms #2 from Moving Platforms #1", value = 0x35, connection_requirements = {"Entry from Moving Platforms #2": [["Dash Hoop"], ["*Air Crawl"]], "Moving Platforms #1 from Moving Platforms #2": [[]]}), 
        RoomEntrance(name = "Moving Platforms #2 from Entry", connection_requirements = {"Entry from Moving Platforms #2": [[]], "Moving Platforms #1 from Moving Platforms #2": [["Dash Hoop"], ["*Air Crawl"]]}), 

        #Boulders
        RoomEntrance(name = "Boulders Start from Entry", value = 0x34, connection_requirements = {"Entry from Boulders Start": [[]], "Entry from Boulders End": [["R.C. Car"], ["*Air Crawl"]]}),
        RoomEntrance(name = "Boulders End from Entry", connection_requirements = {"Entry from Boulders Start": [[]], "Entry from Boulders End": [[]]})
    ]),

    #White Monkey Battle!
    Level(name = "White Monkey Battle!", is_boss = True, room_entrances = [
        #Entry
        RoomEntrance(name = "Entry from Spawn", value = 0x5D)
    ]),

    #Pirate Isle
    Level(name = "Pirate Isle", target_address = {"PAL": 0xC63A40, "NTSC": 0xC63CC0}, room_entrances = [
        #Entry
        RoomEntrance(name = "Entry from Spawn", value = 0x36, connection_requirements = {"Cave Entrance from Entry": [["Water Cannon"], ["*Damage Boost"]], "Mine from Entry": [["*Air Crawl"]]}), 
        RoomEntrance(name = "Entry from Cave Entrance", connection_requirements = {"Cave Entrance from Entry": [["Water Cannon"], ["*Damage Boost"]], "Mine from Entry": [["*Air Crawl"]]}), 
        RoomEntrance(name = "Entry from Mine", connection_requirements = {"Cave Entrance from Entry": [["Water Cannon"], ["*Damage Boost"]], "Mine from Entry": [[]]}),

        #Cave Entrance
        RoomEntrance(name = "Cave Entrance from Entry", value = 0x37, connection_requirements = {"Entry from Cave Entrance": [[]], "Boat from Cave Entrance": [["*Air Crawl"], ["Stun Club", "*Expert"], ["Water Cannon"], ["Sky Flyer", "*Boost Fly", "*Hard"]]}), 
        RoomEntrance(name = "Cave Entrance from Boat", connection_requirements = {"Entry from Cave Entrance": [[]], "Boat from Cave Entrance": [[]]}),

        #Boat
        RoomEntrance(name = "Boat from Cave Entrance", value = 0x38, connection_requirements = {"Cell from Boat": [["Water Cannon", "Sky Flyer"], ["Sky Flyer", "*Damage Boost"], ["*Air Crawl"], ["Sky Flyer", "*Hard"]], "Treasure from Boat": [[]], "Mine from Boat": [["Water Cannon"], ["*Damage Boost", "*Expert"]], "Cave Entrance from Boat": [[]]}), 
        RoomEntrance(name = "Boat from Cell", connection_requirements = {"Cell from Boat": [["Water Cannon", "Sky Flyer"], ["Sky Flyer", "*Damage Boost"], ["*Air Crawl"], ["Sky Flyer", "*Hard"]], "Treasure from Boat": [[]], "Mine from Boat": [["Water Cannon"], ["*Damage Boost", "*Expert"]], "Cave Entrance from Boat": [[]]}), 
        RoomEntrance(name = "Boat from Treasure", connection_requirements = {"Cell from Boat": [["Water Cannon", "Sky Flyer"], ["Sky Flyer", "*Damage Boost"], ["*Air Crawl"], ["Sky Flyer", "*Hard"]], "Treasure from Boat": [[]], "Mine from Boat": [["Water Cannon"], ["*Damage Boost", "*Expert"]], "Cave Entrance from Boat": [[]]}), 
        RoomEntrance(name = "Boat from Mine", connection_requirements = {"Cell from Boat": [["Water Cannon", "Sky Flyer"], ["Water Cannon", "Sky Flyer", "*Damage Boost"], ["*Air Crawl"]], "Treasure from Boat": [["Water Cannon"], ["*Air Crawl"]], "Mine from Boat": [["Water Cannon"], ["*Air Crawl"]], "Cave Entrance from Boat": [["Water Cannon"], ["*Air Crawl"]]}), 

        #Cell
        RoomEntrance(name = "Cell from Boat", connection_requirements = {"Boat from Cell": [[]]}), 

        #Treasure
        RoomEntrance(name = "Treasure from Boat", value = 0x39, connection_requirements = {"Boat from Treasure": [[]]}), 

        #Mine
        RoomEntrance(name = "Mine from Boat", value = 0x3A, connection_requirements = {"Boat from Mine": [[]], "Entry from Mine": [[]]}), 
        RoomEntrance(name = "Mine from Entry", connection_requirements = {"Boat from Mine": [[]], "Entry from Mine": [[]]})
    ]),

    #Land of the Apes
    Level(name = "Land of the Apes", target_address = {"PAL": 0xC63A70, "NTSC": 0xC63CF0}, room_entrances = [
        #Entry
        RoomEntrance(name = "Entry from Spawn", value = 0x3B, connection_requirements = {"Icicles from Entry": [[]]}),
        RoomEntrance(name = "Entry from Icicles", connection_requirements = {"Icicles from Entry": [[]]}),

        #Icicles
        RoomEntrance(name = "Icicles from Entry", value = 0x3C, connection_requirements = {"Entry from Icicles": [[]], "Spa from Icicles": [[]], "Ski Hill from Icicles": [[]]}),
        RoomEntrance(name = "Icicles from Spa", connection_requirements = {"Entry from Icicles": [[]], "Spa from Icicles": [[]], "Ski Hill from Icicles": [[]]}),
        RoomEntrance(name = "Icicles from Ski Hill", connection_requirements = {"Entry from Icicles": [[]], "Spa from Icicles": [[]], "Ski Hill from Icicles": [[]]}),

        #Spa
        RoomEntrance(name = "Spa from Icicles", value = 0x3D, connection_requirements = {"Icicles from Spa": [[]]}),

        #Ski Hill
        RoomEntrance(name = "Ski Hill from Icicles", value = 0x3E, connection_requirements = {"Icicles from Ski Hill": [[]]})
    ]),

    #The Lost World
    Level(name = "The Lost World", target_address = {"PAL": 0xC63AA0, "NTSC": 0xC63D20}, room_entrances = [
        #Entry
        RoomEntrance(name = "Entry from Spawn", value = 0x3F, connection_requirements = {"Trees from Entry": [["Water Net"], ["*Air Crawl"]], "Pterodactyls from Entry": [[]]}),
        RoomEntrance(name = "Entry from Trees", connection_requirements = {"Trees from Entry": [[]], "Pterodactyls from Entry": [[]]}),
        RoomEntrance(name = "Entry from Pterodactyls", connection_requirements = {"Trees from Entry": [["Water Net"], ["*Air Crawl"]], "Pterodactyls from Entry": [[]]}),

        #Trees
        RoomEntrance(name = "Trees from Entry", value = 0x41, connection_requirements = {"Entry from Trees": [[]], "T-Rex from Trees": [["Water Cannon", "Water Net"], ["Water Cannon", "*Hard"], ["*Air Crawl"]]}),
        RoomEntrance(name = "Trees from T-Rex", connection_requirements = {"Entry from Trees": [["Water Net"], ["*Hard"]], "T-Rex from Trees": [[]]}),

        #T-Rex
        RoomEntrance(name = "T-Rex from Trees", connection_requirements = {"Trees from T-Rex": [[]], "Pterodactyls from T-Rex": [["Water Net"], ["*Hard"]]}),
        RoomEntrance(name = "T-Rex from Pterodactyls", value = 0x42, connection_requirements = {"Trees from T-Rex": [["Water Net"], ["*Hard"]], "Pterodactyls from T-Rex": [[]]}),

        #Pterodactyls
        RoomEntrance(name = "Pterodactyls from T-Rex", connection_requirements = {"T-Rex from Pterodactyls": [[]], "Entry from Pterodactyls": [[]]}),
        RoomEntrance(name = "Pterodactyls from Entry", value = 0x40, connection_requirements = {"T-Rex from Pterodactyls": [[]], "Entry from Pterodactyls": [[]]})
    ]),

    #Red Monkey Battle!
    Level(name = "Red Monkey Battle!", is_boss = True, room_entrances = [
        #Entry
        RoomEntrance(name = "Entry from Spawn", value = 0x5E)
    ]),

    #Skyscraper City
    Level(name = "Skyscraper City", target_address = {"PAL": 0xC63B00, "NTSC": 0xC63D80}, room_entrances = [
        #Entry
        RoomEntrance(name = "Entry from Spawn", value = 0x43, connection_requirements = {"Lobby from Entry": [["Electro Magnet"], ["*Air Crawl"], ["Sky Flyer", "*Hard"]]}),
        RoomEntrance(name = "Entry from Lobby", connection_requirements = {"Lobby from Entry": [[]]}),

        #Lobby
        RoomEntrance(name = "Lobby from Entry", value = 0x44, connection_requirements = {"Sewer from Lobby": [[]], "Entry from Lobby": [[]]}),
        RoomEntrance(name = "Lobby from Sewer", connection_requirements = {"Sewer from Lobby": [[]], "Entry from Lobby": [[]]}),
        RoomEntrance(name = "Lobby from Lobby Corridor", connection_requirements = {"Sewer from Lobby": [[]], "Entry from Lobby": [[]], "Lobby Corridor from Lobby": [[]]}),
        RoomEntrance(name = "Lobby from Final Room", connection_requirements = {"Sewer from Lobby": [[]], "Entry from Lobby": [[]]}),

        #Sewer
        RoomEntrance(name = "Sewer from Lobby", value = 0x45, connection_requirements = {"Lobby from Sewer": [[]], "Lobby Corridor from Sewer": [["R.C. Car", "Electro Magnet"]]}),
        RoomEntrance(name = "Sewer from Lobby Corridor", connection_requirements = {"Lobby Corridor from Sewer": [[]]}),

        #Lobby Corridor
        RoomEntrance(name = "Lobby Corridor from Sewer", connection_requirements = {"Sewer from Lobby Corridor": [[]], "Tank from Lobby Corridor": [[]], "Lobby from Lobby Corridor": [[]]}),
        RoomEntrance(name = "Lobby Corridor from Tank", connection_requirements = {"Sewer from Lobby Corridor": [[]], "Tank from Lobby Corridor": [[]], "Lobby from Lobby Corridor": [[]]}),
        RoomEntrance(name = "Lobby Corridor from Lobby", connection_requirements = {"Sewer from Lobby Corridor": [[]], "Tank from Lobby Corridor": [[]], "Lobby from Lobby Corridor": [[]]}),

        #Tank Room
        RoomEntrance(name = "Tank from Lobby Corridor", value = 0x46, connection_requirements = {"Lobby Corridor from Tank": [[]], "Final Room from Tank": [[]]}),
        RoomEntrance(name = "Tank from Final Room", connection_requirements = {"Lobby Corridor from Tank": [[]], "Final Room from Tank": [[]]}),

        #Final Room
        RoomEntrance(name = "Final Room from Tank", value = 0x47, connection_requirements = {"Tank from Final Room": [[]], "Lobby from Final Room": [["Electro Magnet", "Catapult", "R.C. Car"], ["*Air Crawl"], ["Electro Magnet", "Catapult", "Sky Flyer", "*Boost Jump", "*Expert"]]})
    ]),

    #Code C.H.I.M.P. - continue logic from here
    Level(name = "Code C.H.I.M.P.", target_address = {"PAL": 0xC63B30, "NTSC": 0xC63DB0}, room_entrances = [
        #Entry
        RoomEntrance(name = "Entry from Spawn", value = 0x48, connection_requirements = {"Base Entrance from Entry": [["*Air Crawl"], ["*Gear"]], "Moving Platforms from Entry": [["*Air Crawl"]]}),
        RoomEntrance(name = "Entry from Base Entrance", connection_requirements = {"Base Entrance from Entry": [[]], "Moving Platforms from Entry": [["*Air Crawl"]]}),
        RoomEntrance(name = "Entry from Moving Platforms", connection_requirements = {"Base Entrance from Entry": [["*Air Crawl"], ["*Gear"]], "Moving Platforms from Entry": [[]]}),

        #Base Entrance
        RoomEntrance(name = "Base Entrance from Entry", value = 0x49, connection_requirements = {"Entry from Base Entrance": [[]], "Tank from Base Entrance": [["*Air Crawl"], ["Electro Magnet", "Water Cannon"], ["Electro Magnet", "*Damage Boost"], ["*Boost Fly", "*Expert", "*Damage Boost"], ["*Boost Fly", "*Expert", "Water Cannon"]]}),
        RoomEntrance(name = "Base Entrance from Tank", connection_requirements = {"Entry from Base Entrance": [[]], "Tank from Base Entrance": [[]]}),

        #Tank
        RoomEntrance(name = "Tank from Base Entrance", value = 0x4A, connection_requirements = {"Treadmills from Tank": [[]], "Base Entrance from Tank": [[]]}),
        RoomEntrance(name = "Tank from Treadmills", connection_requirements = {"Treadmills from Tank": [[]], "Base Entrance from Tank": [[]]}),

        #Treadmills
        RoomEntrance(name = "Treadmills from Tank", value = 0x4B, connection_requirements = {"Moving Platforms from Treadmills": [["Electro Magnet"], ["Sky Flyer", "*Boost Fly", "*Expert"], ["*Air Crawl", "*Hard"]], "Tank from Treadmills": [[]]}),
        RoomEntrance(name = "Treadmills from Moving Platforms", connection_requirements = {"Moving Platforms from Treadmills": [[]]}),

        #Moving Platforms
        RoomEntrance(name = "Moving Platforms from Treadmills", value = 0x4C, connection_requirements = {"Treadmills from Moving Platforms": [[]], "Magnetic Panels Start from Moving Platforms": [[]]}),
        RoomEntrance(name = "Moving Platforms from Magnetic Panels Start", connection_requirements = {"Treadmills from Moving Platforms": [[]], "Magnetic Panels Start from Moving Platforms": [[]]}),
        RoomEntrance(name = "Moving Platforms from Magnetic Panels End", connection_requirements = {"Treadmills from Moving Platforms": [["*Attack"], ["*Hard"]], "Magnetic Panels Start from Moving Platforms": [["*Attack"], ["*Hard"]], "Magnetic Panels End from Moving Platforms": [[]], "Entry from Moving Platforms": [["*Attack"], ["*Hard"]]}),
        RoomEntrance(name = "Moving Platforms from Entry", connection_requirements = {"Treadmills from Moving Platforms": [[]], "Magnetic Panels Start from Moving Platforms": [[]], "Entry from Moving Platforms": [[]]}),

        #Magnetic Panels
        RoomEntrance(name = "Magnetic Panels Start from Moving Platforms", value = 0x4D, connection_requirements = {"Moving Platforms from Magnetic Panels End": [["Electro Magnet", "Sky Flyer"], ["Electro Magnet", "*Hard", "Pipotchi"], ["*Boost Fly", "*Hard", "Power Punch"]], "Moving Platforms from Magnetic Panels Start": [[]]}),
        RoomEntrance(name = "Magnetic Panels End from Moving Platforms", connection_requirements = {"Moving Platforms from Magnetic Panels End": [[]], "Moving Platforms from Magnetic Panels Start": [["Electro Magnet", "Sky Flyer"], ["Electro Magnet", "*Hard", "Pipotchi"], ["*Boost Fly", "*Hard"]]})
    ]),

    #Giant Yellow Monkey Battle!
    Level(name = "Giant Yellow Monkey Battle!", target_address = {"PAL": 0xC63B60, "NTSC": 0xC63DE0}, is_boss = True, room_entrances = [
        #Entry
        RoomEntrance(name = "Entry from Spawn", value = 0x5F)
    ]),

    #Moon Base
    Level(name = "Moon Base", target_address = {"PAL": 0xC63BB0, "NTSC": 0xC63E30}, room_entrances = [
        #Entry
        RoomEntrance(name = "Entry from Spawn", value = 0x4E, connection_requirements = {"Wheel from Entry": [[]], "UFO Arena from Entry": [[]], "Armoured Monkey Arena from Entry": [["*Air Crawl"]], "Robot from Entry": [["*Air Crawl"]], "Moving Platforms from Entry": [["*Air Crawl"]], "Mech Arena from Entry": [["*Air Crawl"]], "Inside Climb from Entry": [["*Air Crawl"]], "Bomb from Entry": [["*Air Crawl"]]}),
        RoomEntrance(name = "Entry from Wheel", connection_requirements = {"Wheel from Entry": [[]], "UFO Arena from Entry": [[]], "Armoured Monkey Arena from Entry": [["*Air Crawl"]], "Robot from Entry": [["*Air Crawl"]], "Moving Platforms from Entry": [["*Air Crawl"]], "Mech Arena from Entry": [["*Air Crawl"]], "Inside Climb from Entry": [["*Air Crawl"]], "Bomb from Entry": [["*Air Crawl"]]}),
        RoomEntrance(name = "Entry from UFO Arena", connection_requirements = {"Wheel from Entry": [[]], "UFO Arena from Entry": [[]], "Armoured Monkey Arena from Entry": [["*Air Crawl"]], "Robot from Entry": [["*Air Crawl"]], "Moving Platforms from Entry": [["*Air Crawl"]], "Mech Arena from Entry": [["*Air Crawl"]], "Inside Climb from Entry": [["*Air Crawl"]], "Bomb from Entry": [["*Air Crawl"]]}),

        RoomEntrance(name = "Entry from Armoured Monkey Arena", connection_requirements = {"Wheel from Entry": [["*Air Crawl"]], "UFO Arena from Entry": [["*Air Crawl"]], "Armoured Monkey Arena from Entry": [[]], "Robot from Entry": [[]], "Moving Platforms from Entry": [[]], "Mech Arena from Entry": [["*Air Crawl"]], "Inside Climb from Entry": [["*Air Crawl"]], "Bomb from Entry": [["*Air Crawl"]]}),
        RoomEntrance(name = "Entry from Robot", connection_requirements = {"Wheel from Entry": [["*Air Crawl"]], "UFO Arena from Entry": [["*Air Crawl"]], "Armoured Monkey Arena from Entry": [[]], "Robot from Entry": [[]], "Moving Platforms from Entry": [[]], "Mech Arena from Entry": [["*Air Crawl"]], "Inside Climb from Entry": [["*Air Crawl"]], "Bomb from Entry": [["*Air Crawl"]]}),
        RoomEntrance(name = "Entry from Moving Platforms", connection_requirements = {"Wheel from Entry": [["*Air Crawl"]], "UFO Arena from Entry": [["*Air Crawl"]], "Armoured Monkey Arena from Entry": [[]], "Robot from Entry": [[]], "Moving Platforms from Entry": [[]], "Mech Arena from Entry": [["*Air Crawl"]], "Inside Climb from Entry": [["*Air Crawl"]], "Bomb from Entry": [["*Air Crawl"]]}),

        RoomEntrance(name = "Entry from Mech Arena", connection_requirements = {"Wheel from Entry": [["*Air Crawl"]], "UFO Arena from Entry": [["*Air Crawl"]], "Armoured Monkey Arena from Entry": [["*Air Crawl"]], "Robot from Entry": [["*Air Crawl"]], "Moving Platforms from Entry": [["*Air Crawl"]], "Mech Arena from Entry": [[]], "Inside Climb from Entry": [[]], "Bomb from Entry": [["*Air Crawl"]]}),
        RoomEntrance(name = "Entry from Inside Climb", connection_requirements = {"Wheel from Entry": [["*Air Crawl"]], "UFO Arena from Entry": [["*Air Crawl"]], "Armoured Monkey Arena from Entry": [["*Air Crawl"]], "Robot from Entry": [["*Air Crawl"]], "Moving Platforms from Entry": [["*Air Crawl"]], "Mech Arena from Entry": [[]], "Inside Climb from Entry": [[]], "Bomb from Entry": [["*Air Crawl"]]}),

        RoomEntrance(name = "Entry from Bomb", connection_requirements = {"Wheel from Entry": [[]], "UFO Arena from Entry": [[]], "Armoured Monkey Arena from Entry": [["*Air Crawl"]], "Robot from Entry": [["*Air Crawl"]], "Moving Platforms from Entry": [["*Air Crawl"]], "Mech Arena from Entry": [["*Air Crawl"]], "Inside Climb from Entry": [["*Air Crawl"]], "Bomb from Entry": [[]]}),

        #Wheel
        RoomEntrance(name = "Wheel from Entry", value = 0x4F, connection_requirements = {"Entry from Wheel": [[]]}),

        #UFO Arena
        RoomEntrance(name = "UFO Arena from Entry", value = 0x52, connection_requirements = {"Entry from UFO Arena": [[]], "Rotating Magnets from UFO Arena": [[]]}),
        RoomEntrance(name = "UFO Arena from Rotating Magnets", connection_requirements = {"Entry from UFO Arena": [[]], "Rotating Magnets from UFO Arena": [[]]}),

        #Rotating Magnets
        RoomEntrance(name = "Rotating Magnets from UFO Arena", value = 0x51, connection_requirements = {"UFO Arena from Rotating Magnets": [[]], "Armoured Monkey Arena from Rotating Magnets": [["Electro Magnet", "Sky Flyer"], ["Electro Magnet", "*Hard"], ["*Air Crawl"]]}),
        RoomEntrance(name = "Rotating Magnets from Armoured Monkey Arena", connection_requirements = {"UFO Arena from Rotating Magnets": [["Electro Magnet", "Sky Flyer"], ["Electro Magnet", "*Hard"], ["*Air Crawl"]], "Armoured Monkey Arena from Rotating Magnets": [[]]}),

        #Arena
        RoomEntrance(name = "Armoured Monkey Arena from Rotating Magnets", connection_requirements = {"Rotating Magnets from Armoured Monkey Arena": [[]], "Entry from Armoured Monkey Arena": [[]]}),
        RoomEntrance(name = "Armoured Monkey Arena from Entry", value = 0x53, connection_requirements = {"Rotating Magnets from Armoured Monkey Arena": [[]], "Entry from Armoured Monkey Arena": [[]]}),

        #Robot
        RoomEntrance(name = "Robot from Entry", value = 0x50, connection_requirements = {"Entry from Robot": [[]]}),

        #Moving Platforms
        RoomEntrance(name = "Moving Platforms from Entry", value = 0x54, connection_requirements = {"Entry from Moving Platforms": [[]], "Magnetic Panels from Moving Platforms": [["Electro Magnet", "*Moon Fire"], ["*Moon Fire", "*Boost Fly", "*Expert", "Power Punch"], ["*Air Crawl", "Power Punch"]]}),
        RoomEntrance(name = "Moving Platforms from Magnetic Panels", connection_requirements = {"Entry from Moving Platforms": [["Electro Magnet", "Water Cannon"], ["Electro Magnet", "*Damage Boost"]], "Magnetic Panels from Moving Platforms": [[]]}),
        
        #Magnetic Panels
        RoomEntrance(name = "Magnetic Panels from Moving Platforms", value = 0x55, connection_requirements = {"Moving Platforms from Magnetic Panels": [[]], "Mech Arena from Magnetic Panels": [["Electro Magnet"], ["*Boost Fly", "*Expert"], ["*Air Crawl"]]}),
        RoomEntrance(name = "Magnetic Panels from Mech Arena", connection_requirements = {"Moving Platforms from Magnetic Panels": [["Electro Magnet"], ["*Boost Fly", "*Expert"], ["*Air Crawl"]], "Mech Arena from Magnetic Panels": [[]]}),

        #Mech Arena
        RoomEntrance(name = "Mech Arena from Magnetic Panels", value = 0x56, connection_requirements = {"Magnetic Panels from Mech Arena": [[]], "Entry from Mech Arena": [[]]}),
        RoomEntrance(name = "Mech Arena from Entry", connection_requirements = {"Magnetic Panels from Mech Arena": [[]], "Entry from Mech Arena": [[]]}),

        #Inside Climb
        RoomEntrance(name = "Inside Climb from Entry", value = 0x57, connection_requirements = {"Outside Climb Start from Inside Climb": [["R.C. Car", "Sky Flyer", "Catapult", "Electro Magnet", "*Attack"], ["*Boost Fly", "*Expert"], ["Sky Flyer", "Electro Magnet", "*Hard"], ["*Air Crawl"]], "Outside Climb End from Inside Climb": [["*Air Crawl"]], "Entry from Inside Climb": [[]], "Bomb from Inside Climb": [["*Air Crawl"]]}),
        RoomEntrance(name = "Inside Climb from Outside Climb Start", connection_requirements = {"Outside Climb Start from Inside Climb": [[]], "Outside Climb End from Inside Climb": [["*Air Crawl"]], "Entry from Inside Climb": [[]], "Bomb from Inside Climb": [["*Air Crawl"]]}),
        RoomEntrance(name = "Inside Climb from Outside Climb End", connection_requirements = {"Outside Climb Start from Inside Climb": [[]], "Outside Climb End from Inside Climb": [[]], "Entry from Inside Climb": [[]], "Bomb from Inside Climb": [[]]}),
        RoomEntrance(name = "Inside Climb from Bomb", connection_requirements = {"Outside Climb Start from Inside Climb": [[]], "Outside Climb End from Inside Climb": [[]], "Entry from Inside Climb": [[]], "Bomb from Inside Climb": [[]]}),

        #Outside Climb
        RoomEntrance(name = "Outside Climb Start from Inside Climb", value = 0x58, connection_requirements = {"Inside Climb from Outside Climb End": [[]], "Inside Climb from Outside Climb Start": [[]]}),
        RoomEntrance(name = "Outside Climb End from Inside Climb", connection_requirements = {"Inside Climb from Outside Climb End": [[]], "Inside Climb from Outside Climb Start": [[]]}),

        #Bomb
        RoomEntrance(name = "Bomb from Entry", connection_requirements = {"Entry from Bomb": [["Electro Magnet"], ["*Air Crawl", "Sky Flyer", "*Expert"], ["Power Punch", "*Hard"]], "Inside Climb from Bomb": [[]]}),
        RoomEntrance(name = "Bomb from Inside Climb", connection_requirements = {"Entry from Bomb": [["Electro Magnet"], ["*Air Crawl", "Sky Flyer", "*Expert"], ["Power Punch", "*Hard"]], "Inside Climb from Bomb": [[]]})
    ]),

    #Showdown with Specter!
    Level(name = "Showdown with Specter!", is_boss = True, room_entrances = [
        #Entry
        RoomEntrance(name = "Entry from Spawn", value = 0x60)
    ]),

    #Final Showdown with Specter!
    Level(name = "Final Showdown with Specter!", is_boss = True, keep_at_end = True, room_entrances = [
        #Entry
        RoomEntrance(name = "Entry from Spawn", value = 0x61)
    ])
]

level_from_name: dict[str, Level] = {level.name: level for level in levels}

for monkey in monkeys:
    level_from_name[monkey.level].monkeys.append(monkey)
