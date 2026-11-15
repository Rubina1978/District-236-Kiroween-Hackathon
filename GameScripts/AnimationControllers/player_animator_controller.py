class PlayerAnimator:
    def __init__(self, player_idle_camerafacing, player_idle_forward, player_idle_left):
        self.player_idle_camerafacing = player_idle_camerafacing
        self.player_idle_forward = player_idle_forward
        self.player_idle_left = player_idle_left
    
    def idle_left(self):
        return self.player_idle_left
    
    def idle_camerafacing(self):
        return self.player_idle_camerafacing
    
    def idle_forward(self):
        return self.player_idle_forward