import pygame

pygame.init()

WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600

window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Ping Pong")


class Sprite(pygame.sprite.Sprite):
    def __init__(self, image, x, y, width, height):
        super().__init__()

        self.image = pygame.transform.scale(
            pygame.image.load(image),
            (width, height)
        )

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def show(self):
        window.blit(self.image, self.rect)


class PingPong(Sprite):
    def __init__(self, image, x, y, width, height):
        super().__init__(image, x, y, width, height)
        self.speed_x = 2
        self.speed_y = 2
        self.lasttouch = None

    def move(self, racket1, racket2):
        # Gerakkan bola
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        # Pantul atas dan bawah
        if self.rect.top <= 0 or self.rect.bottom >= WINDOW_HEIGHT:
            self.speed_y *= -1

        # Pantul raket kiri
        if self.rect.colliderect(racket1.rect) and self.speed_x < 0:
            self.speed_x *= -1
            self.lasttouch = racket1.name
            self.rect.left = racket1.rect.right
        # Pantul raket kanan
        if self.rect.colliderect(racket2.rect) and self.speed_x > 0:
            self.speed_x *= -1
            self.lasttouch = racket2.name
            self.rect.right = racket2.rect.left
class Racket(Sprite):
    def __init__(self, image, x, y, width, height, name):
        super().__init__(image, x, y, width, height)
        self.speed = 6
        self.name = name
    def control(self, up_key, down_key):
        keys = pygame.key.get_pressed()
        if keys[up_key] and self.rect.top > 0:
            self.rect.y -= self.speed
        if keys[down_key] and self.rect.bottom < WINDOW_HEIGHT:
            self.rect.y += self.speed
clock = pygame.time.Clock()
lapangan = Sprite("lapangan basket.png", 0, -200, WINDOW_WIDTH, 1000)
racket1 = Racket("racket.png", 50, 260, 60, 80, "Player 1")
racket2 = Racket("pemukul tenis.png", 490, 260, 60, 80, "Player 2")
pingpong = PingPong("bola tenis.png", 275, 275, 50, 50)
running = True
game_over = False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if not game_over:
        clock.tick(60)

        racket1.control(pygame.K_w, pygame.K_s)
        racket2.control(pygame.K_UP, pygame.K_DOWN)

        pingpong.move(racket1, racket2)

        if pingpong.rect.right < 0:
            winner = "Player 2 Wins!"
            game_over = True

        if pingpong.rect.left > WINDOW_WIDTH:
            winner = "Player 1 Wins!"
            game_over = True

        window.fill((0,255,0))
        lapangan.show()
        racket1.show()
        racket2.show()
        pingpong.show()

    else:
        window.fill((0,255,0))
        lapangan.show()

        font = pygame.font.Font(None, 50)
        text = font.render(winner, True, (255,0,0))

        window.blit(
            text,
            (
                WINDOW_WIDTH//2 - text.get_width()//2,
                WINDOW_HEIGHT//2 - text.get_height()//2
            )
        )
    pygame.display.update()

pygame.quit()