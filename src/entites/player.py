import os
import pygame as pg
from ..common.enums.direction_type import DirectionType

def clip(surf,x,y,x_size,y_size, player="No"):
    # Recortar imagenes del hojade sprites
  handle_surf = surf.copy()
  clipR = pg.Rect(x,y,x_size,y_size)
  handle_surf.set_clip(clipR)
  image = surf.subsurface(handle_surf.get_clip())
  if player == "Yes":
    rect = image.get_rect()
    image = pg.transform.scale(
      image,
        (
          int(rect.width * 2),
          int(rect.height * 2),
        ),
      )
  return image.copy()

class Player(pg.sprite.Sprite):
  def __init__(self, x = 0, y = 0):
    pg.sprite.Sprite.__init__(self)
    self.LEFT_KEY, self.RIGHT_KEY, self.FACING_RIGHT = False, False, False
    self.is_jumping, self.on_ground = False, False

    path = os.path.join('src', 'assets', 'sprites', 'hero.png')
    self.sprite_sheet = pg.image.load(path)
    self.__load_hero_from_sheet()
    self.rect = self.right_idle_frames[0].get_rect()
    self.rect.x = x
    self.rect.y = y
    self.current_frame = 0
    
    self.position = pg.Vector2(self.rect.x, self.rect.y)
    self.velocity = pg.Vector2(0, 0)
    self.gravity = 0.5

    self.state = "idle_r"
    self.current_image = self.right_idle_frames[0]

    self.last_update = pg.time.get_ticks()


  def __pressed(self):
    keys = pg.key.get_pressed()
    self.state = "idle_r"
    if keys[pg.K_a]:
      self.velocity.x = -5
      self.state = "walk_l"
      self.FACING_RIGHT = False
    elif keys[pg.K_d]:
      self.velocity.x = 5
      self.state = "walk_r"
      self.FACING_RIGHT = True
    else:
      self.velocity.x = 0
    if keys[pg.K_w] and self.hits:
      self.velocity.y -= 13
      if self.velocity.x < 0:
        self.state = "jump_l"
      else: 
        self.state = "jump_r"

  def update(self, hits):
    self.hits = hits

    self.velocity.y += self.gravity

    if self.hits:
      self.velocity.y = -self.gravity

    self.__pressed()

    self.position += self.velocity

    self.rect.x = self.position.x 
    self.rect.y = self.position.y
    self.__animate()

  def draw(self, surface):
    surface.blit(self.current_image, (self.rect.x, self.rect.y))

  def __animate(self):
    now = pg.time.get_ticks() 
    if self.state == "idle_r":
      if now - self.last_update > 200:
        self.last_update = now
        self.current_frame = (self.current_frame + 1) % len(self.right_idle_frames)
        if self.FACING_RIGHT:
          self.current_image = self.right_idle_frames[self.current_frame]
        else:
          self.current_image = self.left_idle_frames[self.current_frame]
    elif self.state == "walk_r" or self.state == "walk_l":
      if now - self.last_update > 200:
        self.last_update = now
        self.current_frame = (self.current_frame + 1) % len(self.right_walk_frames)
        if self.state == "walk_r":
          self.current_image = self.right_walk_frames[self.current_frame]
        elif self.state == "walk_l":
          self.current_image = self.left_walk_frames[self.current_frame]
    else:
      if now - self.last_update > 50:
        self.current_frame = (self.current_frame + 1) % len(self.right_jump_frames)
        if self.state == "jump_r":
          self.current_image = self.right_jump_frames[self.current_frame]
        elif self.state == "jump_l":
          self.current_image = self.left_jump_frames[self.current_frame]


  def __load_hero_from_sheet(self, option="no"):
        self.option = option
        # self.right_frames = []
        # self.left_frames = []

        self.right_idle_frames = []
        self.right_walk_frames = []
        self.right_jump_frames = []
        # self.right_attack_frames = []
        # self.right_duck_frames = []
        # self.right_dead_frames = []

        self.left_idle_frames = []
        self.left_walk_frames = []
        self.left_jump_frames = []
        # self.left_attack_frames = []
        # self.left_duck_frames = []
        # self.left_dead_frames = []

        self.right_idle_frames.append(clip(self.sprite_sheet,10, 5, 24, 29,"Yes"))
        self.right_idle_frames.append(clip(self.sprite_sheet,60, 5, 24, 29,"Yes"))
        self.right_idle_frames.append(clip(self.sprite_sheet,110, 5, 24, 29,"Yes"))
        self.right_idle_frames.append(clip(self.sprite_sheet,160, 5, 24, 29,"Yes"))

        self.right_walk_frames.append(clip(self.sprite_sheet,10, 42, 26, 29,"Yes"))
        self.right_walk_frames.append(clip(self.sprite_sheet,60, 42, 26, 29,"Yes"))
        self.right_walk_frames.append(clip(self.sprite_sheet,110, 42, 26, 29,"Yes"))
        self.right_walk_frames.append(clip(self.sprite_sheet,160, 42, 26, 29,"Yes"))
        self.right_walk_frames.append(clip(self.sprite_sheet,210, 42, 26, 29,"Yes"))
        self.right_walk_frames.append(clip(self.sprite_sheet,260, 42, 26, 29,"Yes"))

        self.right_jump_frames.append(clip(self.sprite_sheet,10, 75, 27, 32,"Yes"))
        self.right_jump_frames.append(clip(self.sprite_sheet,60, 75, 27, 32,"Yes"))
        self.right_jump_frames.append(clip(self.sprite_sheet,110, 75, 27, 32,"Yes"))
        self.right_jump_frames.append(clip(self.sprite_sheet,160, 75, 27, 32,"Yes"))
        self.right_jump_frames.append(clip(self.sprite_sheet,210, 75, 27, 32,"Yes"))
        self.right_jump_frames.append(clip(self.sprite_sheet,260, 75, 27, 32,"Yes"))
        self.right_jump_frames.append(clip(self.sprite_sheet,310, 75, 27, 32,"Yes"))
        self.right_jump_frames.append(clip(self.sprite_sheet,360, 75, 27, 32,"Yes"))
        self.right_jump_frames.append(clip(self.sprite_sheet,410, 75, 27, 32,"Yes"))
        self.right_jump_frames.append(clip(self.sprite_sheet,460, 75, 27, 32,"Yes"))

        for frame in self.right_idle_frames:
            new_image = pg.transform.flip(frame, True, False)
            self.left_idle_frames.append(new_image)

        for frame in self.right_walk_frames:
            new_image = pg.transform.flip(frame, True, False)
            self.left_walk_frames.append(new_image)

        for frame in self.right_jump_frames:
            new_image = pg.transform.flip(frame, True, False)
            self.left_jump_frames.append(new_image)