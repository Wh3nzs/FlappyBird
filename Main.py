#falppy bird
import pygame, sys, random, math

from pygame import event
pygame.init()
info = pygame.display.Info()
WIDTH, HEIGHT = info.current_w // 3, info.current_h // 3
pygame.font.init()
pygame.mixer.pre_init(frequency=60000, size=-16, channels=2, buffer=512)
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
#fonts
score_font = pygame.font.SysFont("fixed", 30)
#sounds
flap_sound = pygame.mixer.Sound("assets/Sounds/wingflap.mp3")
point_sound = pygame.mixer.Sound("assets/Sounds/coin_sound.mp3")


class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y

        self.width = 30
        self.height = 30

        self.gravity = 0.2
        self.velocity = [0,0]

        self.image = pygame.image.load("assets/bird.png").convert_alpha()

    def update(self, dt):

        self.pos = (self.x, self.y)
        self.x += self.velocity[0]

        if self.velocity[1] < -5:
            self.velocity[1] = -5
        if self.y > HEIGHT:
            self.y = HEIGHT
            self.velocity[1] = 0
        else:
            self.y += self.velocity[1]
            self.velocity[1] += self.gravity

        if self.y < 0:
            self.y = self.height
            self.y = 0
            self.velocity[1] = 0

    def draw(self):
        scaled_image = pygame.transform.scale(self.image, (self.width, self.height))
        pygame.draw.rect(screen, (0,0,255), (self.x - self.width // 2, self.y - self.height // 2, self.width, self.height), 1) # Hitbox
        rect = scaled_image.get_rect(center=(self.x, self.y))
        screen.blit(scaled_image, rect)
    def handle_input(self, event):

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
            # flap_sound.play()
                self.velocity[1] = 0
                self.velocity[1] += -10

class Pipes:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 50
        self.height = 350
    def update(self, dt):

        self.x -= 200 * dt

    def draw(self):
        scaled_image = pygame.transform.scale(pipes_image, (self.width, self.height))
        rect = scaled_image.get_rect(center=(self.x, self.y),)
        pygame.draw.rect(screen, (255,0,0), rect, 1)
        screen.blit(scaled_image, rect)




try:
    bird_image = pygame.image.load("assets/bird.png").convert_alpha()
except pygame.error as e:
    print(f"Error loading image: {e}")
    sys.exit()
try:
    pipes_image = pygame.image.load("assets/pipes.png").convert_alpha()
except pygame.error as e:
    print(f"Error loading image: {e}")
    sys.exit()

player = Player(100, 100)

pipes = []

# fuctions
def generate_pipe(nim_of_pipes=1):
    for i in range(nim_of_pipes):
        if random.randint(0,1) == 0:
            y = random.randint(HEIGHT + 50, HEIGHT + 100)
            print("bottom")
        else:
            y = random.randint(0, 100)
            print("top")
        x = WIDTH + i * 200 + random.randint(0, 200)
        pipes.append(Pipes(x, y))
def collision(playerPos,player_radius, rect):
        closest_x = max(rect.left, min(playerPos.x, rect.right))
        closest_y = max(rect.top, min(playerPos.y, rect.bottom))

        distance_x = playerPos.x - closest_x
        distance_y = playerPos.y - closest_y

        return (distance_x ** 2 + distance_y ** 2) < (player_radius ** 2)

bacground_image = pygame.image.load("assets/background.png").convert()
bacground_image = pygame.transform.scale(bacground_image, (WIDTH, HEIGHT))

def main():
    global points
    points = 0
    
    generate_pipe(5)
    running = True
    while running:
        print(player.velocity)

        dt = clock.tick(60) / 1000

        screen.blit(bacground_image, (0,0))
        for event in pygame.event.get():

            player.handle_input(event)

            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:

                
                if event.key == pygame.K_ESCAPE:
                    running = False
                    pygame.quit()
                    sys.exit()
        if any(collision(pygame.Vector2(player.x, player.y), player.width // 2, pygame.Rect(pipe.x - pipe.width // 2, pipe.y - pipe.height // 2, pipe.width, pipe.height)) for pipe in pipes):
            print("Collision detected!")
            lose()


        player.update(dt)
        player.draw()

        for pipe in pipes:
            pipe.update(dt)
            pipe.draw()

        for pipe in pipes:
            if pipe.x < -20:
                print("gone")
                pipes.remove(pipe)
                generate_pipe()
                points += 1
                point_sound.play()
                print(points)

        if player.y > HEIGHT:
            running = False
            lose()

        pygame.display.flip()

def lose():
    running = True
    while running:
        screen.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    running = False
                    pygame.quit()
                    sys.exit()
                
def main_menu():
        running = True
        while running:
            
            try:
                screen.blit(bacground_image, (0,0))
            except pygame.error as e:
                print(f"Error loading background image: {e}")
                screen.fill((0, 0, 0))

            for event in pygame.event.get():

                player.handle_input(event)

                if event.type == pygame.KEYDOWN:
                    print("key down")
                    if event.key == pygame.K_SPACE:
                        running = False
                        main()
                        print("start")

            pygame.display.flip()

        font = pygame.font.SysFont("Arial", 50)
        text = font.render("You Lose!", True, (255, 0, 0))
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(text, text_rect)
        pygame.display.flip()
        pygame.time.wait(2000)
        pygame.quit()
        sys.exit()

main_menu()
