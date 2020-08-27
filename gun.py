from characters import Zombie, player_class
import pygame


class gun_class(pygame.sprite.Sprite):
    def __init__(self, direction_l, direction_r, bullet_location, shot_direction):
        super().__init__()
        self.bullet_img = pygame.image.load('Assets/bullet.png').convert_alpha()
        self.rect = self.bullet_img.get_rect()
        self.bullet_speed = 30
        self.bullet_dmg = 10
        self.rect.x, self.rect.y = bullet_location
        self.bullet_current_location = bullet_location
        self.bullet_change_x = 0
        self.d_left = direction_l
        self.d_right = direction_r


    def bullet_movement(self, direction_left, direction_right):
        if direction_left is True:
            self.bullet_change_x = -self.bullet_speed
        else:
            self.bullet_change_x = self.bullet_speed

    def bullet_update(self):
        self.bullet_movement(self.d_left, self.d_right)
        self.rect.x += self.bullet_change_x
        self.bullet_current_location = self.rect.x, self.rect.y