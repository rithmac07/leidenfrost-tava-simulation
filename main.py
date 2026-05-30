import pygame
import math
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 600
FPS = 60

# Colors (R, G, B)
BG_COLOR = (34, 34, 34)       # Dark gray background
TAVA_COLOR = (43, 43, 43)     # Charcoal pan color
TAVA_BORDER = (85, 85, 85)    # Pan edge border
WATER_COLOR = (173, 216, 230) # Light blue droplets
WHITE = (255, 255, 255)

# Setup screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Leidenfrost Dosa Tava Simulation")
clock = pygame.time.Clock()

# Tava properties
CENTER_X = WIDTH // 2
CENTER_Y = HEIGHT // 2
TAVA_RADIUS = 240

class Droplet:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = random.uniform(4, 9)  # Random starting size
        self.vx = random.uniform(-2, 2)     # X velocity
        self.vy = random.uniform(-2, 2)     # Y velocity

    def update(self):
        # Move the droplet
        self.x += self.vx
        self.y += self.vy

        # Check distance from the center of the circular tava
        dist_from_center = math.hypot(self.x - CENTER_X, self.y - CENTER_Y)
        
        # If droplet hits the tava edge, bounce it back toward the center
        if dist_from_center + self.radius > TAVA_RADIUS:
            angle = math.atan2(self.y - CENTER_Y, self.x - CENTER_X)
            # Reverse direction relative to the boundary angle
            self.vx = -math.cos(angle) * 1.5
            self.vy = -math.sin(angle) * 1.5

    def draw(self, surface):
        # Draw the fluid droplet
        pygame.draw.circle(surface, WATER_COLOR, (int(self.x), int(self.y)), int(self.radius))
        # Draw a subtle white outline
        pygame.draw.circle(surface, WHITE, (int(self.x), int(self.y)), int(self.radius), 1)

def handle_merging(droplets):
    i = 0
    while i < len(droplets):
        j = i + 1
        while j < len(droplets):
            d1 = droplets[i]
            d2 = droplets[j]
            
            # Calculate distance between droplet centers
            distance = math.hypot(d1.x - d2.x, d1.y - d2.y)

            # Collision check
            if distance < d1.radius + d2.radius:
                # Merge math: combine circle areas to find the new radius
                new_radius = math.sqrt(d1.radius**2 + d2.radius**2)
                
                # New position is the average based on their meeting point
                d1.x = (d1.x + d2.x) / 2
                d1.y = (d1.y + d2.y) / 2
                d1.radius = new_radius

                # Combine and average their speeds
                d1.vx = (d1.vx + d2.vx) / 2
                d1.vy = (d1.vy + d2.vy) / 2

                # Remove the second droplet since it merged into the first
                droplets.pop(j)
            else:
                j += 1
        i += 1

def main():
    droplets = []
    running = True

    while running:
        clock.tick(FPS)
        screen.fill(BG_COLOR)

        # 1. Event Handling
        for event in pygame.get_event_get():
            if event.type == pygame.QUIT:
                running = False
                
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                # Check if click is inside the tava boundary
                if math.hypot(mouse_x - CENTER_X, mouse_y - CENTER_Y) < TAVA_RADIUS - 10:
                    droplets.append(Droplet(mouse_x, mouse_y))

        # 2. Draw Tava (Griddle)
        pygame.draw.circle(screen, TAVA_BORDER, (CENTER_X, CENTER_Y), TAVA_RADIUS + 5)
        pygame.draw.circle(screen, TAVA_COLOR, (CENTER_X, CENTER_Y), TAVA_RADIUS)

        # 3. Update and Draw Droplets
        for droplet in droplets:
            droplet.update()
            droplet.draw(screen)

        # 4. Check for Merging
        handle_merging(droplets)

        # Refresh Screen
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
