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
player_run_camerafacing = [
    "",
]
player_run_forward = [
    "",
]
player_run_left = [
    "",
]

def animator_interface(type):
    """ Function for selecting animators """
    
    if type == "player":
        return PlayerAnimator(player_idle_camerafacing=player_idle_camerafacing, player_idle_forward=player_idle_forward, player_idle_left=player_idle_left)

    return 0