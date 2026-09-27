from dataclasses import dataclass, field
from .Monkeys import monkeys, Monkey    
from .Phones import phones, Phone

@dataclass
class RoomEntrance:
    name: str
    connection_requirements: dict[str, list[str]] = field(default_factory = dict)
    source_room: int = -1
    target_room: int = -1
    dest_room: str = ""
    dest_spawn: str = ""
    trigger_pos: list = field(default_factory = list)
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
        RoomEntrance(name = "Entry from Indoors", dest_room = "VEN_A", dest_spawn = "spawn_a_1", source_room = 0xD, target_room = 0xC, connection_requirements = {"Indoors from Entry": [["Water Net"]]}), 

        #Indoors
        RoomEntrance(name = "Indoors from Entry", dest_room = "VEN_A1", dest_spawn = "spawn_a1_1", source_room = 0xC, target_room = 0xD, connection_requirements = {"Entry from Indoors": [["Water Net"]]})
    ]),

    #Viva Apespania
    Level(name = "Viva Apespania", target_address = {"PAL": 0xC63770, "NTSC": 0xC639F0}, room_entrances = [
        #Entry
        RoomEntrance(name = "Entry from Spawn", can_start = True, target_room = 0xE, connection_requirements = {"Village from Entry": [[]]}), 
        RoomEntrance(name = "Entry from Village", trigger_pos = [0xc3c4f36a, 0x40a00f6c, 0xbf8535d5], dest_room = "SPA_A", dest_spawn = "spawn_a_1", source_room = 0xF, target_room = 0xE, connection_requirements = {"Village from Entry": [[]]}), 

        #Village
        RoomEntrance(name = "Village from Entry", trigger_pos = [0x43ad0e48, 0xc03fe3ec, 0xbf4638df], dest_room = "SPA_B", dest_spawn = "spawn_b_1", can_start = True, source_room = 0xE, target_room = 0xF, connection_requirements = {"Entry from Village": [[]], "Bullring from Village": [[]]}),
        RoomEntrance(name = "Village from Bullring", trigger_pos = [0xc0ac2b59, 0x4304037b, 0x441bd7c1], dest_room = "SPA_B", dest_spawn = "spawn_b_2", source_room = 0x10, target_room = 0xF, connection_requirements = {"Entry from Village": [[]], "Bullring from Village": [[]]}),

        #Bullring
        RoomEntrance(name = "Bullring from Village", trigger_pos = [0x40ac1d53, 0x42700200, 0xc3d2ffd5], dest_room = "SPA_C", dest_spawn = "spawn_c_1", can_start = True, source_room = 0xF, target_room = 0x10, connection_requirements = {"Village from Bullring": [[]]})
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
        RoomEntrance(name = "Entry from House", trigger_pos = [0x43a65bac, 0x42d3f322, 0x43dd11e6], dest_room = "MON_A", dest_spawn = "spawn_a_1", source_room = 0x15, target_room = 0x14, connection_requirements = {"House from Entry": [[]]}),

        #House
        RoomEntrance(name = "House from Entry", trigger_pos = [0x43a9c72d, 0x42d2ffb4, 0x4416de4f], dest_room = "MON_B", dest_spawn = "spawn_b_1", can_start = True, target_room = 0x15, connection_requirements = {"Entry from House": [[]], "Dungeon from House": [[]]}),
        RoomEntrance(name = "House from Dungeon", trigger_pos = [0xc1c6f63a, 0x42bfbc42, 0x424314d9], dest_room = "MON_B", dest_spawn = "spawn_b_2", source_room = 0x16, target_room = 0x15, connection_requirements = {"Entry from House": [[]], "Dungeon from House": [[]]}),

        #Dungeon
        RoomEntrance(name = "Dungeon from House", trigger_pos = [0xc2ee1c4a, 0x430c8dc7, 0x426aef4e], dest_room = "MON_C", dest_spawn = "spawn_c_1", can_start = True, source_room = 0x15, target_room = 0x16, connection_requirements = {"House from Dungeon": [[]]})
    ]),

    #Vita-Z Factory
    Level(name = "Vita-Z Factory", target_address = {"PAL": 0xC63800, "NTSC": 0xC63A80}, room_entrances = [
        #Entry
        RoomEntrance(name = "Entry from Spawn", can_start = True, target_room = 0x17, connection_requirements = {"Tunnel from Entry": [["Sky Flyer"], ["*Gear"], ["*Air Crawl"]], "Arena from Entry": [["Power Punch"], ["*Air Crawl", "*Hard"]]}),
        RoomEntrance(name = "Entry from Tunnel", trigger_pos = [0xc29aa101, 0x41d11b5e, 0x43ba0a7c], dest_room = "FAC_A", dest_spawn = "spawn_a_1", source_room = 0x18, target_room = 0x17, connection_requirements = {"Tunnel from Entry": [["Sky Flyer"], ["*Gear"], ["*Air Crawl"]], "Arena from Entry": [["Power Punch"], ["*Air Crawl", "*Hard"]]}),
        RoomEntrance(name = "Entry from Arena", trigger_pos = [0xc3834e72, 0x41ea0405, 0xbeb7742e], dest_room = "FAC_A", dest_spawn = "spawn_a_2", source_room = 0x19, target_room = 0x17, connection_requirements = {"Tunnel from Entry": [["Sky Flyer"], ["*Gear"], ["*Air Crawl"]], "Arena from Entry": [[]]}),
        
        #Tunnel
        RoomEntrance(name = "Tunnel from Entry", trigger_pos = [0x43d834a8, 0x42ce95d6, 0x42fd60a1], dest_room = "FAC_B", dest_spawn = "spawn_b_1", can_start = True, source_room = 0x17, target_room = 0x18, connection_requirements = {"Entry from Tunnel": [[]], "Arena from Tunnel": [[]]}),
        RoomEntrance(name = "Tunnel from Arena", trigger_pos = [0x436ef6b7, 0x41ea0405, 0xc083ac60], dest_room = "FAC_B", dest_spawn = "spawn_b_2", source_room = 0x19, target_room = 0x18, connection_requirements = {"Entry from Tunnel": [[]], "Arena from Tunnel": [[]]}),

        #Arena
        RoomEntrance(name = "Arena from Tunnel", trigger_pos = [0x437803ba, 0x41500802, 0x439b2d91], dest_room = "FAC_C", dest_spawn = "spawn_c_1", can_start = True, source_room = 0x18, target_room = 0x19, connection_requirements = {"Tunnel from Arena": [[]], "Entry from Arena": [[]]}),
        RoomEntrance(name = "Arena from Entry", trigger_pos = [0xc2d2961b, 0x41d212eb, 0x440cfa38], dest_room = "FAC_C", dest_spawn = "spawn_c_2", source_room = 0x17, target_room = 0x19, connection_requirements = {"Tunnel from Arena": [[]], "Entry from Arena": [[]]})
    ]),

    #Casino City
    Level(name = "Casino City", target_address = {"PAL": 0xC63830, "NTSC": 0xC63AB0}, room_entrances = [
        #Entry
        RoomEntrance(name = "Entry from Spawn", can_start = True, target_room = 0x1A, connection_requirements = {"Bar from Entry": [["*Attack"], ["Catapult"], ["*Hard"]], "Circus from Entry": [["Catapult"], ["Stun Club", "*Hard"], ["Power Punch", "*Hard"], ["Sky Flyer", "*Hard"], ["*Expert", "Pipotchi"]]}),
        RoomEntrance(name = "Entry from Circus", trigger_pos = [0xc3006f36, 0x41000802, 0x439549e9], dest_room = "AME_A", dest_spawn = "spawn_a_2", source_room = 0x1C, target_room = 0x1A, connection_requirements = {"Bar from Entry": [["*Attack"], ["Catapult"], ["*Hard"]], "Circus from Entry": [[]]}),
        RoomEntrance(name = "Entry from Bar", trigger_pos = [0x3f9a2615, 0x40d01004, 0x42798e53], dest_room = "AME_A", dest_spawn = "spawn_a_1", source_room = 0x1B, target_room = 0x1A, connection_requirements = {"Bar from Entry": [[]], "Circus from Entry": [["Catapult"]]}),

        #Bar
        RoomEntrance(name = "Bar from Entry", trigger_pos = [0xc337b3da, 0x42200200, 0xc4452769], dest_room = "AME_B", dest_spawn = "spawn_b_1", can_start = True, source_room = 0x1A, target_room = 0x1B, connection_requirements = {"Entry from Bar": [[]]}),

        #Circus
        RoomEntrance(name = "Circus from Entry", trigger_pos = [0x4395b7c8, 0x42a00100, 0xc43082a8], dest_room = "AME_C", dest_spawn = "spawn_c_1", can_start = True, source_room = 0x1A, target_room = 0x1C, connection_requirements = {"Entry from Circus": [[]]})
    ]),   
    
    #Ninja Hideout
    Level(name = "Ninja Hideout", target_address = {"PAL": 0xC63860, "NTSC": 0xC63AE0}, room_entrances = [
        #Entry
        RoomEntrance(name = "Entry from Spawn", can_start = True, target_room = 0x11, connection_requirements = {"Second Room from Entry": [["Water Net", "R.C. Car", "*Hard"], ["Water Net", "R.C. Car", "*Attack"], ["*Air Crawl"], ["R.C. Car", "*Boost Fly", "*Expert"]]}),
        RoomEntrance(name = "Entry from Second Room", trigger_pos = [0x41921a23, 0x42dc00ff, 0x440dc820], dest_room = "JAP_A", dest_spawn = "spawn_a_1", source_room = 0x12, target_room = 0x11, connection_requirements = {"Second Room from Entry": [["Water Net", "R.C. Car", "*Hard"], ["Water Net", "R.C. Car", "*Attack"], ["*Air Crawl"], ["R.C. Car", "*Boost Fly", "*Expert"]]}),

        #Second Room
        RoomEntrance(name = "Second Room from Entry", trigger_pos = [0xc2044c47, 0x4243f917, 0xc2592130], dest_room = "JAP_B", dest_spawn = "spawn_b_1", source_room = 0x11, target_room = 0x12, connection_requirements = {"Entry from Second Room": [[]], "Third Room Start from Second Room": [["R.C. Car"], ["Sky Flyer", "*Hard"], ["*Air Crawl"], ["Dash Hoop", "*Hard", "*Long Jump"]]}), #value = 0x12
        RoomEntrance(name = "Second Room from Third Room Start", trigger_pos = [0x41b29dd7, 0x437c8083, 0xc0065e58], dest_room = "JAP_B", dest_spawn = "spawn_b_3", source_room = 0x13, target_room = 0x12, connection_requirements = {"Entry from Second Room": [[]], "Third Room Start from Second Room": [[]]}),
        RoomEntrance(name = "Second Room from Third Room End", trigger_pos = [0xc49fa290, 0x4388803c, 0xc083e4d9], dest_room = "JAP_B", dest_spawn = "spawn_b_2", source_room = 0x13, target_room = 0x12, connection_requirements = {"Entry from Second Room": [[]], "Third Room Start from Second Room": [["R.C. Car"], ["Sky Flyer", "*Hard"], ["*Air Crawl"], ["Dash Hoop", "*Hard", "*Long Jump"]]}),

        #Third Room
        RoomEntrance(name = "Third Room Start from Second Room", trigger_pos = [0xc40bbdaf, 0x43174a55, 0x43152a4a], dest_room = "JAP_C", dest_spawn = "spawn_c_1", source_room = 0x12, target_room = 0x13, connection_requirements = {"Second Room from Third Room End": [[]], "Second Room from Third Room Start": [[]]}), #value = 0x13
        RoomEntrance(name = "Third Room End from Second Room", trigger_pos = [0x4445dfd1, 0x435a21a0, 0xc4234558], dest_room = "JAP_C", dest_spawn = "spawn_c_2", source_room = 0x12, target_room = 0x13, connection_requirements = {"Second Room from Third Room End": [[]], "Second Room from Third Room Start": [[]]}),
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
        RoomEntrance(name = "Entry from Christmas Tree", trigger_pos = [0xc1209b47, 0x4379dbf1, 0x44263ca3], dest_room = "WIN_A", dest_spawn = "spawn_a_1", source_room = 0x26, target_room = 0x25, connection_requirements = {"Christmas Tree from Entry": [[]], "Ski Hill from Entry": [["*Air Crawl", "*Hard"], ["Sky Flyer", "*Hard"]]}),
        RoomEntrance(name = "Entry from Ski Hill", trigger_pos = [0xc332b13e, 0x42b788e3, 0xc482be0b], dest_room = "WIN_A", dest_spawn = "spawn_a_2", source_room = 0x27, target_room = 0x25, connection_requirements = {"Christmas Tree from Entry": [[]], "Ski Hill from Entry": [[]]}),

        #Christmas Tree
        RoomEntrance(name = "Christmas Tree from Entry", trigger_pos = [0xc420f4f0, 0x42a10713, 0xc3b1ee6a], dest_room = "WIN_B", dest_spawn = "spawn_b_1", can_start = True, source_room = 0x25, target_room = 0x26, connection_requirements = {"Entry from Christmas Tree": [[]], "Ski Hill from Christmas Tree": [["*Air Crawl"], ["Dash Hoop"], ["*Hard"]]}),
        RoomEntrance(name = "Christmas Tree from Ski Hill", trigger_pos = [0x4494bbc5, 0x428bf1fc, 0xc43c10f3], dest_room = "WIN_B", dest_spawn = "spawn_b_2", source_room = 0x27, target_room = 0x26, connection_requirements = {"Entry from Christmas Tree": [[]], "Ski Hill from Christmas Tree": [[]]}),

        #Ski Hill
        RoomEntrance(name = "Ski Hill from Entry", trigger_pos = [0x439c9d9b, 0x4339b15b, 0xc37ee8e7], dest_room = "WIN_C", dest_spawn = "spawn_c_2", can_start = True, source_room = 0x25, target_room = 0x27, connection_requirements = {"Entry from Ski Hill": [[]], "Christmas Tree from Ski Hill": [[]]}),
        RoomEntrance(name = "Ski Hill from Christmas Tree", trigger_pos = [0x43ce224d, 0x43d17cf2, 0xc3c32d41], dest_room = "WIN_C", dest_spawn = "spawn_c_1", source_room = 0x26, target_room = 0x27, connection_requirements = {"Entry from Ski Hill": [[]], "Christmas Tree from Ski Hill": [[]]})
    ]),

    #Lookout Valley
    Level(name = "Lookout Valley", target_address = {"PAL": 0xC638F0, "NTSC": 0xC63B70}, room_entrances = [
        #Entry
        RoomEntrance(name = "Entry from Spawn", dest_room = "HIK_A", can_start = True, target_room = 0x22, connection_requirements = {"Cave Start from Entry": [["*Valley Gap", "*Valley Island", "*Valley Boat"]], "Cave End from Entry": [["*Boost Fly", "*Hard"], ["*Air Crawl", "*Hard"]], "Jungle Start from Entry": [["*Valley Gap", "*Valley Island"]], "Jungle End from Entry": [["*Air Crawl", "*Hard"]]}),
        RoomEntrance(name = "Entry from Cave End", trigger_pos = [0xc40e5fc7, 0x42020200, 0x43993f1c], dest_room = "HIK_A", dest_spawn = "spawn_a_4", source_room = 0x24, target_room = 0x22, connection_requirements = {"Cave Start from Entry": [["*Valley Boat"]], "Cave End from Entry": [[]], "Jungle Start from Entry": [["*Valley Island"]], "Jungle End from Entry": [["*Air Crawl", "*Hard"]]}),
        RoomEntrance(name = "Entry from Cave Start", trigger_pos = [0xc356ede4, 0xc276fdff, 0xc3fb8282], dest_room = "HIK_A", dest_spawn = "spawn_a_3", source_room = 0x24, target_room = 0x22, connection_requirements = {"Cave Start from Entry": [[]], "Cave End from Entry": [["*Boost Fly", "*Hard"], ["*Air Crawl", "*Hard"]], "Jungle Start from Entry": [["*Valley Island"]], "Jungle End from Entry": [["*Air Crawl", "*Hard"]]}),
        RoomEntrance(name = "Entry from Jungle Start", trigger_pos = [0x444bcf5f, 0x3b002000, 0xc2f65e14], dest_room = "HIK_A", dest_spawn = "spawn_a_2", source_room = 0x23, target_room = 0x22, connection_requirements = {"Cave Start from Entry": [["*Valley Island", "*Valley Boat"]], "Cave End from Entry": [["*Boost Fly", "*Hard"], ["*Air Crawl", "*Hard"]], "Jungle Start from Entry": [[]], "Jungle End from Entry": [["*Air Crawl", "*Hard"]]}),
        RoomEntrance(name = "Entry from Jungle End", trigger_pos = [0xc455c566, 0x4308c1b4, 0xc3801599], dest_room = "HIK_A", dest_spawn = "spawn_a_1", source_room = 0x23, target_room = 0x22, connection_requirements = {"Cave Start from Entry": [["*Valley Island", "*Valley Boat"]], "Cave End from Entry": [["*Boost Fly", "*Hard"], ["*Air Crawl", "*Hard"]], "Jungle Start from Entry": [[]], "Jungle End from Entry": [[]]}),

        #Jungle
        RoomEntrance(name = "Jungle Start from Entry", trigger_pos = [0x433ed49a, 0x43532875, 0xc4339dc4], dest_room = "HIK_B", dest_spawn = "spawn_b_1", can_start = True, source_room = 0x22, target_room = 0x23, connection_requirements = {"Entry from Jungle Start": [[]], "Entry from Jungle End": [[]]}),
        RoomEntrance(name = "Jungle End from Entry", trigger_pos = [0xc400b5a9, 0x4383a040, 0xc42d2c38], dest_room = "HIK_B", dest_spawn = "spawn_b_2", source_room = 0x22, target_room = 0x23,connection_requirements = {"Entry from Jungle Start": [[]], "Entry from Jungle End": [[]]}),

        #Cave
        RoomEntrance(name = "Cave Start from Entry", trigger_pos = [0x44823b0e, 0x43020080, 0xc386dff8], dest_room = "HIK_C", dest_spawn = "spawn_c_1", can_start = True, source_room = 0x22, target_room = 0x24, connection_requirements = {"Entry from Cave Start": [[]], "Entry from Cave End": [["*Valley Button", "*Valley Stalag", "Water Net"], ["*Valley Button", "*Valley Stalag", "Sky Flyer", "*Hard"], ["*Valley Button", "*Valley Stalag", "*Expert"]]}),
        RoomEntrance(name = "Cave End from Entry", trigger_pos = [0x43e23c3e, 0x4359c55b, 0xc2d2f63a], dest_room = "HIK_C", dest_spawn = "spawn_c_2", source_room = 0x22, target_room = 0x24, connection_requirements = {"Entry from Cave Start": [["*Air Crawl"], ["Sky Flyer"], ["Water Net"]], "Entry from Cave End": [[]]})
    ]),

    #The Blue Baboon
    Level(name = "The Blue Baboon", target_address = {"PAL": 0xC63920, "NTSC": 0xC63BA0}, room_entrances = [
        #Entry
        RoomEntrance(name = "Entry from Spawn", can_start = True, target_room = 0x1D, connection_requirements = {"Ship from Entry": [[]], "Bananarang Room from Entry": [["Water Net"], ["*Air Crawl"]], "Changing Hut from Entry": [[]]}),
        RoomEntrance(name = "Entry from Ship", trigger_pos = [0x4364b13c, 0xc249d0a2, 0x440e1911], dest_room = "BEA_A", dest_spawn = "spawn_a_1", source_room = 0x21, target_room = 0x1D, connection_requirements = {"Ship from Entry": [[]], "Bananarang Room from Entry": [["Water Net"], ["*Air Crawl"]], "Changing Hut from Entry": [[]]}),
        RoomEntrance(name = "Entry from Bananarang Room", trigger_pos = [0x446b94a2, 0x42c927be, 0x43e33a5c], dest_room = "BEA_A", dest_spawn = "spawn_a_3", source_room = 0x1F, target_room = 0x1D, connection_requirements = {"Ship from Entry": [["Water Net"], ["*Air Crawl"]], "Bananarang Room from Entry": [["Water Net"], ["*Air Crawl"]], "Changing Hut from Entry": [["Water Net"], ["*Air Crawl"]]}),
        RoomEntrance(name = "Entry from Changing Hut", trigger_pos = [0x3f609a89, 0xc0fea6ca, 0x43115d0a], dest_room = "BEA_A", dest_spawn = "spawn_a_2", source_room = 0x1E, target_room = 0x1D, connection_requirements = {"Ship from Entry": [[]], "Bananarang Room from Entry": [["Water Net"], ["*Air Crawl"]], "Changing Hut from Entry": [[]]}),

        #Hut
        RoomEntrance(name = "Changing Hut from Entry", trigger_pos = [0x430480a9, 0x41b90e3b, 0xc2ba323f], dest_room = "BEA_A1", dest_spawn = "spawn_a1_1", can_start = True, source_room = 0x1D, target_room = 0x1E, connection_requirements = {"Entry from Changing Hut": [[]]}),

        #Ship
        RoomEntrance(name = "Ship from Entry", trigger_pos = [0xc38c358f, 0x425be274, 0xc3bd825c], dest_room = "BEA_C", dest_spawn = "spawn_c_1", can_start = True, source_room = 0x1D, target_room = 0x21, connection_requirements = {"Entry from Ship": [[]]}),

        #Bananarang Room
        RoomEntrance(name = "Bananarang Room from Entry", trigger_pos = [0xc3e43fb2, 0x401eaea8, 0x432027a1], dest_room = "BEA_B", dest_spawn = "spawn_b_1", can_start = True, source_room = 0x1D, target_room = 0x1F, connection_requirements = {"Entry from Bananarang Room": [[]]})
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
        RoomEntrance(name = "Entry from Inside Start", trigger_pos = [0xc43bfe1c, 0x43820040, 0x43e0395f], dest_room = "CHI_A", dest_spawn = "spawn_a_1", source_room = 0x29, target_room = 0x28, connection_requirements = {"Inside Start from Entry": [[]], "Wall Start from Entry": [[]]}), 
        RoomEntrance(name = "Entry from Inside End", trigger_pos = [0x44144efd, 0x4336e2a7, 0xc411d825], dest_room = "CHI_A", dest_spawn = "spawn_a_4", source_room = 0x29, target_room = 0x28, connection_requirements = {"Inside Start from Entry": [[]], "Wall Start from Entry": [[]]}), 
        RoomEntrance(name = "Entry from Wall Start", trigger_pos = [0xc31ea5b0, 0x4307f793, 0xc43162e3], dest_room = "CHI_A", dest_spawn = "spawn_a_2", source_room = 0x2A, target_room = 0x28, connection_requirements = {"Inside Start from Entry": [[]], "Wall Start from Entry": [[]]}), 
        RoomEntrance(name = "Entry from Wall End", trigger_pos = [0xc39b6c80, 0x43480080, 0x43efe27f], dest_room = "CHI_A", dest_spawn = "spawn_a_3", source_room = 0x2A, target_room = 0x28, connection_requirements = {"Inside Start from Entry": [[]], "Wall Start from Entry": [[]]}), 

        #Inside
        RoomEntrance(name = "Inside Start from Entry", trigger_pos = [0x3ebd1430, 0x420001fe, 0xc304ec61], dest_room = "CHI_B", dest_spawn = "spawn_b_1", can_start = True, source_room = 0x28, target_room = 0x29, connection_requirements = {"Entry from Inside Start": [[]], "Entry from Inside End": [["*Gear"]]}), 
        RoomEntrance(name = "Inside End from Entry", trigger_pos = [0x43918b76, 0x3b002000, 0x43215722], dest_room = "CHI_B", dest_spawn = "spawn_b_2", source_room = 0x28, target_room = 0x29, connection_requirements = {}), 

        #Wall
        RoomEntrance(name = "Wall Start from Entry", trigger_pos = [0x43cd9c90, 0x42801a9a, 0xc383912f], dest_room = "CHI_C", dest_spawn = "spawn_c_1", can_start = True, source_room = 0x28, target_room = 0x2A, connection_requirements = {"Entry from Wall Start": [[]], "Entry from Wall End": [["R.C. Car"], ["*Air Crawl"], ["*Boost Fly", "*Hard"]]}), 
        RoomEntrance(name = "Wall End from Entry", trigger_pos = [0x4467d1d6, 0x416e52c7, 0xc26174fe], dest_room = "CHI_C", dest_spawn = "spawn_c_2", source_room = 0x28, target_room = 0x2A, connection_requirements = {"Entry from Wall Start": [[]], "Entry from Wall End": [[]]})
    ]),

    #Simian Citadel
    Level(name = "Simian Citadel", target_address = {"PAL": 0xC639B0, "NTSC": 0xC63C30}, room_entrances = [
        #Entry
        RoomEntrance(name = "Entry from Spawn", can_start = True, target_room = 0x2C, connection_requirements = {"Bullring from Entry": [["*Gear", "Water Net"]], "Fountain from Entry": [["*Air Crawl", "*Hard"], ["*Boost Fly", "*Hard"]]}), 
        RoomEntrance(name = "Entry from Bullring", trigger_pos = [0xc1105026, 0x4333031c, 0xc3f9b18b], dest_room = "GRE_A", dest_spawn = "spawn_a_1", source_room = 0x2D, target_room=0x2C, connection_requirements = {"Bullring from Entry": [[]], "Fountain from Entry": [["*Gear", "Water Net", "*Boost Fly", "*Hard"], ["*Gear", "Water Net", "*Air Crawl", "*Hard"]]}), 
        RoomEntrance(name = "Entry from Fountain", trigger_pos = [0xc4170f8b, 0x418003fe, 0xc3e0591a], dest_room = "GRE_A", dest_spawn = "spawn_a_2", source_room = 0x30, target_room=0x2C, connection_requirements = {"Bullring from Entry": [["*Gear", "Water Net"]], "Fountain from Entry": [[]]}), 

        #Bullring
        RoomEntrance(name = "Bullring from Entry", trigger_pos = [0xbfccac1b, 0x4333031b, 0xc416674b], dest_room = "GRE_A1", dest_spawn = "spawn_a1_1", can_start = True, source_room = 0x2C, target_room = 0x2D, connection_requirements = {"Entry from Bullring": [[]], "Whale from Bullring": [["Dash Hoop", "*Bull Fight"], ["*Bull Fight", "*Hard"], ["*Air Crawl", "*Hard"]]}), 
        RoomEntrance(name = "Bullring from Whale", trigger_pos = [0xc3062655, 0xc3227f86, 0xc39755a8], dest_room = "GRE_A1", dest_spawn = "spawn_a1_1", source_room = 0x2E, target_room = 0x2D, connection_requirements = {"Entry from Bullring": [["*Air Crawl"]], "Whale from Bullring": [[]]}), 

        #Whale
        RoomEntrance(name = "Whale from Bullring", trigger_pos = [0xc4a50b0a, 0x4348ccc1, 0xc4e357d0], dest_room = "GRE_B", dest_spawn = "spawn_b_1", can_start = True, source_room = 0x2D, target_room = 0x2E, connection_requirements = {"Submarine from Whale": [["Sky Flyer", "Water Net", "*Attack"], ["Sky Flyer", "*Hard"], ["*Air Crawl"]], "Bullring from Whale": [[]]}), 
        RoomEntrance(name = "Whale from Submarine", trigger_pos = [0xc4568c43, 0x422dd420, 0x449d3cd7], dest_room = "GRE_B", dest_spawn = "spawn_b_2", source_room = 0x2F, target_room = 0x2E, connection_requirements = {}), 

        #Submarine
        RoomEntrance(name = "Submarine from Whale", trigger_pos = [0x41222573, 0xc3477f8c, 0x44157055], dest_room = "GRE_C", dest_spawn = "spawn_c_1", can_start = True, source_room = 0x2E, target_room = 0x2F, connection_requirements = {"Fountain from Submarine": [[]], "Whale from Submarine": [[]]}), 
        RoomEntrance(name = "Submarine from Fountain", trigger_pos = [0x43c6f40d, 0x42700200, 0x440c4efc], dest_room = "GRE_C", dest_spawn = "spawn_c_2", source_room = 0x30, target_room = 0x2F, connection_requirements = {"Fountain from Submarine": [[]], "Whale from Submarine": [[]]}), 

        #Fountain
        RoomEntrance(name = "Fountain from Submarine", trigger_pos = [0x44cd6ac5, 0x432f2cb1, 0x4335c307], dest_room = "GRE_D", dest_spawn = "spawn_d_1", can_start = True, source_room = 0x2F, target_room = 0x30, connection_requirements = {"Submarine from Fountain": [[]], "Entry from Fountain": [[]]}), 
        RoomEntrance(name = "Fountain from Entry", trigger_pos = [0xc421b4f8, 0x426489b2, 0x449cf0a0], dest_room = "GRE_D", dest_spawn = "spawn_d_2", source_room = 0x2C, target_room = 0x30, connection_requirements = {"Submarine from Fountain": [[]], "Entry from Fountain": [[]]})
    ]),

    #Panic Pyramid
    Level(name = "Panic Pyramid", target_address = {"PAL": 0xC639E0, "NTSC": 0xC63C60}, room_entrances = [
        #Entry
        RoomEntrance(name = "Entry from Spawn", can_start = True, target_room = 0x31, connection_requirements = {"Booby Traps from Entry": [[]], "Moving Platforms #2 from Entry": [["*Air Crawl"], ["*Boost Fly", "*Expert"]], "Boulders Start from Entry": [["R.C. Car"], ["Dash Hoop"]], "Boulders End from Entry": [["*Air Crawl"]]}), 
        RoomEntrance(name = "Entry from Booby Traps", trigger_pos = [0x41903524, 0x3b002000, 0xc0694150], dest_room = "EGY_A", dest_spawn = "spawn_a_1", source_room = 0x32, target_room = 0x31, connection_requirements = {"Booby Traps from Entry": [[]], "Moving Platforms #2 from Entry": [["*Air Crawl"], ["*Boost Fly", "*Expert"]], "Boulders Start from Entry": [["R.C. Car"], ["Dash Hoop"]], "Boulders End from Entry": [["*Air Crawl"]]}),
        RoomEntrance(name = "Entry from Moving Platforms #2", trigger_pos = [0x44d57df9, 0xc1cfc4ac, 0xc435b7df], dest_room = "EGY_A", dest_spawn = "spawn_a_2", source_room = 0x35, target_room = 0x31, connection_requirements = {"Booby Traps from Entry": [[]], "Moving Platforms #2 from Entry": [["*Air Crawl"], ["*Boost Fly", "*Expert"]], "Boulders Start from Entry": [["R.C. Car"], ["Dash Hoop"]], "Boulders End from Entry": [["*Air Crawl"]]}), 
        RoomEntrance(name = "Entry from Boulders Start", trigger_pos = [0xc443ae7b, 0x4264e475, 0x43c82af5], dest_room = "EGY_A", dest_spawn = "spawn_a_3", source_room = 0x34, target_room = 0x31, connection_requirements = {"Booby Traps from Entry": [[]], "Moving Platforms #2 from Entry": [["*Air Crawl"], ["*Boost Fly", "*Expert"]], "Boulders Start from Entry": [["R.C. Car"], ["Dash Hoop"]], "Boulders End from Entry": [["*Air Crawl"]]}), 
        RoomEntrance(name = "Entry from Boulders End", trigger_pos = [0xc39ea47d, 0x439cb9a3, 0x441e2e71], dest_room = "EGY_A", dest_spawn = "spawn_a_4", source_room = 0x34, target_room = 0x31, connection_requirements = {"Booby Traps from Entry": [[]], "Moving Platforms #2 from Entry": [["*Air Crawl"], ["*Boost Fly", "*Expert"]], "Boulders Start from Entry": [["R.C. Car"], ["Dash Hoop"]], "Boulders End from Entry": [["*Air Crawl"]]}), 

        #Booby Traps
        RoomEntrance(name = "Booby Traps from Entry", trigger_pos = [0xc3656d28, 0xc2bdfeff, 0x430b979f], dest_room = "EGY_B", dest_spawn = "spawn_b_1", can_start = True, source_room = 0x31, target_room = 0x32, connection_requirements = {"Moving Platforms #1 from Booby Traps": [["Water Net", "R.C. Car", "*Gear", "*Pyramid Sarcophagus"], ["Water Net", "*Air Crawl", "*Gear", "*Pyramid Sarcophagus"]], "Entry from Booby Traps": [[]]}), 
        RoomEntrance(name = "Booby Traps from Moving Platforms #1", trigger_pos = [0xc2d591f6, 0xc281feff, 0x443730c2], dest_room = "EGY_B", dest_spawn = "spawn_b_2", source_room = 0x33, target_room = 0x32, connection_requirements = {"Moving Platforms #1 from Booby Traps": [[]], "Entry from Booby Traps": [["*Gear", "*Air Crawl"], ["*Gear", "*Hard"]]}), 

        #Moving Platforms #1
        RoomEntrance(name = "Moving Platforms #1 from Booby Traps", trigger_pos = [0x4368cfa8, 0x42cfcdc7, 0xc396b54b], dest_room = "EGY_C", dest_spawn = "spawn_c_1", can_start = True, source_room = 0x32, target_room = 0x33, connection_requirements = {"Booby Traps from Moving Platforms #1": [[]], "Moving Platforms #2 from Moving Platforms #1": [["R.C. Car"], ["Water Cannon"], ["*Air Crawl"]]}), 
        RoomEntrance(name = "Moving Platforms #1 from Moving Platforms #2", trigger_pos = [0xc325f994, 0xc21bfa55, 0xc4166e2f], dest_room = "EGY_C", dest_spawn = "spawn_c_1", source_room = 0x35, target_room = 0x33, connection_requirements = {"Booby Traps from Moving Platforms #1": [["R.C. Car"], ["Water Cannon"], ["*Air Crawl"]], "Moving Platforms #2 from Moving Platforms #1": [[]]}), 

        #Moving Platforms #2
        RoomEntrance(name = "Moving Platforms #2 from Moving Platforms #1", trigger_pos = [0xc351323c, 0xc21bfc1d, 0xc413aefd], dest_room = "EGY_E", dest_spawn = "spawn_e_1", can_start = True, source_room = 0x33, target_room = 0x35, connection_requirements = {"Entry from Moving Platforms #2": [["Dash Hoop"], ["*Air Crawl"]], "Moving Platforms #1 from Moving Platforms #2": [[]]}), 
        RoomEntrance(name = "Moving Platforms #2 from Entry", trigger_pos = [0xc395b02f, 0xc0cfeffc, 0x433be9d4], dest_room = "EGY_E", dest_spawn = "spawn_e_2", source_room = 0x31, target_room = 0x35, connection_requirements = {"Entry from Moving Platforms #2": [[]], "Moving Platforms #1 from Moving Platforms #2": [["Dash Hoop"], ["*Air Crawl"]]}), 

        #Boulders
        RoomEntrance(name = "Boulders Start from Entry", trigger_pos = [0x42f731c5, 0xc32fff7d, 0xc3a0f78d], dest_room = "EGY_D", dest_spawn = "spawn_d_1", can_start = True, source_room = 0x31, target_room = 0x34, connection_requirements = {"Entry from Boulders Start": [[]], "Entry from Boulders End": [["R.C. Car"], ["*Air Crawl"]]}),
        RoomEntrance(name = "Boulders End from Entry", trigger_pos = [0x42fd8c4a, 0xc23dfdf7, 0xc3b99399], dest_room = "EGY_D", dest_spawn = "spawn_d_2", source_room = 0x31, target_room = 0x34, connection_requirements = {"Entry from Boulders Start": [[]], "Entry from Boulders End": [[]]})
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
        RoomEntrance(name = "Entry from Cave Entrance", trigger_pos = [0xc0a20841, 0xc2344209, 0xc3807670], dest_room = "OCE_A", dest_spawn = "spawn_a_1", source_room = 0x37, target_room = 0x36, connection_requirements = {"Cave Entrance from Entry": [["Water Cannon"], ["*Damage Boost"]], "Mine from Entry": [["*Air Crawl"]]}), 
        RoomEntrance(name = "Entry from Mine", trigger_pos = [0x431a0ee6, 0xc3021f5c, 0xc425ea57], dest_room = "OCE_A", dest_spawn = "spawn_a_2", source_room = 0x3A, target_room = 0x36, connection_requirements = {"Cave Entrance from Entry": [["Water Cannon"], ["*Damage Boost"]], "Mine from Entry": [[]]}),

        #Cave Entrance
        RoomEntrance(name = "Cave Entrance from Entry", trigger_pos = [0x4446d2ef, 0x41cdc6a8, 0x44511d8a], dest_room = "OCE_B", dest_spawn = "spawn_b_1", can_start = True, source_room = 0x36, target_room = 0x37, connection_requirements = {"Entry from Cave Entrance": [[]], "Boat from Cave Entrance": [["*Air Crawl"], ["Stun Club", "*Expert"], ["Water Cannon"], ["Sky Flyer", "*Boost Fly", "*Hard"]]}), 
        RoomEntrance(name = "Cave Entrance from Boat", trigger_pos = [0x410e5fdf, 0xc1cffbfd, 0xc1a6674a], dest_room = "OCE_B", dest_spawn = "spawn_b_2", source_room = 0x38, target_room = 0x37, connection_requirements = {"Entry from Cave Entrance": [[]], "Boat from Cave Entrance": [[]]}),

        #Boat
        RoomEntrance(name = "Boat from Cave Entrance", trigger_pos = [0xc03e37c5, 0xc335ff7f, 0x44d5e68c], dest_room = "OCE_C", dest_spawn = "spawn_c_1", can_start = True, source_room = 0x37, target_room = 0x38, connection_requirements = {"Cell from Boat": [["Water Cannon", "Sky Flyer"], ["Sky Flyer", "*Damage Boost"], ["*Air Crawl"], ["Sky Flyer", "*Hard"]], "Treasure from Boat": [[]], "Mine from Boat": [["Water Cannon"], ["*Damage Boost", "*Expert"]], "Cave Entrance from Boat": [[]]}), 
        RoomEntrance(name = "Boat from Cell", trigger_pos = [0xc39eb9f0, 0x42d00100, 0xc45bf27c], dest_room = "OCE_C", dest_spawn = "spawn_c_4", source_room = 0x39, target_room = 0x38, connection_requirements = {"Cell from Boat": [["Water Cannon", "Sky Flyer"], ["Sky Flyer", "*Damage Boost"], ["*Air Crawl"], ["Sky Flyer", "*Hard"]], "Treasure from Boat": [[]], "Mine from Boat": [["Water Cannon"], ["*Damage Boost", "*Expert"]], "Cave Entrance from Boat": [[]]}), 
        RoomEntrance(name = "Boat from Treasure", trigger_pos = [0x40d0e952, 0xc1cffbff, 0xc43d9c5d], dest_room = "OCE_C", dest_spawn = "spawn_c_3", source_room = 0x39, target_room = 0x38, connection_requirements = {"Cell from Boat": [["Water Cannon", "Sky Flyer"], ["Sky Flyer", "*Damage Boost"], ["*Air Crawl"], ["Sky Flyer", "*Hard"]], "Treasure from Boat": [[]], "Mine from Boat": [["Water Cannon"], ["*Damage Boost", "*Expert"]], "Cave Entrance from Boat": [[]]}), 
        RoomEntrance(name = "Boat from Mine", trigger_pos = [0x41364fe8, 0xc235ff05, 0xc2c6968b], dest_room = "OCE_C", dest_spawn = "spawn_c_2", source_room = 0x3A, target_room = 0x38, connection_requirements = {"Cell from Boat": [["Water Cannon", "Sky Flyer"], ["Water Cannon", "Sky Flyer", "*Damage Boost"], ["*Air Crawl"]], "Treasure from Boat": [["Water Cannon"], ["*Air Crawl"]], "Mine from Boat": [["Water Cannon"], ["*Air Crawl"]], "Cave Entrance from Boat": [["Water Cannon"], ["*Air Crawl"]]}), 

        #Cell
        RoomEntrance(name = "Cell from Boat", trigger_pos = [0xc39fcca2, 0x42d00100, 0xc459d1c4], dest_room = "OCE_C1", dest_spawn = "spawn_c1_1", source_room = 0x38, target_room = 0x39, connection_requirements = {"Boat from Cell": [[]]}), 

        #Treasure
        RoomEntrance(name = "Treasure from Boat", trigger_pos = [0xb974d664, 0xc1cffbfd, 0xc45dcf79], dest_room = "OCE_c1", dest_spawn = "spawn_c1_2", can_start = True, source_room = 0x38, target_room = 0x39, connection_requirements = {"Boat from Treasure": [[]]}), 

        #Mine
        RoomEntrance(name = "Mine from Boat", trigger_pos = [0x443dfb5a, 0x42fb0100, 0xc2b5e2bd], dest_room = "OCE_D", dest_spawn = "spawn_d_1", can_start = True, source_room = 0x38, target_room = 0x3A, connection_requirements = {"Boat from Mine": [[]], "Entry from Mine": [[]]}), 
        RoomEntrance(name = "Mine from Entry", trigger_pos = [0x4486ee2d, 0x42d0011a, 0x42efc413], dest_room = "OCE_D", dest_spawn = "spawn_d_2", source_room = 0x36, target_room = 0x3A, connection_requirements = {"Boat from Mine": [[]], "Entry from Mine": [[]]})
    ]),

    #Land of the Apes
    Level(name = "Land of the Apes", target_address = {"PAL": 0xC63A70, "NTSC": 0xC63CF0}, room_entrances = [
        #Entry
        RoomEntrance(name = "Entry from Spawn", can_start = True, target_room = 0x3B, connection_requirements = {"Icicles from Entry": [[]]}),
        RoomEntrance(name = "Entry from Icicles", trigger_pos = [0xc0793637, 0x3b002000, 0x42e2aca1], dest_room = "ANT_A", dest_spawn = "spawn_a_1", source_room = 0x3C, target_room = 0x3B, connection_requirements = {"Icicles from Entry": [[]]}),

        #Icicles
        RoomEntrance(name = "Icicles from Entry", trigger_pos = [0x439f8a90, 0xc2508ea9, 0xc4920433], dest_room = "ANT_B", dest_spawn = "spawn_b_1", can_start = True, source_room = 0x3B, target_room = 0x3C, connection_requirements = {"Entry from Icicles": [[]], "Spa from Icicles": [[]], "Ski Hill from Icicles": [[]]}),
        RoomEntrance(name = "Icicles from Spa", trigger_pos = [0xc22c4668, 0x42414156, 0xc2e9a961], dest_room = "ANT_B", dest_spawn = "spawn_b_3", source_room = 0x3D, target_room = 0x3C, connection_requirements = {"Entry from Icicles": [[]], "Spa from Icicles": [[]], "Ski Hill from Icicles": [[]]}),
        RoomEntrance(name = "Icicles from Ski Hill", trigger_pos = [0x42c4127d, 0xc1cffbff, 0xc29a6ef9], dest_room = "ANT_B", dest_spawn = "spawn_b_2", source_room = 0x3E, target_room = 0x3C, connection_requirements = {"Entry from Icicles": [[]], "Spa from Icicles": [[]], "Ski Hill from Icicles": [[]]}),

        #Spa
        RoomEntrance(name = "Spa from Icicles", trigger_pos = [0x442cd22b, 0x42b00100, 0xc2091f91], dest_room = "ANT_C", dest_spawn = "spawn_c_1", can_start = True, source_room = 0x3C, target_room = 0x3D, connection_requirements = {"Icicles from Spa": [[]]}),

        #Ski Hill
        RoomEntrance(name = "Ski Hill from Icicles", trigger_pos = [0x442165a7, 0xc219fdff, 0xc389eb1b], dest_room = "ANT_D", dest_spawn = "spawn_d_1", can_start = True, source_room = 0x3C, target_room = 0x3E, connection_requirements = {"Icicles from Ski Hill": [[]]})
    ]),

    #The Lost World
    Level(name = "The Lost World", target_address = {"PAL": 0xC63AA0, "NTSC": 0xC63D20}, room_entrances = [
        #Entry
        RoomEntrance(name = "Entry from Spawn", can_start = True, target_room = 0x3F, connection_requirements = {"Trees from Entry": [["Water Net"], ["*Air Crawl"]], "Pterodactyls from Entry": [[]]}),
        RoomEntrance(name = "Entry from Trees", trigger_pos = [0xbf0b0a95, 0xc30217ae, 0x43a0842e], dest_room = "LOS_A", dest_spawn = "spawn_a_2", source_room = 0x41, target_room = 0x3F, connection_requirements = {"Trees from Entry": [[]], "Pterodactyls from Entry": [["Water Net"], ["*Air Crawl"], ["Sky Flyer", "*Hard"]]}),
        RoomEntrance(name = "Entry from Pterodactyls", trigger_pos = [0xc3b8384d, 0xc18b749e, 0x430f9b61], dest_room = "LOS_A", dest_spawn = "spawn_a_1", source_room = 0x40, target_room = 0x3F, connection_requirements = {"Trees from Entry": [["Water Net"], ["*Air Crawl"]], "Pterodactyls from Entry": [[]]}),

        #Trees
        RoomEntrance(name = "Trees from Entry", trigger_pos = [0x43dc64eb, 0xc1bffbfb, 0xc413d9c2], dest_room = "LOS_C", dest_spawn = "spawn_c_1", can_start = True, source_room = 0x3F, target_room = 0x41, connection_requirements = {"Entry from Trees": [[]], "T-Rex from Trees": [["Water Cannon", "Water Net"], ["Water Cannon", "*Hard"], ["*Air Crawl"]]}),
        RoomEntrance(name = "Trees from T-Rex", trigger_pos = [0x43c08a12, 0xc1b29b05, 0x43700fe3], dest_room = "LOS_C", dest_spawn = "spawn_c_2", source_room = 0x42, target_room = 0x41, connection_requirements = {"Entry from Trees": [["Water Net"], ["*Hard"]], "T-Rex from Trees": [[]]}),

        #T-Rex
        RoomEntrance(name = "T-Rex from Trees", trigger_pos = [0xc3fae038, 0x42b53a94, 0xc3b9840e], dest_room = "LOS_D", dest_spawn = "spawn_d_2", source_room = 0x41, target_room = 0x42, connection_requirements = {"Trees from T-Rex": [[]], "Pterodactyls from T-Rex": [["Water Net"], ["*Hard"]]}),
        RoomEntrance(name = "T-Rex from Pterodactyls", trigger_pos = [0x44460f30, 0xc212c952, 0x4300c94b], dest_room = "LOS_D", dest_spawn = "spawn_d_1", can_start = True, source_room = 0x40, target_room = 0x42, connection_requirements = {"Trees from T-Rex": [["Water Net"], ["*Hard"]], "Pterodactyls from T-Rex": [[]]}),

        #Pterodactyls
        RoomEntrance(name = "Pterodactyls from T-Rex", trigger_pos = [0xc4176e20, 0xc1975a9c, 0xc41135b3], dest_room = "LOS_B", dest_spawn = "spawn_b_2", source_room = 0x42, target_room = 0x40, connection_requirements = {"T-Rex from Pterodactyls": [[]], "Entry from Pterodactyls": [[]]}),
        RoomEntrance(name = "Pterodactyls from Entry", trigger_pos = [0x436f5bcd, 0x435f13c3, 0xc48350aa], dest_room = "LOS_B", dest_spawn = "spawn_b_1", can_start = True, source_room = 0x3F, target_room = 0x40, connection_requirements = {"T-Rex from Pterodactyls": [[]], "Entry from Pterodactyls": [[]]})
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
        RoomEntrance(name = "Entry from Lobby", trigger_pos = [0xc156d1ac, 0x40d01004, 0x42ece006], dest_room = "CIT_A", dest_spawn = "spawn_a_1", source_room = 0x44, target_room = 0x43, connection_requirements = {"Lobby from Entry": [[]]}),

        #Lobby
        RoomEntrance(name = "Lobby from Entry", trigger_pos = [0x43a2b009, 0x425f0200, 0xc45c685d], dest_room = "CIT_B", dest_spawn = "spawn_b_1", can_start = True, source_room = 0x43, target_room = 0x44, connection_requirements = {"Sewer Start from Lobby": [[]], "Entry from Lobby": [[]]}),
        RoomEntrance(name = "Lobby from Sewer Start", trigger_pos = [0x4416fe6e, 0x421c0200, 0x44c58060], dest_room = "CIT_B", dest_spawn = "spawn_b_2", source_room = 0x45, target_room = 0x44, connection_requirements = {"Sewer Start from Lobby": [[]], "Entry from Lobby": [[]]}),
        RoomEntrance(name = "Lobby from Sewer End", trigger_pos = [0xc1fe6199, 0x42a28100, 0xc428b55b], dest_room = "CIT_B", dest_spawn = "spawn_b_3", source_room = 0x45, target_room = 0x44, connection_requirements = {"Sewer End from Lobby": [[]], "Entry from Lobby": [[]], "Sewer Start from Lobby": [[]], "Tank from Lobby": [[]]}),
        RoomEntrance(name = "Lobby from Tank", trigger_pos = [0x448e485e, 0x43a42040, 0x444cd6df], dest_room = "CIT_B", dest_spawn = "spawn_b_4", source_room = 0x46, target_room = 0x44, connection_requirements = {"Sewer Start from Lobby": [[]], "Entry from Lobby": [[]], "Tank from Lobby": [[]], "Sewer End from Lobby": [[]]}),
        RoomEntrance(name = "Lobby from Final Room", trigger_pos = [0x441768d2, 0x4418c279, 0xc43d9748], dest_room = "CIT_B", dest_spawn = "spawn_b_5", source_room = 0x47, target_room = 0x44, connection_requirements = {"Sewer Start from Lobby": [[]], "Entry from Lobby": [[]]}),

        #Sewer
        RoomEntrance(name = "Sewer Start from Lobby", trigger_pos = [0xc3f4f622, 0x429c0100, 0xc421de94], dest_room = "CIT_C", dest_spawn = "spawn_c_1", can_start = True, source_room = 0x44, target_room = 0x45, connection_requirements = {"Lobby from Sewer Start": [[]], "Lobby from Sewer End": [["R.C. Car", "Electro Magnet"]]}),
        RoomEntrance(name = "Sewer End from Lobby", trigger_pos = [0xc4112474, 0x43020080, 0x4301479b], dest_room = "CIT_C", dest_spawn = "spawn_c_2", source_room = 0x44, target_room = 0x45, connection_requirements = {"Lobby from Sewer End": [[]]}),

        #Tank Room
        RoomEntrance(name = "Tank from Lobby", trigger_pos = [0x42cba2d5, 0x43020080, 0x4301cafd], dest_room = "CIT_D", dest_spawn = "spawn_d_1", can_start = True, source_room = 0x44, target_room = 0x46, connection_requirements = {"Lobby from Tank": [[]], "Final Room from Tank": [[]]}),
        RoomEntrance(name = "Tank from Final Room", trigger_pos = [0xc2567ede, 0x43d34040, 0xc4754e03], dest_room = "CIT_D", dest_spawn = "spawn_d_2", source_room = 0x47, target_room = 0x46, connection_requirements = {"Lobby from Tank": [["Power Punch"]], "Final Room from Tank": [[]]}),

        #Final Room
        RoomEntrance(name = "Final Room from Tank", trigger_pos = [0xc4112d69, 0x43d00040, 0x444d3105], dest_room = "CIT_E", dest_spawn = "spawn_e_1", can_start = True, source_room = 0x46, target_room = 0x47, connection_requirements = {"Tank from Final Room": [[]], "Lobby from Final Room": [["Electro Magnet", "Catapult", "R.C. Car"], ["*Air Crawl"], ["Electro Magnet", "Catapult", "Sky Flyer", "*Boost Jump", "*Expert"]]}),
        RoomEntrance(name = "Final Room from Lobby", trigger_pos = [0x43f8eff1, 0x43020080, 0xc3be787d], dest_room = "CIT_E", dest_spawn = "spawn_e_2", source_room = 0x44, target_room = 0x47, connection_requirements = {}) #Missing logic, though it doesn't really matter since no monkeys are connected to it and you cannot get here without also being able to get every monkey via alternative methods
    ]),

    #Code C.H.I.M.P.
    Level(name = "Code C.H.I.M.P.", target_address = {"PAL": 0xC63B30, "NTSC": 0xC63DB0}, room_entrances = [
        #Entry
        RoomEntrance(name = "Entry from Spawn", can_start = True, target_room = 0x48, connection_requirements = {"Base Entrance from Entry": [["*Air Crawl"], ["*Gear"]], "Moving Platforms from Entry": [["*Air Crawl"]]}),
        RoomEntrance(name = "Entry from Base Entrance", trigger_pos = [0xc29b684b, 0xc11ff7fe, 0x43fc2099], dest_room = "NAZ_A", dest_spawn = "spawn_a_1", source_room = 0x49, target_room = 0x48, connection_requirements = {"Base Entrance from Entry": [[]], "Moving Platforms from Entry": [["*Air Crawl"]]}),
        RoomEntrance(name = "Entry from Moving Platforms", trigger_pos = [0x43023bc1, 0x43160080, 0x44337100], dest_room = "NAZ_A", dest_spawn = "spawn_a_2", source_room = 0x4C, target_room = 0x48, connection_requirements = {"Base Entrance from Entry": [["*Air Crawl"], ["*Gear"]], "Moving Platforms from Entry": [[]]}),

        #Base Entrance
        RoomEntrance(name = "Base Entrance from Entry", trigger_pos = [0xc2cade0d, 0xc299fef2, 0xc491498c], dest_room = "NAZ_B", dest_spawn = "spawn_b_1", can_start = True, source_room = 0x48, target_room = 0x49, connection_requirements = {"Entry from Base Entrance": [[]], "Tank from Base Entrance": [["*Air Crawl"], ["Electro Magnet", "Water Cannon"], ["Electro Magnet", "*Damage Boost"], ["*Boost Fly", "*Expert", "*Damage Boost"], ["*Boost Fly", "*Expert", "Water Cannon"]]}),
        RoomEntrance(name = "Base Entrance from Tank", trigger_pos = [0x42c19599, 0xc356fef7, 0x428f53cf], dest_room = "NAZ_B", dest_spawn = "spawn_b_2", source_room = 0x4A, target_room = 0x49, connection_requirements = {"Entry from Base Entrance": [[]], "Tank from Base Entrance": [[]]}),

        #Tank
        RoomEntrance(name = "Tank from Base Entrance", trigger_pos = [0xc3141a6a, 0xc356fef7, 0x428348f1], dest_room = "NAZ_B1", dest_spawn = "spawn_b1_1", can_start = True, source_room = 0x49, target_room = 0x4A, connection_requirements = {"Treadmills from Tank": [[]], "Base Entrance from Tank": [[]]}),
        RoomEntrance(name = "Tank from Treadmills", trigger_pos = [0x4164c330, 0xc26ee111, 0x42f99f7b], dest_room = "NAZ_B1", dest_spawn = "spawn_b1_2", source_room = 0x4B, target_room = 0x4A, connection_requirements = {"Treadmills from Tank": [[]], "Base Entrance from Tank": [[]]}),

        #Treadmills
        RoomEntrance(name = "Treadmills from Tank", trigger_pos = [0xc4df65bd, 0xc327ff4b, 0xc4dda9c1], dest_room = "NAZ_C", dest_spawn = "spawn_c_1", can_start = True, source_room = 0x4A, target_room = 0x4B, connection_requirements = {"Moving Platforms from Treadmills": [["Electro Magnet"], ["Sky Flyer", "*Boost Fly", "*Expert"], ["*Air Crawl", "*Hard"]], "Tank from Treadmills": [[]]}),
        RoomEntrance(name = "Treadmills from Moving Platforms", trigger_pos = [0xc39fe1d6, 0xc28bbf15, 0x43bd9f8d], dest_room = "NAZ_C", dest_spawn = "spawn_c_2", source_room = 0x4C, target_room = 0x4B, connection_requirements = {"Moving Platforms from Treadmills": [[]]}),

        #Moving Platforms
        RoomEntrance(name = "Moving Platforms from Treadmills", trigger_pos = [0x43bb69fc, 0x430c0080, 0x44e8a80a], dest_room = "NAZ_D", dest_spawn = "spawn_d_1", can_start = True, source_room = 0x4B, target_room = 0x4C, connection_requirements = {"Treadmills from Moving Platforms": [[]], "Magnetic Panels Start from Moving Platforms": [[]]}),
        RoomEntrance(name = "Moving Platforms from Magnetic Panels Start", trigger_pos = [0x44019d20, 0xc295fe17, 0xc43b3461], dest_room = "NAZ_D", dest_spawn = "spawn_d_3", source_room = 0x4D, target_room = 0x4C, connection_requirements = {"Treadmills from Moving Platforms": [[]], "Magnetic Panels Start from Moving Platforms": [[]]}),
        RoomEntrance(name = "Moving Platforms from Magnetic Panels End", trigger_pos = [0xc37eefe3, 0xc2d1feef, 0xc3aa0981], dest_room = "NAZ_D", dest_spawn = "spawn_d_4", source_room = 0x4D, target_room = 0x4C, connection_requirements = {"Treadmills from Moving Platforms": [["*Attack"], ["*Hard"]], "Magnetic Panels Start from Moving Platforms": [["*Attack"], ["*Hard"]], "Magnetic Panels End from Moving Platforms": [[]], "Entry from Moving Platforms": [["*Attack"], ["*Hard"]]}),
        RoomEntrance(name = "Moving Platforms from Entry", trigger_pos = [0xc46e94a5, 0xc1c3fc0b, 0xc1c62b65], dest_room = "NAZ_D", dest_spawn = "spawn_d_2", source_room = 0x48, target_room = 0x4C, connection_requirements = {"Treadmills from Moving Platforms": [[]], "Magnetic Panels Start from Moving Platforms": [[]], "Entry from Moving Platforms": [[]]}),

        #Magnetic Panels
        RoomEntrance(name = "Magnetic Panels Start from Moving Platforms", trigger_pos = [0x43e45af8, 0xc295fd59, 0xc444e5e0], dest_room = "NAZ_D1", dest_spawn = "spawn_d1_1", can_start = True, source_room = 0x4C, target_room = 0x4D, connection_requirements = {"Moving Platforms from Magnetic Panels End": [["Electro Magnet", "Sky Flyer"], ["Electro Magnet", "*Expert", "Pipotchi"]], "Moving Platforms from Magnetic Panels Start": [[]]}),
        RoomEntrance(name = "Magnetic Panels End from Moving Platforms", trigger_pos = [0xc3728c7a, 0xc28bfeff, 0xc38ecd40], dest_room = "NAZ_D1", dest_spawn = "spawn_d1_2", source_room = 0x4C, target_room = 0x4D, connection_requirements = {"Moving Platforms from Magnetic Panels End": [[]], "Moving Platforms from Magnetic Panels Start": [["*Air Crawl"]]})
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
        RoomEntrance(name = "Entry from Wheel", trigger_pos = [0xc4225aae, 0xc2157a51, 0xc080e162], dest_room = "MOO_A", dest_spawn = "spawn_a_1", source_room = 0x4F, target_room = 0x4E, connection_requirements = {"Wheel from Entry": [[]], "UFO Arena from Entry": [[]], "Armoured Monkey Arena from Entry": [["*Air Crawl"]], "Robot from Entry": [["*Air Crawl"]], "Moving Platforms from Entry": [["*Air Crawl"]], "Mech Arena from Entry": [["*Air Crawl"], ["*Boost Fly", "*Hard"]], "Inside Climb from Entry": [["*Air Crawl"]], "Bomb from Entry": [["*Air Crawl"]]}),
        RoomEntrance(name = "Entry from UFO Arena", trigger_pos = [0x4352af6e, 0xc1007f2a, 0x44b86e10], dest_room = "MOO_A", dest_spawn = "spawn_a_2", source_room = 0x52, target_room = 0x4E, connection_requirements = {"Wheel from Entry": [[]], "UFO Arena from Entry": [[]], "Armoured Monkey Arena from Entry": [["*Air Crawl"]], "Robot from Entry": [["*Air Crawl"]], "Moving Platforms from Entry": [["*Air Crawl"]], "Mech Arena from Entry": [["*Air Crawl"], ["*Boost Fly", "*Hard"]], "Inside Climb from Entry": [["*Air Crawl"]], "Bomb from Entry": [["*Air Crawl"]]}),

        RoomEntrance(name = "Entry from Armoured Monkey Arena", trigger_pos = [0x445abd11, 0xc26838d3, 0x43b6d35b], dest_room = "MOO_A", dest_spawn = "spawn_a_3", source_room = 0x53, target_room = 0x4E, connection_requirements = {"Wheel from Entry": [["*Air Crawl"]], "UFO Arena from Entry": [["*Air Crawl"]], "Armoured Monkey Arena from Entry": [[]], "Robot from Entry": [[]], "Moving Platforms from Entry": [[]], "Mech Arena from Entry": [["*Air Crawl"], ["*Boost Fly", "*Hard"]], "Inside Climb from Entry": [["*Air Crawl"]], "Bomb from Entry": [["*Air Crawl"]]}),
        RoomEntrance(name = "Entry from Robot", trigger_pos = [0x4442f1fb, 0xc0ce5c4c, 0xc06bd3dc], dest_room = "MOO_A", dest_spawn = "spawn_a_4", source_room = 0x50, target_room = 0x4E, connection_requirements = {"Wheel from Entry": [["*Air Crawl"]], "UFO Arena from Entry": [["*Air Crawl"]], "Armoured Monkey Arena from Entry": [[]], "Robot from Entry": [[]], "Moving Platforms from Entry": [[]], "Mech Arena from Entry": [["*Air Crawl"], ["*Boost Fly", "*Hard"]], "Inside Climb from Entry": [["*Air Crawl"]], "Bomb from Entry": [["*Air Crawl"]]}),
        RoomEntrance(name = "Entry from Moving Platforms", trigger_pos = [0xc3e64599, 0x41dee1ee, 0x443a50d7], dest_room = "MOO_A", dest_spawn = "spawn_a_5", source_room = 0x54, target_room = 0x4E, connection_requirements = {"Wheel from Entry": [["*Air Crawl"]], "UFO Arena from Entry": [["*Air Crawl"]], "Armoured Monkey Arena from Entry": [[]], "Robot from Entry": [[]], "Moving Platforms from Entry": [[]], "Mech Arena from Entry": [["*Air Crawl"], ["*Boost Fly", "*Hard"]], "Inside Climb from Entry": [["*Air Crawl"]], "Bomb from Entry": [["*Air Crawl"]]}),

        RoomEntrance(name = "Entry from Mech Arena", trigger_pos = [0x44eb5e8b, 0x437aa881, 0x4474a434], dest_room = "MOO_A", dest_spawn = "spawn_a_6", source_room = 0x56, target_room = 0x4E, connection_requirements = {"Wheel from Entry": [["*Air Crawl"]], "UFO Arena from Entry": [["*Air Crawl"]], "Armoured Monkey Arena from Entry": [["*Air Crawl"]], "Robot from Entry": [["*Air Crawl"]], "Moving Platforms from Entry": [["*Air Crawl"]], "Mech Arena from Entry": [[]], "Inside Climb from Entry": [[]], "Bomb from Entry": [["*Air Crawl"]]}),
        RoomEntrance(name = "Entry from Inside Climb", trigger_pos = [0xc321114a, 0xc2942481, 0xc4137a48], dest_room = "MOO_A", dest_spawn = "spawn_a_7", source_room = 0x57, target_room = 0x4E, connection_requirements = {"Wheel from Entry": [["*Air Crawl"]], "UFO Arena from Entry": [["*Air Crawl"]], "Armoured Monkey Arena from Entry": [["*Air Crawl"]], "Robot from Entry": [["*Air Crawl"]], "Moving Platforms from Entry": [["*Air Crawl"]], "Mech Arena from Entry": [[]], "Inside Climb from Entry": [[]], "Bomb from Entry": [["*Air Crawl"]]}),

        RoomEntrance(name = "Entry from Bomb", trigger_pos = [0xc311e5ba, 0x4383e2cc, 0x43386b34], dest_room = "MOO_A", dest_spawn = "spawn_a_8", source_room = 0x58, target_room = 0x4E, connection_requirements = {"Wheel from Entry": [[]], "UFO Arena from Entry": [[]], "Armoured Monkey Arena from Entry": [["*Air Crawl"]], "Robot from Entry": [["*Air Crawl"]], "Moving Platforms from Entry": [["*Air Crawl"]], "Mech Arena from Entry": [["*Air Crawl"]], "Inside Climb from Entry": [["*Air Crawl"]], "Bomb from Entry": [[]]}),

        #Wheel
        RoomEntrance(name = "Wheel from Entry", trigger_pos = [0xbfc6a79b, 0x41f62fc8, 0xc483a9ca], dest_room = "MOO_A1", dest_spawn = "spawn_a1_1", can_start = True, source_room = 0x4E, target_room = 0x4F, connection_requirements = {"Entry from Wheel": [[]]}),

        #UFO Arena
        RoomEntrance(name = "UFO Arena from Entry", trigger_pos = [0x43ec10b3, 0x41f62fc8, 0xc48eace2], dest_room = "MOO_B1", dest_spawn = "spawn_b1_1", can_start = True, source_room = 0x4E, target_room = 0x52, connection_requirements = {"Entry from UFO Arena": [[]], "Rotating Magnets from UFO Arena": [[]]}),
        RoomEntrance(name = "UFO Arena from Rotating Magnets", trigger_pos = [0xc4096393, 0xc2222e87, 0x4482f957], dest_room = "MOO_B1", dest_spawn = "spawn_b1_2", source_room = 0x51, target_room = 0x52, connection_requirements = {"Entry from UFO Arena": [[]], "Rotating Magnets from UFO Arena": [[]]}),

        #Rotating Magnets
        RoomEntrance(name = "Rotating Magnets from UFO Arena", trigger_pos = [0xc4056a7a, 0xc2222e87, 0x44843c5a], dest_room = "MOO_B", dest_spawn = "spawn_b_1", can_start = True, source_room = 0x52, target_room = 0x51, connection_requirements = {"UFO Arena from Rotating Magnets": [[]], "Armoured Monkey Arena from Rotating Magnets": [["Electro Magnet", "Sky Flyer"], ["Electro Magnet", "*Hard"], ["*Air Crawl"]]}),
        RoomEntrance(name = "Rotating Magnets from Armoured Monkey Arena", trigger_pos = [0x448325bd, 0xc2b53ae5, 0xc3c65332], dest_room = "MOO_B", dest_spawn = "spawn_b_2", source_room = 0x53, target_room = 0x51, connection_requirements = {"UFO Arena from Rotating Magnets": [["*Air Crawl"]], "Armoured Monkey Arena from Rotating Magnets": [[]]}),

        #Arena
        RoomEntrance(name = "Armoured Monkey Arena from Rotating Magnets", trigger_pos = [0x44815420, 0xc2c07693, 0xc3e078af], dest_room = "MOO_B2", dest_spawn = "spawn_b2_2", source_room = 0x51, target_room = 0x53, connection_requirements = {"Rotating Magnets from Armoured Monkey Arena": [[]], "Entry from Armoured Monkey Arena": [[]]}),
        RoomEntrance(name = "Armoured Monkey Arena from Entry", trigger_pos = [0x443dea36, 0x41f61dcd, 0xc46125dd], dest_room = "MOO_B2", dest_spawn = "spawn_b2_1", can_start = True, source_room = 0x4E, target_room = 0x53, connection_requirements = {"Rotating Magnets from Armoured Monkey Arena": [[]], "Entry from Armoured Monkey Arena": [[]]}),

        #Robot
        RoomEntrance(name = "Robot from Entry", trigger_pos = [0x448d4b0f, 0x41f62fc8, 0xc3ebc3e7], dest_room = "MOO_A2", dest_spawn = "spawn_a2_1", can_start = True, source_room = 0x4E, target_room = 0x50, connection_requirements = {"Entry from Robot": [[]]}),

        #Moving Platforms
        RoomEntrance(name = "Moving Platforms from Entry", trigger_pos = [0x44876013, 0x41f62fc8, 0xc07085d0], dest_room = "MOO_C", dest_spawn = "spawn_c_1", can_start = True, source_room = 0x4E, target_room = 0x54, connection_requirements = {"Entry from Moving Platforms": [[]], "Magnetic Panels from Moving Platforms": [["Electro Magnet", "*Moon Fire"], ["*Moon Fire", "*Boost Fly", "*Expert", "Power Punch"], ["*Air Crawl", "Power Punch"]]}),
        RoomEntrance(name = "Moving Platforms from Magnetic Panels", trigger_pos = [0xc2ca75b6, 0x428a0e60, 0xc1a3de6c], dest_room = "MOO_C", dest_spawn = "spawn_c_2", source_room = 0x55, target_room = 0x54, connection_requirements = {"Entry from Moving Platforms": [["Electro Magnet", "Water Cannon", "Sky Flyer", "Power Punch"], ["Electro Magnet", "*Damage Boost", "Sky Flyer", "Power Punch"], ["Electro Magnet", "Water Cannon", "*Air Crawl", "Power Punch"], ["Electro Magnet", "*Damage Boost", "*Air Crawl", "Power Punch"]], "Magnetic Panels from Moving Platforms": [[]]}),
        
        #Magnetic Panels
        RoomEntrance(name = "Magnetic Panels from Moving Platforms", trigger_pos = [0xc3433fe1, 0x41df3f4f, 0xc1b20ad8], dest_room = "MOO_C1", dest_spawn = "spawn_c1_1", can_start = True, source_room = 0x54, target_room = 0x55, connection_requirements = {"Moving Platforms from Magnetic Panels": [[]], "Mech Arena from Magnetic Panels": [["Electro Magnet"], ["*Boost Fly", "*Expert"], ["*Air Crawl"]]}),
        RoomEntrance(name = "Magnetic Panels from Mech Arena", trigger_pos = [0x447d20e2, 0x4352d244, 0x43ec7398], dest_room = "MOO_C1", dest_spawn = "spawn_c1_2", source_room = 0x56, target_room = 0x55, connection_requirements = {"Moving Platforms from Magnetic Panels": [["*Air Crawl"]], "Mech Arena from Magnetic Panels": [[]]}),

        #Mech Arena
        RoomEntrance(name = "Mech Arena from Magnetic Panels", trigger_pos = [0x446fe3d8, 0x434944d0, 0x43dab531], dest_room = "MOO_C2", dest_spawn = "spawn_c2_1", can_start = True, source_room = 0x55, target_room = 0x56, connection_requirements = {"Magnetic Panels from Mech Arena": [[]], "Entry from Mech Arena": [[]]}),
        RoomEntrance(name = "Mech Arena from Entry", trigger_pos = [0x4496c0c3, 0x41f61dcd, 0x43bd4897], dest_room = "MOO_C2", dest_spawn = "spawn_c2_2", source_room = 0x4E, target_room = 0x56, connection_requirements = {"Magnetic Panels from Mech Arena": [[]], "Entry from Mech Arena": [[]]}),

        #Inside Climb
        RoomEntrance(name = "Inside Climb from Entry", dest_room = "MOO_D", dest_spawn = "spawn_d_1", trigger_pos = [0x43785031, 0x41c8e903, 0x4376e6c6], can_start = True, source_room = 0x4E, target_room = 0x57, connection_requirements = {"Outside Climb Start from Inside Climb": [["R.C. Car", "Sky Flyer", "Catapult", "Electro Magnet", "*Attack"], ["*Boost Fly", "*Expert"], ["Sky Flyer", "Electro Magnet", "*Hard"], ["*Air Crawl"]], "Outside Climb End from Inside Climb": [["*Air Crawl"]], "Entry from Inside Climb": [[]], "Bomb from Inside Climb": [["*Air Crawl"]]}),
        RoomEntrance(name = "Inside Climb from Outside Climb Start", trigger_pos = [0x43b41769, 0x42850ec5, 0x4372d440], dest_room = "MOO_D", dest_spawn = "spawn_d_2", source_room = 0x58, target_room = 0x57, connection_requirements = {"Outside Climb Start from Inside Climb": [[]], "Outside Climb End from Inside Climb": [["*Air Crawl"]], "Entry from Inside Climb": [[]], "Bomb from Inside Climb": [["*Air Crawl"]]}),
        RoomEntrance(name = "Inside Climb from Outside Climb End", trigger_pos = [0xc2074256, 0x4309a589, 0x43942aa4], dest_room = "MOO_D", dest_spawn = "spawn_d_3", source_room = 0x58, target_room = 0x57, connection_requirements = {"Outside Climb Start from Inside Climb": [[]], "Outside Climb End from Inside Climb": [[]], "Entry from Inside Climb": [[]], "Bomb from Inside Climb": [[]]}),
        RoomEntrance(name = "Inside Climb from Bomb", trigger_pos = [0xc4459dea, 0x43860040, 0xbedc5e1b], dest_room = "MOO_D", dest_spawn = "spawn_d_4", source_room = 0x58, target_room = 0x57, connection_requirements = {"Outside Climb Start from Inside Climb": [[]], "Outside Climb End from Inside Climb": [[]], "Entry from Inside Climb": [[]], "Bomb from Inside Climb": [[]]}),

        #Outside Climb
        RoomEntrance(name = "Outside Climb Start from Inside Climb", trigger_pos = [0xc3a93b11, 0x42fac870, 0x44124408], dest_room = "MOO_D1", dest_spawn = "spawn_d1_1", can_start = True, source_room = 0x57, target_room = 0x58, connection_requirements = {"Inside Climb from Outside Climb End": [[]], "Inside Climb from Outside Climb Start": [[]]}),
        RoomEntrance(name = "Outside Climb End from Inside Climb", trigger_pos = [0xc42599f8, 0x4396038a, 0x4330dd58], dest_room = "MOO_D1", dest_spawn = "spawn_d1_2", source_room = 0x57, target_room = 0x58, connection_requirements = {"Inside Climb from Outside Climb End": [[]], "Inside Climb from Outside Climb Start": [[]]}),

        #Bomb
        RoomEntrance(name = "Bomb from Entry", trigger_pos = [0xc358861c, 0x41c8e903, 0xc3586124], dest_room = "MOO_D1", dest_spawn = "spawn_d1_3", source_room = 0x4E, target_room = 0x58, connection_requirements = {"Entry from Bomb": [["Electro Magnet"], ["*Air Crawl", "Sky Flyer", "*Expert"], ["Power Punch", "*Hard"]], "Inside Climb from Bomb": [[]]}),
        RoomEntrance(name = "Bomb from Inside Climb", trigger_pos = [0xc31ccf4f, 0x43a3bfcf, 0xc34fb79c], dest_room = "MOO_D1", dest_spawn = "spawn_d1_4", source_room = 0x57, target_room = 0x58, connection_requirements = {"Entry from Bomb": [["Electro Magnet"], ["*Air Crawl", "Sky Flyer", "*Expert"], ["Power Punch", "*Hard"]], "Inside Climb from Bomb": [[]]})
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
gate_from_name: dict[str, RoomEntrance] = {}

for level in levels:
    for room_entrance in level.room_entrances:
        gate_from_name[f"{room_entrance.name} - {level.name}"] = room_entrance
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