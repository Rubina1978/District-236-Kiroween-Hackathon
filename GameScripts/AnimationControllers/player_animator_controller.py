class PlayerAnimator:
    def __init__(self, player_idle_camerafacing, player_idle_forward, player_idle_left, player_run_camerafacing, player_run_forward, player_run_left):
        self.player_idle_camerafacing = player_idle_camerafacing
        self.player_idle_forward = player_idle_forward
        self.player_idle_left = player_idle_left
        self.player_run_camerafacing = player_run_camerafacing
        self.player_run_forward = player_run_forward
        self.player_run_left = player_run_left
    
    def idle_left(self):
        return self.player_idle_left
    
    def idle_camerafacing(self):
        return self.player_idle_camerafacing
    
    def idle_forward(self):
        return self.player_idle_forward

    def run_camerafacing(self):
        return self.player_run_camerafacing
    
    def run_forward(self):
        return self.player_run_forward
    
    def run_left(self):
        return self.player_run_left