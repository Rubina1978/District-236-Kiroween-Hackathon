class Score:
    def __init__(self):
        self.points = 0

    def give_points(self, points, multiplier):
        self.points += (points * multiplier)
    
    def return_points(self):
        return self.points
