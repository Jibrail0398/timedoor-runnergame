import pygame
from random import randint

pygame.init()
pygame.mixer.init()

#game environment configuration
frame_size_x = 800 
frame_size_y = 400 
window_screen = pygame.display.set_mode((frame_size_x, frame_size_y))
game_active = False  
current_frame = 0
player_index = 0
player_gravity = 0
start_time = 0
character_index = 0
pygame.display.set_caption("Running Game")
clock = pygame.time.Clock()
FPS = 60

#Load Assets

#background
skybox = pygame.image.load('gallery/sprites/sky.png').convert()
ground = pygame.image.load('gallery/sprites/Ground.png').convert()

#player
player_jump = pygame.image.load("gallery/sprites/player/Player3.png").convert_alpha()
player_walk_1 = pygame.image.load("gallery/sprites/player/Player.png").convert_alpha()
player_walk_2 = pygame.image.load("gallery/sprites/player/Player2.png").convert_alpha()
player_walk = [player_walk_1, player_walk_2]
player_index = 0
player = player_walk[player_index]
player_rect = player.get_rect(midbottom = (80, 320))

#font
font = pygame.font.Font('fonts/Jersey15-Regular.ttf',32)

#sound
jump_sound = pygame.mixer.Sound("gallery/audio/jump.mp3")

#enemy
enemy_frame1 = pygame.image.load("gallery/sprites/enemies/Enemy.png").convert_alpha()
enemy_frame2 = pygame.image.load("gallery/sprites/enemies/Enemy_2.png").convert_alpha()
enemy_frames = [enemy_frame1, enemy_frame2]
enemy_frame_index = 0
enemy = enemy_frames[enemy_frame_index]

enemy2_frame1 = pygame.image.load("gallery/sprites/enemies/Enemy2.png").convert_alpha()
enemy2_frame2 = pygame.image.load("gallery/sprites/enemies/Enemy2_2.png").convert_alpha()
enemy2_frames = [enemy2_frame1, enemy2_frame2]
enemy2_frame_index = 0
enemy2 = enemy2_frames[enemy2_frame_index]

obstacle_rect_list = [] 

#enemy appearance timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1000)

enemy_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(enemy_animation_timer, 200)

enemy2_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(enemy2_animation_timer, 500)

#game functions
def active_game():
    global player_gravity, obstacle_rect_list
    window_screen.blit(skybox, (0,0))    #Show the background
    window_screen.blit(ground, (0, 320))    #Show the ground
    score = display_score()
    player_animation()   #Run the player animation
    window_screen.blit(player, player_rect)   #Show the player on the screen
    obstacle_rect_list = obstacle_movement(obstacle_rect_list)
    player_gravity += 1
    player_rect.y += player_gravity
    if player_rect.bottom >= 320:
        player_rect.bottom = 320

def inactive_game():
    window_screen.fill((64,64,64))  #Set background color to gray
    player_animation()
    game_name = font.render("Runner Game", True, (255,255,255))
    game_name = pygame.transform.scale2x(game_name)
    game_name_rect = game_name.get_rect(center = (400, 80))
    game_message = font.render("Press Space to start", False, "white")
    game_message_rect = game_message.get_rect(center = (400, 300))
    window_screen.blit(game_name, game_name_rect)
    window_screen.blit(game_message, game_message_rect)
    window_screen.blit(player, (frame_size_x // 2 - 30 , frame_size_y//2 - 30 ))

def player_animation():
    global player, player_index
    if player_rect.bottom < 320:
        player = player_jump
    else:
        player_index += 0.1
        if player_index >= len(player_walk):
            player_index = 0
        player = player_walk[int(player_index)]

def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= 5
            if obstacle_rect.bottom == 320:
                window_screen.blit(enemy, obstacle_rect)
            else:
                window_screen.blit(enemy2, obstacle_rect)
        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100]
        return obstacle_list
    else:
        return []

def spawn_enemy():
    global enemy_frame_index, enemy2_frame_index, enemy, enemy2
    if event.type == obstacle_timer:
        if randint(0, 2):
            print('enemy has been spawned')
            obstacle_rect_list.append(enemy.get_rect(bottomright = (randint(900, 1100), 320)))
        else:
            obstacle_rect_list.append(enemy2.get_rect(bottomright = (randint(900, 1100), 210)))
    if event.type == enemy_animation_timer:
        if enemy_frame_index == 0:
            enemy_frame_index = 1
        else:
            enemy_frame_index = 0
        enemy = enemy_frames[enemy_frame_index]

    if event.type == enemy2_animation_timer:
        if enemy2_frame_index == 0:
            enemy2_frame_index = 1
        else:
            enemy2_frame_index = 0
        enemy2 = enemy2_frames[enemy2_frame_index]

def display_score():
    current_time = int(pygame.time.get_ticks() / 600) - start_time
    score = font.render(f"{current_time}", False, "white")
    score_rect = score.get_rect(center = (400, 50))
    window_screen.blit(score, score_rect)
    return current_time


#Main game loop
while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            pygame.quit()
            exit()
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                start_time = int(pygame.time.get_ticks() / 600)
                spawn_enemy()
            if event.type == pygame.KEYDOWN and player_rect.bottom == 320:
                if event.key == pygame.K_SPACE:
                    player_gravity = -20
                    jump_sound.play()

    if game_active:
        active_game()
        spawn_enemy()
    else:
        inactive_game()

    pygame.display.update()
    clock.tick(FPS)

