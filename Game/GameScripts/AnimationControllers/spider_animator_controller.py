class SpiderAnimator:
    def __init__(
            self, spider_camera_facing,
            spider_death,
            spider_forward_facing,
            spider_idle,
            spider_left_facing,
            spider_leftBottom_facing,
            spider_leftTop_facing,
            spider_right_facing,
            spider_rightBottom_facing,
            spider_rightTop_facing
        ):

        self.spider_camera_facing = spider_camera_facing
        self.spider_death = spider_death
        self.spider_forward_facing = spider_forward_facing
        self.spider_idle = spider_idle
        self.spider_left_facing = spider_left_facing
        self.spider_leftBottom_facing = spider_leftBottom_facing
        self.spider_leftTop_facing = spider_leftTop_facing
        self.spider_right_facing = spider_right_facing
        self.spider_rightBottom_facing = spider_rightBottom_facing
        self.spider_rightTop_facing = spider_rightTop_facing

    def idle(self):
        return self.spider_idle
    
    def death(self):
        return self.spider_death
    
    def move_camerafacing(self):
        return self.spider_camera_facing
    
    def move_right(self):
        return self.spider_right_facing
    
    def move_rightBottom(self):
        return self.spider_rightBottom_facing
    
    def move_rightTop(self):
        return self.spider_rightTop_facing
    
    def move_left(self):
        return self.spider_left_facing
    
    def move_leftBottom(self):
        return self.spider_leftBottom_facing
    
    def move_leftTop(self):
        return self.spider_leftTop_facing
    
    def move_forward(self):
        return self.spider_forward_facing
    