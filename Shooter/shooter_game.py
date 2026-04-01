import pygame
from random import randint


pygame.init()
pygame.font.init()
pygame.mixer.init()

# Fuentes del sistema
font1 = pygame.font.SysFont("arial", 80)
font2 = pygame.font.SysFont("arial", 36)

win_text = font1.render("¡GANASTE!", True, (255, 255, 255))
lose_text = font1.render("¡PERDISTE!", True, (180, 0, 0))

# Música de fondo
pygame.mixer.music.load("gd_practice_mode.mp3")
pygame.mixer.music.play(-1)
fire_sound = pygame.mixer.Sound("fire.ogg")

# Imágenes
img_back = "galaxy.jpg"
img_bullet = "bullet.png"
img_hero = "rocket.png"
img_enemy = "ufo.png"

# Variables del juego
score = 0
goal = 100
lost = 0
max_lost = 10

# Tamaño de ventana
win_width = 700
win_height = 500

pygame.display.set_caption("Tirador")
window = pygame.display.set_mode((win_width, win_height))
background = pygame.transform.scale(
    pygame.image.load(img_back), (win_width, win_height)
)


class GameSprite(pygame.sprite.Sprite):
    def __init__(
        self,
        player_image,
        player_x,
        player_y,
        size_x,
        size_y,
        player_speed
    ):
        super().__init__()
        self.image = pygame.transform.scale(
            pygame.image.load(player_image), (size_x, size_y)
        )
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


class Player(GameSprite):
    def update(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed

        if keys[pygame.K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed

    def fire(self):
        bullet = Bullet(
            img_bullet,
            self.rect.centerx - 7,
            self.rect.top,
            15,
            20,
            -30
        )
        bullets.add(bullet)


class Enemy(GameSprite):
    def update(self):
        global lost

        self.rect.y += self.speed

        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost += 1


class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed

        if self.rect.y < 0:
            self.kill()


# Crear objetos
ship = Player(img_hero, 5, win_height - 100, 80, 100, 10)

# Grupo de enemigos
monsters = pygame.sprite.Group()
for _ in range(5):
    monster = Enemy(
        img_enemy,
        randint(80, win_width - 80),
        -40,
        80,
        50,
        randint(1, 3)
    )
    monsters.add(monster)

# Grupo de balas
bullets = pygame.sprite.Group()

finish = False
run = True
clock = pygame.time.Clock()

while run:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            run = False

        elif e.type == pygame.KEYDOWN:
            if e.key == pygame.K_SPACE:
                fire_sound.play()
                ship.fire()

    if not finish:
        window.blit(background, (0, 0))

        ship.update()
        monsters.update()
        bullets.update()

        ship.reset()
        monsters.draw(window)
        bullets.draw(window)

        # Colisión bala-enemigo
        collides = pygame.sprite.groupcollide(monsters, bullets, True, True)
        for _ in collides:
            score += 1
            monster = Enemy(
                img_enemy,
                randint(80, win_width - 80),
                -40,
                80,
                50,
                randint(1, 3)
            )
            monsters.add(monster)

        # Derrota
        if pygame.sprite.spritecollide(ship, monsters, False) or lost >= max_lost:
            finish = True
            window.blit(lose_text, (200, 200))

        # Victoria
        if score >= goal:
            finish = True
            window.blit(win_text, (200, 200))

        # Textos
        text_score = font2.render(f"Puntaje: {score}", True, (255, 255, 255))
        window.blit(text_score, (10, 20))

        text_lost = font2.render(f"Fallados: {lost}", True, (255, 255, 255))
        window.blit(text_lost, (10, 50))

        pygame.display.update()

    else:
        pygame.display.update()
        pygame.time.delay(3000)

        finish = False
        score = 0
        lost = 0

        bullets.empty()
        monsters.empty()

        for _ in range(5):
            monster = Enemy(
                img_enemy,
                randint(80, win_width - 80),
                -40,
                80,
                50,
                randint(1, 5)
            )
            monsters.add(monster)

    clock.tick(60)

pygame.quit()