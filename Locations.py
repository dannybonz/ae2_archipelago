from BaseClasses import Location
from .Monkeys import monkeys
from .Phones import phones
from .Levels import levels

class AE2Location(Location):
    game: str = "Ape Escape 2"

location_id_from_name: dict[str, int] = {}
for monkey in monkeys:
    location_id_from_name[monkey.get_location_name()] = monkey.id
for phone in phones:
    location_id_from_name[phone.get_location_name()] = phone.id
location_name_from_id: dict[int, str] = {v: k for k, v in location_id_from_name.items()}

location_groups = {}
for level in levels:
    location_groups[level.name] = {monkey.get_location_name() for monkey in level.monkeys} | {phone.get_location_name() for phone in level.phones}