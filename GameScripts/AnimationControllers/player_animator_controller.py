class PlayerAnimator:
    def __init__(
            self, player_idle_camerafacing, 
            player_idle_forward, 
            player_idle_left,
            player_idle_leftBottom,
            player_idle_leftTop,
            player_idle_right,
            player_idle_rightBottom,
            player_idle_rightTop,
            player_run_camerafacing, 
            player_run_forward, 
            player_run_left,
            player_run_leftBottom,
            player_run_leftTop,
            player_run_rightBottom,
            player_run_rightTop,
            player_run_right
        ):

        self.player_idle_camerafacing = player_idle_camerafacing
        self.player_idle_forward = player_idle_forward
        self.player_idle_left = player_idle_left
        self.player_idle_leftBottom = player_idle_leftBottom
        self.player_idle_leftTop = player_idle_leftTop
        self.player_idle_right = player_idle_right
        self.player_idle_rightBottom = player_idle_rightBottom
        self.player_idle_rightTop = player_idle_rightTop
        self.player_run_camerafacing = player_run_camerafacing
        self.player_run_forward = player_run_forward
        self.player_run_left = player_run_left
        self.player_run_leftBottom = player_run_leftBottom
        self.player_run_leftTop = player_run_leftTop
        self.player_run_right = player_run_right
        self.player_run_rightBottom = player_run_rightBottom
        self.player_run_rightBottom = player_run_rightTop
    
    def idle_left(self):
        return self.player_idle_left
    
    def idle_leftBottom(self):
        return self.player_idle_leftBottom
    
    def idle_leftTop(self):
        return self.player_idle_leftTop
    
    def idle_camerafacing(self):
        return self.player_idle_camerafacing
    
    def idle_forward(self):
        return self.player_idle_forward
    
    def idle_right(self):
        return self.player_idle_right
    
    def idle_rightBottom(self):
        return self.player_idle_rightBottom
    
    def idle_rightTop(self):
        return self.player_idle_rightTop

    def run_camerafacing(self):
        return self.player_run_camerafacing
    
    def run_forward(self):
        return self.player_run_forward
    
    def run_left(self):
        return self.player_run_left
    
    def run_leftBottom(self):
        return self.player_run_leftBottom
    
    def run_leftTop(self):
        return self.player_run_leftTop
    
    def run_right(self):
        return self.player_run_right
    
    def run_rightBottom(self):
        return self.player_run_rightBottom
    
    def run_rightTop(self):
        return self.player_run_rightTop