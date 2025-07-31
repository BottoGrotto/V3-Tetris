# I thought this would make having the different colors for the shapes easier. Kinda did
class Color:
    def __init__(self, color):
        self.color = color

    def __sub__(self, other):
        "Allows you to subtract a part of the color class with an int"
        if isinstance(other, int):
            tmp_color = self.color.copy()
            for i, val in enumerate(self.color):
                if val != 0 and val - other >= 0:
                    tmp_color[i] = val - other
        return tuple(tmp_color)
    
    def colorize(self):
        return tuple(self.color)
        