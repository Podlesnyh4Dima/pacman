import pygame
import os
from pygame.locals import *

pygame.display.set_caption('Pacman')
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
    screen.blit(pygame.transform.scale(
        load_image('fon.png'), (1000, 50)),  (0, 600))
    screen.blit(font.render('Счёт: ' + str(count), False,
                            (255, 255, 255)), (0, 600))
    screen.blit(font.render('Win', False,
                            (255, 255, 255)), (400, 600))
    screen.blit(font.render('Game over', False, (255, 255, 255)), (750, 600))


def load_image(name):
    fullname = os.path.join('data', name)
    image = pygame.image.load(fullname).convert_alpha()
    return image


def load_level(filename):
    filename = "data/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


pygame.display.set_icon(load_image('logo.png'))
player_image = load_image("pacman/pacman1.png")
tile_images = {
    'b': (load_image('map/black.png'), (False, False, False, False)),
    '#': (load_image('map/wall.png'), (True, True, True, True)),
    '$': (load_image('map/wall2.png'), (False, True, False, True)),
    '!': (load_image('map/wall3.png'), (True, False, True, False)),
    '%': (load_image('map/wall4.png'), (False, False, True, True)),
    '^': (load_image('map/wall5.png'), (True, False, False, True)),
    '&': (load_image('map/wall6.png'), (True, True, False, False)),
    '*': (load_image('map/wall7.png'), (False, True, True, False)),
    '`': (load_image('map/wall8.png'), (True, False, True, True)),
    '~': (load_image('map/wall9.png'), (True, True, False, True)),
    '/': (load_image('map/wall10.png'), (True, True, True, False)),
    '?': (load_image('map/wall11.png'), (False, True, True, True)),
    '|': (load_image('map/wall12.png'), (False, False, False, True)),
    '>': (load_image('map/wall13.png'), (True, False, False, False)),
    ',': (load_image('map/wall14.png'), (False, True, False, False)),
    '<': (load_image('map/wall15.png'), (False, False, True, False)),
}

all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
points_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
cherry_group = pygame.sprite.Group()
super_points_group = pygame.sprite.Group()
borders_group = pygame.sprite.Group()


class Border(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h):
        super().__init__(borders_group)
        self.rect = pygame.Rect(x, y, w, h)
        self.type = "hor" if w > h else "ver"

    @staticmethod
    def create(x, y, top, right, bottom, left):
        x *= tile_width
        y *= tile_height
        if (top):
            Border(x, y, tile_width, 2)
        if (bottom):
            Border(x, y + tile_height - 2, tile_width, 2)
        if (left):
            Border(x, y, 2, tile_height)
        if (right):
            Border(x + tile_width - 2, y, 2, tile_height)


class GameObj(pygame.sprite.Sprite):
    image = pygame.image.load('data/cherry.png')
    group = all_sprites
    d = (0, 0)

    def __init__(self, x_pos, y_pos):
        super().__init__(self.group, all_sprites)
        self.rect = self.image.get_rect().move(
            x_pos * tile_width + self.d[0], y_pos * tile_height + self.d[1])


class Cherry(GameObj):
    image = pygame.image.load('data/cherry.png')
    group = cherry_group
    d = (15, 15)


class Point(GameObj):
    image = pygame.image.load('data/point.png')
    group = points_group
    d = (23, 23)


class SuperPoint(GameObj):
    image = pygame.image.load('data/super_point.png')
    group = super_points_group
    d = (15, 15)


class Tile(GameObj):
    group = tiles_group

    def __init__(self, tile_type, x_pos, y_pos):
        self.image = tile_images[tile_type][0]
        super().__init__(x_pos, y_pos)


class Sprite(GameObj):
    image = player_image
    columns, rows = 1, 1

    def __init__(self, x_pos, y_pos):
        self.movement_x = 0
        self.movement_y = 0
        self.frames = []
        self.cut_sheet(self.image, self.columns, self.rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.lookD = "right"
        super().__init__(x_pos, y_pos)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(
                    pygame.Rect(frame_location, self.rect.size)))

    def update(self):
        self.rect.x += self.movement_x
        self.rect.y += self.movement_y

        collisions = []
        collide = pygame.sprite.groupcollide(
            self.group, borders_group, False, False)
        if collide and self in collide:
            self.movement_x = 0
            self.movement_y = 0
            for border in collide[self]:
                if (border.type == "hor"):
                    if (self.rect.centery > border.rect.centery):
                        self.rect.y = border.rect.bottom
                        collisions.append("top")
                    else:
                        self.rect.y = border.rect.y - self.rect.height
                        collisions.append("bottom")
                else:
                    self.rect.right
                    if (self.rect.centerx > border.rect.centerx):
                        self.rect.x = border.rect.right
                        collisions.append("left")
                    else:
                        self.rect.x = border.rect.x - self.rect.width
                        collisions.append("right")

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

        return collisions


class Player(Sprite):
    image = player_image
    group = player_group
    columns, rows = 3, 1
    d = (15, 5)

    def update(self):
        if event.type == KEYDOWN:
            if event.key == K_RIGHT:
                self.movement_x = v
                self.movement_y = 0
                self.lookD = "right"
            if event.key == K_LEFT:
                self.movement_x = -v
                self.movement_y = 0
                self.lookD = "left"
            if event.key == K_DOWN:
                self.movement_y = v
                self.movement_x = 0
                self.lookD = "down"
            if event.key == K_UP:
                self.movement_y = -v
                self.movement_x = 0
                self.lookD = "up"
        return super().update()


class Enemy(Sprite):
    image = load_image("red_ghost.png")
    group = enemy_group
    columns, rows = 2, 1
    d = (25, 5)

    def __init__(self, x_pos, y_pos):
        super().__init__(x_pos, y_pos)
        self.movement_x = -v

    def update(self):
        collisions = super().update()
        if (len(collisions) == 0):
            return
        self.movement_x = 0
        self.movement_y = 0
        for collision in collisions:
            if (collision == "top"):
                self.movement_x = v
            elif (collision == "bottom"):
                self.movement_x = -v
            elif (collision == "left"):
                self.movement_y = -v
            elif (collision == "right"):
                self.movement_y = v


def generate_level(level):
    for y in range(len(level)):
        for x in range(len(level[y])):
            id = level[y][x]
            if (id in tile_images):
                Tile(id, x, y)
                Border.create(x, y, *tile_images[id][1])
                continue
            Tile('b', x, y)
            if id == '.':
                Point(x, y)
            elif id == 'c':
                Cherry(x, y)
            elif id == 's':
                SuperPoint(x, y)
            elif id == '@':
                Player(x, y)
            elif id == 'e':
                Enemy(x, y)
                Point(x, y)


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


generate_level(load_level('level3.txt'))
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
