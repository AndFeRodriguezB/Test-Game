import pygame
import constants
import math
import random

#from main import image_bullet


class Weapon():
    def __init__(self,image,image_bullet):
        self.image_bullet = image_bullet
        self.image_original = image
        self.angle = 0
        self.imagen = pygame.transform.rotate(self.image_original, self.angle)
        self.shape = self.imagen.get_rect()
        self.shot = False
        self.last_shot = pygame.time.get_ticks()

    def update(self, character):
        shot_cooldown = constants.COOLDOWN_BULLET
        bullet = None
        self.shape.center = character.shape.center
        if character.flip == False:
            self.shape.x += character.shape.width/4
            self.rotate_weapon(False)
        if character.flip == True:
            self.shape.x -= character.shape.width/4
            self.rotate_weapon(True)

        # Move the weapon with the mouse
        mouse_pos = pygame.mouse.get_pos()
        distance_x = mouse_pos[0] - self.shape.centerx
        distance_y = -(mouse_pos[1] - self.shape.centery)
        self.angle = math.degrees(math.atan2(distance_y, distance_x))

        # Detect mouse clicks
        if pygame.mouse.get_pressed()[0] and  self.shot == False and (pygame.time.get_ticks()-self.last_shot >= shot_cooldown):
            bullet = Bullet(self.image_bullet, self.shape.centerx, self.shape.centery, self.angle)
            self.shot = True
            self.last_shot = pygame.time.get_ticks()
            # Reset mouse click
        if pygame.mouse.get_pressed()[0] == False:
            self.shot = False
        return bullet


    def rotate_weapon(self, rotate):
        if rotate == True:
            image_flip = pygame.transform.flip(self.image_original,True,False)
            self.imagen = pygame.transform.rotate(image_flip,self.angle)
        else:
            image_flip = pygame.transform.flip(self.image_original,False,False)
            self.imagen = pygame.transform.rotate(image_flip, self.angle)

    def draw(self,interface):
        self.imagen = pygame.transform.rotate(self.imagen, self.angle)
        interface.blit(self.imagen,self.shape)
       # pygame.draw.rect(interface, constants.COLOR_GUN,self.shape,1)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, image, x, y, angle):
        pygame.sprite.Sprite.__init__(self)
        self.image_original = image
        self.angulo = angle
        self.image = pygame.transform.rotate(self.image_original, self.angulo)
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)

        # Speed calculation
        self.delta_x = math.cos(math.radians(self.angulo)) * constants.SPEED_BULLET
        self.delta_y = -math.sin(math.radians(self.angulo)) * constants.SPEED_BULLET

    def update(self, enemy_list, obstacle_tiles):
        damage = 0
        pos_damage = None
        self.rect.x += self.delta_x
        self.rect.y += self.delta_y

        # See If the bullets left the screen
        if self.rect.right < 0 or self.rect.left > constants.WIDTH_SCREEN or self.rect.bottom < 0 or self.rect.top > constants.HEIGHT_SCREEN:
            self.kill()

        # Check for collisions with enemies
        for enemy in enemy_list:
            if enemy.shape.colliderect(self.rect):
                damage = 15 + random.randint(-7,7)
                pos_damage = enemy.shape
                enemy.energy -= damage
                self.kill()
                break
        # Check for collisions with enemies
        for obs in obstacle_tiles:
            if obs[1].colliderect(self.rect):
                self.kill()
                break

        return damage, pos_damage

    def draw(self,interface):
        interface.blit(self.image,(self.rect.centerx,
                                  self.rect.centery - int(self.image.get_height()/2)))