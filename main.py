import os
import random
import math
import pygame
from os import listdir
from os.path import isfile, join

# initialize pygame module
pygame.init()

# set caption and window for pygame
pygame.display.set_caption("2D PLATFORMER")

# set global variables
WIDTH, HEIGHT = 500, 400
FPS = 60
PLAYER_VEL = 5  # speed of player

# set up pygame window
window = pygame.display.set_mode((WIDTH, HEIGHT))


# flip sprite so we can face the correct direction
def flip(sprites):
  return [pygame.transform.flip(sprite, True, False) for sprite in sprites]


# load all sprite sheets for character
def load_sprite_sheet(dir1, dir2, width, height, direction=False):
  path = join("assets", dir1, dir2)
  # load every file inside desired directory
  images = [f for f in listdir(path) if isfile(join(path, f))]

  all_sprites = {}

  for image in images:
    # load sprite sheet with transparent background
    sprite_sheet = pygame.image.load(join(path, image)).convert_alpha()

    sprites = []

    for i in range(sprite_sheet.get_width() // width):
      # slice sprite sheet based on width
      surface = pygame.Surface((width, height), pygame.SRCALPHA, 32)
      rect = pygame.Rect(i * width, 0, width, height)
      surface.blit(sprite_sheet, (0, 0), rect)
      sprites.append(pygame.transform.scale2x(surface))

    # create a left and right version if needed
    if direction:
      all_sprites[image.replace(".png", "") + "_right"] = sprites
      all_sprites[image.replace(".png", "") + "_left"] = flip(sprites)
    else:
      all_sprites[image.replace(".png", "")] = sprites

  return all_sprites


def load_block(size):
  path = join("assets", "Terrain", "Terrain.png")
  image = pygame.image.load(path).convert_alpha()
  surface = pygame.Surface((size, size), pygame.SRCALPHA, 32)
  #96,0 is the location of the green block in Terrain.png
  rect = pygame.Rect(96, 0, size, size)
  surface.blit(image, (0, 0), rect)
  return surface


# create a player that inherits from pygame's Sprite
class Player(pygame.sprite.Sprite):
  COLOR = (255, 0, 0)
  GRAVITY = 1
  SPRITES = load_sprite_sheet("MainCharacters", "PinkMan", 32, 32, True)
  ANIMATION_DELAY = 3

  def __init__(self, x, y, width, height):
    super().__init__()
    # using pygame.Rect to help with collision
    self.rect = pygame.Rect(x, y, width, height)
    self.x_vel = 0
    self.y_vel = 0  # how fast the player moves within each frame
    self.mask = None
    self.direction = "left"  #keep track of facing direction for sprite usage
    self.animation_count = 0  # animation does not wobbly when switching left/right
    self.fall_count = 0  # to help with gravity acceleration

  def move(self, dx, dy):
    self.rect.x += dx
    self.rect.y += dy

  def move_left(self, vel):
    self.x_vel = -vel
    if self.direction != "left":
      self.direction = "left"
      self.animation_count = 0

  def move_right(self, vel):
    self.x_vel = vel
    if self.direction != "right":
      self.direction = "right"
      self.animation_count = 0

  def landed(self):
    self.fall_count = 0
    self.y_vel = 0
    self.jump_count = 0

  def hit_head(self):
    self.count = 0
    self.y_vel *= -1

  # will be called every frame to handle movement and animation
  def loop(self, fps):
    self.y_vel += min(1, (self.fall_count / fps) * self.GRAVITY)
    self.move(self.x_vel, self.y_vel)

    self.fall_count += 1
    self.update_sprite()

  # this updates the sprite image to act as an animated character
  def update_sprite(self):
    sprite_sheet = "idle"
    if self.x_vel != 0:
      sprite_sheet = "run"

    sprite_sheet_name = sprite_sheet + "_" + self.direction
    sprites = self.SPRITES[sprite_sheet_name]
    sprite_index = (self.animation_count //
                    self.ANIMATION_DELAY) % len(sprites)

    self.sprite = sprites[sprite_index]
    self.animation_count += 1
    self.update()

  def update(self):
    self.rect = self.sprite.get_rect(topleft=(self.rect.x, self.rect.y))
    self.mask = pygame.mask.from_surface(self.sprite)

  # draw the sprite at the set location in the window
  def draw(self, window):
    window.blit(self.sprite, (self.rect.x, self.rect.y))


# base class used for all objects (uniform collision across all)
class Object(pygame.sprite.Sprite):

  def __init__(self, x, y, width, height, name=None):
    super().__init__()
    self.rect = pygame.Rect(x, y, width, height)
    self.image = pygame.Surface((width, height), pygame.SRCALPHA)
    self.width = width
    self.height = height
    self.name = name

  def draw(self, window):
    window.blit(self.image, (self.rect.x, self.rect.y))


class Block(Object):

  def __init__(self, x, y, size):
    super().__init__(x, y, size, size)
    block = load_block(size)
    self.image.blit(block, (0, 0))
    self.mask = pygame.mask.from_surface(self.image)


# pass in the color to change the background color/image
def get_background(name):
  # load image based on color name
  image = pygame.image.load(join("assets", "Background", name))
  _, _, width, height = image.get_rect()  # get width and height of image

  tiles = []
  # fill the screen with tiles (+1 to ensure no gaps)
  for i in range(WIDTH // width + 1):
    for j in range(HEIGHT // height + 1):
      pos = (i * width, j * height)  # pos of top left corner of current tile
      tiles.append(pos)

  return tiles, image


def draw(window, background, bg_image, player, objects):
  # draw bg_image at every tile pos
  for tile in background:
    window.blit(bg_image, tile)

  for obj in objects:
    obj.draw(window)

  # draw player
  player.draw(window)

  pygame.display.update()


def handle_vertical_collision(player, objects, dy):
  collided_objects = []
  for obj in objects:
    if pygame.sprite.collide_mask(player, obj):
      if dy > 0:  # if moving down and colide with object
        player.rect.bottom = obj.rect.top  # move bottom of player to top of object
        player.landed()
      elif dy < 0:
        player.rect.top = obj.rect.bottom  # move top of player to bottom of object
        player.hit_head()

    collided_objects.append(obj)

  return collided_objects


def handle_move(player, objects):
  # get key pressed
  keys = pygame.key.get_pressed()

  player.x_vel = 0  # player only moves if key is held

  # check key pressed and handle that
  if keys[pygame.K_LEFT] or keys[pygame.K_a]:
    player.move_left(PLAYER_VEL)
  if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
    player.move_right(PLAYER_VEL)

  handle_vertical_collision(player, objects, player.y_vel)


# event loop
def main(window):
  clock = pygame.time.Clock()

  # set and get background info
  background, bg_image = get_background("Gray.png")

  # create a player
  player = Player(100, 100, 50, 50)
  block_size = 48
  floor = [
      Block(i * block_size, HEIGHT - block_size, block_size)
      for i in range(-WIDTH // block_size, (WIDTH * 2) // block_size)
  ]

  # define game loop
  run = True
  while run:
    clock.tick(FPS)  # ensure loop runs at FPS fps

    for event in pygame.event.get():
      # check for user quit
      if event.type == pygame.QUIT:
        run = False
        break

    player.loop(FPS)
    handle_move(player, floor)
    # draw tiled background
    draw(window, background, bg_image, player, floor)

  pygame.quit()
  quit()


# only call main if we run this file directly
#   won't run main if this file is imported into another file
if __name__ == "__main__":
  main(window)
