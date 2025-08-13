import pygame, sys
from shapespawner import ShapeSpawner
from utilities import Button, Slider
from color import Color
from pygame import Vector2 as vec2
from timer import Timer

pygame.font.init()
pygame.mixer.init()

BOX_SIZE = 40
FALLING_SPEED = 250

"""
    Screen state guide:
        '0': Main menu
        '0-1': Settings but in the main menu renderer
        '1': Game state, you are playing
        '2': You just lost and its waiting for input to continue to next screen
        '3': Game over screen
"""

class Game:
    def __init__(self, size):
        # Initializes the screen and clock and other necessary values
        self.screen = pygame.display.set_mode(size)
        self.clock = pygame.time.Clock()
        self.size = size

        self.grid = self.make_grid()
        self.score = 0
        self.style = 4
        self.current_falling_speed = FALLING_SPEED

        self.screen_state = '0'
        self.game_started = False
        self.paused = False
        
        # Default values for settings.txt
        musicVolume = 0.3
        effectVolume = 0.3
        show_grid_lines = False
        show_ghost = True

        # Attempts to load values from settings.txt, if not it uses default values
        with open("settings.txt", 'r') as settings:
            lines = settings.readlines()
            if len(lines) == 4:
                try:
                    musicVolume = int(lines[0].split(",")[1].replace("\n", ""))/100
                    effectVolume = int(lines[1].split(",")[1].replace("\n", ""))/100
                    show_grid_lines = lines[2].split(",")[1].replace("\n", "")
                    show_ghost = lines[3].split(",")[1].replace("\n", "")

                    if show_grid_lines == "True":
                        show_grid_lines = True
                    else:
                        show_grid_lines = False

                    if show_ghost == "True":
                        show_ghost = True
                    else:
                        show_ghost = False
                    
                except:
                    print("error loading settings - using default")

        self.draw_grid_lines = show_grid_lines
        self.show_ghost = show_ghost

        # Initilaizes music with saved or default audio level
        self.line_clear_sounds = [pygame.mixer.Sound("Assets/lineclear.mp3"), pygame.mixer.Sound("Assets/lineclear4.wav")]
        self.music = pygame.mixer.Sound("Assets/Tetris.mp3")
        self.gameover = pygame.mixer.Sound("Assets/gameover.mp3")
        self.movementSounds = [pygame.mixer.Sound("Assets/piecemoved.wav"), pygame.mixer.Sound("Assets/piecerotated.wav"), pygame.mixer.Sound("Assets/piecelanded.wav")]

        self.music.set_volume(musicVolume)
        for sound in self.line_clear_sounds:
            sound.set_volume(effectVolume)
        self.gameover.set_volume(effectVolume)
        for sound in self.movementSounds:
            sound.set_volume(effectVolume)

        # Creates the spawner object
        self.spawner = ShapeSpawner()

        # Populates the shapes list with a random starting shape and starts the falling loop
        self.shapes = [self.spawner.pull_randomly_from_bag()]
        self.shapes[-1].falling_speed.start(loop=True)
                   
        self.font = pygame.font.SysFont('Comic Sans MS', 30)

        # Initializing all of the buttons and sliders
        self.settingsButton = Button(vec2(self.size[0]/2, self.size[1] - 50), Color([0, 0, 0]), Color([0, 255, 0]), "Settings", center=True)
        self.backButton = Button(vec2(self.size[0]/2, self.size[1] - 50), Color([0, 0, 0]), Color([0, 255, 0]), "Back", center=True)
        self.showGridButton = Button(vec2(self.size[0]/2, self.size[1]/4), Color([0, 0, 0]), Color([255 if not self.draw_grid_lines else 0, 0 if not self.draw_grid_lines else 255, 0]), f"{self.draw_grid_lines}", center=True)
        self.mainMenuButton = Button(vec2(self.size[0] - 160, 0), Color([0, 0, 0]), Color([255, 255, 255]), "Main Menu", bgTransparent=True)
        self.showGhostButton = Button(vec2(self.size[0]/2, self.size[1]/8), Color([0, 0, 0]), Color([0, 255, 0]), f"{self.show_ghost}", center=True)

        self.musicSlider = Slider(vec2(self.size[0]/2, self.size[1]/2), vec2(self.size[0] - 100, 20), Color([255, 0, 0]), Color([0, 255, 0]), value=int(musicVolume * 100), center=True)
        self.effectsSlider = Slider(vec2(self.size[0]/2, self.size[1]/2 + 100), vec2(self.size[0] - 100, 20), Color([255, 0, 0]), Color([0, 255, 0]), value=int(effectVolume * 100), center=True)

        # This is initilization for animation start menu that kinda sucks but it works!
        self.animation_size = 30
        self.animation_direction = 1
        self.animation_speed = Timer(50)
        self.animation_speed.start(loop=True)

        # This is initilization for animation for game over
        self.next_block_speed = Timer(50)
        self.row = len(self.grid) - 1
        self.col = len(self.grid[0]) - 1
        self.next_block_speed.start(loop=True)
        self.wait_timer = Timer(500)


    def check_fail(self):
        """Checks if a shape is not falling and its at the top"""
        if len(self.shapes) >= 1:
            if not self.shapes[0].falling:
                if self.shapes[0].pos.y == 0:
                    return True
        return False
    
    def draw_fail_transition_forward(self):
        for i in range(len(self.grid) - 1, self.row, -1):
            for j in range(len(self.grid[i]) - 1, self.col, -1):
                pygame.draw.rect(self.screen, (25, 25, 25), ((j * BOX_SIZE, i * BOX_SIZE), (BOX_SIZE, BOX_SIZE)), width=self.style, border_radius=5)
                pygame.draw.rect(self.screen, (60, 60, 60), ((j * BOX_SIZE + self.style, i * BOX_SIZE + self.style), (BOX_SIZE-self.style, BOX_SIZE-self.style)), border_radius=5)
                # pygame.time.wait(50)
        # pygame.time.wait(1000)
        if self.row > -1 and self.col > -1:
            if self.next_block_speed.has_expired():
                self.row -= 2
                self.col -= 1
            return True
        else:
            return False
    
    def draw_fail_transition_backward(self):
        for i in range(len(self.grid) - 1, self.row, -1):
            for j in range(len(self.grid[i]) - 1, self.col, -1):
                pygame.draw.rect(self.screen, (25, 25, 25), ((j * BOX_SIZE, i * BOX_SIZE), (BOX_SIZE, BOX_SIZE)), width=self.style, border_radius=5)
                pygame.draw.rect(self.screen, (60, 60, 60), ((j * BOX_SIZE + self.style, i * BOX_SIZE + self.style), (BOX_SIZE-self.style, BOX_SIZE-self.style)), border_radius=5)
        
        if self.row < len(self.grid) - 1 and self.col < len(self.grid[0]) - 1:
            if self.next_block_speed.has_expired():
                self.row += 2
                self.col += 1
            return True
        else:
            return False
        
    def calculate_falling_speed(self, score):
        """Calculates the falling speed of a shape based on their score, fastest speed is 25ms between attempts at movement down"""
        delay = 250 - (score / 20)
        return max(delay, 25)

    def check_line_and_clear(self):
        """ Checks if the line is full and clears if necessary """
        clear_lines = []
        # loops over each line and checks if full, sets to clear then adds the row level to the clear_lines list
        for i in range(len(self.grid)-1, -1, -1):
            line_len = 0
            for j in range(0, len(self.grid[0])):
                if self.grid[i][j] != 0:
                    line_len += 1
            if line_len == len(self.grid[0]):
                for j in range(0, len(self.grid[0])):
                    self.grid[i][j] = 0
                clear_lines.append(i)

        # Sorts the lines that have been cleared and shifts everything down to the new y_level  
        clear_lines.sort()
        for i, y_level in enumerate(clear_lines):
            self.shift_grid(y_level)

        # Accurate score based on tetris wiki
        if len(clear_lines) == 4:
            self.score += 1200
        elif len(clear_lines) == 3:
            self.score += 300
        elif len(clear_lines) == 2:
            self.score += 100
        elif len(clear_lines) == 1:
            self.score += 40

        # Plays the sound if a line has been cleared
        if len(clear_lines) > 0:
            self.current_falling_speed = self.calculate_falling_speed(self.score)
            if len(self.shapes) > 0:
                self.shapes[0].falling_speed.duration = self.current_falling_speed
                self.shapes[0].current_falling_speed = self.current_falling_speed
            if len(clear_lines) == 4:
                self.line_clear_sounds[1].play()
            else:
                self.line_clear_sounds[0].play()
    
    def shift_grid(self, y_level):
        """ This shifts the grid down y_level places """
        for i in range(y_level, 0, -1):
            for j in range(0, len(self.grid[0])):
                tmp = self.grid[i-1][j]
                self.grid[i-1][j] = 0
                self.grid[i][j] = tmp
    
    def make_grid(self):
        """ This makes a 2D grid """
        arr = list(range(0, self.size[1] // BOX_SIZE))
        for i in range(len(arr)):
            arr[i] = list(range(0, self.size[0] // BOX_SIZE))
            for j in range(len(arr[i])):
                arr[i][j] = 0
        return arr
    
    def draw_boxes(self):
        """ Based on the id of the box it draws a colored box to represent different parts of tetris pieces """
        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                id = self.grid[i][j]
                if id != 0:
                    pygame.draw.rect(self.screen, self.spawner.colors[id-1] - 75, ((j * BOX_SIZE, i * BOX_SIZE), (BOX_SIZE, BOX_SIZE)), width=self.style, border_radius=5)
                    pygame.draw.rect(self.screen, self.spawner.colors[id-1].colorize(), ((j * BOX_SIZE + self.style, i * BOX_SIZE + self.style), (BOX_SIZE-self.style, BOX_SIZE-self.style)), border_radius=5)

    def clear_grid(self):
        """ Clears the grid of the falling shape by setting its value to 0.
            \nThis is so it doesn't display every position it has been, only where it is"""
        for shape in self.shapes:
             for pos in shape.shape:
                x = int(shape.pos.x + pos.x)
                y = int(shape.pos.y + pos.y)
                self.grid[y][x] = 0   
    
    def draw_grid(self):
        # Draws the grid lines to the screen

        # Draws lines in the horizontal direction
        y = BOX_SIZE
        for i in range(len(self.grid)):
            pygame.draw.line(self.screen, (69, 69, 69), (0, y), (self.size[0], y), 1)
            y += BOX_SIZE

        # Draws lines in the vertical direction
        x = BOX_SIZE
        for i in range(len(self.grid)):
            pygame.draw.line(self.screen, (69, 69, 69), (x, 0), (x, self.size[1]), 1)
            x += BOX_SIZE

    # This draws text at a pos with a size and color
    def draw_text(self, pos: tuple, text: str, size: int, color: tuple, draw=True, center=False):
        font = pygame.font.SysFont('Comic Sans MS', size)
        text_surface = font.render(f'{text}', True, color)
        render_pos = pos
        if center:
            render_pos = (render_pos[0] - text_surface.get_width()/2, render_pos[1])
        if draw:
            self.screen.blit(text_surface, render_pos)
        return text_surface

    # This utilizes the draw_text function to draw the score of the user
    def draw_score(self):
        self.draw_text((10, 0), self.score, 30, (255, 255, 255))

    # Function for settings button
    def set_state_settings(self):
        self.screen_state = "0-1"

    # Function for back button
    def back_button(self):
        self.screen_state = "0"

    # Function for the main menu button
    def main_menu_button(self):
        self.screen_state = "0"
    
    # Function for show grid (Toggles the draw_grid_lines variable and updates button values)
    def show_grid_button(self):
        if self.draw_grid_lines:
            self.draw_grid_lines = False
            self.showGridButton.text = "False"
            self.showGridButton.textColor = Color([255, 0, 0])
            self.showGridButton.configure_surface()
        else:
            self.draw_grid_lines = True
            self.showGridButton.text = "True"
            self.showGridButton.textColor = Color([0, 255, 0])
            self.showGridButton.configure_surface()

    # Function for show ghost (Toggles the show_ghost variable and updates button values)
    def show_ghost_button(self):
        if self.show_ghost:
            self.show_ghost = False
            self.showGhostButton.text = "False"
            self.showGhostButton.textColor = Color([255, 0, 0])
            self.showGhostButton.configure_surface()
        else:
            self.show_ghost = True
            self.showGhostButton.text = "True"
            self.showGhostButton.textColor = Color([0, 255, 0])
            self.showGhostButton.configure_surface()
    
    # Main loop for the game
    def run(self):
        while True:
            # Updates the caption to show FPS
            pygame.display.set_caption(f"Tetris  FPS: {int(self.clock.get_fps())}")
            
            mouse_buttons = pygame.mouse.get_pressed()
            events = pygame.event.get()

            # Clears the screen
            self.screen.fill((0, 0, 0))
            
            # Runs the game at 60 FPS (if possible)
            self.clock.tick(60)
            
            # Starting screen
            if self.screen_state == '0':
                self.draw_text((self.size[0]/8, 0), "Tetris", 100, (255, 0, 0))
                self.screen = self.settingsButton.update(screen=self.screen, func=self.set_state_settings, events=events)
                self.draw_text((self.size[0]/2, self.size[1]/2), "Press Space to Play", self.animation_size, (0, 0, 255), center=True)
                
                # Janky scale animation for press to play text
                if self.animation_speed.has_expired():
                    self.animation_size += self.animation_direction
                    if (self.animation_size >= 40 or self.animation_size <= 30):
                        self.animation_direction *= -1

            # Settings screen
            elif self.screen_state == '0-1':
                # Updates the buttons for back, grid, and ghost
                self.screen = self.backButton.update(screen=self.screen, func=self.back_button, events=events)

                self.screen = self.showGridButton.update(screen=self.screen, func=self.show_grid_button, events=events)
                self.screen = self.showGhostButton.update(screen=self.screen, func=self.show_ghost_button, events=events)

                # Draws the text above the grid Button and ghost Button
                self.draw_text((self.size[0]/2, self.size[1]/4 - 40), "Show Grid Lines", 30, (255, 255, 255), center=True)
                self.draw_text((self.size[0]/2, self.size[1]/8 - 40), "Show Ghost", 30, (255, 255, 255), center=True)

                 # Updates the sliders
                self.screen = self.musicSlider.update(screen=self.screen, mouse_buttons=mouse_buttons)
                self.screen = self.effectsSlider.update(screen=self.screen, mouse_buttons=mouse_buttons)

                # Draws the text and updates the music volume
                self.draw_text((self.size[0]/2, self.size[1]/2 - 50), f"Music Volume: {self.musicSlider.value}", 30, (255, 255, 255), center=True)
                self.music.set_volume((self.musicSlider.value / self.musicSlider.maxValue))

                # Draws the text and updates the music volume
                self.draw_text((self.size[0]/2, self.size[1]/2 + 50), f"Effect Volume: {self.effectsSlider.value}", 30, (255, 255, 255), center=True)
                val = (self.effectsSlider.value / self.effectsSlider.maxValue)
                for sound in self.line_clear_sounds:
                    sound.set_volume(val)
                self.gameover.set_volume(val)
                for sound in self.movementSounds:
                    sound.set_volume(val)

            # Playing state and end state
            if self.screen_state == '1':
                # Starts the music if it hasn't only on playing state
                if not self.game_started:
                    self.music.play(loops=100)
                    self.game_started = True

                # Only draws the lines if toggled
                if self.draw_grid_lines:
                    self.draw_grid()
                # Only draws ghost if toggled
                if self.show_ghost:
                    for shape in self.shapes: 
                        self.screen = shape.render_ghost(self.grid, BOX_SIZE, self.screen, self.style)
                # Draws all of the boxes on the grid (tetris pieces)
                self.draw_boxes()
                # Clears the grid for piece falling but only after the current grid has been drawn
                self.clear_grid()
                # Checks if any lines are full
                self.check_line_and_clear()
                # Draws the players score to the screen
                self.draw_score()

                # Displays main menu button if paused so you can go back to settings
                if self.paused:
                    self.screen = self.mainMenuButton.update(screen=self.screen, func=self.main_menu_button, events=events)

                # Shape falling and spawning logic
                # If there isn't a shape, spawn one and make it fall at the default falling speed using a timer class
                if len(self.shapes) == 0:
                    self.shapes.append(self.spawner.pull_randomly_from_bag())
                    self.shapes[-1].falling_speed.start(loop=True)
                    self.shapes[-1].falling_speed.duration = self.current_falling_speed
                    self.shapes[-1].current_falling_speed = self.current_falling_speed
                    
                
                # Checks if the game is paused, if not it runs fall logic for the shape that is currently falling
                if not self.paused:
                    for shape in self.shapes:
                        # Updates the shapes position and does all of the collision checking logic, along with input logic
                        shape.update(self.grid, self.movementSounds)
                        # Checks if the game is over if so sets state to game over state and resets values
                        if self.check_fail():
                            self.screen_state = '2'
                            self.game_started  = False
                            self.shapes = []
                            self.music.stop()
                            self.current_falling_speed = FALLING_SPEED
                            self.gameover.play()
                        elif not shape.falling:
                            self.shapes.remove(shape)
                else:
                    # Draws the shape to the grid
                    for shape in self.shapes:
                        shape.draw(self.grid)
                    self.draw_text(vec2(self.size[0]/2, self.size[1]/2), "Paused!", 40, (255, 255, 255), center=True)

                
            # Lost screen state
            if self.screen_state == '2':
                if not self.wait_timer.is_running():
                    self.draw_boxes()
                    self.draw_score()
                if not self.draw_fail_transition_forward():
                # if self.row >= len(self.grid):
                    if not self.wait_timer.is_running():
                        self.wait_timer.start()
                    elif self.wait_timer.has_expired():
                        self.screen_state = '3'
                    
                    # if self.started_backwards:
                    #     self.screen_state == '3'
                
                    
                # self.draw_boxes()
                # self.draw_score()
                # Draws the shape to the grid
                # for shape in self.shapes:
                #     shape.draw(self.grid)

            # Game over state
            if self.screen_state == '3':
                    
                    self.draw_text((self.size[0]/2, self.size[1]/4), "Game Over!", 55, (255, 0, 0), center=True)
                    # score_text = self.draw_text((self.size[0]/4 + 8, self.size[1]/4 + 100), f"Your score: {self.score}", 30, (255, 255, 255), draw=False)
                    self.draw_text((self.size[0]/2, self.size[1]/4 + 100), f"Your score: {self.score}", 30, (255, 255, 255), center=True)
                    
                    self.draw_text((self.size[0]/2, self.size[1]/2 + 100), "Press Space to continue", self.animation_size - 10, (0, 0, 255), center=True)
                    # self.draw_text((self.size[0]/2, self.size[1]/2), "Press Space to Play", self.animation_size, (0, 0, 255), center=True)
                
                    # Janky scale animation for press to play text
                    if self.animation_speed.has_expired():
                        self.animation_size += self.animation_direction
                        if (self.animation_size >= 40 or self.animation_size <= 30):
                            self.animation_direction *= -1

                    self.draw_fail_transition_backward()

            # Main event loop
            for event in events:
                # This is for closing the window
                if event.type == pygame.QUIT:
                    with open("settings.txt", 'w') as settings:
                        lines = [f"Music,{self.musicSlider.value}\n", f"Effect,{self.effectsSlider.value}\n", f"Lines,{self.draw_grid_lines}\n", f"Ghost,{self.show_ghost}\n"]
                        settings.writelines(lines)
                    pygame.quit()
                    sys.exit()
                
                # Checks for any key down
                if event.type == pygame.KEYDOWN:
                    # Pauses if escape key is pressed
                    if event.key == pygame.K_ESCAPE:
                        self.paused = not self.paused
                    # Depending on the state (playing, gameover) it changes the functionality of space
                    if event.key == pygame.K_SPACE:
                        if self.screen_state == '3':
                            self.screen_state = '0'
                        elif self.screen_state == '2':
                            self.screen_state = '3'
                        elif self.screen_state == '1':
                            # Drops the shape on space press if there is a shape
                            if len(self.shapes) >= 1 and not self.paused:
                                self.shapes[0].falling_speed.duration = 1
                                self.shapes[0].move_speed.restart()
                        elif self.screen_state == '0':
                            self.screen_state = '1'
                            # Only clears the grid if you are starting a new gamee
                            if not self.paused:
                                self.grid = self.make_grid()
                            self.score = 0
 
                    # This is for adjusting how large the show padding is on the boxes (Has no effect on actual gameplay)
                    if event.key == pygame.K_i and self.screen_state == '1':
                        if self.style > 4:
                            self.style = 2
                        else:
                            self.style += 2
                    
                # Only lets the user rotate if they have released the rotate key
                if event.type == pygame.KEYUP:
                    if (event.key == pygame.K_UP or event.key == pygame.K_w) and self.screen_state == '1':
                        if len(self.shapes) >= 1:
                            self.shapes[0].can_rotate = True
                    if (event.key == pygame.K_s or event.key == pygame.K_DOWN):
                        if len(self.shapes) >= 1:
                            self.shapes[0].falling_speed.duration = self.shapes[0].current_falling_speed
            pygame.display.update()

if __name__ == "__main__":
    Game((400, 800)).run()
