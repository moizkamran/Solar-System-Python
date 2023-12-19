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

        if len(self.orbit) > 2:
            updated_points = []
            for point in self.orbit:
                x, y = point
                x = x * self.SCALE + WIDTH / 2
                y = y * self.SCALE + HEIGHT / 2
                updated_points.append((x, y))

            pygame.draw.lines(win, self.color, False, updated_points, 2)
        pygame.draw.circle(win, self.color, (int(x), int(y)), self.radius)

        if not self.sun:
                # Display mass and distance to the sun
                font = pygame.font.Font(None, 20)
                mass_text = font.render(f"Mass: {self.mass / 1e24:.2f}e24 kg", True, WHITE)
                distance_text = font.render(f"Distance to Sun: {self.distance_to_sun / 1e9:.2f}e9 meters", True, WHITE)
                # Display planet name
                if self.color == BLUE:
                    planet_name = font.render("Earth", True, WHITE)
                elif self.color == RED:
                    planet_name = font.render("Mars", True, WHITE)
                elif self.color == ORANGE:
                    planet_name = font.render("Mercury", True, WHITE)

                win.blit(mass_text, (int(x) - 40, int(y) - 50))
                win.blit(distance_text, (int(x) - 40, int(y) - 30))
                win.blit(planet_name, (int(x) - 40, int(y) - 10))

    def attraction(self, other):
        other_x, other_y = other.x, other.y
        distance_x = other_x - self.x
        distance_y = other_y - self.y
        distance = math.sqrt(distance_x ** 2 + distance_y ** 2) # using pythagorean theorem to find distance between two points

        if other.sun:
            self.distance_to_sun = distance
        
        force = self.G * self.mass * other.mass / (distance ** 2)
        theta = math.atan2(distance_y, distance_x)
        force_x = math.cos(theta) * force
        force_y = math.sin(theta) * force

        return force_x, force_y
    
    def update_position(self, planets):
        total_fx = total_fy = 0
        for planet in planets:
            if self == planet:
                continue
            fx, fy = self.attraction(planet)
            total_fx += fx
            total_fy += fy

        self.x_vel += (total_fx / self.mass) * self.TIMESTEP
        self.y_vel += (total_fy / self.mass) * self.TIMESTEP
        # F = ma, a = F/m

        self.x += self.x_vel * self.TIMESTEP
        self.y += self.y_vel * self.TIMESTEP
        self.orbit.append((self.x, self.y))


def main():
    run = True
    paused = False
    clock = pygame.time.Clock()

    sun = Planet(0, 0, 30, YELLOW, 1.989e30)
    sun.sun = True

    earth = Planet(-1 * Planet.AU, 0, 16, BLUE, 5.972e24)
    earth.y_vel = 29.783 * 1000  # m/s

    mars = Planet(-1.524 * Planet.AU, 0, 12, RED, 6.39e23)
    mars.y_vel = 24.077 * 1000  # m/s

    mercury = Planet(0.387 * Planet.AU, 0, 10, ORANGE, 3.285e23)
    mercury.y_vel = -47.362 * 1000  # m/s

    planets = [sun, earth, mars, mercury]

    # Timestep slider parameters
    slider_x = 10
    slider_y = HEIGHT - 40
    slider_width = 200
    slider_height = 10
    min_timestep = 60  # minimum timestep in seconds
    max_timestep = 3600 * 24 * 30  # maximum timestep in seconds
    timestep_range = max_timestep - min_timestep

    while run:
        clock.tick(60)
        WIN.fill((0, 0, 0))
        pygame.display.set_caption("Solar Simulation | FPS: " + str(round(clock.get_fps())))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_x, mouse_y = pygame.mouse.get_pos()

                    # Check if the click is within the pause button area
                    if WIDTH - 100 <= mouse_x <= WIDTH and 0 <= mouse_y <= 30:
                        paused = not paused

                    # Check if the click is within the slider area
                    elif slider_x <= mouse_x <= slider_x + slider_width and slider_y <= mouse_y <= slider_y + slider_height:
                        # Update timestep based on slider position
                        relative_x = mouse_x - slider_x
                        normalized_x = min(max(relative_x / slider_width, 0), 1)
                        timestep = min_timestep + normalized_x * timestep_range
                        Planet.TIMESTEP = timestep

        if not paused:
            for planet in planets:
                planet.update_position(planets)

        for planet in planets:
            planet.draw(WIN)

        # Draw the pause button
        pygame.draw.rect(WIN, WHITE, (WIDTH - 100, 0, 100, 30))
        font = pygame.font.Font(None, 24)
        pause_text = font.render("Pause" if not paused else "Resume", True, (0, 0, 0))
        WIN.blit(pause_text, (WIDTH - 90, 5))

        # Draw the timestep slider
        pygame.draw.rect(WIN, WHITE, (slider_x, slider_y, slider_width, slider_height))
        slider_position = slider_x + (Planet.TIMESTEP - min_timestep) / timestep_range * slider_width
        pygame.draw.circle(WIN, RED, (int(slider_position), int(slider_y + slider_height / 2)), 8)

        pygame.display.update()

    pygame.quit()

main()