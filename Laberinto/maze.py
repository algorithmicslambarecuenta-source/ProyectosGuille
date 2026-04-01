from pygame import *
init()

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (65,65))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < 700 - 80:
            self.rect.x += self.speed
        if keys[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.y < 500 - 80:
            self.rect.y += self.speed

class Enemy(GameSprite):
    def update(self):
        if self.rect.x <= 470:
            self.direction = "derecha"
        if self.rect.x >= 700 - 85:
            self.direction = "Izquierda"
        
        if self.direction == "Izquierda":
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed


class Wall(sprite.Sprite):
    def __init__(self, color_1, color_2, color_3, wall_x, wall_y, wall_width, wall_height):
        super().__init__()
        self.color_1 = color_1
        self.color_2 = color_2
        self.color_3 = color_3
        self.width = wall_width
        self.height = wall_height
        self.image = Surface((self.width, self.height))
        self.image.fill((color_1, color_2, color_3))
        self.rect = self.image.get_rect()
        self.rect.x = wall_x
        self.rect.y = wall_y
    def draw_wall(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


window = display.set_mode((700, 500))
display.set_caption("Laberinto")
background = transform.scale(image.load("background.jpg"), (700, 500))

game = True
finish = False
clock = time.Clock()

mixer.init()
mixer.music.load('jungles.ogg')
mixer.music.play()

font.init()
fuente1 = font.SysFont('arial', 70)
wintext = fuente1.render("GANASTE", True, (115, 208, 77))
losetext = fuente1.render("PERDISTE", True, (204, 9, 11))

money = mixer.Sound('money.ogg')
kick = mixer.Sound("kick.ogg")

fanstasma = Player('hero.png', 5, 420, 4)
monstruo = Enemy('cyborg.png', 620, 280, 2)
final = GameSprite('treasure.png', 580, 420, 0)
color = (154, 205, 50)
w1 = Wall(154, 205, 50, 70, 0,  10, 350)   # pared vertical izquierda grande
w2 = Wall(154, 205, 50, 70, 0,  300, 10)   # pared horizontal superior izquierda
w3 = Wall(154, 205, 50, 200, 350, 10, 130)  # pared vertical izquierda abajo
w4 = Wall(30, 30, 30, 30, 30, 30, 30) # pared vertical central grande
w5 = Wall(154, 205, 50, 200, 100, 250, 10) # pared horizontal central
w6 = Wall(154, 205, 50, 350, 150, 10, 250) # pared vertical derecha grande
w7 = Wall(154, 205, 50, 350, 150, 150, 10) # pared horizontal derecha superior


while game:
    for e in event.get():
        if e.type == QUIT:
            game = False

    if finish != True:
        window.blit(background,(0,0))
        fanstasma.update()
        monstruo.update()

        fanstasma.reset()
        monstruo.reset()
        final.reset()

        w1.draw_wall()
        w2.draw_wall()
        w3.draw_wall()

        if sprite.collide_rect(fanstasma, monstruo) or sprite.collide_rect(fanstasma, w1) or sprite.collide_rect(fanstasma, w2) or sprite.collide_rect(fanstasma, w3):
            finish = True
            window.blit(losetext, (200, 200))
            kick.play()
        if sprite.collide_rect(fanstasma, final):
            finish = True
            window.blit(wintext, (200, 200))
            money.play()

    display.update()
    clock.tick(60)