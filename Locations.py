from BaseClasses import Location
from .Monkeys import monkeys

class AE2Location(Location):
    game: str = "Ape Escape 2"

location_id_from_name: dict[str, int] = {}
for monkey in monkeys:
    location_id_from_name[monkey.get_location_name()] = monkey.id
location_name_from_id: dict[int, str] = {v: k for k, v in location_id_from_name.items()}