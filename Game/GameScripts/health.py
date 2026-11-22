

class LifeLine:
    def __init__(self, lives=3, max_lives=5):
        self.max_lives = max_lives
        self.lives = min(lives, max_lives)
        
    
    def gain(self):
        self.lives = min(self.lives + 1, self.max_lives)

    def lose(self):
        self.lives = max(self.lives - 1, 0)

    def is_dead(self):
        return self.lives == 0
