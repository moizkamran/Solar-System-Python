import pygame
import math
pygame.init()

# Set up the window
WIDTH, HEIGHT = 800, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Solar Simulation")

WHITE = (255,255,255)
YELLOW = (255,255,0)
BLUE = (0,0,255)
RED = (255,0,0)
ORANGE = (255,165,0)

class Planet:
    AU = 149.6e6 * 1000 # meters
    G = 6.67408e-11 # m^3 kg^-1 s^-2
    SCALE = 200 / AU # 1 AU = 250 pixels
    TIMESTEP = 3600 * 24 # 1 day in seconds

    def __init__(self, x, y, radius, color, mass):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.mass = mass
        self.vel = 0
        self.angle = 0

        self.orbit = []
        self.sun = False
        self.distance_to_sun = 0

        self.x_vel = 0
        self.y_vel = 0

    def draw(self, win):
        x = self.x * self.SCALE + WIDTH / 2
        y = self.y * self.SCALE + HEIGHT / 2
        pygame.draw.circle(win, self.color, (int(x), int(y)), self.radius)

def main():
    run = True
    clock = pygame.time.Clock()

    sun = Planet(0, 0, 30, YELLOW, 1.989e30)
    sun.sun = True

    earth = Planet(-1 * Planet.AU, 0, 16, BLUE, 5.972e24)

    mars = Planet(-1.524 * Planet.AU, 0, 12, RED, 6.39e23)

    mercury = Planet(0.387 * Planet.AU, 0, 10, ORANGE, 3.285e23)

    planets = [sun, earth, mars, mercury]
    
    while run:
        clock.tick(60)
        # show an fps counter
        pygame.display.set_caption("Solar Simulation | FPS: " + str(round(clock.get_fps())))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
        for planet in planets:
            planet.draw(WIN)
        
        pygame.display.update()

    pygame.quit()

main()