import pygame
from mypackage import GameBoard, Player


diff = 1
WIDTH = 1000 * diff
HEIGHT = (WIDTH * 0.555) * diff


def start():
    pygame.init()

    g_b = GameBoard(WIDTH, HEIGHT)
    screen = pygame.display.set_mode((g_b.width, g_b.height))
    clock = pygame.time.Clock()


    player_1 = Player(WIDTH, HEIGHT, 1, "p1", int(WIDTH * 0.1))
    player_2 = Player(WIDTH, HEIGHT, 2, "p2", WIDTH * 0.9)

    
    running = True
    while running:

        g_b.render_game(screen)
        key = pygame.key.get_pressed()

        # Update all player's details
        player_1.update(key, screen)
        player_2.update(key, screen)

        # Check if either player has been hit
        player_1.check_bullet_collision(player_2.rect)
        player_2.check_bullet_collision(player_1.rect)
        

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                
            # Get the state of all keyboard buttons
        
        pygame.display.flip()
        clock.tick(g_b.fps)



if __name__ == "__main__":
    start()
