import pygame


class BackGround(pygame.sprite.Sprite):
    def __init__(self, img, location):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(img).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location
