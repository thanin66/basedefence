import pygame,sys
from stee
class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set.mode(())

    def run(self):
        while True :
            for event in pygame.QUIT:
                pygame.quit()
                sys.exit()

        self.screen.fill('black')
        pygame.display.update()
        self.clock.tick(FPS)

if __name__ == '__main__':
    game = Game()
    game.run()

