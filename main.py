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
WIDTH, HEIGHT = 500, 200
FPS = 60
PLAYER_VEL = 5  # speed of player

# set up pygame window
window = pygame.display.set_mode((WIDTH, HEIGHT))


# create a player that inherits from pygame's Sprite
class Player(pygame.sprite.Sprite):
  COLOR = (255, 0, 0)

  def __init__(self, x, y, width, height):
    # using pygame.Rect to help with collision
    self.rect = pygame.Rect(x, y, width, height)
    self.x_vel = 0
    self.y_vel = 0  # how fast the player moves within each frame
    self.mask = None
    self.direction = "left"  #keep track of facing direction for sprite usage
    self.animation_count = 0  # animation does not wobbly when switching left/right

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

  # will be called every frame to handle movement and animation
  def loop(self, fps):
    self.move(self.x_vel, self.y_vel)

  def draw(self, window):
    pygame.draw.rect(window, self.COLOR, self.rect)


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


def draw(window, background, bg_image, player):
  # draw bg_image at every tile pos
  for tile in background:
    window.blit(bg_image, tile)

  # draw player
  player.draw(window)

  pygame.display.update()


# event loop
def main(window):
  clock = pygame.time.Clock()

  # set and get background info
  background, bg_image = get_background("Gray.png")

  # create a player
  player = Player(100, 100, 50, 50)

  # define game loop
  run = True
  while run:
    clock.tick(FPS)  # ensure loop runs at FPS fps

    for event in pygame.event.get():
      # check for user quit
      if event.type == pygame.QUIT:
        run = False
        break

    # draw tiled background
    draw(window, background, bg_image, player)

  pygame.quit()
  quit()


# only call main if we run this file directly
#   won't run main if this file is imported into another file
if __name__ == "__main__":
  main(window)
