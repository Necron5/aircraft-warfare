# Import related modules
import pygame
import sys
from random import *
from pygame.locals import *
from pygame.mixer import pause

import myplane
import enemy
import bullet
import supply

from configurations import *

# Start of the project
pygame.init()
pygame.mixer.init()

# Initializing screen
bg_size = (width, height) = GAME_BG_SIZE
screen = pygame.display.set_mode(bg_size)
pygame.display.set_caption(GAME_CAPTION)
background = pygame.image.load(GAME_BG_SRC)

# Load game music
pygame.mixer.music.load(GAME_MUSIC_SRC)
pygame.mixer.music.set_volume(VOLUME_SMALL)
bullet_sound = pygame.mixer.Sound(BULLET_SOUND_SRC)
bullet_sound.set_volume(VOLUME_SMALL)
bomb_sound = pygame.mixer.Sound(BOMB_SOUND_SRC)
bomb_sound.set_volume(VOLUME_SMALL)
supply_sound = pygame.mixer.Sound(SUPPLY_SOUND_SRC)
supply_sound.set_volume(VOLUME_SMALL)
get_bomb_sound = pygame.mixer.Sound(GET_BOMB_SOUND_SRC)
get_bomb_sound.set_volume(VOLUME_SMALL)
get_bullet_sound = pygame.mixer.Sound(GET_BULLET_SOUND_SRC)
get_bullet_sound.set_volume(VOLUME_SMALL)
upgrade_sound = pygame.mixer.Sound(UPGRADE_SOUND_SRC)
upgrade_sound.set_volume(VOLUME_SMALL)
enemy3_fly_sound = pygame.mixer.Sound(E3_FLY_SOUND_SRC)
enemy3_fly_sound.set_volume(VOLUME_SMALL)
enemy1_down_sound = pygame.mixer.Sound(E1_DOWN_SOUND_SRC)
enemy1_down_sound.set_volume(VOLUME_SMALL)
enemy2_down_sound = pygame.mixer.Sound(E2_DOWN_SOUND_SRC)
enemy2_down_sound.set_volume(VOLUME_SMALL)
enemy3_down_sound = pygame.mixer.Sound(E3_DOWN_SOUND_SRC)
enemy3_down_sound.set_volume(VOLUME_MEDIUM)
player_down_sound = pygame.mixer.Sound(PLAYER_DOWN_SOUND_SRC)
player_down_sound.set_volume(VOLUME_SMALL)


# Define method to add small enemies to groups
def add_small_enemies(group1, group2, num):
    for i in range(num):
        se = enemy.SmallEnemy(bg_size)
        group1.add(se)
        group2.add(se)

# Define method to add medium enemies to groups
def add_medium_enemies(group1, group2, num):
    for i in range(num):
        me = enemy.MediumEnemy(bg_size)
        group1.add(me)
        group2.add(me)

# Define method to add large enemies to groups
def add_large_enemies(group1, group2, num):
    for i in range(num):
        le = enemy.LargeEnemy(bg_size)
        group1.add(le)
        group2.add(le)

# Define method to increase enemy's speed
def speed_up(enemies, increment):
    for enemy in enemies:
        enemy.speed += increment

# Game's main function
def main():
    # Keep playing the background music
    pygame.mixer.music.play(-1)

    # Generate player's plane object
    player = myplane.MyPlane(bg_size)

    # Generate enemy groups and add enemies
    enemies = pygame.sprite.Group()
    small_enemies = pygame.sprite.Group()
    add_small_enemies(small_enemies, enemies, INITIAL_SMALL_ENEMIES_NUM)

    medium_enemies = pygame.sprite.Group()
    add_medium_enemies(medium_enemies, enemies, INITIAL_MEDIUM_ENEMIES_NUM)

    large_enemies = pygame.sprite.Group()
    add_large_enemies(large_enemies, enemies, INITIAL_LARGE_ENEMIES_NUM)

    # Score system
    score = 0
    score_font = pygame.font.Font(GAME_FONT_SRC, MEDIUM_FONT_SIZE)
    level = 1

    # Life system
    life_num = INITIAL_LIFE_NUM
    life_image = pygame.image.load(LIFE_IMAGE_SRC).convert_alpha()
    life_rect = life_image.get_rect()

    # Bomb
    bomb_num = INITIAL_BOMB_NUM
    bomb_image = pygame.image.load(BOMB_IMAGE_SRC).convert_alpha()
    bomb_rect = bomb_image.get_rect()
    bomb_font = pygame.font.Font(GAME_FONT_SRC, LARGE_FONT_SIZE)

    # Bomb supply
    bomb_supply = supply.BombSupply(bg_size)
    
    # Bullet supply
    bullet_supply = supply.BulletSupply(bg_size)

    # Double bullet flag
    is_double_bullet = False

    # Supply timer event 
    SUPPLY_TIME = USEREVENT
    pygame.time.set_timer(SUPPLY_TIME, SUPPLY_TIME_DURATION)  # 15 seconds = 15 * 1000 milliseconds

    DOUBLE_BULLET_TIME = USEREVENT + 1

    INVINCIBLE_TIME = USEREVENT + 2

    # Pause
    paused = False
    pause_nor_image = pygame.image.load(PAUSE_NOR_IMAGE_SRC).convert_alpha()
    pause_pressed_image = pygame.image.load(PAUSE_PRESSED_IMAGE_SRC).convert_alpha()
    resume_nor_image = pygame.image.load(RESUME_NOR_IMAGE_SRC).convert_alpha()
    resume_pressed_image = pygame.image.load(RESUME_PRESSED_IMAGE_SRC).convert_alpha()
    paused_rect = pause_nor_image.get_rect()
    paused_rect.left, paused_rect.top = width - paused_rect.width - 10, 10
    paused_image = pause_nor_image

    # Gameover image
    gameover_font = pygame.font.Font(GAME_FONT_SRC, LARGE_FONT_SIZE)
    gameover_image = pygame.image.load(GAMEOVER_IMAGE_SRC).convert_alpha()
    gameover_rect = gameover_image.get_rect()
    restart_image = pygame.image.load(RESTART_IMAGE_SRC).convert_alpha()
    restart_rect = restart_image.get_rect()

    # Generate bullets
    bullet1_list = []
    bullet1_index = 0
    bullet1_num = 4
    for i in range(bullet1_num):
        bullet1_list.append(bullet.Bullet1(player.rect.midtop))

    bullet2_list = []
    bullet2_index = 0
    bullet2_num = 8
    for i in range(bullet2_num // 2):
        bullet2_list.append(bullet.Bullet2((player.rect.centerx - 33, player.rect.centery)))
        bullet2_list.append(bullet.Bullet2((player.rect.centerx + 30, player.rect.centery)))

    # Set game's clock
    clock = pygame.time.Clock()
    
    # Set player's image switch flag
    switch_image = False

    # Set score record flag
    recorded = False

    # Set an initial time counter
    delay = 60

    # Set planes' destroy index 
    player_destroy_index = 0
    se_destroy_index = 0
    me_destroy_index = 0
    le_destroy_index = 0

    running = True

    while running:
        # Detect operations
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == MOUSEMOTION:
                if paused_rect.collidepoint(event.pos):
                    if paused:
                        paused_image = resume_pressed_image
                    else:
                        paused_image = pause_pressed_image
                else:
                    if paused:
                        paused_image = resume_nor_image
                    else:
                        paused_image = pause_nor_image
            
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1 and paused_rect.collidepoint(event.pos):
                    paused = not paused
                    if paused:
                        pygame.time.set_timer(SUPPLY_TIME, 0)
                        pygame.mixer.music.pause()
                        pygame.mixer.pause()
                    else:
                        pygame.time.set_timer(SUPPLY_TIME, SUPPLY_TIME_DURATION)
                        pygame.mixer.music.unpause()
                        pygame.mixer.unpause()

            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    if bomb_num > 0:
                        bomb_num -= 1
                        bomb_sound.play()
                        for each in enemies:
                            if each.rect.bottom > 0:
                                each.active = False
            if event.type == SUPPLY_TIME:
                supply_sound.play()
                if choice([True, False]):
                    bomb_supply.reset()
                else:
                    bullet_supply.reset()
            if event.type == DOUBLE_BULLET_TIME:
                is_double_bullet = False
                pygame.time.set_timer(DOUBLE_BULLET_TIME, 0)
            if event.type == INVINCIBLE_TIME:
                player.invincible = False
                pygame.time.set_timer(INVINCIBLE_TIME, 0)

        # Draw the background image to the game window
        screen.blit(background, (0, 0))

        # Draw the pause image
        if life_num > 0:
            # display pause button
            screen.blit(paused_image, paused_rect)
            # display score
            score_text = score_font.render(f"Score: {score}", True, WHITE)
            screen.blit(score_text, SCORE_TEXT_POSITION)
        
        # level upgrade
        if level == 1 and score > L2_SCORE_THRESHOLD:
            level = 2
            upgrade_sound.play()
            add_small_enemies(small_enemies, enemies, L2_SMALL_ENEMIES_INCRE)
            add_medium_enemies(medium_enemies, enemies, L2_MEDIUM_ENEMIES_INCRE)
            add_large_enemies(large_enemies, enemies, L2_LARGE_ENEMIES_INCRE)
            speed_up(small_enemies, L2_SMALL_SPEED_INCRE)
        elif level == 2 and score > L3_SCORE_THRESHOLD:
            level = 3
            upgrade_sound.play()
            add_small_enemies(small_enemies, enemies, L3_SMALL_ENEMIES_INCRE)
            add_medium_enemies(medium_enemies, enemies, L3_MEDIUM_ENEMIES_INCRE)
            add_large_enemies(large_enemies, enemies, L3_LARGE_ENEMIES_INCRE)
            speed_up(small_enemies, L3_SMALL_SPEED_INCRE)
            speed_up(medium_enemies, L3_MEDIUM_SPEED_INCRE)
        elif level == 3 and score > L4_SCORE_THRESHOLD:
            level = 4
            upgrade_sound.play()
            add_small_enemies(small_enemies, enemies, L4_SMALL_ENEMIES_INCRE)
            add_medium_enemies(medium_enemies, enemies, L4_MEDIUM_ENEMIES_INCRE)
            add_large_enemies(large_enemies, enemies, L4_LARGE_ENEMIES_INCRE)
            speed_up(small_enemies, L4_SMALL_SPEED_INCRE)
            speed_up(medium_enemies, L4_MEDIUM_SPEED_INCRE)
        elif level == 4 and score > L5_SCORE_THRESHOLD:
            level = 5
            upgrade_sound.play()
            add_small_enemies(small_enemies, enemies, L5_SMALL_ENEMIES_INCRE)
            add_medium_enemies(medium_enemies, enemies, L5_MEDIUM_ENEMIES_INCRE)
            add_large_enemies(large_enemies, enemies, L5_LARGE_ENEMIES_INCRE)
            speed_up(small_enemies, L5_SMALL_SPEED_INCRE)
            speed_up(medium_enemies, L5_MEDIUM_SPEED_INCRE)
            speed_up(large_enemies, L5_LARGE_SPEED_INCRE)

        if life_num > 0 and (not paused):
            # Detect keyboard operations
            key_pressed = pygame.key.get_pressed()
            if key_pressed[K_UP] or key_pressed[K_w]:
                player.move_up()
            if key_pressed[K_DOWN] or key_pressed[K_s]:
                player.move_down()
            if key_pressed[K_LEFT] or key_pressed[K_a]:
                player.move_left()
            if key_pressed[K_RIGHT] or key_pressed[K_d]:
                player.move_right()

            # display lives image
            for i in range(life_num):
                screen.blit(life_image, \
                            (width - 10 - (i + 1) * life_rect.width, \
                            height - 10 - life_rect.height))

            # display bomb
            bomb_text = bomb_font.render("× %d" % bomb_num, True, WHITE)
            bomb_text_rect = bomb_text.get_rect()
            screen.blit(bomb_image, (10, height - 10 - bomb_rect.height))
            screen.blit(bomb_text, (20 + bomb_rect.width, height - 5 - bomb_text_rect.height))

            # release bomb supply package
            if bomb_supply.active:
                bomb_supply.move()
                screen.blit(bomb_supply.image, bomb_supply.rect)
                if pygame.sprite.collide_mask(bomb_supply, player):
                    if bomb_num < INITIAL_BOMB_NUM:
                        bomb_num += 1
                        get_bomb_sound.play()
                    bomb_supply.active = False

            #  release bullet supply package
            if bullet_supply.active:
                bullet_supply.move()
                screen.blit(bullet_supply.image, bullet_supply.rect)
                if pygame.sprite.collide_mask(bullet_supply, player):
                    get_bullet_sound.play()
                    pygame.time.set_timer(DOUBLE_BULLET_TIME, DOUBLE_BULLET_TIME_DURATION)
                    is_double_bullet = True
                    bullet_supply.active = False

            # every 10 times of refresh, fire a bullet
            if not (delay % 10):
                bullet_sound.play()
                if is_double_bullet:
                    bullets = bullet2_list
                    bullets[bullet2_index].reset((player.rect.centerx - 33, player.rect.centery))
                    bullets[bullet2_index + 1].reset((player.rect.centerx + 30, player.rect.centery))
                    bullet2_index = (bullet2_index + 2) % bullet2_num
                else:
                    bullets = bullet1_list
                    bullets[bullet1_index].reset(player.rect.midtop)
                    bullet1_index = (bullet1_index + 1) % bullet1_num
                    
            # Check hitting an enemy
            for b in bullets:
                if b.active:
                    b.move()
                    screen.blit(b.image, b.rect)
                    enemies_hit = pygame.sprite.spritecollide(b, enemies, False, pygame.sprite.collide_mask)
                    if enemies_hit:
                        b.active = False
                        for e in enemies_hit:
                            if e in large_enemies or e in medium_enemies:
                                e.energy -= 1
                                e.hit = True
                                if e.energy == 0:
                                    e.active = False
                            else:
                                e.active = False

            # Small enemies behavior
            for each in small_enemies:
                if each.active:
                    each.move()
                    screen.blit(each.image, each.rect)
                else:
                    if not delay % 3:
                        screen.blit(each.destroy_images[se_destroy_index], each.rect)
                        se_destroy_index = (se_destroy_index + 1) % 4
                        if se_destroy_index == 0:
                            enemy1_down_sound.play()
                            score += SMALL_ENEMY_SCORE
                            each.reset()

            # Medium enemies behavior
            for each in medium_enemies:
                if each.active:
                    each.move()
                    
                    if each.hit:
                        screen.blit(each.image_hit, each.rect)
                        each.hit = False
                    else:
                        screen.blit(each.image, each.rect)
                    # Energy bar
                    pygame.draw.line(screen, BLACK, \
                                    (each.rect.left, each.rect.top - 5), \
                                    (each.rect.right, each.rect.top - 5), \
                                    2)
                    
                    energy_remain = each.energy / enemy.MediumEnemy.energy
                    if energy_remain > 0.2:
                        energy_color = GREEN
                    else:
                        energy_color = RED
                    # Re-draw the energy bar
                    pygame.draw.line(screen, energy_color, \
                                    (each.rect.left, each.rect.top - 5), \
                                    (each.rect.left + each.rect.width * energy_remain, each.rect.top - 5), \
                                    2)     
                
                else:
                    if not delay % 3:
                        screen.blit(each.destroy_images[me_destroy_index], each.rect)
                        me_destroy_index = (me_destroy_index + 1) % 4
                        if me_destroy_index == 0:
                            enemy2_down_sound.play()
                            score += MEDIUM_ENEMY_SCORE
                            each.reset()

            # Large enemies behavior 
            for each in large_enemies:
                if each.active:
                    each.move()
                    if each.hit:
                        screen.blit(each.image_hit, each.rect)
                        each.hit = False
                    else:
                        if switch_image:
                            screen.blit(each.image1, each.rect)
                        else:
                            screen.blit(each.image2, each.rect)

                    pygame.draw.line(screen, BLACK, \
                                    (each.rect.left, each.rect.top - 5), \
                                    (each.rect.right, each.rect.top - 5), 2)
                    energy_remain = each.energy / enemy.LargeEnemy.energy
                    if energy_remain > 0.2:
                        energy_color = GREEN
                    else:
                        energy_color = RED
                    pygame.draw.line(screen, energy_color, \
                                    (each.rect.left, each.rect.top - 5), \
                                    (each.rect.left + each.rect.width * energy_remain, each.rect.top - 5), \
                                    2)
                
                else:
                    if not delay % 3:
                        screen.blit(each.destroy_images[le_destroy_index], each.rect)
                        le_destroy_index = (le_destroy_index + 1) % 6
                        if le_destroy_index == 0:
                            enemy3_down_sound.play()
                            score += LARGE_ENEMY_SCORE
                            each.reset()

            # Play behavior
            if player.active:
                # switch player's image 
                if switch_image:
                    screen.blit(player.image1, player.rect)
                else:
                    screen.blit(player.image2, player.rect)
            else:
                # load destroy images
                if not delay % 3:
                    screen.blit(player.destroy_images[player_destroy_index], player.rect)
                    player_destroy_index = (player_destroy_index + 1) % 4
                    if player_destroy_index == 0:
                        player_down_sound.play()
                        life_num -= 1
                        player.reset()
                        pygame.time.set_timer(INVINCIBLE_TIME, INVINCIBLE_TIME_DURATION)

            # Detect collision (player vs. enemies)
            enemies_down = pygame.sprite.spritecollide(player, enemies, False, pygame.sprite.collide_mask)
            if enemies_down and not player.invincible:
                player.active = False
                for e in enemies_down:
                    e.active = False

        elif life_num == 0:
            pygame.mixer.music.stop()
            pygame.mixer.stop()

            pygame.time.set_timer(SUPPLY_TIME, 0)
            
            if not recorded:
                recorded = True
                with open(RECORD_SCORE_FILE_NAME, "r") as f:
                    record_score = int(f.read())
                if score > record_score:
                    with open(RECORD_SCORE_FILE_NAME, "w") as f:
                        f.write(str(score))

            record_score_text = score_font.render(f"Best score: {record_score}", True, WHITE)
            screen.blit(record_score_text, RECORD_SCORE_TEXT_POSITION)

            gameover_score_text = gameover_font.render("Your Score", True, WHITE)
            gameover_score_text_rect = gameover_score_text.get_rect()
            gameover_score_text_rect.left = (width - gameover_score_text_rect.width) // 2
            gameover_score_text_rect.top = height // 3
            screen.blit(gameover_score_text, gameover_score_text_rect)

            gameover_score_text2 = gameover_font.render(str(score), True, WHITE)
            gameover_score_text2_rect = gameover_score_text2.get_rect()
            gameover_score_text2_rect.left = (width - gameover_score_text2_rect.width) // 2
            gameover_score_text2_rect.top = gameover_score_text_rect.bottom + 10
            screen.blit(gameover_score_text2, gameover_score_text2_rect)

            restart_rect.left = (width - restart_rect.width) // 2
            restart_rect.top = height - 200
            screen.blit(restart_image, restart_rect)

            gameover_rect.left = (width - restart_rect.width) // 2
            gameover_rect.top = restart_rect.bottom + 10
            screen.blit(gameover_image, gameover_rect)

            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                if restart_rect.left < pos[0] < restart_rect.right and restart_rect.top < pos[1] < restart_rect.bottom:
                    main()
                elif gameover_rect.left < pos[0] < gameover_rect.right and gameover_rect.top < pos[1] < gameover_rect.bottom:
                    pygame.quit()
                    sys.exit()




        # every 6 times of refresh, switch the player's image
        if not delay % 6:
            switch_image = not switch_image

        # every refresh reduce time counter by 1
        # once the time counter is 0, reset it back to 60
        if delay == 0:
            delay = 60
        delay -= 1
        pygame.display.flip()
         # refresh 60 times per second
        clock.tick(60)



main()