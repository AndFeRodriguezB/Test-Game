import pygame.sprite

class DamageText(pygame.sprite.Sprite):
    def __init__(self, x, y, damage, font, color):
        pygame.sprite.Sprite.__init__(self)
        self.image = font.render(damage, True, color)
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.contador = 0

    def update(self, position_screen):
        self.rect.x += position_screen[0]
        self.rect.y += position_screen[1]

        self.rect.y -= 2
        self.contador += 1
        if self.contador > 50:
            self.kill()