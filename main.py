import pygame as pg

from settings import *
from life import Life


class Game:

    def __init__(self) -> None:
        pg.init()

        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption("Game of Life")
        self.clock = pg.time.Clock()

        self.life = Life(self.screen)
        for i in range(10):
            self.life.create_life(i + 10, 20)

        self.new_generation = pg.USEREVENT + 1
        pg.time.set_timer(self.new_generation, int(NEW_GEN_WAIT * 1000))

    def run(self) -> None:
        running = True

        while running:
            self.clock.tick(FPS)

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
                if event.type == self.new_generation:
                    self.life.new_generation()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        running = False

            self.screen.fill((0, 0, 0))
            self.life.draw()

            pg.display.flip()

        pg.quit()


if __name__ == "__main__":
    Game().run()
