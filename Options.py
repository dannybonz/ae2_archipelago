from dataclasses import dataclass
from Options import Choice, Range, Toggle, PerGameCommonOptions, DeathLink, OptionCounter, OptionGroup, OptionList

class Goal(Choice):
    """
    Determines your victory condition.

    - specter: Find your World Keys and complete the "Showdown with Specter!" boss fight.
    - final_specter: Find your World Keys, catch every monkey in the game and complete the "Final Showdown with Specter!" boss fight.
    """
    display_name = "Goal"
    option_specter = 0
    option_final_specter = 1
    default = 0

class LevelShuffle(Choice):
    """
    Randomises the order of level unlocks.
    Your final battle with Specter will always be placed at the end of the game.

    - off: Levels will appear in their default order.
    - separate: Levels and bosses will be shuffled separately.
    - mixed: Levels and bosses will be shuffled together.
    """
    display_name = "Level Shuffle"
    option_off = 0
    option_separate = 1
    option_mixed = 2
    default = 0

class RandomiseStartingRoom(Toggle):
    """
    Randomises the starting room of each level.
    """
    display_name = "Randomise Starting Room"
    default = False

class RandomiseAreaTransitions(Toggle):
    """
    Randomises the destinations of mid-level transitions.
    """
    display_name = "Randomise Area Transitions"
    default = False

class WorldKeyBehaviour(Choice):
    """
    Determines the behaviour of "World Key" items.

    - level: Each "World Key" item will unlock one additional level.
    - world: Each "World Key" item will unlock all levels up to (and including) the next boss fight.
    - alternating: "World Key" items will alternate between unlocking all levels leading up to the next boss fight, and unlocking the boss fight itself.
    """
    display_name = "World Key Behaviour"
    option_level = 0
    option_world = 1
    option_alternating = 2
    default = 2

class ExtraWorldKeys(Range):
    """
    Adds extra "World Key" items to the pool, making it easier to unlock new levels.
    """
    display_name = "Extra World Keys"
    range_start = 0
    range_end = 20
    default = 0

class MessagePhoneLocations(Toggle):
    """
    Adds locations for activating each message phone.
    """
    display_name = "Message Phone Locations"
    default = False

class StartingGadgets(OptionList):
    """
    Determines which gadgets you will begin the game with.
    You may enter "Random" multiple times to receive multiple random gadgets.

    Starting without the Monkey Net requires that message phone locations be enabled.

    Valid names are: "Random", "Monkey Net", "Stun Club", "Monkey Radar", "Dash Hoop", "Catapult", "Sky Flyer", "R.C. Car", "Bananarang", "Water Cannon", "Electro Magnet", "Power Punch"
    """
    display_name = "Starting Gadgets"
    valid_keys = ["Random", "Monkey Net", "Stun Club", "Monkey Radar", "Dash Hoop", "Catapult", "Sky Flyer", "R.C. Car", "Bananarang", "Water Cannon", "Electro Magnet", "Power Punch"]
    default = ["Monkey Net", "Stun Club"]

class ShuffleWaterNet(Toggle):
    """
    Determines whether to lock the Water Net behind receiving an item.
    If this is enabled and you haven't received the Water Net, then touching water will instantly cause you to respawn.
    """
    display_name = "Shuffle Water Net"
    default = True

class MusicRandomisation(Choice):
    """
    Randomises the music played throughout the game.

    - default: Music will not be touched by randomisation.
    - level: The music track for each level will be randomised. Levels with multiple music tracks will have each track randomised individually.
    - room: The music track for each individual room will be randomised.
    """
    display_name = "Music Randomisation"
    option_default = 0
    option_level = 1
    option_room = 2
    default = 0

class AirCrawlBehaviour(Choice):
    """
    Determines the behaviour of the "Air Crawl" glitch.

    - default: You can perform the Air Crawl glitch as normal.
    - patched: The Air Crawl glitch is impossible to perform.
    - item: The Air Crawl glitch can be performed after receiving the "Air Crawl" item.
    - progressive: The Air Crawl glitch can be performed after receiving two "Progressive Catapult" items.
    """
    display_name = "Air Crawl Behaviour"
    option_default = 0
    option_patched = 1
    option_item = 2
    option_progressive = 3
    default = 0

class PlayableCharacter(Choice):
    """
    Determines which character you will play as.

    - hikaru: Play as Hikaru (Jimmy). Pipotchi will tag along to help you out.
    - kakeru: Play as Kakeru (Spike). You won't have Pipotchi's help. 

    *Note that playing as Kakeru will disable message phones.
    """
    display_name = "Playable Character"
    option_hikaru = 0
    option_kakeru = 1
    default = 0

class LogicDifficulty(Choice):
    """
    Determines the overall difficulty of logic.
    Certain tricks or glitches can be enabled separately.

    - normal: You will be logically expected to have a majority of gadgets at your disposal.
    - hard: You will be logically expected to use gadgets in novel ways.
    - expert: You will be logically expected to make difficult jumps and use gadgets in unexpected ways. Hip drop attacks and rocket dives may be essential.
    """
    display_name = "Logic Difficulty"
    option_normal = 0
    option_hard = 1
    option_expert = 2
    default = 0    

class HiddenMonkeyLogic(Toggle):
    """
    If this option is enabled, certain well-hidden monkeys will logically expect the Monkey Radar or See-All Scope.
    This option is recommended for inexperienced players who do not already know where each monkey is located.
    """
    display_name = "Hidden Monkey Logic"
    default = False

class DamageBoostLogic(Toggle):
    """
    If this option is enabled, intentionally taking damage to pass through fire and other hazards will be logically expected.
    """
    display_name = "Damage Boost Logic"
    default = True

class AirCrawlLogic(Toggle):
    """
    If this option is enabled, using the Air Crawl glitch will be logically expected.
    """
    display_name = "Air Crawl Logic"
    default = False

class BoostJumpingLogic(Toggle):
    """
    If this option is enabled, swinging the net as you double jump before swapping to another gadget for increased height will be logically expected.
    """
    display_name = "Boost Jumping Logic"
    default = False

class BoostFlyingLogic(Toggle):
    """
    If this option is enabled, performing a boost jump into the Sky Flyer will be logically expected.
    """
    display_name = "Boost Flying Logic"
    default = False

class LongJumpingLogic(Toggle):
    """
    If this option is enabled, performing a neutral jump with the Dash Hoop will be logically expected.
    """
    display_name = "Long Jumping Logic"
    default = False  
   
@dataclass
class AE2Options(PerGameCommonOptions):
    death_link: DeathLink
    goal: Goal
    level_shuffle: LevelShuffle
    randomise_starting_room: RandomiseStartingRoom
    music_randomisation: MusicRandomisation
    world_key_behaviour: WorldKeyBehaviour
    extra_world_keys: ExtraWorldKeys
    message_phone_locations: MessagePhoneLocations
    playable_character: PlayableCharacter
    starting_gadgets: StartingGadgets
    shuffle_water_net: ShuffleWaterNet
    air_crawl_behaviour: AirCrawlBehaviour
    logic_difficulty: LogicDifficulty
    hidden_monkey_logic: HiddenMonkeyLogic
    damage_boost_logic: DamageBoostLogic
    air_crawl_logic: AirCrawlLogic
    boost_jump_logic: BoostJumpingLogic
    boost_fly_logic: BoostFlyingLogic
    long_jump_logic: LongJumpingLogic

option_groups = [
    OptionGroup("AP Settings", [DeathLink]),
    OptionGroup("Playthrough", [Goal, LevelShuffle, RandomiseStartingRoom, MusicRandomisation, WorldKeyBehaviour, ExtraWorldKeys, MessagePhoneLocations, PlayableCharacter, StartingGadgets, ShuffleWaterNet, AirCrawlBehaviour]),
    OptionGroup("Logic & Tricks", [LogicDifficulty, HiddenMonkeyLogic, DamageBoostLogic, AirCrawlLogic, BoostJumpingLogic, BoostFlyingLogic, LongJumpingLogic]),
]    