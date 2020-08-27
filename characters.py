import pygame
import random


class Zombie(pygame.sprite.Sprite):
    def __init__(self, zombie_img_r, zombie_location, player_pos_x):
        pygame.sprite.Sprite.__init__(self)
        self.zombie_img_right = pygame.image.load(zombie_img_r).convert_alpha()
        self.rect = self.zombie_img_right.get_rect()
        self.rect.x, self.rect.y = zombie_location
        self.z_current_location = zombie_location

        self.zombie_right = False
        self.zombie_left = False
        self.zombie_hit = False
        self.zombie_hit_wall = False
        self.zombie_next_hit = 0

        self.zombie_health = 50
        self.zombie_damage = 5
        self.zombie_speed = 1
        self.zombie_drops = 10
        self.zombie_change_x = 0

    def zombie_health_bar(self):
        pass

    def stop_zombie(self):
        self.zombie_change_x = 0

    def move_zombie(self, player, walls, p_current_pos):
        if self.z_current_location[0] < p_current_pos and not pygame.sprite.collide_rect(self, player):
            self.zombie_change_x = self.zombie_speed
            self.zombie_left = True
            self.zombie_right = False
        elif self.z_current_location[0] > p_current_pos and not pygame.sprite.collide_rect(self, player):
            self.zombie_change_x = -self.zombie_speed
            self.zombie_left = False
            self.zombie_right = True
        if pygame.sprite.collide_rect(self, player):
            self.stop_zombie()
            if pygame.time.get_ticks() < self.zombie_next_hit:
                return
            self.zombie_next_hit = pygame.time.get_ticks() + 600
            self.zombie_hit = True
        if pygame.sprite.spritecollideany(self, walls):
            self.stop_zombie()
            if pygame.time.get_ticks() < self.zombie_next_hit:
                return
            self.zombie_next_hit = pygame.time.get_ticks() + 600
            self.zombie_hit_wall = True

    def update(self, player, walls, player_x):
        self.move_zombie(player, walls, player_x)
        self.rect.x += self.zombie_change_x
        self.z_current_location = self.rect.x, self.rect.y


class player_class(pygame.sprite.Sprite):
    def __init__(self, player_image_left, player_location, game_floor, *groups):
        self.player_img_left = pygame.image.load(player_image_left)
        self.rect = self.player_img_left.get_rect()
        self.rect.x, self.rect.y = player_location
        self.current_location = player_location
        self.next_jump = 0
        self.player_floor = game_floor
        self.player_speed = 5
        self.player_change_x = 0
        self.player_change_y = 0
        self.player_health = 100
        self.player_coins = 0
        self.player_walls = 0

        self.player_first_aid_kits = 0
        self.player_heal = 40
        self.shields = 0

    def move_left(self):
        self.player_change_x = -self.player_speed

    def move_right(self):
        self.player_change_x = self.player_speed

    def player_stop_x(self):
        self.player_change_x = 0

    def player_stop_y(self):
        self.player_change_y = 0

    def player_jump(self):
        if pygame.time.get_ticks() < self.next_jump:
            return
        self.next_jump = pygame.time.get_ticks() + 1200
        self.player_change_y = -10

    def player_gravity(self):
        if self.current_location[1] < self.player_floor - 190:
            self.player_change_y += .3
        else:
            self.player_change_y = 0

    def player_update(self):
        self.rect.x += self.player_change_x
        self.rect.y += self.player_change_y
        self.current_location = self.rect.x, self.rect.y
        self.player_gravity()


class wall(pygame.sprite.Sprite):
    def __init__(self, wall_location, game_floor):
        pygame.sprite.Sprite.__init__(self)
        self.wall_image = pygame.image.load("Assets/wall.png")
        self.wall_image_red = pygame.image.load("Assets/wall_red.png")
        self.wall_image_green = pygame.image.load("Assets/wall_green.png")
        self.floor = game_floor - 138
        self.rect = self.wall_image.get_rect()
        self.rect_x, self.rect_y = wall_location
        self.wall_permanent = False
        self.wall_permanent_location = 0

        self.wall_hp = 200

    def stop_movement(self):
        pass

    def update(self):
         self.rect = (self.wall_permanent_location, self.floor, 70, 138)


