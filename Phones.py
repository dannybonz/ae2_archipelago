from dataclasses import dataclass, field

@dataclass
class Phone:
    name: str
    description: str
    level: str
    connection_requirements: dict[str, list[str]] = field(default_factory = lambda: {"Entry from Spawn": [[]]})
    room: str = "Entry"
    is_blue: bool = False
    
    def get_location_name(self):
        if self.room == "Entry":
            return f'{self.level}: "{self.description}" Phone'
        else:
            return f'{self.level} ({self.room}): "{self.description}" Phone'

phones = [
    #Liberty Island
    Phone(name = "tel002", description = "Gadget Tutorial", level = "Liberty Island"),
    Phone(name = "tel003", description = "Jumping Tutorial", level = "Liberty Island"),
    Phone(name = "tel101", description = "Double Jump Tutorial", level = "Liberty Island", is_blue = True),
    Phone(name = "tel004", description = "Cookie Tutorial", level = "Liberty Island"),

    #Breezy Village
    Phone(name = "tel007", description = "Gadget Select Tutorial", level = "Breezy Village"),
    Phone(name = "tel105", description = "Aqua-Blue Pants Monkeys", level = "Breezy Village", is_blue = True),
    Phone(name = "tel005", description = "Monkey Bars Tutorial", level = "Breezy Village"),
    Phone(name = "tel006", description = "Double Jump Reminder", level = "Breezy Village"),

    #Port Calm
    Phone(name = "tel108", description = "Water Net Tutorial", level = "Port Calm", is_blue = True, connection_requirements = {"Entry from Spawn": [["Water Net"], ["*Air Crawl"], ["Sky Flyer", "*Hard"], ["*Expert"]], "Entry from Indoors": [["Water Net"]]}),
    Phone(name = "tel109", description = "Pipotchi", level = "Port Calm", is_blue = True, connection_requirements = {"Entry from Spawn": [["Water Net"], ["*Air Crawl"], ["Sky Flyer", "*Hard"], ["*Expert"]], "Entry from Indoors": [["Water Net"]]}),

    #Viva Apespania
    Phone(name = "tel111", description = "Blue Pants Monkeys", level = "Viva Apespania", is_blue = True, connection_requirements = {"Entry from Spawn": [[]], "Entry from Village": [[]]}),
    Phone(name = "tel112", description = "Gadget Select Reminder", level = "Viva Apespania", room = "Village", is_blue = True, connection_requirements = {"Village from Entry": [[]], "Village from Bullring": [[]]}),
    Phone(name = "tel011", description = "Life Tutorial", level = "Viva Apespania", room = "Bullring", connection_requirements = {"Bullring from Village": [[]]}),

    #Castle Frightmare
    Phone(name = "tel114", description = "White Pants Monkeys", level = "Castle Frightmare", is_blue = True, connection_requirements = {"Entry from Spawn": [[]], "Entry from House": [[]]}),

    #Vita-Z Factory
    Phone(name = "tel008", description = "Climbing Tutorial", level = "Vita-Z Factory", connection_requirements = {"Entry from Spawn": [[]], "Entry from Tunnel": [[]]}),
    Phone(name = "tel017", description = "Pipobot Tutorial", level = "Vita-Z Factory", room = "Mech Tunnel", connection_requirements = {"Tunnel from Entry": [[]], "Tunnel from Arena": [[]]}),

    #Casino City
    Phone(name = "tel120", description = "Black Pants Monkeys", level = "Casino City", connection_requirements = {"Entry from Spawn": [[]], "Entry from Circus": [[]], "Entry from Bar": [[]]}),
    Phone(name = "tel020", description = "Special Pellets", level = "Casino City", connection_requirements = {"Entry from Spawn": [[]], "Entry from Circus": [[]], "Entry from Bar": [[]]}),

    #Ninja Hideout
    Phone(name = "tel023", description = "R.C. Car Respawn Tutorial", level = "Ninja Hideout"),
    Phone(name = "tel123", description = "Tiptoe Tutorial", level = "Ninja Hideout", room = "Second Room", is_blue = True, connection_requirements = {"Second Room from Entry": [["*Attack"], ["*Hard"]], "Second Room from Third Room Start": [["*Attack"], ["*Hard"]], "Second Room from Third Room End": [["*Attack"], ["*Hard"]]}),

    #Snowball Mountain
    Phone(name = "tel126", description = "Slippery Ice", level = "Snowball Mountain", room = "Christmas Tree", is_blue = True, connection_requirements = {"Christmas Tree from Entry": [[]], "Christmas Tree from Ski Hill": [[]]}),
    Phone(name = "tel026", description = "Snowmobile Tutorial", level = "Snowball Mountain", room = "Ski Hill", connection_requirements = {"Ski Hill from Christmas Tree": [[]], "Ski Hill from Entry": [[]]}),

    #Lookout Valley
    Phone(name = "tel129", description = "Red Pants Monkeys", level = "Lookout Valley", is_blue = True, connection_requirements = {"Entry from Spawn": [["*Valley Gap", "*Valley Island"]], "Entry from Jungle End": [["Water Net"], ["*Air Crawl"]], "Entry from Jungle Start": [["Water Net"], ["*Air Crawl"]], "Entry from Cave Start": [["Water Net"], ["*Air Crawl"]], "Entry from Cave End": [["Water Net"], ["*Air Crawl"]]}),
    Phone(name = "tel029", description = "Boat Tutorial", level = "Lookout Valley", connection_requirements = {"Entry from Spawn": [["*Valley Gap", "*Valley Island", "*Valley Boat"]], "Entry from Jungle End": [["*Valley Island", "*Valley Boat"]], "Entry from Jungle Start": [["*Valley Island", "*Valley Boat"]], "Entry from Cave Start": [[]], "Entry from Cave End": [[]]}),

    #The Blue Baboon
    Phone(name = "tel032", description = "Submarine Tutorial", level = "The Blue Baboon", room = "Ship", connection_requirements = {"Ship from Entry": [[]]}),

    #Simian Citadel
    Phone(name = "tel138", description = "Green Pants Monkeys", level = "Simian Citadel", room = "Bullring", is_blue = True, connection_requirements = {"Bullring from Entry": [["*Bull Fight", "Dash Hoop"], ["*Bull Fight", "*Hard"]], "Bullring from Whale": [[]]}),

    #Panic Pyramid
    Phone(name = "tel141", description = "Moving Platform", level = "Panic Pyramid", room = "Moving Platforms #1", is_blue = True, connection_requirements = {"Moving Platforms #1 from Booby Traps": [[]], "Moving Platforms #1 from Moving Platforms #2": [["R.C. Car"], ["Water Cannon"], ["*Air Crawl"]]}),

    #Pirate Isle
    Phone(name = "tel144", description = "Boat Reminder", level = "Pirate Isle", room = "Boat", is_blue = True, connection_requirements = {"Boat from Cave Entrance": [[]], "Boat from Treasure": [[]], "Boat from Cell": [[]], "Boat from Mine": [["Water Cannon"], ["*Air Crawl"]]}),

    #The Lost World
    Phone(name = "tel150", description = "Dinosaurs", level = "The Lost World", is_blue = True, connection_requirements = {"Entry from Spawn": [[]], "Entry from Pterodactyls": [[]], "Entry from Trees": [["Water Net"], ["*Air Crawl"], ["Sky Flyer", "*Hard"]]}),

    #Skyscraper City
    Phone(name = "tel053", description = "Tank Tutorial", level = "Skyscraper City", room = "Tank", connection_requirements = {"Tank from Lobby Corridor": [[]], "Tank from Final Room": [[]]})
]

for i in range(0, len(phones)):
    if (phones[i].is_blue): #Automatically add Attack requirement to blue phones
        for connection_name in phones[i].connection_requirements:
            altered_requirements = []
            for requirement in phones[i].connection_requirements[connection_name]:
                altered_requirements.append(requirement + ["*Attack"])
                altered_requirements.append(requirement + ["*Hard"])
            phones[i].connection_requirements[connection_name] = altered_requirements
    phones[i].id = i + 1001
            
phone_from_name: dict[str, Phone] = {phone.name: phone for phone in phones}