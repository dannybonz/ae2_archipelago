from BaseClasses import Item

class AE2Item(Item):
	game: str = "Ape Escape 2"

item_id_from_name: dict[str, int] = {
	#Gadgets
	"Monkey Net": 1,
	"Stun Club": 2,
	"Monkey Radar": 3,
	"Water Net": 4,
	"Dash Hoop": 5,
	"Catapult": 6,
	"Sky Flyer": 7,
	"R.C. Car": 8,
	"Bananarang": 9,
	"Water Cannon": 10,
	"Electro Magnet": 11,
	"Power Punch": 12,
	"Pipotchi": 13,
	"See-All Scope": 14,

	#Progression
	"World Key": 101,
	"Victory": 102,

	#Filler
	"Jacket": 201,
	"Cookie": 202,
	"Deluxe Cookie": 203,
	"Explosive Pellet": 204,
	"Guided Pellet": 205,
	"Gold Coin": 206,
	"10 Gold Coins": 207,
	"20 Gold Coins": 208,
	"Case of Explosive Pellets": 209,
	"Case of Guided Pellets": 210,

	#Other
	"Air Crawl": 300,

	#Other
	"Glitched Item": 500
}

gadget_aliases = {
	"Net": "Monkey Net",
	"Time Net": "Monkey Net",
	"Club": "Stun Club",
	"Radar": "Monkey Radar",
	"Hoop": "Dash Hoop",
	"Super Hoop": "Dash Hoop",
	"Sling": "Catapult",
	"Slingshot": "Catapult",
	"Slingback Shooter": "Catapult",
	"Slingback": "Catapult",
	"Flyer": "Sky Flyer",
	"RC Car": "R.C. Car",
	"Car": "R.C. Car",
	"Magnet": "Electro Magnet",
	"Magic Punch": "Power Punch",
	"Punch": "Power Punch"
}

item_name_from_id: dict[int, str] = {v: k for k, v in item_id_from_name.items()}