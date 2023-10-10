import pygame
from network import Network

width = 500
height = 500
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Client")

clientNumber = 0


class Player():
  def __init__(self, x, y, width, height, color):
    self.x = x
    self.y = y
    self.width = width
    self.height = height
    self.color = color
    self.rect = (x,y,width,height)
    self.vel = 3

  def draw(self, win):
    pygame.draw.rect(win, self.color, self.rect)

  def move(self):
    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
      self.x -= self.vel

    if keys[pygame.K_RIGHT]:
      self.x += self.vel

    if keys[pygame.K_UP]:
      self.y -= self.vel

    if keys[pygame.K_DOWN]:
      self.y += self.vel
    
    self.update()
  
  def update(self):
    self.rect = (self.x, self.y, self.width, self.height)

def decode_pos(str_):
  str_ = str_.split(",")
  return int(str_[0]), int(str_[1])

def encode_pos(position):
  return str(position[0]) + "," + str(position[1])

def redrawWindow(win,player, player2):
  win.fill((255,255,255))
  player.draw(win)
  player2.draw(win)
  pygame.display.update()


def main():
  run = True
  n = Network()
  startPos = decode_pos(n.get_pos())
  p1 = Player(startPos[0], startPos[1],100,100,(0,255,0))
  
  p2 = Player(0, 0,100,100,(0,255,0))
  clock = pygame.time.Clock()

  while run:
    clock.tick(60)
    
    p2Pos = decode_pos(n.send(encode_pos((p1.x, p1.y))))
    p2.x = p2Pos[0]
    p2.y = p2Pos[1]
    p2.update()
    
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        run = False
        pygame.quit()

    p1.move()
    redrawWindow(win, p1, p2)

main()