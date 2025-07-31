import pygame
from pygame import Vector2 as vec2
from timer import Timer

class Shape:
    """Shape class to represent a shape object"""
    def __init__(self, id):
        self.id = id
        self.shape = None
        self.pos = vec2(4, 0)
        self.falling = True
        # This is the speed that the shape will fall at
        self.falling_speed = Timer(250)
        
        # This is the speed that the shape will move side to side at
        self.move_speed = Timer(75)
        self.move_speed.start(loop=True)

        self.can_rotate = True
        self.allowed_to_rotate = True

        self.current_falling_speed = 250
    
    def render_ghost(self, grid, BOX_SIZE, screen, style):
        """Renders a ghost shape at the first collision point"""
        # Creates a copy of the current position of the shape
        tmpPos = self.pos.copy()

        # Default values
        isFalling = True
        render = True

        # Shifts the ghost to the bottom of the shape so it doesn't collide with itself
        tmpPos.y += self.shape[-1].y + 1

        # Checks if the ghost collides with anything after this shift, if it did it no longer renders it and considers it not falling
        for pos in self.shape:
            x = int(tmpPos.x + pos.x)
            y = int(tmpPos.y + pos.y) + 1
            if y >= len(grid) or ((grid[y][x] == self.id and vec2(y, x) not in self.shape) if y < len(grid) else False) or (grid[y][x] != self.id and vec2(y, x) not in self.shape and grid[y][x] != 0) if y <= len(grid) else False:
                isFalling = False
                render = False
        # If the shift was out of the grid it doesn't consider it falling
        if tmpPos.y > len(grid):
            isFalling = False

        # If its falling it will move it down one then check if it collided with anything, and repeat until it collides, then it no longer moves down
        while isFalling:
            for i, pos in enumerate(self.shape):
                x = int(tmpPos.x + pos.x)
                y = int(tmpPos.y + pos.y) + 1
                if y < len(grid):
                    if y >= len(grid) or ((grid[y][x] == self.id and vec2(y, x) not in self.shape) if y < len(grid) else False) or (grid[y][x] != self.id and vec2(y, x) not in self.shape and grid[y][x] != 0) if y <= len(grid) else False:
                        isFalling = False
                        break
                else:
                    isFalling = False
                    
                    break
            if isFalling:
                tmpPos.y += 1

        # Renders the ghost shape
        if render:
            for i, pos in enumerate(self.shape):
                x = int(tmpPos.x + pos.x)
                y = int(tmpPos.y + pos.y)
                pygame.draw.rect(screen, (20, 20, 20), ((x * BOX_SIZE, y * BOX_SIZE), (BOX_SIZE, BOX_SIZE)), width=style, border_radius=5)
                pygame.draw.rect(screen, (46, 46, 46), ((x * BOX_SIZE + style, y * BOX_SIZE + style), (BOX_SIZE-style, BOX_SIZE-style)), border_radius=5)
        return screen
    
    def check_valid_pos(self, tmp_shape, grid):
        """Checks if a rotation was valid"""
        for pos in tmp_shape:
            x = int(pos.x + self.pos.x)
            y = int(pos.y + self.pos.y)
            # Makes sure that it doesn't rotate outside of the grid                                                                          Makes sure that the shape doesn't collide with another shape or itself. Kinda complicated logic but if you look deep you'll understand it. HAHAHA
            if pos.x + self.pos.x < 0 or pos.x + self.pos.x >= len(grid[0]) or pos.y + self.pos.y < 0 or pos.y + self.pos.y >= len(grid) or ((grid[y][x] == self.id or grid[y][x] != self.id and grid[y][x] != 0) and vec2(y, x) not in tmp_shape):
                return False
        return True

    def rotate(self, grid):
        """Attempts to rotate the shape. If any of the pieces are outside of the Grids bounds or is inside of another shape it doesn't rotate it. Otherwise it rotates it"""
        can_rotate = True
        tmp_shape = self.shape.copy()

        for i, pos in enumerate(tmp_shape):
            tmp_shape[i] = pos.rotate(90)
        
        can_rotate = self.check_valid_pos(tmp_shape, grid)

        if not can_rotate:
            return False
            
        self.shape = tmp_shape

        # Sorts the shapes vectors
        self.sort()
        return True

    def sorted(self):
        """Checks if the list is sorted by height with the lowest down on the screen last"""
        last_pos = self.shape[0]
        for pos in self.shape:
            if pos.y < last_pos.y:
                return False
            last_pos = pos
        return True
    
    # Sorts the shapes shape for collison checking, so it doesn't collide with itself
    def sort(self):
        """Utilizes Bubble Sort to sort the list from smallest to largest"""
        # Sorts until it is sorted
        while not self.sorted():
            for i, pos1 in enumerate(self.shape):
                for j, pos2 in enumerate(self.shape):
                    if pos1 == pos2:
                        continue
                    if pos1.y < pos2.y:
                        tmp = self.shape[i]
                        self.shape[i] = self.shape[j]
                        self.shape[j] = tmp
                       
    def input(self, grid, sounds):
        """Uses pygames built in key pressed method to get all keys pressed and checks if that movement is allowed using the move function and the direction"""
        # self.falling_speed.duration = 250
        keys = pygame.key.get_pressed()
        if self.move_speed.has_expired():
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                if self.move(grid, -1):
                    sounds[0].play()
                # self.falling_speed.duration = 250
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                if self.move(grid, 1):
                    sounds[0].play()
                # self.falling_speed.duration = 250
        
        if (keys[pygame.K_UP] or keys[pygame.K_w]) and self.allowed_to_rotate:
            if self.can_rotate:
                if self.rotate(grid):
                    sounds[1].play()
                self.can_rotate = False

        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.falling_speed.duration = max(self.current_falling_speed - 150, 25)
        # if keys[pygame.K_SPACE]:
        #     self.falling_speed.duration = 25

    def move(self, grid, direction):
        """Checks if the shape is falling, then checks the side collisons and if it can move it shifts it over by 1 in that direction"""
        if self.falling:
            if not self.check_collision_sides(grid, direction, self.shape):
                self.pos.x += direction
                return True
        return False

    def check_collision_sides(self, grid, direction, shape):
        """Uses a similar conditional to down just adjusted slightly for movement left and right"""
        for pos in shape:
            x = int(self.pos.x + pos.x) + direction
            y = int(self.pos.y + pos.y)
            # Checks if out of bounds     Checks if the position it wants to move to is occupied by a shape with the same id other then itself      Checks if the desired position is taken by a shape that is a different id avoids checking itself
            if x < 0 or x >= len(grid[0]) or ((grid[y][x] == self.id and vec2(y, x) not in shape) if x < len(grid[0]) else False) or (grid[y][x] != self.id and vec2(y, x) not in shape and grid[y][x] != 0) if x <= len(grid[0]) else False:
                return True
        return False

    def check_collision_down(self, grid):
        """Uses a similar conditional to sides just adjusted slightly for movement down"""
        for pos in self.shape:
            x = int(self.pos.x + pos.x)
            y = int(self.pos.y + pos.y) + 1
             # Checks if out of bounds     Checks if the position it wants to move to is occupied by a shape with the same id other then itself      Checks if the desired position is taken by a shape that is a different id avoids checking itself
            if y >= len(grid) or ((grid[y][x] == self.id and vec2(y, x) not in self.shape) if y < len(grid) else False) or (grid[y][x] != self.id and vec2(y, x) not in self.shape and grid[y][x] != 0) if y <= len(grid) else False:
                return True
        return False
    
    def remove_from_shapes(self, shapes):
        """It removes itself from the shapes list"""
        shapes.remove(self)
        return shapes
    
    def draw(self, grid):
        """'Draws the shape to the screen by setting the grid at its positions on the grid to its id"""
        for pos in self.shape:
            x = int(self.pos.x + pos.x)
            y = int(self.pos.y + pos.y)
            grid[y][x] = self.id
        return grid

    def update(self, grid, sounds):
        """Checks for user input then checks for collisions then moves it down and draws it if it can, otherwise it sets it to no longer falling"""
        self.input(grid, sounds)
        if self.falling and self.falling_speed.has_expired():
            if self.check_collision_down(grid):
                self.falling = False
                sounds[2].play()
            else:
                self.pos.y += 1
        
        return self.draw(grid)
                

# The following are all of the shapes. self.shape is a list containing pygames vec2 class to represent the shape, can easily make custom shapes with correct collision!
class Square(Shape):
    def __init__(self):
        super().__init__(1)
        self.shape = [vec2(0, 0), vec2(1, 0), vec2(0, 1), vec2(1, 1)]
        self.allowed_to_rotate = False

class L_1(Shape):
    def __init__(self):
        super().__init__(2)
        self.shape = [vec2(-1, 0), vec2(0, 0), vec2(1, 0), vec2(1, 1)]
        self.sort()

class L_2(Shape):
    def __init__(self):
        super().__init__(3)
        self.shape = [vec2(-1, 0), vec2(0, 0), vec2(1, 0), vec2(-1, 1)]
        self.sort()

class T(Shape):
    def __init__(self):
        super().__init__(4)
        self.shape = [vec2(0, 0), vec2(0, 1), vec2(1, 0), vec2(-1, 0)]
        self.sort()

class I(Shape):
    def __init__(self):
        super().__init__(5)
        self.shape = [vec2(-1, 0), vec2(0, 0), vec2(1, 0), vec2(2, 0)]
        self.sort()

class Z_1(Shape):
    def __init__(self):
        super().__init__(6)
        self.shape = [vec2(-1, 0), vec2(0, 0), vec2(0, 1), vec2(1, 1)]
        self.sort()

class Z_2(Shape):
    def __init__(self):
        super().__init__(7)
        self.shape = [vec2(-1, 1), vec2(0, 0), vec2(0, 1), vec2(1, 0)]
        self.sort()



if __name__ == "__main__":
    sq = Square()
    print(sq.shape)
    sq.rotate()
    print(sq.shape)