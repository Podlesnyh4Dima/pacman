import pygame
import os
from pygame.locals import *


pygame.display.set_caption('Pacman')
movement_x = movement_y = 0
FPS = 10
clock = pygame.time.Clock()
v = 0.0625
tile_width = tile_height = 50
size = width, height = 1000, 600
screen = pygame.display.set_mode(size)


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    image = pygame.image.load(fullname)
    return image


right = load_image("pacman/pacman1.png")
left = load_image("pacman/pacman2.png")
up = load_image("pacman/pacman3.png")
down = load_image("pacman/pacman4.png")
character = up


def load_level(filename):
    filename = "data/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


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
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()


class Border(pygame.sprite.Sprite):
    def __init__(self, image, x):
        super().__init__(all_sprites)
        self.image = image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.bottomleft = x


imageL1 = load_image('map/borderL1.png')
borderL1 = Border(imageL1, (0, 600))

imageL2 = load_image('map/borderL2.png')
borderL2 = Border(imageL2, (500, 600))

imageR1 = load_image('map/borderR1.png')
borderR1 = Border(imageR1, (0, 600))

imageR2 = load_image('map/borderR2.png')
borderR2 = Border(imageR2, (500, 600))

imageU1 = load_image('map/borderU1.png')
borderU1 = Border(imageU1, (0, 600))

imageU2 = load_image('map/borderU2.png')
borderU2 = Border(imageU2, (500, 600))

imageD1 = load_image('map/borderD1.png')
borderD1 = Border(imageD1, (0, 600))

imageD2 = load_image('map/borderD2.png')
borderD2 = Border(imageD2, (500, 600))


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, x_pos, y_pos):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * x_pos, tile_height * y_pos)


class Player(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x_pos, y_pos):
        super().__init__(all_sprites)
        self.movement_x = movement_x
        self.movement_y = movement_y
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.image.get_rect().move(
            tile_width * x_pos + 15, tile_height * y_pos + 5)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns, sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(frame_location, self.rect.size)))

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]
        if event.type == KEYDOWN:
            if event.key == K_RIGHT and not pygame.sprite.collide_mask(self, borderR1) \
                    and not pygame.sprite.collide_mask(self, borderR2):
                self.movement_x = 5
                self.movement_y = 0
            if event.key == K_LEFT and not pygame.sprite.collide_mask(self, borderL1) \
                    and not pygame.sprite.collide_mask(self, borderL2):
                self.movement_x = -5
                self.movement_y = 0
            if event.key == K_DOWN and not pygame.sprite.collide_mask(self, borderD1) \
                    and not pygame.sprite.collide_mask(self, borderD2):
                self.movement_y = 5
                self.movement_x = 0
            if event.key == K_UP and not pygame.sprite.collide_mask(self, borderU1) \
                    and not pygame.sprite.collide_mask(self, borderU2):
                self.movement_y = -5
                self.movement_x = 0

        self.rect.x += self.movement_x
        self.rect.y += self.movement_y

        if pygame.sprite.collide_mask(self, borderL1) or pygame.sprite.collide_mask(self, borderL2):
            self.rect.x += 5
        if pygame.sprite.collide_mask(self, borderR1) or pygame.sprite.collide_mask(self, borderR2):
            self.rect.x += -5
        if pygame.sprite.collide_mask(self, borderD1) or pygame.sprite.collide_mask(self, borderD2):
            self.rect.y += -5
        if pygame.sprite.collide_mask(self, borderU1) or pygame.sprite.collide_mask(self, borderU2):
            self.rect.y += 5


        if int(self.rect.x) >= width:
            self.rect.x = 0
        elif int(self.rect.x) < 0:
            self.rect.x = width
        if int(self.rect.y) >= height:
            self.rect.y = 0
        elif int(self.rect.y) < 0:
            self.rect.y = height



def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '$':
                Tile('wall2', x, y)
            elif level[y][x] == '!':
                Tile('wall3', x, y)
            elif level[y][x] == '%':
                Tile('wall4', x, y)
            elif level[y][x] == '^':
                Tile('wall5', x, y)
            elif level[y][x] == '&':
                Tile('wall6', x, y)
            elif level[y][x] == '*':
                Tile('wall7', x, y)
            elif level[y][x] == '`':
                Tile('wall8', x, y)
            elif level[y][x] == '~':
                Tile('wall9', x, y)
            elif level[y][x] == '/':
                Tile('wall10', x, y)
            elif level[y][x] == '?':
                Tile('wall11', x, y)
            elif level[y][x] == '|':
                Tile('wall12', x, y)
            elif level[y][x] == '>':
                Tile('wall13', x, y)
            elif level[y][x] == ',':
                Tile('wall14', x, y)
            elif level[y][x] == '<':
                Tile('wall15', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                new_player = Player(character, 3, 1, x, y)
    return new_player, x, y


player, level_x, level_y = generate_level(load_level('levelex.txt'))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    all_sprites.draw(screen)
    all_sprites.update()
    clock.tick(FPS)
    pygame.display.flip()
pygame.quit()
