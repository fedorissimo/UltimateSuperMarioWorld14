import pygame
import os
import sys


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


pygame.init()
size = width, height = 500, 500
screen = pygame.display.set_mode(size)
sprite_group = pygame.sprite.Group()
hero_group = pygame.sprite.Group()

tile_sprite = {'wall': load_image('box.png'), 'empty': load_image('grass.png')}
player_sprite = load_image('mar.png')

tile_width = tile_height = 50


class Camera:
    def __init__(self):
        self.dx = 0
        self.dy = 0

    def apply(self, obj):
        obj.rect.x = obj.abs_pos[0] + self.dx
        obj.rect.y = obj.abs_pos[1] + self.dy

    def update(self, target):
        self.dx = 0
        self.dy = 0



class Sprite(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)
        self.rect = None


class Tile(Sprite):
    def __init__(self, tile_type, x, y):
        super().__init__(sprite_group)
        self.image = tile_sprite[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * x, tile_height * y)
        self.abs_pos = (self.rect.x, self.rect.y)

    def camera(self):
        pass


class Player(Sprite):
    def __init__(self, x, y):
        super().__init__(hero_group)
        self.image = player_sprite
        self.rect = self.image.get_rect().move(
            tile_width * x + 15, tile_height * y + 5)
        self.pos = (x, y)

    def move(self, x, y):
        camera.dx -= tile_width * (x - self.pos[0])
        camera.dy -= tile_height * (y - self.pos[1])
        self.pos = (x, y)
        for sprite in sprite_group:
            camera.apply(sprite)


def start_screen():
    background = pygame.transform.scale(load_image('fon.jpg'), size)
    screen.blit(background, (0, 0))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()


def load_level(filename):
    filename1 = 'data/' + input()
    filename = 'data/' + filename
    if os.path.exists(filename1):
        with open(filename1, 'r') as carta:
            level_map = [line.strip() for line in carta]
        max_width = max(map(len, level_map))
        return list(map(lambda x: list(x.ljust(max_width, '.')), level_map))
    else:
        raise IOError()


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                new_player = Player(x, y)
                level[y][x] = '.'
    return new_player, x, y


camera = Camera()
running = True
start_screen()
level_map = load_level('map.map')
hero, max_x, max_y = generate_level(level_map)
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            x, y = hero.pos
            if event.key == pygame.K_UP:
                if y > 0 and level_map[y - 1][x] == '.':
                    hero.move(x, y - 1)
            if event.key == pygame.K_DOWN:
                if y < max_y - 1 and level_map[y + 1][x] == '.':
                    hero.move(x, y + 1)
            if event.key == pygame.K_RIGHT:
                if x < max_x - 1 and level_map[y][x + 1] == '.':
                    hero.move(x + 1, y)
            if event.key == pygame.K_LEFT:
                if x > 0 and level_map[y][x - 1] == '.':
                    hero.move(x - 1, y)
    screen.fill(pygame.Color('black'))
    sprite_group.draw(screen)
    hero_group.draw(screen)
    pygame.display.flip()
pygame.quit()
