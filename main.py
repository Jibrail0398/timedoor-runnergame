import pygame

pygame.init()
frame_size_x = 800 
frame_size_y = 400 

window_screen = pygame.display.set_mode((frame_size_x, frame_size_y))

pygame.display.set_caption("Running Game")

clock = pygame.time.Clock()
FPS = 60

game_active = False   #This variable is used to check whether the game is active or not

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            pygame.quit()
            exit()

        if game_active:
            print("Game Active")
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True

    if game_active:
        print("Game Active")
    else:
        print("Game Inactive")

    pygame.display.update()
    clock.tick(FPS)
