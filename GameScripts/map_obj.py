import pygame

class GridMap:
    def __init__(self, grid):
        self.grid = grid

    def draw(self, screen):
        for row in range(len(self.grid)):
            for col in range(len(self.grid[row])):

                # Get the environment object
                obj = self.grid[row][col]

                if obj != 0:
                    if obj.get_type() == "box":
                        # Load its artwork
                        img = pygame.image.load(
                            "DylanFiles/Artwork/Environment/Objects/Box/" 
                            + obj.get_type() + "_1.png"
                        )

                        # Calculate its position on screen
                        x = col * 120
                        y = row * 120

                        # Draw the image
                        screen.blit(img, (x, y))
                    else:
                        # Load its artwork
                        img = pygame.image.load(
                            "DylanFiles/Artwork/Environment/Scenery/" 
                            + obj.get_type() + ".png"
                        )

                        # Calculate its position on screen
                        x = col * 120
                        y = row * 120

                        # Draw the image
                        screen.blit(img, (x, y))