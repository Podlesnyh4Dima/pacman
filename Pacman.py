import pygame
import os
from pygame.locals import *
import sys

pygame.display.set_caption('Pacman')
movement_x = movement_y = 0
FPS = 10
clock = pygame.time.Clock()
v = 5
count = 0
tile_width = tile_height = 50
size = width, height = 1000, 650
screen = pygame.display.set_mode(size)


def draw(screen):
    global count
    pygame.font.init()
    font = pygame.font.Font(None, 50)
    screen.blit(pygame.transform.scale(load_image('fon.png'), (1000, 50)),  (0, 600))
    screen.blit(font.render('Счёт: ' + str(count), False,
                            (255, 255, 255)), (0, 600))
    screen.blit(font.render('Win', False,
                            (255, 255, 255)), (400, 600))
    screen.blit(font.render('Game over', False, (255, 255, 255)), (750, 600))


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    image = pygame.image.load(fullname).convert_alpha()
    return image


def load_level(filename):
    filename = "data/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


# pygame.display.set_icon(load_image('logo.png'))
player_image = load_image("pacman/pacman1.png")
tile_images = {
    'b': load_image('map/black.png'),
    '#': load_image('map/wall.png'),
    '$': load_image('map/wall2.png'),
    '!': load_image('map/wall3.png'),
    '%': load_image('map/wall4.png'),
    '^': load_image('map/wall5.png'),
    '&': load_image('map/wall6.png'),
    '*': load_image('map/wall7.png'),
    '`': load_image('map/wall8.png'),
    '~': load_image('map/wall9.png'),
    '/': load_image('map/wall10.png'),
    '?': load_image('map/wall11.png'),
    '|': load_image('map/wall12.png'),
    '>': load_image('map/wall13.png'),
    ',': load_image('map/wall14.png'),
    '<': load_image('map/wall15.png')
}

all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
points_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
cherry_group = pygame.sprite.Group()
super_points_group = pygame.sprite.Group()


class Border(pygame.sprite.Sprite):
    def __init__(self, imagePath, x):
        super().__init__(all_sprites)
        self.image = load_image(imagePath)
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.bottomleft = x


borderL1 = Border('map/borderL1.png', (0, 600))
borderL2 = Border('map/borderL2.png', (500, 600))
borderR1 = Border('map/borderR1.png', (0, 600))
borderR2 = Border('map/borderR2.png', (500, 600))
borderU1 = Border('map/borderU1.png', (0, 600))
borderU2 = Border('map/borderU2.png', (500, 600))
borderD1 = Border('map/borderD1.png', (0, 600))
borderD2 = Border('map/borderD2.png', (500, 600))


class GameObj(pygame.sprite.Sprite):
    image = pygame.image.load('data/cherry.png')
    group = cherry_group
    d = (0, 0)
    def __init__(self, x_pos, y_pos):
        super().__init__(self.group, all_sprites)
        self.rect = self.image.get_rect().move(x_pos * tile_width + self.d[0], y_pos * tile_height + self.d[0])


class Cherry(GameObj):
    image = pygame.image.load('data/cherry.png')
    group = cherry_group
    d = (23, 23)


class Point(GameObj):
    image = pygame.image.load('data/point.png')
    group = points_group
    d = (23, 23)


class SuperPoint(GameObj):
    image = pygame.image.load('data/super_point.png')
    group = super_points_group
    d = (23, 23)


class Tile(GameObj):
    group = tiles_group
    def __init__(self, tile_type, x_pos, y_pos):
        self.image = tile_images[tile_type]
        super().__init__(x_pos, y_pos)


class Player(pygame.sprite.Sprite):
    image = player_image

    def __init__(self, columns, rows, x_pos, y_pos):
        super().__init__(all_sprites, player_group)
        self.movement_x = movement_x
        self.movement_y = movement_y
        self.frames = []
        self.cut_sheet(Player.image, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.image.get_rect().move(
            tile_width * x_pos + 15, tile_height * y_pos + 5)
        self.lookD = "right"

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(frame_location,
                                                    self.rect.size)))

    def update(self):
        if event.type == KEYDOWN:
            if event.key == K_RIGHT \
                    and not pygame.sprite.collide_mask(self, borderR1) \
                    and not pygame.sprite.collide_mask(self, borderR2):
                self.movement_x = v
                self.movement_y = 0
                self.lookD = "right"
            if event.key == K_LEFT \
                    and not pygame.sprite.collide_mask(self, borderL1) \
                    and not pygame.sprite.collide_mask(self, borderL2):
                self.movement_x = -v
                self.movement_y = 0
                self.lookD = "left"
            if event.key == K_DOWN \
                    and not pygame.sprite.collide_mask(self, borderD1) \
                    and not pygame.sprite.collide_mask(self, borderD2):
                self.movement_y = v
                self.movement_x = 0
                self.lookD = "down"
            if event.key == K_UP \
                    and not pygame.sprite.collide_mask(self, borderU1) \
                    and not pygame.sprite.collide_mask(self, borderU2):
                self.movement_y = -v
                self.movement_x = 0
                self.lookD = "up"

        self.rect.x += self.movement_x
        self.rect.y += self.movement_y

        if pygame.sprite.collide_mask(self, borderL1) \
                or pygame.sprite.collide_mask(self, borderL2):
            self.rect.x += v
        if pygame.sprite.collide_mask(self, borderR1) \
                or pygame.sprite.collide_mask(self, borderR2):
            self.rect.x += -v
        if pygame.sprite.collide_mask(self, borderD1) \
                or pygame.sprite.collide_mask(self, borderD2):
            self.rect.y += -v
        if pygame.sprite.collide_mask(self, borderU1) \
                or pygame.sprite.collide_mask(self, borderU2):
            self.rect.y += v

        if int(self.rect.x) >= width:
            self.rect.x = 0
        elif int(self.rect.x) < 0:
            self.rect.x = width
        if int(self.rect.y) >= height:
            self.rect.y = 0
        elif int(self.rect.y) < 0:
            self.rect.y = height

        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]
        if (self.lookD == "left"):
            self.image = pygame.transform.flip(self.image, True, False)
        if (self.lookD == "up"):
            self.image = pygame.transform.rotate(self.image, 90)
        if (self.lookD == "down"):
            self.image = pygame.transform.rotate(self.image, -90)


class Enemy(pygame.sprite.Sprite):
    image = load_image("red_ghost.png")

    def __init__(self, columns, rows, x_pos, y_pos):
        super().__init__(all_sprites, enemy_group)
        self.movement_x = movement_x
        self.movement_y = movement_y
        self.frames = []
        self.cut_sheet(Enemy.image, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.image.get_rect().move(
            tile_width * x_pos + 25, tile_height * y_pos + 5)
        self.lookD = "left"

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location,  self.rect.size)))

    def update(self):
        self.rect.x += -v
        self.rect.x += self.movement_x
        self.rect.y += self.movement_y

        if pygame.sprite.collide_mask(self, borderL1):
            self.rect.x += v
            self.rect.y += v * 1.5
            self.lookD = "up"
        if pygame.sprite.collide_mask(self, borderL2):
            self.rect.x += v
            self.rect.y += v
            self.lookD = "up"
        if pygame.sprite.collide_mask(self, borderR1):
            self.rect.x += v
            self.rect.y += v
            self.lookD = "down"
        if pygame.sprite.collide_mask(self, borderR2):
            self.rect.x += v
            self.rect.y += v
            self.lookD = "down"
        if pygame.sprite.collide_mask(self, borderD1) \
                or pygame.sprite.collide_mask(self, borderD2):
            self.rect.y += -v
            self.rect.x += v
            self.lookD = "left"
        if pygame.sprite.collide_mask(self, borderU2):
            self.rect.x += v * 1.5
            self.lookD = "right"
        if pygame.sprite.collide_mask(self, borderU1):
            self.rect.x += v + 4
            self.lookD = "right"

        if int(self.rect.x) >= width:
            self.rect.x = 0
        elif int(self.rect.x) < 0:
            self.rect.x = width
        if int(self.rect.y) >= height:
            self.rect.y = 0
        elif int(self.rect.y) < 0:
            self.rect.y = height

        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]
        if self.lookD == "left":
            self.image = pygame.transform.flip(self.image, True, False)
        if self.lookD == "up":
            self.image = pygame.transform.rotate(self.image, 90)
        if self.lookD == "down":
            self.image = pygame.transform.rotate(self.image, -90)



def generate_level(level):
    for y in range(len(level)):
        for x in range(len(level[y])):
            id = level[y][x]
            if (id in tile_images):
                Tile(id, x, y)
                continue
            Tile('b', x, y)
            if id == '.':
                Point(x, y)
            elif id == 'c':
                Cherry(x, y)
            elif id == 's':
                SuperPoint(x, y)
            elif id == '@':
                Player(3, 1, x, y)
            elif id == 'e':
                Enemy(2, 1, x, y)
                Point(x, y)


generate_level(load_level('level3.txt'))


def collision(points_group, player_group, cherry_group, enemy_group,
              super_points_group):
    global count
    collisions = pygame.sprite.groupcollide(player_group, points_group,
                                            False, True)
    collisions_for_cherry = pygame.sprite.groupcollide(
        player_group, cherry_group, False, True)
    super_point = pygame.sprite.groupcollide(player_group, super_points_group,
                                             False, True)
    enemy_and_player = pygame.sprite.groupcollide(enemy_group, player_group,
                                                  False, True)
    if collisions:
        count += 10
    if collisions_for_cherry:
        count += 100
    if super_point:
        count += 50
        pygame.sprite.groupcollide(enemy_group, player_group, True, False)
    if enemy_and_player:
        pygame.font.init()
        font = pygame.font.SysFont('Comic Sans MS', 30)
        screen.blit(font.render('Game over', False, (255, 0, 0)), (750, 600))
    if count >= 1510 and count < 3030:
        generate_level(load_level('level2.txt'))
    elif count >= 3030 and count < 4450:
        generate_level(load_level('level3.txt'))
    elif count >= 4450:
        pygame.font.init()
        font = pygame.font.Font(None, 50)
        screen.blit(font.render('Win', False, (0, 255, 0)), (400, 600))


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    all_sprites.draw(screen)
    draw(screen)
    all_sprites.update()
    collision(points_group, player_group, cherry_group, enemy_group,
              super_points_group)
    clock.tick(FPS)
    pygame.display.flip()
pygame.quit()
