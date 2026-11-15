# Main Interface for Animator
from .AnimationControllers.player_animator_controller import PlayerAnimator

player_idle_camerafacing = [
    "DylanFiles/Artwork/Characters/Player/Idle/Camera/sprite_idle0.png",
    "DylanFiles/Artwork/Characters/Player/Idle/Camera/sprite_idle1.png"
]
player_idle_forward = [
    "DylanFiles/Artwork/Characters/Player/Idle/Forward/sprite_idle_forward0.png",
    "DylanFiles/Artwork/Characters/Player/Idle/Forward/sprite_idle_forward1.png"
]
player_idle_left = [
    "DylanFiles/Artwork/Characters/Player/Idle/Left/sprite_idle_left0.png",
    "DylanFiles/Artwork/Characters/Player/Idle/Left/sprite_idle_left1.png",
    "DylanFiles/Artwork/Characters/Player/Idle/Left/sprite_idle_left2.png",
    "DylanFiles/Artwork/Characters/Player/Idle/Left/sprite_idle_left3.png"
]
player_idle_right = [
    "DylanFiles/Artwork/Characters/Player/Idle/Right/sprite_idle_right0.png",
    "DylanFiles/Artwork/Characters/Player/Idle/Right/sprite_idle_right1.png",
    "DylanFiles/Artwork/Characters/Player/Idle/Right/sprite_idle_right2.png",
    "DylanFiles/Artwork/Characters/Player/Idle/Right/sprite_idle_right3.png"
]
player_run_camerafacing = [
    "DylanFiles/Artwork/Characters/Player/Run/Camera/sprite_run0.png",
    "DylanFiles/Artwork/Characters/Player/Run/Camera/sprite_run1.png",
    "DylanFiles/Artwork/Characters/Player/Run/Camera/sprite_run2.png",
    "DylanFiles/Artwork/Characters/Player/Run/Camera/sprite_run3.png"
]
player_run_forward = [
    "DylanFiles/Artwork/Characters/Player/Run/Forward/sprite_run_forward0.png",
    "DylanFiles/Artwork/Characters/Player/Run/Forward/sprite_run_forward1.png",
    "DylanFiles/Artwork/Characters/Player/Run/Forward/sprite_run_forward2.png",
    "DylanFiles/Artwork/Characters/Player/Run/Forward/sprite_run_forward3.png"
]
player_run_left = [
    "DylanFiles/Artwork/Characters/Player/Run/Left/sprite_run_left0.png",
    "DylanFiles/Artwork/Characters/Player/Run/Left/sprite_run_left1.png",
    "DylanFiles/Artwork/Characters/Player/Run/Left/sprite_run_left2.png",
    "DylanFiles/Artwork/Characters/Player/Run/Left/sprite_run_left3.png"
]
player_run_right = [
    "DylanFiles/Artwork/Characters/Player/Run/Right/sprite_run_right0.png",
    "DylanFiles/Artwork/Characters/Player/Run/Right/sprite_run_right1.png",
    "DylanFiles/Artwork/Characters/Player/Run/Right/sprite_run_right2.png",
    "DylanFiles/Artwork/Characters/Player/Run/Right/sprite_run_right3.png"
]

def animator_interface(type):
    """ Function for selecting animators """
    
    if type == "player":
        return PlayerAnimator(player_idle_camerafacing=player_idle_camerafacing, player_idle_forward=player_idle_forward, player_idle_left=player_idle_left, player_idle_right=player_idle_right, player_run_camerafacing=player_run_camerafacing, player_run_forward=player_run_forward, player_run_left=player_run_left, player_run_right=player_run_right)

    return 0