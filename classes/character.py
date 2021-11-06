import pygame
import random
damage_text_group = pygame.sprite.Group()
pygame.font.init()
font = pygame.font.SysFont("Times New Roman", 26)


class Color:
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    DARK_GREEN = (0, 100, 0)
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)


class DamageText(pygame.sprite.Sprite):
    def __init__(self, x, y, damage, color):
        pygame.sprite.Sprite.__init__(self)
        self.image = font.render(damage, True, color)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.counter = 0

    def update(self):
        self.rect.y -= 1
        # delete after a few seconds
        self.counter += 1
        if self.counter > 100:
            self.kill()


class HealthBar:
    def __init__(self, x, y, hp, max_hp, color=Color.DARK_GREEN):
        self.x = x
        self.y = y
        self.hp = hp
        self.max_hp = max_hp
        self.color = color

    def draw(self, screen, hp):
        # update with new health
        self.hp = hp
        # calculate health ratio
        ratio = self.hp / self.max_hp
        pygame.draw.rect(screen, Color.RED, (self.x, self.y, 150, 20), border_radius=25)
        pygame.draw.rect(screen, self.color, (self.x, self.y, 150 * ratio, 20), border_radius=25)


class Character:
    def __init__(self, x, y, name, max_hp, atk, items, flip=False, scale_size=2, frame_list=(8, 8, 7, 10)):
        self.x = x
        self.y = y
        self.name = name
        self.hp = max_hp
        self.max_hp = max_hp
        self.atk = atk
        self.start_items = items.copy()
        self.items = items
        self.alive = True
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        self.animation_list = []
        # --> 0:idle 1:atk 2:damaged 3:death 4:fire_attack
        self.action = 0

        # load idle images
        temp_list = []
        for i in range(1, frame_list[0]):
            img = pygame.image.load(f"./player_asset/{self.name}/idle/idle_{i}.png")
            if flip:
                img = pygame.transform.smoothscale(pygame.transform.flip(img, True, False),
                                                   (img.get_width() * scale_size, img.get_height() * scale_size))
            else:
                img = pygame.transform.smoothscale(img, (img.get_width() * scale_size, img.get_height() * scale_size))
            temp_list.append(img)
        self.animation_list.append(temp_list)
        # load atk images
        temp_list = []
        for i in range(1, frame_list[1]):
            img = pygame.image.load(f"./player_asset/{self.name}/atk/atk_{i}.png")
            if flip:
                img = pygame.transform.smoothscale(pygame.transform.flip(img, True, False),
                                                   (img.get_width() * scale_size, img.get_height() * scale_size))
            else:
                img = pygame.transform.smoothscale(img, (img.get_width() * scale_size, img.get_height() * scale_size))
            temp_list.append(img)
        self.animation_list.append(temp_list)
        # load hurt images
        temp_list = []

        for i in range(1, frame_list[2]):
            img = pygame.image.load(f"./player_asset/{self.name}/hurt/hurt_{i}.png")
            if flip:
                img = pygame.transform.smoothscale(pygame.transform.flip(img, True, False),
                                                   (img.get_width() * scale_size, img.get_height() * scale_size))
            else:
                img = pygame.transform.smoothscale(img, (img.get_width() * scale_size, img.get_height() * scale_size))
            temp_list.append(img)
        self.animation_list.append(temp_list)
        # load death images
        temp_list = []
        for i in range(1, frame_list[3]):
            img = pygame.image.load(f"./player_asset/{self.name}/death/death_{i}.png")
            if flip:
                img = pygame.transform.smoothscale(pygame.transform.flip(img, True, False),
                                                   (img.get_width() * scale_size, img.get_height() * scale_size))
            else:
                img = pygame.transform.smoothscale(img, (img.get_width() * scale_size, img.get_height() * scale_size))
            temp_list.append(img)
        self.animation_list.append(temp_list)

        # load fire magic images
        if len(self.items) > 1:
            temp_list = []
            for i in range(1, 29):
                img = pygame.image.load(f"./player_asset/{self.name}/fire_atk/f_atk_{i}.png")
                if flip:
                    img = pygame.transform.smoothscale(pygame.transform.flip(img, True, False),
                                                       (img.get_width() * scale_size, img.get_height() * scale_size))
                else:
                    img = pygame.transform.smoothscale(img, (img.get_width() * scale_size,
                                                             img.get_height() * scale_size))
                temp_list.append(img)
        self.animation_list.append(temp_list)
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self):
        animation_cool_down = 100
        # update image
        self.image = self.animation_list[self.action][self.frame_index]
        # check last update
        if pygame.time.get_ticks() - self.update_time > animation_cool_down:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        if self.frame_index >= len(self.animation_list[self.action]):
            if self.action == 3:
                self.frame_index = len(self.animation_list[self.action]) - 1
            else:
                self.idle()

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def dead(self):
        # set death animation
        self.action = 3
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

    def hurt(self):
        # set hurt animation
        self.action = 2
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

    def attack(self, target):
        # deal damage
        rand = random.randint(-5, 5)
        damage = self.atk + rand
        target.hp -= damage
        target.hurt()
        # check if target has died
        if target.hp < 1:
            target.hp = 0
            target.alive = False
            target.dead()
        damage_text = DamageText(target.rect.centerx, target.rect.centery - 90, str(damage), Color.RED)
        damage_text_group.add(damage_text)
        # set atk animation
        self.action = 1
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

    def idle(self):
        # set idle animation
        self.action = 0
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

    def restart(self):
        self.alive = True
        self.items = self.start_items
        self.start_items = self.items.copy()
        self.hp = self.max_hp
        self.frame_index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()

    def fire_magic(self, target, damage):
        target.hp -= damage
        target.hurt()
        # check if target has died
        if target.hp < 1:
            target.hp = 0
            target.alive = False
            target.dead()
        damage_text = DamageText(target.rect.centerx, target.rect.centery - 90, str(damage), Color.RED)
        damage_text_group.add(damage_text)
        # set fire attack animation
        self.action = 4
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
