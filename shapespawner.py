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
        """Chooses a random shape to spawn"""
        return self.options[random.randint(0, len(self.options) - 1)]()
    
    def generate_bag(self):
        list_to_shuffle = self.options.copy()
        random.shuffle(list_to_shuffle)
        for i in range(0, len(list_to_shuffle)):
            self.bag.append(list_to_shuffle[i])
        
    def pull_randomly_from_bag(self):
        choice = random.randint(0, len(self.bag)-1)

        shape = self.bag.pop(choice)()
        
        if len(self.bag) == 0:
            self.generate_bag()

        return shape
    