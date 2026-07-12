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

class StartingGadgets(OptionList):
    """
    Determines which gadgets you will begin the game with, in addition to the Monkey Net.
    You may enter "Random" multiple times to receive multiple random gadgets.

    Valid names are: "Random", "Stun Club", "Monkey Radar", "Dash Hoop", "Catapult", "Sky Flyer", "R.C. Car", "Bananarang", "Water Cannon", "Electro Magnet", "Power Punch"
    """
    display_name = "Starting Gadgets"
    valid_keys = ["Random", "Stun Club", "Monkey Radar", "Dash Hoop", "Catapult", "Sky Flyer", "R.C. Car", "Bananarang", "Water Cannon", "Electro Magnet", "Power Punch"]
    default = ["Stun Club"]

class ShuffleWaterNet(Toggle):
    """
    Determines whether to lock the Water Net behind receiving an item.
    If this is enabled and you haven't received the Water Net, then touching water will instantly cause you to respawn.
    """
    display_name = "Shuffle Water Net"
    default = True

class ShuffleAirCrawl(Toggle):
    """
    Determines whether to lock the Air Crawl glitch behind receiving an item.
    If this is enabled and you haven't received the Air Crawl item, then you will be unable to perform the glitch.
    """
    display_name = "Shuffle Air Crawl"
    default = False

class PlayableCharacter(Choice):
    """
    Determines which character you will play as.

    - hikaru: Play as Hikaru (Jimmy). Pipotchi will tag along to help you out.
    - kakeru: Play as Kakeru (Spike). You won't have Pipotchi's help. 
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
    world_key_behaviour: WorldKeyBehaviour
    playable_character: PlayableCharacter
    starting_gadgets: StartingGadgets
    shuffle_water_net: ShuffleWaterNet
    shuffle_air_crawl: ShuffleAirCrawl
    logic_difficulty: LogicDifficulty
    hidden_monkey_logic: HiddenMonkeyLogic
    damage_boost_logic: DamageBoostLogic
    air_crawl_logic: AirCrawlLogic
    boost_jump_logic: BoostJumpingLogic
    boost_fly_logic: BoostFlyingLogic
    long_jump_logic: LongJumpingLogic

option_groups = [
    OptionGroup("AP Settings", [DeathLink]),
    OptionGroup("Playthrough", [Goal, LevelShuffle, WorldKeyBehaviour, PlayableCharacter, StartingGadgets, ShuffleWaterNet, ShuffleAirCrawl]),
    OptionGroup("Logic & Tricks", [LogicDifficulty, HiddenMonkeyLogic, DamageBoostLogic, AirCrawlLogic, BoostJumpingLogic, BoostFlyingLogic, LongJumpingLogic]),
]    