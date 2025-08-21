import random
from shape import Square, L_1, L_2, T, I, Z_1, Z_2
from timer import Timer
from color import Color

class ShapeSpawner:
    def __init__(self):
        self.options = [Square, L_1, L_2, T, I, Z_1, Z_2]
        self.colors = [Color([255, 0, 0]), Color([0, 255, 0]), Color([0, 0, 255]), Color([0, 255, 255]), Color([255, 255, 0]), Color([255, 0, 255]), Color([255, 180, 0]), Color([122, 122, 122])]
        self.spawn_timer = Timer(2000)
        self.spawn_timer.start(loop=True)
        self.bag = []
        self.generate_bag()

    def random_shape(self):
        """Chooses a random shape to spawn from the options list.
        \nDeprecated: Use pull_randomly_from_bag instead for balancing purposes."""
        return self.options[random.randint(0, len(self.options) - 1)]()
    
    def generate_bag(self):
        """Generates a bag of shapes so that each shape is guaranteed to be spawned once before any shape is repeated."""
        list_to_shuffle = self.options.copy()
        random.shuffle(list_to_shuffle)
        for i in range(0, len(list_to_shuffle)):
            self.bag.append(list_to_shuffle[i])
    
    def pull_randomly_from_bag(self):
        """Pulls a random shape from the bag and returns it. If the bag is empty, it generates a new bag."""
        choice = random.randint(0, len(self.bag)-1)

        shape = self.bag.pop(choice)()
        
        if len(self.bag) == 0:
            self.generate_bag()

        return shape
    