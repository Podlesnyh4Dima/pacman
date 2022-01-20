import pygame
import os
from pygame.locals import *
from time import time

pygame.display.set_caption('Pacman')
movement_x = movement_y = 0
FPS = 10
clock = pygame.time.Clock()
ve = 5
v = 5
count = 0
tile_width = tile_height = 50
size = width, height = 1000, 650
screen = pygame.display.set_mode(size)
color = (255, 255, 255)
win_color = (255, 255, 255)
time_now = time()
timer = time() - time_now
pygame.mixer.init()
start_sound = pygame.mixer.Sound('data/sounds/pacman_beginning.wav')
death_sound = pygame.mixer.Sound('data/sounds/pacman_death.wav')
background_sound = pygame.mixer.Sound('data/sounds/siren_1.wav')
eatfruit_sound = pygame.mixer.Sound('data/sounds/pacman_eatfruit.wav')
point_sound = pygame.mixer.Sound('data/sounds/pacman_chomp.wav')


def draw(screen):
    global count
    global timer
    pygame.font.init()
    font = pygame.font.Font(None, 50)
    screen.blit(pygame.transform.scale(
        load_image('fon.png'), (1000, 50)),  (0, 600))
    screen.blit(font.render('Счёт: ' + str(count), False,
                            (255, 255, 255)), (0, 600))
    screen.blit(font.render('Win', False,
                            (255, 255, 255)), (400, 600))
    screen.blit(font.render('Game over', False, color), (750, 600))
    screen.blit(font.render('Time: ' + str(int(timer)), False,
                            (255, 255, 255)), (500, 600))
    screen.blit(font.render('Win', False, win_color), (400, 600))


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

def start_screen():
    background = pygame.transform.scale(load_image('wallpaper.jpg'), (1000, 650))
    screen.blit(background, (0, 0))



pygame.display.set_icon(load_image('logo.png'))
player_image = pygame.transform.scale(load_image('pacman/pacman1.png'), (int(tile_width * 2.5), int(tile_height * (50/59))))
tile_images = {
    'wall': load_image('map/wall.png'),
    'empty': load_image('map/black.png'),
    'wall2': load_image('map/wall2.png'),
    'wall3': load_image('map/wall3.png'),
    'wall4': load_image('map/wall4.png'),
    'wall5': load_image('map/wall5.png'),
    'wall6': load_image('map/wall6.png'),
    'wall7': load_image('map/wall7.png'),
    'wall8': load_image('map/wall8.png'),
    'wall9': load_image('map/wall9.png'),
    'wall10': load_image('map/wall10.png'),
    'wall11': load_image('map/wall11.png'),
    'wall12': load_image('map/wall12.png'),
    'wall13': load_image('map/wall13.png'),
    'wall14': load_image('map/wall14.png'),
    'wall15': load_image('map/wall15.png')
}

all_sprites = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
points_group = pygame.sprite.Group()
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
        if top:
            Border(x, y, tile_width, 2)
        if bottom:
            Border(x, y + tile_height - 2, tile_width, 2)
        if left:
            Border(x, y, 2, tile_height)
        if right:
            Border(x + tile_width - 2, y, 2, tile_height)


class Cherry(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos):
        super().__init__(cherry_group, all_sprites)
        self.image = pygame.image.load('data/cherry.png')
        self.rect = self.image.get_rect().move(
            x_pos * tile_width + 23, 23 + y_pos * tile_height)


class Point(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos):
        super().__init__(points_group, all_sprites)
        self.image = pygame.image.load('data/point.png')
        self.rect = self.image.get_rect().move(
            x_pos * tile_width + 23, 23 + y_pos * tile_height)


class SuperPoint(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos):
        super().__init__(super_points_group, all_sprites)
        self.image = pygame.image.load('data/super_point.png')
        self.rect = self.image.get_rect().move(
            x_pos * tile_width + 23, 23 + y_pos * tile_height)


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, x_pos, y_pos):
        super().__init__(tiles_group)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * x_pos, tile_height * y_pos)


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

        self.rect.x += self.movement_x
        self.rect.y += self.movement_y

        collide = pygame.sprite.groupcollide(
            player_group, borders_group, False, False)
        if collide and self in collide:
            self.movement_x = 0
            self.movement_y = 0
            for border in collide[self]:
                if (border.type == "hor"):
                    if (self.rect.centery > border.rect.centery):
                        self.rect.y = border.rect.bottom
                    else:
                        self.rect.y = border.rect.y - self.rect.height
                else:
                    self.rect.right
                    if (self.rect.centerx > border.rect.centerx):
                        self.rect.x = border.rect.right
                    else:
                        self.rect.x = border.rect.x - self.rect.width

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
    image = pygame.transform.scale(load_image('red_ghost.png'), (int(tile_width * 2), int(tile_height * 1)))
    pygame.draw.rect(screen, "red", (0, 0, 950, 550))

    def __init__(self, columns, rows, x_pos, y_pos):
        super().__init__(all_sprites, enemy_group)
        self.movement_x = -v
        self.movement_y = 0
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
        self.rect.x += self.movement_x
        self.rect.y += self.movement_y

        collide = pygame.sprite.groupcollide(
            enemy_group, borders_group, False, False)
        if collide and self in collide:
            self.movement_x = 0
            self.movement_y = 0
            for border in collide[self]:
                if (border.type == "hor"):
                    if (self.rect.centery > border.rect.centery):
                        self.rect.y = border.rect.bottom
                        self.movement_x = ve
                    else:
                        self.rect.y = border.rect.y - self.rect.height
                        self.movement_x = -ve
                else:
                    self.rect.right
                    if self.rect.centerx > border.rect.centerx:
                        self.rect.x = border.rect.right
                        self.movement_y = -ve
                    else:
                        self.rect.x = border.rect.x - self.rect.width
                        self.movement_y = ve

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
    new_enemy, new_player, x, y = None, None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == 'e':
                Tile('empty', x, y)
                Point(x, y)
                new_enemy = Enemy(2, 1, x, y)
            elif level[y][x] == '.':
                Tile('empty', x, y)
                Point(x, y)
            elif level[y][x] == 'c':
                Tile('empty', x, y)
                Cherry(x, y)
            elif level[y][x] == 's':
                Tile('empty', x, y)
                SuperPoint(x, y)
            elif level[y][x] == 'b':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
                Border.create(x, y, True, True, True, True)
            elif level[y][x] == '$':
                Tile('wall2', x, y)
                Border.create(x, y, False, True, False, True)
            elif level[y][x] == '!':
                Tile('wall3', x, y)
                Border.create(x, y, True, False, True, False)
            elif level[y][x] == '%':
                Tile('wall4', x, y)
                Border.create(x, y, False, False, True, True)
            elif level[y][x] == '^':
                Tile('wall5', x, y)
                Border.create(x, y, True, False, False, True)
            elif level[y][x] == '&':
                Tile('wall6', x, y)
                Border.create(x, y, True, True, False, False)
            elif level[y][x] == '*':
                Tile('wall7', x, y)
                Border.create(x, y, False, True, True, False)
            elif level[y][x] == '`':
                Tile('wall8', x, y)
                Border.create(x, y, True, False, True, True)
            elif level[y][x] == '~':
                Tile('wall9', x, y)
                Border.create(x, y, True, True, False, True)
            elif level[y][x] == '/':
                Tile('wall10', x, y)
                Border.create(x, y, True, True, True, False)
            elif level[y][x] == '?':
                Tile('wall11', x, y)
                Border.create(x, y, False, True, True, True)
            elif level[y][x] == '|':
                Tile('wall12', x, y)
                Border.create(x, y, False, False, False, True)
            elif level[y][x] == '>':
                Tile('wall13', x, y)
                Border.create(x, y, True, False, False, False)
            elif level[y][x] == ',':
                Tile('wall14', x, y)
                Border.create(x, y, False, True, False, False)
            elif level[y][x] == '<':
                Tile('wall15', x, y)
                Border.create(x, y, False, False, True, False)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                new_player = Player(3, 1, x, y)
    return new_player, x, y, new_enemy


def collision(points_group, player_group, cherry_group, enemy_group,
              super_points_group):
    global count
    global ve
    global v
    global win_color
    global color
    global timer
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
        point_sound.play()
    if collisions_for_cherry:
        count += 100
        eatfruit_sound.play()
    if super_point:
        count += 50
        pygame.sprite.groupcollide(enemy_group, player_group, True, False)
    if enemy_and_player:
        background_sound.stop()
        death_sound.play()
        color = (255, 0, 0)
    if count == 1510:
        level2()
    elif count == 3030:
        level3()
    elif count == 10000010:
        win_color = (0, 255, 0)
        background_sound.stop()
        pygame.font.init()
        font = pygame.font.Font(None, 50)
        screen.blit(font.render('Win', False, (0, 255, 0)), (400, 600))


def level1():
    generate_level(load_level('levelex.txt'))


def level2():
    global count
    global ve
    generate_level(load_level('level2.txt'))
    ve += 5


def level3():
    global count
    global ve
    global v
    generate_level(load_level('level3.txt'))
    v -= 1


level1()
start_sound.play()
background_sound.play(-1)
running = True
game_start = False
while running:
    start_screen()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                game_start = True
    if game_start:
        timer = time() - time_now
        tiles_group.draw(screen)
        all_sprites.draw(screen)
        draw(screen)
        all_sprites.update()
        collision(points_group, player_group, cherry_group, enemy_group,
                super_points_group)
        clock.tick(FPS)
        pygame.display.flip()
pygame.quit()
