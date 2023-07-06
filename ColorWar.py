import pygame as pg
import numpy as np

import random
import math

import time

WIDTH = 300
HEIGHT = 300

INTERACTION_DISTANCE = 5

clock = pg.time.Clock()

pg.init()
screen = pg.display.set_mode((WIDTH,HEIGHT))

#  RED:    1   (200,0,0)
#  ORANGE: 2   (200,100,0)
#  YELLOW: 3   (200,200,0)
#  GREEN: 4    (0,200,0)
#  BLUE: 5     (40,100,200)
#  PURPLE: 6   (100,0,180)
# #

dots = []

TIMESCALE = 1
BABYTIME = 30

DEATHTIMEMIN = 50
DEATHTIMEMAX = 100

MINCHILDREN = 1
MAXCHILDREN = 4

RADCAPMIN = 1
RADCAPMAX = 25

STEPSIZE = 1

BUFFER = 0.1

def distance(pos1, pos2):
  distance = np.sqrt((pos2[0] - pos1[0])**2 + (pos2[1]-pos1[1])**2)
  return distance

def radiansfromratio(num, dem):
   if num == 0 and dem == 0:
      return 0

   if dem == 0:
      if num > 0:
         return (np.pi)/2
      elif num < 0:
         return (3*np.pi)/2
   else:
      return np.arctan(num/dem)

class Dot:
  def __init__ (self, color):
    self.age = 0
    self.children = 0
    self.maxChildren = int(np.round(random.uniform(MINCHILDREN, MAXCHILDREN)))
    self.maxAge = int(np.round(random.uniform(DEATHTIMEMIN, DEATHTIMEMAX)))
    self.maxSize = int(np.round(random.uniform(RADCAPMIN, RADCAPMAX)))

    self.radius = 2
    self.color = color

    self.x = int(np.round(random.uniform(self.radius, WIDTH-self.radius)))
    self.y = int(np.round(random.uniform(self.radius, HEIGHT-self.radius)))

    self.stepSize = STEPSIZE

    self.stepx = int(np.round(random.uniform(-self.radius-self.stepSize, self.radius+self.stepSize)))
    self.stepy = int(np.round(random.uniform(-self.radius-self.stepSize, self.radius+self.stepSize)))

  def behave(self):
    self.age += TIMESCALE 
    
    if self.age > self.maxAge:
      self.color = 0
      return
    
    if self.radius > self.maxSize:
      self.children += 1
      newDot = Dot(self.color)
      newDot.x = self.x
      newDot.y = self.y
      radCut = int(self.radius/2)
      newDot.radius = radCut
      self.radius = self.radius-radCut
      dots.append(newDot)

    self.x += self.stepx
    self.y -= self.stepy

    if self.x <= -self.radius:
      self.x = WIDTH + self.radius
    if self.x >= self.radius + WIDTH:
      self.x = -self.radius
    if self.y <= -self.radius:
      self.y = HEIGHT + self.radius
    if self.y >= self.radius + HEIGHT:
      self.y = -self.radius

    self.stepx = int(np.round(random.uniform(-self.radius*self.stepSize, self.radius*self.stepSize)))
    self.stepy = int(np.round(random.uniform(-self.radius*self.stepSize, self.radius*self.stepSize)))

    for particle in dots:
      dist = distance((self.x, self.y),(particle.x, particle.y))
      if dist <= self.radius + particle.radius + INTERACTION_DISTANCE and particle is not self:
        rotation = radiansfromratio(particle.y-self.y, particle.x-self.x)
        self.x += int(np.round(np.cos(rotation) * ((self.radius+particle.radius) - dist)))
        self.y += int(np.round(np.sin(rotation) * ((self.radius+particle.radius) - dist)))

        if particle.color == 0:
          self.age -= BABYTIME/2
          self.radius += 1
          particle.radius -= 1
          if particle.radius == 0:
            dots.remove(particle)
            particle = None
        elif particle.color != self.color:
          particle.color = self.color
        elif self.age > BABYTIME+(BABYTIME*self.children) and particle.age > BABYTIME+(BABYTIME*self.children) and self.children < self.maxChildren and particle.children < particle.maxChildren:
          self.children += 1
          particle.children += 1
          newDot = Dot(self.color)
          newDot.x = self.x
          newDot.y = self.y
          newDot.radius = int(np.round((self.radius + particle.radius)/2))
          newDot.maxAge = int(np.round((self.maxAge + particle.maxAge)/2))
          newDot.maxChildren = int(np.round((self.maxChildren + particle.maxChildren)/2))
          newDot.maxSize = int(np.round((self.maxSize + particle.maxSize)/2))
          dots.append(newDot)

  def draw(self):
    if self.color == 0:
      pg.draw.circle(screen, (90,90,90), (self.x, self.y), self.radius)
    elif self.color == 1:
      pg.draw.circle(screen, (200,0,0), (self.x, self.y), self.radius)
    elif self.color == 2:
      pg.draw.circle(screen, (200,100,0), (self.x, self.y), self.radius)
    elif self.color == 3:
      pg.draw.circle(screen, (200,200,0), (self.x, self.y), self.radius)
    elif self.color == 4:
      pg.draw.circle(screen, (0,200,0), (self.x, self.y), self.radius)
    elif self.color == 5:
      pg.draw.circle(screen, (40,100,200), (self.x, self.y), self.radius)
    elif self.color == 6:
      pg.draw.circle(screen, (100,0,180), (self.x, self.y), self.radius)

    self.behave()

playing = True

random.seed(time.localtime)

DOT_COUNT = 20
for i in range(DOT_COUNT):
  newDot = Dot(6)
  dots.append(newDot)
  newDot = Dot(5)
  dots.append(newDot)
  newDot = Dot(4)
  dots.append(newDot)
  newDot = Dot(3)
  dots.append(newDot)
  newDot = Dot(2)
  dots.append(newDot)
  newDot = Dot(1)
  dots.append(newDot)
   

while playing:

  for event in pg.event.get():
    if event.type == pg.QUIT:
        playing = False
        pg.display.quit()
        pg.quit()

  screen.fill((0,0,0))
  for dot in dots:
    dot.draw()
  
  time.sleep(BUFFER)

  pg.display.update()
