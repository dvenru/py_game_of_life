import pygame as pg

from settings import *
from life import Life
from gameui import Label, UIGroup


class Game:

    def __init__(self) -> None:
        pg.init()

        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption("Game of Life")
        pg.display.set_icon(pg.image.load("resources/pyGLicon.png"))
        self.clock = pg.time.Clock()

        self.life = Life(self.screen)
        self.group_ui = UIGroup()

        self.is_paused = False
        self.select_speed = 1
        self.speed_label = Label(self.screen, "SPEED: " + ">" * int(self.select_speed + 1), (10, 10), self.group_ui, 20)

        self.new_generation = pg.USEREVENT + 1
        pg.time.set_timer(self.new_generation, int(WAIT_LIST[self.select_speed] * 1000))

    def update_event_wait(self, new_speed: int = 0) -> None:
        if new_speed == 0:
            self.is_paused = not self.is_paused
            pg.time.set_timer(self.new_generation, int((0 if self.is_paused else WAIT_LIST[self.select_speed]) * 1000))
            self.speed_label.set_text("SPEED: ||" if self.is_paused else "SPEED: " + ">" * int(self.select_speed + 1))

        elif 0 <= self.select_speed + new_speed < len(WAIT_LIST) and not self.is_paused:
            self.select_speed += new_speed
            self.speed_label.set_text("SPEED: " + ">" * int(self.select_speed + 1))
            pg.time.set_timer(self.new_generation, int(WAIT_LIST[self.select_speed] * 1000))

    def run(self) -> None:
        running = True

        while running:
            self.clock.tick(FPS)

            for event in pg.event.get():
                # Обработка основных событий
                if event.type == pg.QUIT:
                    running = False
                elif event.type == self.new_generation:
                    self.life.new_generation()

                # Обработка нажатий клавиш
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        running = False
                    elif event.key == pg.K_TAB:
                        self.life.set_grid_visible()
                    elif event.key == pg.K_RIGHT:
                        self.update_event_wait(1)
                    elif event.key == pg.K_LEFT:
                        self.update_event_wait(-1)
                    elif event.key == pg.K_SPACE:
                        self.update_event_wait()
                    elif event.key == pg.K_DELETE:
                        self.life.clear()

                # Обработка нажатий мыши
                if self.is_paused:
                    pressed = pg.mouse.get_pressed()
                    if pressed[0]:
                        self.life.set_life(pg.mouse.get_pos()[0] // TILE_SIZE, pg.mouse.get_pos()[1] // TILE_SIZE, '1')
                    elif pressed[2]:
                        self.life.set_life(pg.mouse.get_pos()[0] // TILE_SIZE, pg.mouse.get_pos()[1] // TILE_SIZE, '0')

            self.screen.fill((0, 0, 0))
            self.life.draw(self.is_paused, pg.mouse.get_pos()[0] // TILE_SIZE, pg.mouse.get_pos()[1] // TILE_SIZE)
            self.group_ui.update()

            pg.display.flip()

        pg.quit()


if __name__ == "__main__":
    Game().run()
