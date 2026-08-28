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

gadget_ids = {"Stun Club": 1, "Monkey Net": 2, "Monkey Radar": 3, "Dash Hoop": 4, "Catapult": 5, "R.C. Car": 6, "Sky Flyer": 7, "Bananarang": 8, "Water Cannon": 9, "Electro Magnet": 10, "Power Punch": 11}
gadget_from_id = {gadget_id: gadget for gadget, gadget_id in gadget_ids.items()}

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

equipped_gadget_addresses = {
    "cross": {"PAL": 0x4D5F24, "NTSC": 0x4D4D24},
    "triangle": {"PAL": 0x4D5F1C, "NTSC": 0x4D4D1C},
    "square": {"PAL": 0x4D5F28, "NTSC": 0x4D4D28},
    "circle": {"PAL": 0x4D5F20, "NTSC": 0x4D4D20}
}

misc_addresses = {
    #Game State
    "screen": {"PAL": 0x3B3618, "NTSC": 0x3B2118}, #Current stage/screen/area
    "visited": {"PAL": 0x3E198C, "NTSC": 0x3E067C}, #Number of levels visited (updates your unlocked gadgets) - just keep it at 255
    "cleared": {"PAL": 0x3E1988, "NTSC": 0x3E0678}, #How many levels are cleared
    "air_meter_showing": {"PAL": 0x53D058, "NTSC": 0x53C0D4}, #1 = air meter visible (so check for water net unlock)
    "natsumi_introduced": {"PAL": 0x3B366D, "NTSC": 0x3B216D}, #0 = Natsumi hasn't done her introduction, 1 = Natsumi has done her introduction
    "game_paused": {"PAL": 0x3B3604, "NTSC": 0x3B2104}, #0 = unpaused, 3 = paused
    "message_info_pointer": {"PAL": 0x3DE2CC, "NTSC": 0x3DCF6C}, #points to active message information

    #Level Select
    "levels": {"PAL": 0x3E1984, "NTSC": 0x3E0674}, #How many levels you can select from
    "selected": {"PAL": 0x1F5D80C, "NTSC": 0x1F5D80C}, #Current level hovered on level select screen (addresses are the same)
    "level_to_be_loaded": {"PAL": 0x3B3624, "NTSC": 0x3B2124}, #Room we're going to 

    #Player
    "character": {"PAL": 0x3E1974, "NTSC": 0x3E0664}, #01 = Hikaru, 02 = Hikaru (+See-All Scope), 03 = Kakeru, 04 = Kakeru (+See-All Scope)
    "health": {"PAL": 0x3E197C, "NTSC": 0x3E066C}, #Current cookie count
    "x_position": {"PAL": 0x4D5CC0, "NTSC": 0x4D4AC0}, #X position
    "y_position": {"PAL": 0x4D5CC4, "NTSC": 0x4D4AC4}, #Y position
    "z_position": {"PAL": 0x4D5CC8, "NTSC": 0x4D4AC8}, #Z position
    "y_velocity": {"PAL": 0x4D5D14, "NTSC": 0x4D4BC7},
    "hikaru_state": {"PAL": 0x4D5784, "NTSC": 0x4D4584}, #7 = crouched, 8 = crawling, 9 = hidden, 17 = submerged, 18 = floating, 49 = celebrating
    "jump_state": {"PAL": 0x4D5D9C, "NTSC": 0x4D4B9C},
    "hikaru_visible": {"PAL": 0x4D5796, "NTSC": 0x4D4596}, #0 = invisible, 1 = visible
    "hikaru_max_speed": {"PAL": 0x4D57A4, "NTSC": 0x4D45A4}, #0x3FC7AE12 = normal, 0x50000000 = rocket boots trap, 0x3F200000 = slowness trap

    #Consumables
    "coins": {"PAL": 0x3E1980, "NTSC": 0x3E0670}, #How many coins you have right now
    "lives": {"PAL": 0x3E1978, "NTSC": 0x3E0668}, #How many lives you have right now
    "explosive_pellets": {"PAL": 0x3E19A9, "NTSC": 0x3E0699},
    "guided_pellets": {"PAL": 0x3E19AA, "NTSC": 0x3E069A},

    #Gadgets
    "equipped": {"PAL": 0x4D5F34, "NTSC": 0x4D4D34}, #Current held gadget
    "selected_face_button": {"PAL": 0x4D5F2C, "NTSC": 0x4D4D2C}, 
    "gadget_visible": {"PAL": 0x4D5797, "NTSC": 0x4D4597}, #0 = invisible, 1 = visible
    "invisible_hoop_giver": {"PAL": 0x284488, "NTSC": 0x2833B8}, #nop this to prevent you being given an invisible dash hoop - restore behaviour with 0xAE220B14

    #Camera
    "camera_state": {"PAL": 0x4CCD40, "NTSC": 0x4CBB40}, #0 = frozen, 2 = active
    "camera_zoom": {"PAL": 0x4CCEC8, "NTSC": -1},
    "in_first_person": {"PAL": 0x4D1AF4, "NTSC": 0x4D08F4}, #0 = normal, 1 = first person, other numbers are different camera angles

    #Transitions
    "transition_function_a": {"PAL": 0x383104, "NTSC": 0x381BE4}, #AC620004 = transition updates enabled, 00000000 = disabled 
    "transition_function_b": {"PAL": 0x38329C, "NTSC": 0x381D7C}, #B2060007 = transition updates enabled, 00000000 = disabled 
    "reload_room": {"PAL": 0x3B35D4, "NTSC": 0x3B20D4}, #4 = reload room
    "gate_pointer": {"PAL": 0x1E60B8C, "NTSC": 0x1E60B8C},
    "room_to_be_loaded": {"PAL": 0x3B3620, "NTSC": 0x3B2120},
    "in_transition": {"PAL": 0x3B35D0, "NTSC": 0x3B20D0}, #0 = normal, 2 = in transition

    #Gotcha Box
    "gotcha_box_enabled": {"PAL": 0x1F5924C, "NTSC": 0x1F5924C}, #0 = disabled, 1 = enabled
    "dispense_gotcha_box_capsule": {"PAL": 0x305BB4, "NTSC": 0x3049FC},
    "gotcha_box_patch_a": {"PAL": 0x305D04, "NTSC": 0x304B4C},
    "gotcha_box_patch_b": {"PAL": 0x305D08, "NTSC": 0x304B50},
    "gotcha_box_patch_c": {"PAL": 0x305D0C, "NTSC": 0x304B54}
}

#00284488 - nop this out for the invisible hoop fix

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

gotcha_box_collectibles = {
    'Monkey Football': {"PAL": 0X3E1C65, "NTSC": 0X3E0955},
    'Dance, Monkey, Dance!': {"PAL": 0X3E1C64, "NTSC": 0X3E0954},
    'Monkey Climber': {"PAL": 0X3E1C66, "NTSC": 0X3E0956},

    'Black R.C. Car Body': {"PAL": 0X3E1CA1, "NTSC": 0X3E0991},
    'Tissues R.C. Car Body': {"PAL": 0X3E1CA2, "NTSC": 0X3E0992},
    'Sushi R.C. Car Body': {"PAL": 0X3E1CA3, "NTSC": 0X3E0993},
    'Pudding R.C. Car Body': {"PAL": 0X3E1CA4, "NTSC": 0X3E0994},

    'Monkey Fable: "Monkey Taro"': {"PAL": 0X3E1C14, "NTSC": 0X3E0904},
    'Monkey Fable: "Monkey Taro II"': {"PAL": 0X3E1C18, "NTSC": 0X3E0908},
    'Monkey Fable: "The Monkey Who Cried Hikaru"': {"PAL": 0X3E1C1C, "NTSC": 0X3E090C},
    'Monkey Fable: "Monkerella"': {"PAL": 0X3E1C20, "NTSC": 0X3E0910},
    'Monkey Fable: "Apeshima Taro"': {"PAL": 0X3E1C24, "NTSC": 0X3E0914},
    'Monkey Fable: "The Grateful Monkey"': {"PAL": 0X3E1C28, "NTSC": 0X3E0918},
    'Monkey Fable: "The Wise Monkey"': {"PAL": 0X3E1C2C, "NTSC": 0X3E091C},
    'Monkey Fable: "Little Red Monkey Helmet"': {"PAL": 0X3E1C30, "NTSC": 0X3E0920},
    'Monkey Fable: "Monkerella II"': {"PAL": 0X3E1C34, "NTSC": 0X3E0924},
    'Monkey Fable: "The Monkey Statue"': {"PAL": 0X3E1C38, "NTSC": 0X3E0928},
    'Monkey Fable: "The Gold and Silver Bananas"': {"PAL": 0X3E1C3C, "NTSC": 0X3E092C},
    'Monkey Fable: "The Never Ending Banana"': {"PAL": 0X3E1C40, "NTSC": 0X3E0930},
    'Monkey Fable: "The Monkey Village"': {"PAL": 0X3E1C44, "NTSC": 0X3E0934},
    'Monkey Fable: "The Three Little Monkeys"': {"PAL": 0X3E1C48, "NTSC": 0X3E0938},
    'Monkey Fable: "Jack and the Bananastalk"': {"PAL": 0X3E1C4C, "NTSC": 0X3E093C},
    'Monkey Fable: "Hikaru and Pipotchi"': {"PAL": 0X3E1C50, "NTSC": 0X3E0940},
    'Monkey Fable: "Thumbelotchi"': {"PAL": 0X3E1C54, "NTSC": 0X3E0944},
    'Monkey Fable: "The Monkey\'s New Clothes"': {"PAL": 0X3E1C58, "NTSC": 0X3E0948},
    'Monkey Fable: "The Giant Bananastalk"': {"PAL": 0X3E1C5C, "NTSC": 0X3E094C},
    'Monkey Fable: "Nightmare Scenario"': {"PAL": 0X3E1C60, "NTSC": 0X3E0950},

    'Movie: "Monkeys on Parade"': {"PAL": 0X3E1C67, "NTSC": 0X3E0957},
    'Movie: "The Beginning"': {"PAL": 0X3E1C68, "NTSC": 0X3E0958},
    'Movie: "Meet Specter"': {"PAL": 0X3E1C69, "NTSC": 0X3E0959},
    'Movie: "Hikaru and the Professor"': {"PAL": 0X3E1C6A, "NTSC": 0X3E095A},
    'Movie: "It\'s Giant Yellow Monkey!"': {"PAL": 0X3E1C6B, "NTSC": 0X3E095B},
    'Movie: "Battle with Specter!"': {"PAL": 0X3E1C6C, "NTSC": 0X3E095C},
    'Movie: "Final Battle with Specter!"': {"PAL": 0X3E1C6D, "NTSC": 0X3E095D},
    'Movie: "Escape the Ape in You!"': {"PAL": 0X3E1C6E, "NTSC": 0X3E095E},

    'Soundtrack: "Theme Tune"': {"PAL": 0X3E1C6F, "NTSC": 0X3E095F},
    'Soundtrack: "Monkeys On Parade!"': {"PAL": 0X3E1C70, "NTSC": 0X3E0960},
    'Soundtrack: "The Beginning"': {"PAL": 0X3E1C71, "NTSC": 0X3E0961},
    'Soundtrack: "Liberty Island"': {"PAL": 0X3E1C72, "NTSC": 0X3E0962},
    'Soundtrack: "Breezy Village"': {"PAL": 0X3E1C73, "NTSC": 0X3E0963},
    'Soundtrack: "Port Calm"': {"PAL": 0X3E1C74, "NTSC": 0X3E0964},
    'Soundtrack: "Viva Apespania!"': {"PAL": 0X3E1C75, "NTSC": 0X3E0965},
    'Soundtrack: "Castle Frightmare"': {"PAL": 0X3E1C76, "NTSC": 0X3E0966},
    'Soundtrack: "Vita-Z Factory"': {"PAL": 0X3E1C77, "NTSC": 0X3E0967},
    'Soundtrack: "Casino City"': {"PAL": 0X3E1C78, "NTSC": 0X3E0968},
    'Soundtrack: "Ninja Hideout"': {"PAL": 0X3E1C79, "NTSC": 0X3E0969},
    'Soundtrack: "Snowball Mountain"': {"PAL": 0X3E1C7A, "NTSC": 0X3E096A},
    'Soundtrack: "Snowball Ski Slope"': {"PAL": 0X3E1C7B, "NTSC": 0X3E096B},
    'Soundtrack: "Lookout Valley"': {"PAL": 0X3E1C7C, "NTSC": 0X3E096C},
    'Soundtrack: "The Blue Baboon"': {"PAL": 0X3E1C7D, "NTSC": 0X3E096D},
    'Soundtrack: "Enter the Monkey"': {"PAL": 0X3E1C7E, "NTSC": 0X3E096E},
    'Soundtrack: "Simian Citadel"': {"PAL": 0X3E1C7F, "NTSC": 0X3E096F},
    'Soundtrack: "Panic Pyramid"': {"PAL": 0X3E1C80, "NTSC": 0X3E0970},
    'Soundtrack: "Pirate Isle"': {"PAL": 0X3E1C81, "NTSC": 0X3E0971},
    'Soundtrack: "Land of the Apes"': {"PAL": 0X3E1C82, "NTSC": 0X3E0972},
    'Soundtrack: "Monkey Hot Springs"': {"PAL": 0X3E1C83, "NTSC": 0X3E0973},
    'Soundtrack: "Monkey Ski Slope"': {"PAL": 0X3E1C84, "NTSC": 0X3E0974},
    'Soundtrack: "The Lost World"': {"PAL": 0X3E1C85, "NTSC": 0X3E0975},
    'Soundtrack: "Skyscraper City"': {"PAL": 0X3E1C86, "NTSC": 0X3E0976},
    'Soundtrack: "Code C.H.I.M.P."': {"PAL": 0X3E1C87, "NTSC": 0X3E0977},
    'Soundtrack: "Code C.H.I.M.P. II"': {"PAL": 0X3E1C88, "NTSC": 0X3E0978},
    'Soundtrack: "Moon Base 1"': {"PAL": 0X3E1C89, "NTSC": 0X3E0979},
    'Soundtrack: "Moon Base 2"': {"PAL": 0X3E1C8A, "NTSC": 0X3E097A},
    'Soundtrack: "Scheming Specter"': {"PAL": 0X3E1C8B, "NTSC": 0X3E097B},
    'Soundtrack: "Song of the Freaky Monkey Five"': {"PAL": 0X3E1C8C, "NTSC": 0X3E097C},
    'Soundtrack: "Escape the Ape in You!"': {"PAL": 0X3E1C8D, "NTSC": 0X3E097D},
    'Soundtrack: "Freaky Monkey Five Battle!"': {"PAL": 0X3E1C8E, "NTSC": 0X3E097E},
    'Soundtrack: "Giant Yellow Monkey Battle!"': {"PAL": 0X3E1C8F, "NTSC": 0X3E097F},
    'Soundtrack: "Battle with Specter!"': {"PAL": 0X3E1C90, "NTSC": 0X3E0980},
    'Soundtrack: "Specter\'s Theme"': {"PAL": 0X3E1C91, "NTSC": 0X3E0981},
    'Soundtrack: "Final Battle with Specter!"': {"PAL": 0X3E1C92, "NTSC": 0X3E0982},
    'Soundtrack: "Ending 1"': {"PAL": 0X3E1C93, "NTSC": 0X3E0983},
    'Soundtrack: "Ending 2"': {"PAL": 0X3E1C94, "NTSC": 0X3E0984},
    'Soundtrack: "Staff Credits"': {"PAL": 0X3E1C95, "NTSC": 0X3E0985},
    'Soundtrack: "Travel Station"': {"PAL": 0X3E1C96, "NTSC": 0X3E0986},
    'Soundtrack: "Gadget Trainer"': {"PAL": 0X3E1C97, "NTSC": 0X3E0987},
    'Soundtrack: "New Gotcha Gadget!"': {"PAL": 0X3E1C98, "NTSC": 0X3E0988},
    'Soundtrack: "Stage Cleared!"': {"PAL": 0X3E1C99, "NTSC": 0X3E0989},
    'Soundtrack: "Stage Perfectly Cleared!"': {"PAL": 0X3E1C9A, "NTSC": 0X3E098A},
    'Soundtrack: "Monkey Football!"': {"PAL": 0X3E1C9B, "NTSC": 0X3E098B},
    'Soundtrack: "Kick Off!"': {"PAL": 0X3E1C9C, "NTSC": 0X3E098C},
    'Soundtrack: "Gotcha Rhythm"': {"PAL": 0X3E1C9D, "NTSC": 0X3E098D},
    'Soundtrack: "Monkeys\' Gonna Getchu!"': {"PAL": 0X3E1C9E, "NTSC": 0X3E098E},
    'Soundtrack: "Monkey Chorus"': {"PAL": 0X3E1C9F, "NTSC": 0X3E098F},
    'Soundtrack: "Monkey Climber"': {"PAL": 0X3E1CA0, "NTSC": 0X3E0990},

    'Comic Strip: "An Extra Slice"': {"PAL": 0X3E1CA5, "NTSC": 0X3E0995},
    'Comic Strip: "The Scent of Banana"': {"PAL": 0X3E1CA6, "NTSC": 0X3E0996},
    'Comic Strip: "Girl Hunting"': {"PAL": 0X3E1CA7, "NTSC": 0X3E0997},
    'Comic Strip: "The Leak in the Roof"': {"PAL": 0X3E1CA8, "NTSC": 0X3E0998},
    'Comic Strip: "The Little Matchstick Girl"': {"PAL": 0X3E1CA9, "NTSC": 0X3E0999},
    'Comic Strip: "Multi-Purpose Stun Club"': {"PAL": 0X3E1CAA, "NTSC": 0X3E099A},
    'Comic Strip: "The Bowling Tournament"': {"PAL": 0X3E1CAB, "NTSC": 0X3E099B},
    'Comic Strip: "First Day of School"': {"PAL": 0X3E1CAC, "NTSC": 0X3E099C},
    'Comic Strip: "Birth of an Enemy"': {"PAL": 0X3E1CAD, "NTSC": 0X3E099D},
    'Comic Strip: "An Amazing Magic Show"': {"PAL": 0X3E1CAE, "NTSC": 0X3E099E},
    'Comic Strip: "A Completely Sealed Room"': {"PAL": 0X3E1CAF, "NTSC": 0X3E099F},
    'Comic Strip: "The Race"': {"PAL": 0X3E1CB0, "NTSC": 0X3E09A0},
    'Comic Strip: "Missing Weapon"': {"PAL": 0X3E1CB1, "NTSC": 0X3E09A1},
    'Comic Strip: "Ms. Banana is Saved!"': {"PAL": 0X3E1CB2, "NTSC": 0X3E09A2},
    'Comic Strip: "Spinning Specs"': {"PAL": 0X3E1CB3, "NTSC": 0X3E09A3},
    'Comic Strip: "Monkey Test"': {"PAL": 0X3E1CB4, "NTSC": 0X3E09A4},
    'Comic Strip: "Safety Precautions"': {"PAL": 0X3E1CB5, "NTSC": 0X3E09A5},

    'Concept Artwork: "Freaky Monkey Five"': {"PAL": 0X3E1CB6, "NTSC": 0X3E09A6},
    'Concept Artwork: "Blue Monkey"': {"PAL": 0X3E1CB7, "NTSC": 0X3E09A7},
    'Concept Artwork: "Yellow Monkey"': {"PAL": 0X3E1CB8, "NTSC": 0X3E09A8},
    'Concept Artwork: "Pink Monkey"': {"PAL": 0X3E1CB9, "NTSC": 0X3E09A9},
    'Concept Artwork: "White Monkey"': {"PAL": 0X3E1CBA, "NTSC": 0X3E09AA},
    'Concept Artwork: "Red Monkey"': {"PAL": 0X3E1CBB, "NTSC": 0X3E09AB},
    'Concept Artwork: "Hikaru 1"': {"PAL": 0X3E1CBC, "NTSC": 0X3E09AC},
    'Concept Artwork: "Pipotchi 1"': {"PAL": 0X3E1CBD, "NTSC": 0X3E09AD},
    'Concept Artwork: "Hikaru and Pipotchi 1"': {"PAL": 0X3E1CBE, "NTSC": 0X3E09AE},
    'Concept Artwork: "Natsumi 1"': {"PAL": 0X3E1CBF, "NTSC": 0X3E09AF},
    'Concept Artwork: "Professor 1"': {"PAL": 0X3E1CC0, "NTSC": 0X3E09B0},
    'Concept Artwork: "Expression 1"': {"PAL": 0X3E1CC1, "NTSC": 0X3E09B1},
    'Concept Artwork: "Expression 2"': {"PAL": 0X3E1CC2, "NTSC": 0X3E09B2},
    'Concept Artwork: "Pipotchi 2"': {"PAL": 0X3E1CC3, "NTSC": 0X3E09B3},
    'Concept Artwork: "Pipotchi 3"': {"PAL": 0X3E1CC4, "NTSC": 0X3E09B4},
    'Concept Artwork: "Pipotchi 4"': {"PAL": 0X3E1CC5, "NTSC": 0X3E09B5},
    'Concept Artwork: "Hikaru 2"': {"PAL": 0X3E1CC6, "NTSC": 0X3E09B6},
    'Concept Artwork: "Hikaru 3"': {"PAL": 0X3E1CC7, "NTSC": 0X3E09B7},
    'Concept Artwork: "Hikaru and Pipotchi 2"': {"PAL": 0X3E1CC8, "NTSC": 0X3E09B8},
    'Concept Artwork: "Hikaru 4"': {"PAL": 0X3E1CC9, "NTSC": 0X3E09B9},
    'Concept Artwork: "Hikaru 5"': {"PAL": 0X3E1CCA, "NTSC": 0X3E09BA},
    'Concept Artwork: "Hikaru 6"': {"PAL": 0X3E1CCB, "NTSC": 0X3E09BB},
    'Concept Artwork: "Hikaru 7"': {"PAL": 0X3E1CCC, "NTSC": 0X3E09BC},
    'Concept Artwork: "Hikaru and Pipotchi 3"': {"PAL": 0X3E1CCD, "NTSC": 0X3E09BD},
    'Concept Artwork: "Hikaru 8"': {"PAL": 0X3E1CCE, "NTSC": 0X3E09BE},
    'Concept Artwork: "Hikaru 9"': {"PAL": 0X3E1CCF, "NTSC": 0X3E09BF},
    'Concept Artwork: "Hikaru and Pipotchi 4"': {"PAL": 0X3E1CD0, "NTSC": 0X3E09C0},
    'Concept Artwork: "Hikaru 10"': {"PAL": 0X3E1CD1, "NTSC": 0X3E09C1},
    'Concept Artwork: "Pipotchi 5"': {"PAL": 0X3E1CD2, "NTSC": 0X3E09C2},
    'Concept Artwork: "Pipotchi 6"': {"PAL": 0X3E1CD3, "NTSC": 0X3E09C3},
    'Concept Artwork: "Pipotchi 7"': {"PAL": 0X3E1CD4, "NTSC": 0X3E09C4},
    'Concept Artwork: "Natsumi 2"': {"PAL": 0X3E1CD5, "NTSC": 0X3E09C5},
    'Concept Artwork: "Hikaru 11"': {"PAL": 0X3E1CD6, "NTSC": 0X3E09C6},
    'Concept Artwork: "Kakeru"': {"PAL": 0X3E1CD7, "NTSC": 0X3E09C7},
    'Concept Artwork: "Hiroki"': {"PAL": 0X3E1CD8, "NTSC": 0X3E09C8},
    'Concept Artwork: "Charu 1"': {"PAL": 0X3E1CD9, "NTSC": 0X3E09C9},
    'Concept Artwork: "Charu 2"': {"PAL": 0X3E1CDA, "NTSC": 0X3E09CA},
    'Concept Artwork: "Charu 3"': {"PAL": 0X3E1CDB, "NTSC": 0X3E09CB},
    'Concept Artwork: "Charu 4"': {"PAL": 0X3E1CDC, "NTSC": 0X3E09CC},
    'Concept Artwork: "The Professor 2"': {"PAL": 0X3E1CDD, "NTSC": 0X3E09CD},
    'Concept Artwork: "Stage Settings 1"': {"PAL": 0X3E1CDE, "NTSC": 0X3E09CE},
    'Concept Artwork: "Stage Settings 2"': {"PAL": 0X3E1CDF, "NTSC": 0X3E09CF},
    'Concept Artwork: "Stage Settings 3"': {"PAL": 0X3E1CE0, "NTSC": 0X3E09D0},
    'Concept Artwork: "Stage Settings 4"': {"PAL": 0X3E1CE1, "NTSC": 0X3E09D1},
    'Concept Artwork: "Stage Settings 5"': {"PAL": 0X3E1CE2, "NTSC": 0X3E09D2},
    'Concept Artwork: "Stage Settings 6"': {"PAL": 0X3E1CE3, "NTSC": 0X3E09D3},
    'Concept Artwork: "Stage Settings 7"': {"PAL": 0X3E1CE4, "NTSC": 0X3E09D4},
    'Concept Artwork: "Stage Settings 8"': {"PAL": 0X3E1CE5, "NTSC": 0X3E09D5},
    'Concept Artwork: "Stage Settings 9"': {"PAL": 0X3E1CE6, "NTSC": 0X3E09D6},
    'Concept Artwork: "Stage Settings 10"': {"PAL": 0X3E1CE7, "NTSC": 0X3E09D7},

    'Secret Photo: "The Three Afro Brothers"': {"PAL": 0X3E1CE8, "NTSC": 0X3E09D8},
    'Secret Photo: "Rock-Paper-Scissors Tournament"': {"PAL": 0X3E1CE9, "NTSC": 0X3E09D9},
    'Secret Photo: "You beast!"': {"PAL": 0X3E1CEA, "NTSC": 0X3E09DA},
    'Secret Photo: "Festival in the Forest"': {"PAL": 0X3E1CEB, "NTSC": 0X3E09DB},
    'Secret Photo: "Fruits of Training"': {"PAL": 0X3E1CEC, "NTSC": 0X3E09DC},
    'Secret Photo: "Oh my?!"': {"PAL": 0X3E1CED, "NTSC": 0X3E09DD},
    'Secret Photo: "Quite Close Friends"': {"PAL": 0X3E1CEE, "NTSC": 0X3E09DE},
    'Secret Photo: "Give It All You\'ve Got"': {"PAL": 0X3E1CEF, "NTSC": 0X3E09DF},
    'Secret Photo: "Happy Banana Gang"': {"PAL": 0X3E1CF0, "NTSC": 0X3E09E0},
    'Secret Photo: "This Year\'s Style"': {"PAL": 0X3E1CF1, "NTSC": 0X3E09E1},
    'Secret Photo: "Toilet Incident"': {"PAL": 0X3E1CF2, "NTSC": 0X3E09E2},
    'Secret Photo: "Photo of Two"': {"PAL": 0X3E1CF3, "NTSC": 0X3E09E3},
    'Secret Photo: "Almighty? Ski Gang"': {"PAL": 0X3E1CF4, "NTSC": 0X3E09E4},
    'Secret Photo: "Dry Throat"': {"PAL": 0X3E1CF5, "NTSC": 0X3E09E5},
    'Secret Photo: "Nice One"': {"PAL": 0X3E1CF6, "NTSC": 0X3E09E6},
    'Secret Photo: "Advanced RC Car"': {"PAL": 0X3E1CF7, "NTSC": 0X3E09E7},
    'Secret Photo: "Debut Concert"': {"PAL": 0X3E1CF8, "NTSC": 0X3E09E8},
    'Secret Photo: "Program Input"': {"PAL": 0X3E1CF9, "NTSC": 0X3E09E9},
    'Secret Photo: "Ape World Champion"': {"PAL": 0X3E1CFA, "NTSC": 0X3E09EA},
    'Secret Photo: "Ultra Goliath Armour"': {"PAL": 0X3E1CFB, "NTSC": 0X3E09EB},
    'Secret Photo: "Specter\'s Entrance"': {"PAL": 0X3E1CFC, "NTSC": 0X3E09EC},
    'Secret Photo: "Advanced Strategy?"': {"PAL": 0X3E1CFD, "NTSC": 0X3E09ED},
    'Secret Photo: "Monkey Cannon"': {"PAL": 0X3E1CFE, "NTSC": 0X3E09EE},
    'Secret Photo: "Monkey UFO"': {"PAL": 0X3E1CFF, "NTSC": 0X3E09EF},
    'Secret Photo: "RoboCow"': {"PAL": 0X3E1D00, "NTSC": 0X3E09F0},
    'Secret Photo: "\'Banana Buffet\' research"': {"PAL": 0X3E1D01, "NTSC": 0X3E09F1},
    'Secret Photo: "RoboApe"': {"PAL": 0X3E1D02, "NTSC": 0X3E09F2},
    'Secret Photo: "Legendary Captain"': {"PAL": 0X3E1D03, "NTSC": 0X3E09F3},
    'Secret Photo: "Quite a photo, eh?"': {"PAL": 0X3E1D04, "NTSC": 0X3E09F4},
    'Secret Photo: "Sauna, anyone?"': {"PAL": 0X3E1D05, "NTSC": 0X3E09F5},
    'Secret Photo: "Advanced Sky Flyer"': {"PAL": 0X3E1D06, "NTSC": 0X3E09F6},
    'Secret Photo: "Everyone gather together!"': {"PAL": 0X3E1D07, "NTSC": 0X3E09F7},
    'Secret Photo: "Robo Kong"': {"PAL": 0X3E1D08, "NTSC": 0X3E09F8},
    'Secret Photo: "I\'ll never let you go..."': {"PAL": 0X3E1D09, "NTSC": 0X3E09F9},
    'Secret Photo: "Gotcha!"': {"PAL": 0X3E1D0A, "NTSC": 0X3E09FA},
    'Secret Photo: "Get both of them!"': {"PAL": 0X3E1D0B, "NTSC": 0X3E09FB},
    'Secret Photo: "I\'m staying right here."': {"PAL": 0X3E1D0C, "NTSC": 0X3E09FC},
    'Secret Photo: "Monkey VS Pudding"': {"PAL": 0X3E1D0D, "NTSC": 0X3E09FD},
    'Secret Photo: "Monkey Statue of Liberty"': {"PAL": 0X3E1D0E, "NTSC": 0X3E09FE},
    'Secret Photo: "The Last Straw"': {"PAL": 0X3E1D0F, "NTSC": 0X3E09FF},
    'Secret Photo: "Break the sound barrier!"': {"PAL": 0X3E1D10, "NTSC": 0X3E0A00},
    'Secret Photo: "Monkey Sauna"': {"PAL": 0X3E1D11, "NTSC": 0X3E0A01},
    'Secret Photo: "You Are the Driver"': {"PAL": 0X3E1D12, "NTSC": 0X3E0A02},
    'Secret Photo: "Underwater Rendezvous"': {"PAL": 0X3E1D13, "NTSC": 0X3E0A03},
    'Secret Photo: "Ultimate Confrontation"': {"PAL": 0X3E1D14, "NTSC": 0X3E0A04},
    'Secret Photo: "There\'s no stopping"': {"PAL": 0X3E1D15, "NTSC": 0X3E0A05},
    'Secret Photo: "You\'re not bad!"': {"PAL": 0X3E1D16, "NTSC": 0X3E0A06},
    'Secret Photo: "We\'re not friends anymore?"': {"PAL": 0X3E1D17, "NTSC": 0X3E0A07},
    'Secret Photo: "Get a home run"': {"PAL": 0X3E1D18, "NTSC": 0X3E0A08},
    'Secret Photo: "Out for Blood!"': {"PAL": 0X3E1D19, "NTSC": 0X3E0A09},

    'Enemy Photo: "Porky"': {"PAL": 0X3E1D1A, "NTSC": 0X3E0A0A},
    'Enemy Photo: "Blue Porky"': {"PAL": 0X3E1D1B, "NTSC": 0X3E0A0B},
    'Enemy Photo: "Armoured Porky"': {"PAL": 0X3E1D1C, "NTSC": 0X3E0A0C},
    'Enemy Photo: "Skeleton Swine"': {"PAL": 0X3E1D1D, "NTSC": 0X3E0A0D},
    'Enemy Photo: "Mohawk Porky"': {"PAL": 0X3E1D1E, "NTSC": 0X3E0A0E},
    'Enemy Photo: "Tank Porky"': {"PAL": 0X3E1D1F, "NTSC": 0X3E0A0F},
    'Enemy Photo: "Tank Piglet"': {"PAL": 0X3E1D20, "NTSC": 0X3E0A10},
    'Enemy Photo: "Flame Porky"': {"PAL": 0X3E1D21, "NTSC": 0X3E0A11},
    'Enemy Photo: "Tomato Bird"': {"PAL": 0X3E1D22, "NTSC": 0X3E0A12},
    'Enemy Photo: "Eggplant Bee"': {"PAL": 0X3E1D23, "NTSC": 0X3E0A13},
    'Enemy Photo: "Pineapple Finch"': {"PAL": 0X3E1D24, "NTSC": 0X3E0A14},
    'Enemy Photo: "AAA Jellyfish"': {"PAL": 0X3E1D25, "NTSC": 0X3E0A15},
    'Enemy Photo: "Wax Owl"': {"PAL": 0X3E1D26, "NTSC": 0X3E0A16},
    'Enemy Photo: "Wax Queen"': {"PAL": 0X3E1D27, "NTSC": 0X3E0A17},
    'Enemy Photo: "Charred Chester"': {"PAL": 0X3E1D28, "NTSC": 0X3E0A18},
    'Enemy Photo: "They Might Be Slime"': {"PAL": 0X3E1D29, "NTSC": 0X3E0A19},
    'Enemy Photo: "Lousy rat"': {"PAL": 0X3E1D2A, "NTSC": 0X3E0A1A},
    'Enemy Photo: "Pinguin"': {"PAL": 0X3E1D2B, "NTSC": 0X3E0A1B},
    'Enemy Photo: "Boney M"': {"PAL": 0X3E1D2C, "NTSC": 0X3E0A1C},
    'Enemy Photo: "Sky Bomber"': {"PAL": 0X3E1D2D, "NTSC": 0X3E0A1D},
    'Enemy Photo: "Barbell Bomber"': {"PAL": 0X3E1D2E, "NTSC": 0X3E0A1E},
    'Enemy Photo: "Puffy the Blowfish"': {"PAL": 0X3E1D2F, "NTSC": 0X3E0A1F},
    'Enemy Photo: "Grinning Piranha"': {"PAL": 0X3E1D30, "NTSC": 0X3E0A20},
    'Enemy Photo: "The Bombettes"': {"PAL": 0X3E1D31, "NTSC": 0X3E0A21},
    'Enemy Photo: "Space Can"': {"PAL": 0X3E1D32, "NTSC": 0X3E0A22},
    'Enemy Photo: Submarine Lookalike""': {"PAL": 0X3E1D33, "NTSC": 0X3E0A23},
    'Enemy Photo: "Robo Kong"': {"PAL": 0X3E1D34, "NTSC": 0X3E0A24},

    'Stage Photo: "Liberty Park"': {"PAL": 0X3E1D35, "NTSC": 0X3E0A25},
    'Stage Photo: "Breezy Village"': {"PAL": 0X3E1D36, "NTSC": 0X3E0A26},
    'Stage Photo: "Port Calm"': {"PAL": 0X3E1D37, "NTSC": 0X3E0A27},
    'Stage Photo: "Viva Apespania!"': {"PAL": 0X3E1D38, "NTSC": 0X3E0A28},
    'Stage Photo: "Castle Frightmare"': {"PAL": 0X3E1D3A, "NTSC": 0X3E0A2A},
    'Stage Photo: "Vita-Z Factory"': {"PAL": 0X3E1D3B, "NTSC": 0X3E0A2B},
    'Stage Photo: "Casino City"': {"PAL": 0X3E1D3C, "NTSC": 0X3E0A2C},
    'Stage Photo: "Ninja Hideout"': {"PAL": 0X3E1D3D, "NTSC": 0X3E0A2D},
    'Stage Photo: "Snowball Mountain"': {"PAL": 0X3E1D3E, "NTSC": 0X3E0A2E},
    'Stage Photo: "Lookout Valley"': {"PAL": 0X3E1D3F, "NTSC": 0X3E0A2F},
    'Stage Photo: "The Blue Baboon"': {"PAL": 0X3E1D40, "NTSC": 0X3E0A30},
    'Stage Photo: "Enter the Monkey"': {"PAL": 0X3E1D4C, "NTSC": 0X3E0A3C},
    'Stage Photo: "Simian Citadel"': {"PAL": 0X3E1D4D, "NTSC": 0X3E0A3D},
    'Stage Photo: "Panic Pyramid"': {"PAL": 0X3E1D44, "NTSC": 0X3E0A34},
    'Stage Photo: "Pirate Isle"': {"PAL": 0X3E1D45, "NTSC": 0X3E0A35},
    'Stage Photo: "Land of the Apes"': {"PAL": 0X3E1D46, "NTSC": 0X3E0A36},
    'Stage Photo: "The Lost World"': {"PAL": 0X3E1D47, "NTSC": 0X3E0A37},
    'Stage Photo: "Skyscraper City"': {"PAL": 0X3E1D49, "NTSC": 0X3E0A39},
    'Stage Photo: "Code C.H.I.M.P."': {"PAL": 0X3E1D4A, "NTSC": 0X3E0A3A},
    'Stage Photo: "Moon Base"': {"PAL": 0X3E1D4E, "NTSC": 0X3E0A3E}
}


#00196CA0 - something to do with monkey names? (PAL)
#0024B0F0 - puts name pointer in v0?
#D6A040