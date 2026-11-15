import random

class EnvrionmentObject:
    def __init__(self, type, artwork):
        self.type = type
        self.artwork = artwork
    
    def get_type(self):
        return self.type
    
    def get_artwork(self):
        return self.artwork

    def give_loot(self):
        items = [
            "junk",
            "spider",
            "health"
        ]
        if self.type == "box":
            return random.choice(items)
        else:
            return 0
