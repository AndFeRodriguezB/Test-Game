import math
import pygame
import constants

class Characters():
    def __init__(self,x,y,animations, energy, tipo):
        self.score = 0
        self.energy = energy
        self. life = True
        self.flip = False
        self.animations = animations
        # Image of animation currently being shown
        self.frame_index = 0
        # The current time is stored here (in milliseconds since 'pygame' was started)
        self.update_time = pygame.time.get_ticks()
        self.image = animations[self.frame_index]
        self.shape = self.image.get_rect()
        self.shape.center = (x, y)
        self.tipo = tipo
        self.hit = False
        self.last_hit = pygame.time.get_ticks()

    def update_coordinates(self, tupla):
        self.shape.center = (tupla[0], tupla[1])

    def movement(self, delta_x, delta_y, obstacles_tiles, exit_tile):
        position_screen = [0,0]
        level_completed = False
        if delta_x < 0:
            self.flip = True
        if delta_x > 0:
            self.flip = False

        self.shape.x = self.shape.x + delta_x
        for obstacle in obstacles_tiles:
            if obstacle[1].colliderect(self.shape):
                if delta_x > 0:
                    self.shape.right = obstacle[1].left
                if delta_x < 0:
                    self.shape.left = obstacle[1].right

        self.shape.y = self.shape.y + delta_y
        for obstacle in obstacles_tiles:
            if obstacle[1].colliderect(self.shape):
                if delta_y > 0:
                    self.shape.bottom = obstacle[1].top
                if delta_y < 0:
                    self.shape.top = obstacle[1].bottom

        # Logic only applies to player, no enemies
        if self.tipo == 1:
            # Check the collision with the exit tile
            if exit_tile is not None and exit_tile[1].colliderect(self.shape):
                level_completed = True
                print("level completed")

            if self.shape.right > (constants.WIDTH_SCREEN - constants.LIMIT_SCREEN):
                position_screen [0] = (constants.WIDTH_SCREEN - constants.LIMIT_SCREEN) - self.shape.right
                self.shape.right = constants.WIDTH_SCREEN - constants.LIMIT_SCREEN

            if self.shape.left < constants.LIMIT_SCREEN:
                position_screen [0] = constants.LIMIT_SCREEN - self.shape.left
                self.shape.left = constants.LIMIT_SCREEN

            if self.shape.bottom > (constants.HEIGHT_SCREEN - constants.LIMIT_SCREEN):
                position_screen [1] = (constants.HEIGHT_SCREEN - constants.LIMIT_SCREEN) - self.shape.bottom
                self.shape.bottom = constants.HEIGHT_SCREEN - constants.LIMIT_SCREEN

            if self.shape.top < constants.LIMIT_SCREEN:
                position_screen [1] = constants.LIMIT_SCREEN - self.shape.top
                self.shape.top = constants.LIMIT_SCREEN
            return position_screen, level_completed

    def enemies(self, player, obstacles_tiles, position_screen, exit_tile):
        clipped_line = ()
        ene_dx = 0
        ene_dy = 0

        # Screen-based enemies replenishment
        self.shape.x += position_screen[0]
        self.shape.y += position_screen[1]

        # Create a vision line
        vision_line = ((self.shape.centerx, self.shape.centery),
                       (player.shape.centerx, player.shape.centery))

        # Check if there are any obstacles in the enemy's vision
        for obs in obstacles_tiles:
            if obs[1].clipline(vision_line):
                clipped_line = obs[1].clipline(vision_line)


        # Distance from the player
        distance = math.sqrt(((self.shape.centerx - player.shape.centerx)**2) +
                             ((self.shape.centery- player.shape.centery)**2))

        if not clipped_line and distance < constants.RANGO:
            if self.shape.centerx > player.shape.centerx:
                ene_dx = -constants.SPEED_ENEMY
            if self.shape.centerx < player.shape.centerx:
                ene_dx = constants.SPEED_ENEMY
            if self.shape.centery > player.shape.centery:
                ene_dy = -constants.SPEED_ENEMY
            if self.shape.centery < player.shape.centery:
                ene_dy = constants.SPEED_ENEMY

        self.movement(ene_dx, ene_dy, obstacles_tiles, exit_tile)

        # Attack the player
        if distance < constants.RANGO_ATTACK and player.hit == False:
            player.energy -= 10
            player.hit = True
            player.last_hit = pygame.time.get_ticks()

    def update(self):
        # Check if the character has died
        if self.energy <= 0:
            self.energy = 0
            self.life = False

        hit_cooldown = 800
        if self.tipo == 1:
            if self.hit == True:
                if pygame.time.get_ticks() - self.last_hit > hit_cooldown:
                    self.hit = False

        cooldown_animation = 80
        self.image = self.animations[self.frame_index]
        if pygame.time.get_ticks() - self.update_time >= cooldown_animation:
            self.frame_index = self.frame_index + 1
            self.update_time = pygame.time.get_ticks()
        if self.frame_index >= len(self.animations):
            self.frame_index = 0

    def draw(self, interface):
        image_flip = pygame.transform.flip(self.image, self.flip, False)
        interface.blit(image_flip, self.shape)
        #pygame.draw.rect(interface, constants.COLOR_CHARACTER, self.shape, 1)