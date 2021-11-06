import pygame
import random
from classes.button import Button
from classes.character import Character, damage_text_group, DamageText, Color, HealthBar
from pygame import mixer
import time

# Main Characters
binder = Character(120, 410, "Binder", 30, 25, {"potion": 3, 'fire': 2}, frame_list=(8, 12, 7, 12))

# Enemies
ninja = Character(680, 490, "Ninja", 30, 5, {"potion": 3})
binja = Character(680, 410, "Binja", 30, 5, {"potion": 3})
demon = Character(450, 420, "Demon", 30, 5, {"potion": 3}, scale_size=1, frame_list=(8, 12, 7, 18))
enemies = [ninja, binja, demon]

# Initialize Pygame
pygame.init()
clock = pygame.time.Clock()
fps = 60

# background sound
mixer.music.load('./sound/background_soundtrack.mp3')
mixer.music.play(-1)


# Game Window
right_panel = 400
screen_width, screen_height = 800 + right_panel, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Vicious World")
icon = pygame.image.load("./game_images/demon.png").convert_alpha()
restart_image = pygame.image.load("./game_images/restart.png").convert_alpha()
restart_image = pygame.transform.smoothscale(restart_image, (100, 100))
victory_image = pygame.image.load("./game_images/victory.png").convert_alpha()
victory_image = pygame.transform.smoothscale(victory_image, (300, 300))
defeat_image = pygame.image.load("./game_images/defeat.png").convert_alpha()
defeat_image = pygame.transform.smoothscale(defeat_image, (300, 300))
# sword image
sword = pygame.image.load("./game_images/sword.png").convert_alpha()
sword = pygame.transform.smoothscale(sword, (30, 30))
# button images
potion_img = pygame.image.load("./game_images/potion.png").convert_alpha()
potion_img = pygame.transform.smoothscale(potion_img, (30, 30))
fire_img = pygame.image.load("./game_images/fire.png").convert_alpha()
fire_img = pygame.transform.smoothscale(fire_img, (30, 30))
# paper img
paper_img = pygame.image.load("./game_images/paper.png").convert_alpha()
paper_img = pygame.transform.smoothscale(paper_img, (210, 200))
# health icon
health_img = pygame.image.load("./game_images/health.png").convert_alpha()
health_img = pygame.transform.smoothscale(health_img, (25, 25))
# game variables
current_fighter = 1
total_fighter = 4
action_cool_down = 0
action_wait_time = 90
attack = False
potion = False
fire = False
potion_effect = 15
fire_effect = 15
clicked = False
game_over = 0
victory_flag = True
narration = ""


# Health bars initialization
binder_health_bar = HealthBar(screen_width - right_panel + 30, 55, binder.hp, binder.max_hp)
ninja_health_bar = HealthBar(screen_width - right_panel + 30, 150, ninja.hp, ninja.max_hp)
binja_health_bar = HealthBar(screen_width - right_panel + 30, 250, binja.hp, binja.max_hp)
demon_health_bar = HealthBar(screen_width - right_panel + 30, 350, demon.hp, demon.max_hp)

# create buttons
potion_button = Button(screen, screen_width - right_panel + 20, 450, potion_img, 64, 64)
fire_button = Button(screen, screen_width - right_panel + 100, 450, fire_img, 64, 64)
restart_button = Button(screen, screen_width - right_panel + 200, 450, restart_image, 64, 64)
# define font for the window
font = pygame.font.SysFont("comicsansms", 23)

# load images
# background images
bg = pygame.image.load("./game_images/bg.png").convert_alpha()
panel_bg = pygame.image.load("./game_images/wood.jpg").convert_alpha()
# set window Icon
pygame.display.set_icon(icon)


def draw_panel():
    screen.blit(panel_bg, (screen_width - right_panel, 0))
    # show player stats
    draw_text(f'{binder.name} HP:{binder.hp}/{binder.max_hp}', font, Color.WHITE, screen_width - right_panel + 20, 15)
    for count, enemy in enumerate(enemies, start=1):
        draw_text(f'{enemy.name} HP:{enemy.hp}/{enemy.max_hp}', font, Color.BLACK,
                  screen_width - right_panel + 20, 100 * count)


def draw_bg():
    screen.blit(bg, (0, 0))


def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


def draw_img(img, x, y):
    screen.blit(img, (x, y))


run = True


while run:

    clock.tick(fps)
    # draw background
    draw_bg()
    # draw panel
    draw_panel()
    binder_health_bar.draw(screen, binder.hp)
    ninja_health_bar.draw(screen, ninja.hp)
    binja_health_bar.draw(screen, binja.hp)
    demon_health_bar.draw(screen, demon.hp)
    draw_img(health_img, screen_width - right_panel + 20, 52)
    draw_img(paper_img, screen_width - right_panel + 190, 52)

    # draw character
    binder.update()
    binder.draw(screen)
    for enemy in enemies:
        enemy.update()
        enemy.draw(screen)

    # draw damage text
    damage_text_group.update()
    damage_text_group.draw(screen)

    # Control Player actions
    # rest action variables
    attack = False
    potion = False
    fire = False
    target = None
    pygame.mouse.set_visible(True)
    pos = pygame.mouse.get_pos()
    for count, enemy in enumerate(enemies):
        if enemy.rect.collidepoint(pos):
            pygame.mouse.set_visible(False)
            # display sword icon
            screen.blit(sword, pos)
            if clicked and enemy.alive:
                attack = True
                target = enemies[count]
    if fire_button.draw():
        fire = True
    if potion_button.draw():
        potion = True

    # show remaining items
    draw_text(f"{binder.items['potion']}", font, Color.WHITE, screen_width - right_panel + 10, 450)
    draw_text(f"{binder.items['fire']}", font, Color.WHITE, screen_width - right_panel + 100, 450)
    draw_text(f'{narration}', pygame.font.SysFont("comicsansms", 12),
              Color.BLACK, screen_width - right_panel + 225, 150)

    if game_over == 0:
        # player actions
        if binder.alive:
            if current_fighter == 1:
                action_cool_down += 1
                if action_cool_down >= action_wait_time:
                    # waiting for player action
                    # attack
                    if attack and target is not None:
                        narration = f"Binder attacks {target.name}"
                        binder.attack(target)
                        atk_sound = mixer.Sound(f"./sound/binder/atk/atk_{random.randint(1,3)}.wav")
                        atk_sound.play()
                        if not target.alive:
                            enemy_death_dialog = mixer.Sound(f"./sound/binder/dialog/enemy_death.wav")
                            enemy_death_dialog.play()
                            if target.name == "Demon":
                                demon_death = mixer.Sound(f"./sound/demon/death/death.mp3")
                                demon_death.play()
                        current_fighter += 1
                        action_cool_down = 0
                    # Fire
                    if fire:
                        if binder.items['fire'] > 0:
                            # the animation is longer than the others
                            narration = f"Binder uses fire"
                            action_wait_time = 210
                            for enemy in enemies:
                                if enemy.alive:
                                    binder.fire_magic(enemy, fire_effect)
                            binder.items['fire'] -= 1
                            current_fighter += 1
                            action_cool_down = 0
                            fire_atk_dialog = mixer.Sound(f"./sound/binder/dialog/fire_atk.wav")
                            fire_atk_dialog.play()
                    # Potion
                    if potion:
                        if binder.items['potion'] > 0:
                            # to make sure the hp won't exceed max hp

                            if binder.max_hp - binder.hp > potion_effect:
                                heal_amount = potion_effect
                            else:
                                heal_amount = binder.max_hp - binder.hp
                            binder.hp += heal_amount
                            narration = f"Binder heals for {heal_amount}"
                            binder.items['potion'] -= 1
                            damage_text = DamageText(binder.rect.centerx,
                                                     binder.rect.centery, str(heal_amount), Color.GREEN)
                            damage_text_group.add(damage_text)
                            current_fighter += 1
                            action_cool_down = 0
                            heal_sound = mixer.Sound(f"./sound/binder/heal/heal.wav")
                            heal_sound.play()

        else:
            death_sound = mixer.Sound(f"./sound/binder/death/death.wav")
            death_sound.play()
            game_over = -1

        # enemy actions
        for count, enemy in enumerate(enemies):
            if current_fighter == 2 + count:
                if enemy.alive:
                    action_cool_down += 1
                    if action_cool_down >= action_wait_time:
                        # check heal for enemy
                        if (enemy.hp / enemy.max_hp) < 0.5 and enemy.items['potion'] > 0:
                            # to make sure the hp won't exceed max hp
                            if enemy.max_hp - enemy.hp > potion_effect:
                                heal_amount = potion_effect
                            else:
                                heal_amount = enemy.max_hp - enemy.hp

                            enemy.hp += heal_amount
                            narration = f"{enemy.name} heals for {heal_amount}"
                            enemy.items['potion'] -= 1
                            damage_text = DamageText(enemy.rect.centerx,
                                                     enemy.rect.centery, str(heal_amount), Color.GREEN)
                            damage_text_group.add(damage_text)
                            current_fighter += 1
                            action_cool_down = 0
                            # resetting action_wait_time to original
                            action_wait_time = 90

                        # attack
                        else:
                            # resetting action_wait_time to original
                            if enemy.name == 'Demon':
                                demon_sound = mixer.Sound(f"./sound/demon/atk/atk.mp3")
                                demon_sound.play()
                            narration = f"{enemy.name} attacks for Binder"
                            action_wait_time = 90
                            enemy.attack(binder)
                            current_fighter += 1
                            action_cool_down = 0
                            hurt_sound = mixer.Sound(f"./sound/binder/hurt/hurt_{random.randint(1,6)}.wav")
                            hurt_sound.play()
                else:
                    current_fighter += 1
                    # resetting action_wait_time to original
                    action_wait_time = 90
        # when all fighters have had a turn , reset
        if current_fighter > total_fighter:
            current_fighter = 1

    # check all enemies are dead
    alive_enemy = 0
    for enemy in enemies:
        if enemy.alive:
            alive_enemy += 1
    if alive_enemy == 0:

        if victory_flag:

            time.sleep(.1)
            victory_dialog = mixer.Sound(f"./sound/binder/dialog/victory.wav")
            victory_dialog.play()
            victory_flag = False
        game_over = 1

    # check if game is over
    if game_over != 0:
        if game_over == 1:
            narration = f"You defeated the Demon"
            screen.blit(victory_image, (250, 150))

        elif game_over == -1:
            narration = f"        R.I.P Binder"
            screen.blit(defeat_image, (250, 50))
        if restart_button.draw():
            binder.restart()
            for enemy in enemies:
                enemy.restart()
                current_fighter = 1
                action_cool_down = 0
                game_over = 0
                victory_flag = True
                narration = ""
            current_bg = random.choice(['bg', 'bg1', 'bg2', 'bg3'])
            bg = pygame.image.load(f"./game_images/{current_bg}.png").convert_alpha()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            clicked = True

        else:
            clicked = False

    pygame.display.update()
pygame.quit()
