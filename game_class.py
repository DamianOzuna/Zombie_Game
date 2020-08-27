import pygame, random
import sys
import time
from pygame.locals import *
from background import BackGround
from characters import player_class, Zombie, wall
from gun import gun_class

white = (255, 255, 255)
red = (255, 0, 0)


class Game:
    def __init__(self):
        self.window_width = 1920
        self.window_height = 1080
        self.player_right = True
        self.player_left = False
        self.game_round = 0
        self.round_range = range(1, self.game_round)

        self.shooting = False
        self.last_shot = 0
        self.shot_delay = 200

        self.bullet_list = pygame.sprite.Group()
        self.zombie_list = pygame.sprite.Group()
        self.wall_list = pygame.sprite.Group()
        self.next_round = True
        self.menu_countdown = 0
        self.time_remaining = 1
        self.time_created = False

        self.buy_menu_running = True
        self.main_menu_running = True
        self.game_running = True
        self.between_rounds = False
        self.placing_wall = False

        pygame.init()
        pygame.mixer.pre_init(16500, -16, 2, 2048)

        self.mouse_position = pygame.mouse.get_pos()
        self.game_font = pygame.font.Font('Assets/ItalicFont.ttf', 100)
        self.print_health = self.game_font.render("Health:", False, red)
        self.print_wave = self.game_font.render("WAVE:", False, red)
        self.main_menu_font = pygame.font.Font('Assets/DEATH_FONT.TTF', 200)
        self.agency_font = pygame.font.SysFont('agency fb', 50, True)

        self.print_start = self.main_menu_font.render("start", False, white)
        self.print_exit = self.main_menu_font.render("quit", False, white)
        self.print_settings = self.main_menu_font.render("settings", False, white)
        self.print_start_red = self.main_menu_font.render("start", False, red)
        self.print_exit_red = self.main_menu_font.render("quit", False, red)
        self.print_settings_red = self.main_menu_font.render("settings", False, red)

        self.start_ticks = pygame.time.get_ticks()

        self.floor = self.window_height - 200
        self.window = pygame.display.set_mode((self.window_width, self.window_height))
        self.bg = BackGround('Assets/background.jpg', [0, 0])
        self.main_menu_bg = BackGround('Assets/main_menu_bg.jpg', [0, 0])
        self.player_object = player_class('Assets/player_sprite.png', [100, self.floor - 195], self.floor)
        self.buy_menu_bg = BackGround('Assets/buy_menu.png', [0, 0])
        self.coin_img = pygame.image.load('Assets/gold_coin.png')
        self.medkit_img = pygame.image.load('Assets/medkit_keybind.png')

        self.gun_sound = pygame.mixer.Sound('Assets/9MM-3.wav')
        pygame.mixer.music.load("Assets/Damien_Type_Beat_Preview.wav")
        pygame.mixer.music.set_volume(.5)
        pygame.mixer.music.play(-1)
        # self.button_sound = pygame.mixer_music.load('button_sound.mp3')
        pygame.mixer.Sound.set_volume(self.gun_sound, .03)
        self.clock = pygame.time.Clock()

    def shooting_update(self):
        if self.shooting:
            if pygame.time.get_ticks() - self.last_shot > self.shot_delay:
                self.gun_sound.play()
                if self.player_left:
                    self.bullet = gun_class(self.player_left, self.player_right,
                                            (self.player_object.current_location[0],
                                             self.player_object.current_location[1] + 25), self.shot_direction)
                elif self.player_right:
                    self.bullet = gun_class(self.player_left, self.player_right,
                                            (self.player_object.current_location[0] + 145,
                                             self.player_object.current_location[1] + 25), self.shot_direction)
                self.bullet_list.add(self.bullet)
                self.last_shot = pygame.time.get_ticks()
            self.next_shot = pygame.time.get_ticks() + 100

    def update_fps(self):
        fps = str(int(self.clock.get_fps()))
        fps_text = self.game_font.render(fps, 1, pygame.Color("red"))
        return fps_text

    def restart_game(self):
        self.game_round = 0
        self.round_range = (0, self.game_round)
        self.player_object = None
        for self.zombie_object in self.zombie_list:
            pygame.sprite.Sprite.kill(self.zombie_object)
        self.player_object = player_class('Assets/player_sprite.png', [100, self.floor - 190], self.floor)
        self.run_game()

    def round_update(self):
        if not self.zombie_list:
            if self.game_round > 0 and self.time_remaining > 0:
                self.between_rounds = True
            else:
                self.between_rounds = False
                self.time_remaining = 1
            self.round_range = range(0, self.game_round + 1)
            if self.between_rounds is False:
                self.game_round += 1
                self.spawn_enemies()

    def spawn_enemies(self):
        zombie_count = self.game_round
        if self.game_round % 10 == 0:
            horde_game_round = self.game_round
            self.game_round = horde_game_round * 2
            self.round_range = range(0, self.game_round)
        for i in self.round_range:
            self.zombie_object = Zombie('Assets/zombie_sprite1_right.png', [random.randrange(self.window_width - 500,
                                                                                      self.window_width),
                                                                     self.floor - 188], self.floor)
            self.zombie_list.add(self.zombie_object)
            self.zombie_object.zombie_health += ((zombie_count - 1) * 5)
            if self.game_round % 5 == 0:
                self.zombie_object.zombie_damage += ((self.game_round - (self.game_round - 1)) * 2)
        if self.game_round % 10 == 0:
            self.game_round = horde_game_round

    def main_menu_update(self):
        self.window.fill(white)
        self.window.blit(self.main_menu_bg.image, self.main_menu_bg.rect)
        if 1100 < self.mouse_position[0] < 1620 and 200 < self.mouse_position[1] < 375:
            self.window.blit(self.print_start_red, (1100, 200))
        else:
            self.window.blit(self.print_start, (1100, 200))
        if 980 < self.mouse_position[0] < 1720 and 410 < self.mouse_position[1] < 580:
            self.window.blit(self.print_settings_red, (980, 400))
        else:
            self.window.blit(self.print_settings, (980, 400))
        if 1150 < self.mouse_position[0] < 1530 and 600 < self.mouse_position[1] < 800:
            self.window.blit(self.print_exit_red, (1150, 600))
        else:
            self.window.blit(self.print_exit, (1150, 600))
        pygame.display.update()

    def run_main_menu(self):
        pygame.mouse.set_visible(True)
        while self.main_menu_running:
            self.mouse_position = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == QUIT:
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if 1100 < self.mouse_position[0] < 1620 and 200 < self.mouse_position[1] < 375:
                        self.main_menu_running = False
                        self.run_game()
                    if 980 < self.mouse_position[0] < 1720 and 410 < self.mouse_position[1] < 580:
                        pass
                    if 1150 < self.mouse_position[0] < 1530 and 600 < self.mouse_position[1] < 800:
                        sys.exit()
            self.main_menu_update()

    def run_death_screen(self):
        pass

    def run_buy_menu(self, time):
        self.seconds = int((pygame.time.get_ticks() - self.start_ticks) / 1000)
        self.menu_countdown = self.seconds + time
        self.empty_rect = pygame.image.load('Assets/black_rect.png')
        while self.buy_menu_running:
            self.mouse_position = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_f or event.key == pygame.K_b:
                        return self.menu_countdown - self.seconds
            if self.seconds >= self.menu_countdown:
                return self.menu_countdown - self.seconds
            self.buy_menu_update()

    def buy_menu_update(self):
        self.window.fill(white)
        self.window.blit(self.buy_menu_bg.image, self.buy_menu_bg.rect)
        # print(str(self.mouse_position))

        if 265 < self.mouse_position[0] < 665 and 70 < self.mouse_position[1] < 500:
            self.window.blit(self.empty_rect, (265, 70))
        elif 265 < self.mouse_position[0] < 665 and 500 < self.mouse_position[1] < 930:
            self.window.blit(self.empty_rect, (265, 500))

        self.seconds = int((pygame.time.get_ticks() - self.start_ticks) / 1000)
        time_remaining_str = self.agency_font.render("Time Remaining:", True, white)
        count_down_str = self.agency_font.render(str(int(self.menu_countdown - self.seconds)), True, red)
        self.window.blit(time_remaining_str, (20, 970))
        self.window.blit(count_down_str, (300, 970))

        coin_str = self.agency_font.render(str(self.player_object.player_coins), True, white)
        self.window.blit(coin_str, (1625, 970))
        pygame.display.update()

    def run_game(self):
        # pygame.mouse.set_visible(False)
        while self.game_running:
            if self.between_rounds is True and self.time_created is False:
                self.time_created = True
                self.seconds = int((pygame.time.get_ticks() - self.start_ticks) / 1000)
                self.menu_countdown = self.seconds + 30
            self.mouse_position = pygame.mouse.get_pos()
            # self.round_update()
            for event in pygame.event.get():
                if event.type == QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        self.player_object.move_left()
                        self.player_left = True
                        self.player_right = False
                    if event.key == pygame.K_d:
                        self.player_object.move_right()
                        self.player_left = False
                        self.player_right = True
                    if event.key == pygame.K_w or event.key == pygame.K_SPACE:
                        self.player_object.player_jump()
                    if event.key == pygame.K_b and self.between_rounds is True:
                        self.time_remaining = self.run_buy_menu(self.time_remaining)
                    if event.key == pygame.K_f and self.between_rounds is True:
                        self.between_rounds = False
                        self.time_created = False
                        self.time_remaining = 0
                    if event.key == pygame.K_q and self.between_rounds is True:
                        self.wall_object = wall(self.mouse_position, self.floor)
                        self.wall_list.add(self.wall_object)
                        self.placing_wall = True
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.placing_wall is True:
                    for self.wall_object in self.wall_list:
                        if self.wall_object.wall_permanent is False:
                            self.wall_object.wall_permanent = True
                            self.wall_object.wall_permanent_location = self.mouse_position[0]
                            self.wall_object.wall_permanent = True
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.between_rounds is False:
                    self.shooting = True
                    self.shot_direction = self.mouse_position
                if event.type == pygame.MOUSEBUTTONUP:
                    self.shooting = False
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_a and self.player_object.player_change_x < 0:
                        self.player_object.player_stop_x()
                    if event.key == pygame.K_d and self.player_object.player_change_x > 0:
                        self.player_object.player_stop_x()
                    if event.key == pygame.K_w and self.player_object.player_change_y < 0:
                        self.player_object.player_stop_y()
            for self.bullet in self.bullet_list:
                self.bullet.bullet_update()
            for self.zombie_object in self.zombie_list:
                self.zombie_object.update(self.player_object, self.wall_list, self.player_object.current_location[0])
                if self.zombie_object.zombie_hit is True:
                    self.player_object.player_health -= self.zombie_object.zombie_damage
                    self.zombie_object.zombie_hit = False
                if self.zombie_object.zombie_hit_wall is True:
                    pass
            for self.wall_object in self.wall_list:
                self.wall_object.update()

            self.round_update()
            self.redraw_window()
            self.clock.tick(60)
            self.player_object.player_update()
            if self.player_object.player_health <= 0:
                self.restart_game()

    def redraw_window(self):
        self.window.fill([255, 255, 255])
        self.window.blit(self.bg.image, self.bg.rect)

        self.window.blit(self.print_health, (50, self.floor + 30))

        health_str = self.game_font.render(str(self.player_object.player_health), True, white)
        self.window.blit(health_str, (600, self.floor + 30))
        self.window.blit(self.print_wave, (1320, self.floor + 30))
        round_str = self.game_font.render(str(self.game_round), True, white)
        self.window.blit(round_str, (1760, self.floor + 30))
        self.window.blit(self.coin_img, (20, 20))
        coin_str = self.agency_font.render(str(self.player_object.player_coins), True, white)
        self.window.blit(coin_str, (120, 25))
        self.window.blit(self.medkit_img, (1500, 25))

        self.shooting_update()

        if self.player_left:
            self.window.blit(self.player_object.player_img_left, self.player_object.current_location)
        elif self.player_right:
            self.window.blit(pygame.transform.flip(self.player_object.player_img_left, True, False),
                             self.player_object.current_location)

        # self.window.blit(self.update_fps(), (10, 0))

        for self.wall_object in self.wall_list:
            # pygame.draw.rect(self.window, white, self.wall_object.rect)
            # print("Wall: " + str(self.wall_object.rect))
            if self.wall_object.wall_permanent is False:
                self.window.blit(self.wall_object.wall_image_green, (self.mouse_position[0], self.floor - 138))
            else:
                self.window.blit(self.wall_object.wall_image,
                                 (self.wall_object.wall_permanent_location, self.floor - 138))

        for self.bullet in self.bullet_list:
            self.window.blit(self.bullet.bullet_img, self.bullet.bullet_current_location)
            if self.bullet.bullet_current_location[0] > self.window_width or self.bullet.bullet_current_location[0] < 0:
                pygame.sprite.Sprite.kill(self.bullet)
            for self.zombie_object in self.zombie_list:
                if pygame.sprite.collide_rect(self.bullet, self.zombie_object):
                    self.zombie_object.zombie_health -= 10
                    pygame.sprite.Sprite.kill(self.bullet)

        for self.zombie_object in self.zombie_list:
            if self.zombie_object.zombie_left is True:
                self.window.blit(self.zombie_object.zombie_img_right, self.zombie_object.z_current_location)
            elif self.zombie_object.zombie_right is True:
                self.window.blit(pygame.transform.flip(self.zombie_object.zombie_img_right, True, False),
                                 self.zombie_object.z_current_location)
            if self.zombie_object.zombie_health <= 0:
                pygame.sprite.Sprite.kill(self.zombie_object)
                self.player_object.player_coins += self.zombie_object.zombie_drops

        if self.time_created is True and self.between_rounds is True:
            self.seconds = int((pygame.time.get_ticks() - self.start_ticks) / 1000)
            if self.seconds > self.menu_countdown:
                self.between_rounds = False
                self.time_created = False
            else:
                self.time_remaining = self.menu_countdown - self.seconds
                time_remaining_str = self.agency_font.render("Time Remaining:", True, white)
                press_f_str = self.agency_font.render("Press F to continue", True, white)
                press_b_str = self.agency_font.render("Press B to buy", True, white)
                count_down_str = self.agency_font.render(str(int(self.menu_countdown - self.seconds)), True, red)
                self.window.blit(time_remaining_str, (self.window_width * (2 / 5), self.window_height * .2))
                self.window.blit(count_down_str, (self.window_width * (.55), self.window_height * .2))
                self.window.blit(press_f_str, (self.window_width * .4, self.window_height * .25))
                self.window.blit(press_b_str, (self.window_width * .4, self.window_height * .3))
        else:
            self.time_remaining = 1

        pygame.display.update()


Game().run_main_menu()
