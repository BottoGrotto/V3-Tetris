import pygame

class Timer:
    def __init__(self, duration):
        self.duration = duration
        self.start_time = None
        self.running = False
        self.loop = False

    def restart(self):
        """Restarts the timer"""
        self.stop()
        self.start(self.loop)

    def start(self, loop=False):
        """Starts the timer"""
        self.start_time = pygame.time.get_ticks()
        self.running = True
        self.loop = loop

    def stop(self):
        """Stops the timer"""
        self.start_time = None
        self.running = False
        self.loop = False

    def is_running(self):
        """Returns the state of the timer"""
        return self.running

    def has_expired(self):
        """Checks if the timer has expired and restarts it if it is set to loop"""
        if not self.running:
            return False

        # Gets the time since the timer started
        elapsed_time = pygame.time.get_ticks() - self.start_time
        # Checks if the elapsed time is >= to the set duration then loops or stops the timer
        if elapsed_time >= self.duration:
            if self.loop:
                self.start_time = pygame.time.get_ticks()
            else:
                self.stop()
            return True
        return False