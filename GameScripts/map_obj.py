class GridMap:
    def __init__(self, grid):
        self.grid = grid

        # Collect every non-empty cell into a list of sprites so they can be
        # y-sorted and drawn together with the player in one group. The objects
        # are already pygame sprites (EnvrionmentObject), so they have .image
        # and .rect ready for the group.
        self.sprites = []
        for row in range(len(grid)):
            for col in range(len(grid[row])):
                obj = grid[row][col]
                if obj != 0:
                    self.sprites.append(obj)

    def get_sprites(self):
        """Return all environment sprites on this map."""
        return self.sprites
