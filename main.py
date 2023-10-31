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

# 


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


def draw(window, background, bg_image):
  # draw bg_image at every tile pos
  for tile in background:
    window.blit(bg_image, tile)

  pygame.display.update()


# event loop
def main(window):
  clock = pygame.time.Clock()

  # set and get background info
  background, bg_image = get_background("Gray.png")

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
    draw(window, background, bg_image)

  pygame.quit()
  quit()


# only call main if we run this file directly
#   won't run main if this file is imported into another file
if __name__ == "__main__":
  main(window)
