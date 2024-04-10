import pygame
import math
import numpy as np
import random as random
# Initialize Pygame
pygame.init()

# Set the dimensions of the window
WIDTH, HEIGHT = 1800, 1300
screen = pygame.display.set_mode((WIDTH, HEIGHT))


screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Solar System Simulation")
SCALE_EXPONENT = 9.85
SCALE_FACTOR = pow(10, -SCALE_EXPONENT)

# Global variables for gravitational constant and time step
G = 6.67428e-11
timeStep = 3600 * 24

class HeavenlyBody:
    AstroUnit = 149.6e6 * 1200

    def __init__(self, x, y, mass, color, radius, x_vel=0, y_vel=0):
        self.x = x
        self.y = y
        self.mass = mass
        self.color = color
        self.radius = radius
        self.x_vel = x_vel
        self.y_vel = y_vel
    
        self.sun = False  
        self.distance_to_sun = 0 
        self.name = None
    # Method to draw the HeavenlyBody on the screen
    def draw(self, screen):
        # Convert position to screen coordinates
        x_screen = int(self.x * SCALE_FACTOR + WIDTH / 2)
        y_screen = int(self.y * SCALE_FACTOR + HEIGHT / 2)
        pygame.draw.circle(screen, self.color, (x_screen, y_screen), self.radius)
        font = pygame.font.Font(None, 12)
        text_surface = font.render(self.name, True, (255, 255, 255))
        screen.blit(text_surface, (x_screen - 15, y_screen + self.radius + 5))

    # Method to calculate gravitational attraction between two bodies
    def gravitational_attraction(self, other):
        distance_vector = np.array([other.x - self.x, other.y - self.y])
        distance = np.linalg.norm(distance_vector)

        if other.sun:
            self.distance_to_sun = distance
        force_magnitude = G * self.mass * other.mass / distance ** 2
        force_direction = distance_vector / distance
        force_vector = force_magnitude * force_direction
        return force_vector[0], force_vector[1]

    # Method to calculate gravitational acceleration on the body
    def gravitational_acceleration(self, planets, vel_x=0, vel_y=0):
        total_force = np.zeros(2)
        for planet in planets:
            if self == planet:
                continue

            force_x, force_y = self.gravitational_attraction(planet)
            total_force += np.array([force_x, force_y])

        total_force += np.array([vel_x, vel_y])
        acceleration = total_force / self.mass
        return acceleration[0], acceleration[1]

    # Method to perform one iteration of the Runge-Kutta 4th order method
    def rk4_step(self, planets):
        k1x, k1y = self.gravitational_acceleration(planets)
        k2x, k2y = self.gravitational_acceleration(planets, vel_x=k1x * 0.5, vel_y=k1y * 0.5)
        k3x, k3y = self.gravitational_acceleration(planets, vel_x=k2x * 0.5, vel_y=k2y * 0.5)
        k4x, k4y = self.gravitational_acceleration(planets, vel_x=k3x, vel_y=k3y)

        self.x_vel += (k1x + 2 * k2x + 2 * k3x + k4x) / 6 * timeStep
        self.y_vel += (k1y + 2 * k2y + 2 * k3y + k4y) / 6 * timeStep

        self.x += self.x_vel * timeStep
        self.y += self.y_vel * timeStep
    
def display_welcome_screen(screen):
    screen.fill((0, 0, 0))  
    font = pygame.font.Font(None, 36)
    text = font.render("Welcome to Solar System Simulation", True, (255, 255, 255))
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
    screen.blit(text, text_rect)

    instructions = [
        "Instructions:",
        "Press 'A' to increase simulation speed.",
        "Press 'D' to decrease simulation speed.",
        "Press 'W' to increase gravitational constant.",
        "Press 'S' to decrease gravitational constant.",
        "Press 'N' to add a random new celestial body.",
        "Press 'P' to add a random new stray planet.",
        "Press SPACE to start the simulation."
    ]

    y_offset = 0
    for line in instructions:
        instruction_text = font.render(line, True, (255, 255, 255))
        instruction_rect = instruction_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + y_offset))
        screen.blit(instruction_text, instruction_rect)
        y_offset += 30

    pygame.display.flip()

def main():
    global G, timeStep

    run = True
    clock = pygame.time.Clock()
    simulation_speed = 1
    base_frame_rate = 60
    welcome_screen = True  

    # Create instances of HeavenlyBody for each planet
    sun = HeavenlyBody(0, 0, 1.98892 * 10 ** 30, (255, 255, 0), 9)
    sun.sun = True
    sun.name = "Sun"

    mercury = HeavenlyBody(0.387 * HeavenlyBody.AstroUnit, 0, 3.30 * 10 ** 23, (173, 216, 230), 1, y_vel=-47.4 * 1000)
    mercury.name = "Mercury"

    venus = HeavenlyBody(0.723 * HeavenlyBody.AstroUnit, 0, 4.8685 * 10 ** 24, (255, 255, 255), 3, y_vel=-35.02 * 1000)
    venus.name = "Venus"

    earth = HeavenlyBody(-1 * HeavenlyBody.AstroUnit, 0, 5.9742 * 10 ** 24, (100, 149, 237), 3, y_vel=29.783 * 1000)
    earth.name = "Earth"

    mars = HeavenlyBody(-1.524 * HeavenlyBody.AstroUnit, 0, 6.39 * 10 ** 23, (188, 39, 50), 2, y_vel=24.077 * 1000)
    mars.name = "Mars"

    jupiter = HeavenlyBody(5.203 * HeavenlyBody.AstroUnit, 0, 1.898 * 10 ** 27, (255, 165, 0), 7, y_vel=-13.07 * 1000)
    jupiter.name = "Jupiter"

    saturn = HeavenlyBody(9.537 * HeavenlyBody.AstroUnit, 0, 5.683 * 10 ** 26, (50, 205, 50), 6, y_vel=-9.69 * 1000)
    saturn.name = "Saturn"

    uranus = HeavenlyBody(19.191 * HeavenlyBody.AstroUnit, 0, 8.681 * 10 ** 25, (173, 216, 230), 5, y_vel=-6.81 * 1000)
    uranus.name = "Uranus"

    neptune = HeavenlyBody(30.069 * HeavenlyBody.AstroUnit, 0, 1.024 * 10 ** 26, (30, 144, 255), 5, y_vel=-5.43 * 1000)
    neptune.name = "Neptune"

    astroBodies = [sun, mercury, venus, earth, mars, jupiter, saturn, uranus, neptune]

    while run:
        clock.tick(base_frame_rate * simulation_speed)
        screen.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                if welcome_screen:
                    if event.key == pygame.K_SPACE:
                        welcome_screen = False
                else:
                    if event.key == pygame.K_a:
                        simulation_speed += 0.1
                    elif event.key == pygame.K_d:
                        simulation_speed -= 0.1  
                        if simulation_speed < 0.1:
                            simulation_speed = 0.1
                    elif event.key == pygame.K_w:
                        G *= 1.1 
                    elif event.key == pygame.K_s:
                        G /= 1.1  
                    elif event.key == pygame.K_n:
                        x = random.randint(-30, 30) * HeavenlyBody.AstroUnit
                        y = random.randint(-20, 20) * HeavenlyBody.AstroUnit
                        mass = random.uniform(1e30, 1e32)
                        color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
                        radius = random.randint(5, 15)
                        new_star = HeavenlyBody(x, y, mass, color, radius)
                        new_star.name = "Foreign Star"
                        astroBodies.append(new_star)

                        
                    elif event.key == pygame.K_p:
                        x = random.randint(-30, 30) * HeavenlyBody.AstroUnit
                        y = random.randint(-20, 20) * HeavenlyBody.AstroUnit
                        mass = random.uniform(1e23, 1e27)
                        color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
                        radius = random.randint(1, 5)
                        x_vel = random.randint(-5, 5)*1000
                        y_vel = random.randint(-5,5)*1000
                        new_planet = HeavenlyBody(x, y, mass, color, radius, x_vel, y_vel)
                        new_planet.name = "Foreign Planet"
                        astroBodies.append(new_planet)

        if welcome_screen:
            display_welcome_screen(screen)
        else:
            for body in astroBodies:
                body.rk4_step(astroBodies)
                body.draw(screen)

            pygame.display.update()

    pygame.quit()

main()