import pygame.sprite

class Item(pygame.sprite.Sprite):
    def __init__(self, x, y, item_type, animation_list):
       pygame.sprite.Sprite.__init__(self)
       self.item_type = item_type # 0 = coins, 1 = potions
       self.animation_list = animation_list
       self.frame_index = 0
       self.update_time = pygame.time.get_ticks()
       self.image = self.animation_list[self.frame_index]
       self.rect = self.image.get_rect()
       self.rect.center = (x,y)

    # screen-based items replenishment
    def update(self, position_screen, character):
       self.rect.x += position_screen[0]
       self.rect.y += position_screen[1]
       # Check the collision between the character and the items
       if self.rect.colliderect(character.shape):
          # Coins
          if self.item_type == 0:
             character.score += 1
          elif self.item_type == 1:
             character.energy += 50
             if character.energy > 100:
               character.energy = 100
          self.kill()

       cooldown_animation = 100
       self.image = self.animation_list[self.frame_index]

       if pygame.time.get_ticks() - self.update_time > cooldown_animation:
          self.frame_index += 1
          self.update_time = pygame.time.get_ticks()

       if self.frame_index >= len(self.animation_list):
          self.frame_index = 0

