from dataclasses import dataclass
from Options import Choice, Range, Toggle, PerGameCommonOptions, DeathLink, OptionCounter, OptionGroup, OptionList

#Playthrough

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

#Locations

class MessagePhoneLocations(Toggle):
    """
    Adds locations for activating each message phone.

    *Note that playing as Kakeru will disable message phones.
    """
    display_name = "Message Phone Locations"
    default = False

class GotchaBoxLocations(Range):
    """
    Determines how many locations can be obtained through usage of the Gotcha Box.
    Please be mindful of other players in your world when increasing this number.
    """
    display_name = "Gotcha Box Locations"
    range_start = 0
    range_end = 999
    default = 0

class GotchaBoxGating(Choice):
    """
    Determines how new items will be made accessible from the Gotcha Box.
    To prevent excessive grinding, logic will not always expect you to obtain all accessible items from the Gotcha Box.
    More items will be logically expected as you progress through the game.

    - none: All items within the Gotcha Box are accessible from the beginning. This does not mean you are logically expected to immediately obtain them all.
    - levels: More items will become available from the Gotcha Box as you unlock more levels.
    - restock_items: More items will become available from the Gotcha Box as you receive "Gotcha Box Restock" items.
    """
    display_name = "Gotcha Box Gating"
    option_none = 0
    option_levels = 1
    option_restock_items = 2
    default = 1

class GotchaBoxForcedFillerPercentage(Range):
    """
    Determines a percentage of Gotcha Box locations that will be forced to contain filler items.
    """
    display_name = "Gotcha Box Forced Filler Percentage"
    range_start = 0
    range_end = 100
    default = 50

#Items

class StartingGadgets(OptionList):
    """
    Determines which gadgets you will begin the game with.
    You may enter "Random" multiple times to receive multiple random gadgets.

    Starting without the Monkey Net requires that message phone or Gotcha Box locations be enabled.

    Valid names are: "Random", "Monkey Net", "Stun Club", "Monkey Radar", "Dash Hoop", "Catapult", "Sky Flyer", "R.C. Car", "Bananarang", "Water Cannon", "Electro Magnet", "Power Punch"
    """
    display_name = "Starting Gadgets"
    valid_keys = ["Random", "Monkey Net", "Stun Club", "Monkey Radar", "Dash Hoop", "Catapult", "Sky Flyer", "R.C. Car", "Bananarang", "Water Cannon", "Electro Magnet", "Power Punch"]
    default = ["Monkey Net", "Stun Club"]

class ExtraWorldKeys(Range):
    """
    Adds extra "World Key" items to the pool, making it easier to unlock new levels.
    """
    display_name = "Extra World Keys"
    range_start = 0
    range_end = 20
    default = 0

class ShuffleCollectibleFiller(Toggle):
    """
    Adds filler items for each unlockable Monkey Fable, Movie, Soundtrack, Comic Strip, Concept Artwork, Secret Photo and Stage Photo.
    """
    display_name = "Shuffle Collectible Filler"
    default = False

class ShuffleWaterNet(Toggle):
    """
    Determines whether to lock the Water Net behind receiving an item.
    If this is enabled and you haven't received the Water Net, then touching water will instantly cause you to lose a Cookie and respawn.
    """
    display_name = "Shuffle Water Net"
    default = True

#Logic & Tricks

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
   
class TrapPercentage(Range):
    """
    Determines the percentage of filler items that will be replaced with trap items.
    """
    display_name = "Trap Percentage"
    range_start = 0
    range_end = 100
    default = 0

class LazyCameraTrapWeight(Range):
    """
    This trap causes the camera to temporarily stop following you.
    A higher number means that you are more likely to see the given trap. A value of 0 means the trap will not appear.
    """
    display_name = "Lazy Camera Trap Weight"
    range_start = 0
    range_end = 100
    default = 50    

class RocketBootsTrapWeight(Range):
    """
    This trap causes you to temporarily run at incredible speeds.
    A higher number means that you are more likely to see the given trap. A value of 0 means the trap will not appear.
    """
    display_name = "Rocket Boots Trap Weight"
    range_start = 0
    range_end = 100
    default = 50   

class SlownessTrapWeight(Range):
    """
    This trap causes you to temporarily run incredibly slowly.
    A higher number means that you are more likely to see the given trap. A value of 0 means the trap will not appear.
    """
    display_name = "Slowness Trap Weight"
    range_start = 0
    range_end = 100
    default = 50   

@dataclass
class AE2Options(PerGameCommonOptions):
    death_link: DeathLink
    goal: Goal
    world_key_behaviour: WorldKeyBehaviour
    level_shuffle: LevelShuffle
    randomise_starting_room: RandomiseStartingRoom
    music_randomisation: MusicRandomisation
    playable_character: PlayableCharacter
    message_phone_locations: MessagePhoneLocations
    gotcha_box_locations: GotchaBoxLocations
    gotcha_box_gating: GotchaBoxGating
    gotcha_box_forced_filler_percentage: GotchaBoxForcedFillerPercentage
    starting_gadgets: StartingGadgets
    extra_world_keys: ExtraWorldKeys
    shuffle_water_net: ShuffleWaterNet
    shuffle_collectible_filler: ShuffleCollectibleFiller
    logic_difficulty: LogicDifficulty
    hidden_monkey_logic: HiddenMonkeyLogic
    damage_boost_logic: DamageBoostLogic
    air_crawl_logic: AirCrawlLogic
    air_crawl_behaviour: AirCrawlBehaviour
    boost_jump_logic: BoostJumpingLogic
    boost_fly_logic: BoostFlyingLogic
    long_jump_logic: LongJumpingLogic
    trap_percentage: TrapPercentage
    lazy_camera_trap_weight: LazyCameraTrapWeight
    rocket_boots_trap_weight: RocketBootsTrapWeight
    slowness_trap_weight: SlownessTrapWeight

option_groups = [
    OptionGroup("AP Settings", [DeathLink]),
    OptionGroup("Playthrough", [Goal, WorldKeyBehaviour, LevelShuffle, RandomiseStartingRoom, MusicRandomisation, PlayableCharacter]),
    OptionGroup("Locations", [MessagePhoneLocations, GotchaBoxLocations, GotchaBoxGating, GotchaBoxForcedFillerPercentage]),
    OptionGroup("Items", [StartingGadgets, ExtraWorldKeys, ShuffleWaterNet, ShuffleCollectibleFiller]),
    OptionGroup("Logic & Tricks", [LogicDifficulty, HiddenMonkeyLogic, DamageBoostLogic, AirCrawlLogic, AirCrawlBehaviour, BoostJumpingLogic, BoostFlyingLogic, LongJumpingLogic]),
    OptionGroup("Traps", [TrapPercentage, LazyCameraTrapWeight, RocketBootsTrapWeight, SlownessTrapWeight]),
]    