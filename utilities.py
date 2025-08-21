import pygame, math
from color import Color
from pygame import Vector2 as vec2

class Button:
    def __init__(self, pos: vec2, bgColor: Color, textColor: Color, text: str, fontSize: int=30, bgTransparent: bool=False, center=False):
        """Custom button class that will run a function when clicked"""
        self.pos = pos
        self.bgColor = bgColor
        self.textColor = textColor
        
        self.text = text
        self.fontSize = fontSize
        self.bgTransparent = bgTransparent
        self.center = center

        self.configure_surface()


    def configure_surface(self):
        """Initializes the values for text_size, text_surface, and the rect and surface"""
        font = pygame.font.SysFont('Comic Sans MS', self.fontSize)
        self.text_size = font.size(self.text)
        self.text_surface = font.render(self.text, True, self.textColor.colorize())
        # Centers the rect if centered
        render_pos = self.pos.copy()
        if self.center:
            render_pos.x -= self.text_surface.get_width()/2
        self.rect = pygame.Rect(render_pos.x, render_pos.y, self.text_size[0], self.text_size[1])
        self.surface = pygame.Surface(self.rect.size, pygame.SRCALPHA)
        
    def update(self, screen, func, events):
        """Takes in the screen to draw to, a function to run, and the events each frame"""
        # Draws the rect to the surface and puts the text on that surface, then draws it onto the screen
        pygame.draw.rect(self.surface, self.bgColor.colorize() if not self.bgTransparent else (self.bgColor.color[0], self.bgColor.color[0], self.bgColor.color[0], 0), self.rect)
        self.surface.blit(self.text_surface, (0, 0))
        # Centers the surf if centered
        screen.blit(self.surface, self.pos if not self.center else (self.pos.x - self.text_surface.get_width()/2, self.pos.y))

        # Checks if there was a mousebutton event and if it was on the button using pygame built in collidepoint method for Rect class
        # Then runs the function if it was on the button
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse = pygame.mouse.get_pos()
                    if self.rect.collidepoint(mouse):
                        func()
        return screen

class Slider:
    def __init__(self, pos: vec2, size: vec2, bgColor: Color, nobColor: Color, minValue: int=0, value: int=50, maxValue: int=100, center=False):
        self.pos = pos
        self.size = size
        self.bgColor = bgColor
        self.nobColor = nobColor
        self.center = center

        self.rect = pygame.Rect(0, 0, size.x, size.y)
        self.surface = pygame.Surface(self.rect.size)

        # Centers the slider if centered
        self.render_pos = self.pos.copy()
        if self.center:
            self.render_pos.x -= size.x/2

        self.collisionRect = pygame.Rect(self.render_pos.x, self.render_pos.y, size.x, size.y)
        
        # Initializes the min, value, and max values for the slider
        self.minValue = minValue
        self.value = value
        self.maxValue = maxValue + 1

        

    def draw(self, screen, pos):
        """Draws the slider to the screen"""

        pygame.draw.rect(self.surface, self.bgColor.colorize(), self.rect)

        pygame.draw.circle(self.surface, self.nobColor.colorize(), (pos[0], self.rect.height/2), self.size.y/2)
        screen.blit(self.surface, self.render_pos)

    def update(self, screen, mouse_buttons):
        """Takes in a screen to draw to and if a mouse_button has been clicked"""
        # Checks if the left click key was pressed then checks if it was on the slider
        mouse = pygame.mouse.get_pos()
        if mouse_buttons[0]:
            if self.collisionRect.collidepoint(mouse):
                # If it was on the slider then it calculates the value based on where the click was on the horizontal direciton of the slider
                relativeX = mouse[0] - self.collisionRect.x
                relativeX = max(0, min(self.collisionRect.width, relativeX))
                ratio = relativeX / self.collisionRect.width
                self.value = math.floor(self.minValue + (self.maxValue - self.minValue) * ratio)
            
            # Draws the slider to the screen
            self.draw(screen, mouse)

        # If there wasn't a mouse event it still draws it to the screen just it does the opposite of getting a value from position it gets a position from value
        clampedValue = max(self.minValue, min(self.maxValue, self.value))

        ratio = (clampedValue - self.minValue) / (self.maxValue - self.minValue)

        xPosition = math.floor(self.rect.left + ratio * self.rect.width)
        # Draws it to the screen with the correct position based on value
        self.draw(screen, (xPosition, 0))
        return screen

        
            
