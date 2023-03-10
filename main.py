import pygame as pg

from settings import *
from gridController import GridController
from gameUI import UIGroup, Label

from cellDefault import CellDefault

class Game:

    def __init__(self) -> None:
        pg.init()

        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption("Game of Life")
        pg.display.set_icon(pg.image.load("resources/pyGLicon.png"))
        self.clock = pg.time.Clock()

        self.grid_ctrl = GridController(self.screen)

        self.grid_ctrl.register_cell_type(CellDefault)

        self.grid_ctrl.set_rule_str(DEFAULT_LIFE_RULE)
        self.group_ui = UIGroup()

        self.is_paused = False
        self.select_speed = 1
        self.speed_label = Label(self.screen, "SPEED: " + ">" * int(self.select_speed + 1), (10, 10), 23)
        self.group_ui.append(self.speed_label)

        self.rule_label = Label(self.screen, "RULE: " + self.grid_ctrl.get_rule(), (10, 40), 23)
        self.group_ui.append(self.rule_label)

        self.system_label = Label(self.screen, "! None !", (0, 0), 23, "red", 5)
        self.system_label.set_center((WIDTH // 2, HEIGHT - 30))
        # self.group_ui.append(self.system_label)

        self.new_generation = pg.USEREVENT + 1
        self.system_label_hide = pg.USEREVENT + 2
        pg.time.set_timer(self.new_generation, int(WAIT_LIST[self.select_speed] * 1000))
        # pg.time.set_timer(self.system_label_hide, int(self.system_label.get_timer() * 1000), 1)

        self.draw_hide_list = []

    def update_event_wait(self, new_speed: int = 0) -> None:
        if new_speed == 0:
            self.is_paused = not self.is_paused
            pg.time.set_timer(self.new_generation, int((0 if self.is_paused else WAIT_LIST[self.select_speed]) * 1000))
            self.speed_label.set_text("SPEED: PAUSE" if self.is_paused else "SPEED: " + ">" * int(self.select_speed + 1))

        elif 0 <= self.select_speed + new_speed < len(WAIT_LIST) and not self.is_paused:
            self.select_speed += new_speed
            self.speed_label.set_text("SPEED: " + ">" * int(self.select_speed + 1))
            pg.time.set_timer(self.new_generation, int(WAIT_LIST[self.select_speed] * 1000))

    def draw_rect(self, start_position: tuple = (int, int), end_position: tuple = (int, int), fill: bool = False) -> None:

        x_step = -1 if end_position[0] > start_position[0] else 1
        y_step = -1 if end_position[1] > start_position[1] else 1

        self.draw_hide_list = [(x, y) for x in range(end_position[0], start_position[0] + x_step, x_step)
                               for y in range(end_position[1], start_position[1] + y_step, y_step)
                               if fill or ((x == end_position[0] or x == start_position[0])
                               or (y == end_position[1] or y == start_position[1]))]

    def draw_pattern(self) -> None:
        pass

    def run(self) -> None:
        # Локальный переменные
        drawing = False
        start_position = (0, 0)
        running = True

        while running:
            self.clock.tick(FPS)

            for event in pg.event.get():
                # Обработка основных событий
                if event.type == pg.QUIT:
                    running = False
                if event.type == self.new_generation:
                    self.grid_ctrl.new_generation()
                if event.type == self.system_label_hide:
                    self.group_ui.change_draw(self.system_label, False)

                # Обработка нажатий клавиш
                if event.type == pg.KEYDOWN:
                    match event.key:
                        case pg.K_ESCAPE:
                            running = False
                        case pg.K_TAB:
                            self.grid_ctrl.set_grid_visible()
                        case pg.K_RIGHT:
                            self.update_event_wait(1)
                        case pg.K_LEFT:
                            self.update_event_wait(-1)
                        case pg.K_SPACE:
                            self.update_event_wait()
                        case pg.K_DELETE:
                            self.grid_ctrl.clear()

                # Обработка нажатий мыши
                if self.is_paused:

                    # Рисование квадрата
                    if pg.key.get_pressed()[pg.K_LCTRL]:

                        if event.type == pg.MOUSEBUTTONDOWN:
                            start_position = (pg.mouse.get_pos()[0] // TILE_SIZE, pg.mouse.get_pos()[1] // TILE_SIZE)
                            drawing = True
                        if event.type == pg.MOUSEMOTION and drawing:
                            end_position = (pg.mouse.get_pos()[0] // TILE_SIZE, pg.mouse.get_pos()[1] // TILE_SIZE)
                            self.draw_rect(start_position, end_position, True if pg.key.get_pressed()[pg.K_LSHIFT] else False)
                        if event.type == pg.MOUSEBUTTONUP:
                            drawing = False
                            if event.button == 1:
                                self.grid_ctrl.set_life(0, 0, '1', self.draw_hide_list)
                            if event.button == 3:
                                self.grid_ctrl.set_life(0, 0, '0', self.draw_hide_list)
                            self.draw_hide_list = []

                    # Рисование точек
                    else:
                        if pg.mouse.get_pressed()[0]:
                            self.grid_ctrl.set_life(pg.mouse.get_pos()[0] // TILE_SIZE, pg.mouse.get_pos()[1] // TILE_SIZE, '1')
                        elif pg.mouse.get_pressed()[2]:
                            self.grid_ctrl.set_life(pg.mouse.get_pos()[0] // TILE_SIZE, pg.mouse.get_pos()[1] // TILE_SIZE, '0')
                        self.draw_hide_list = []

            # Рисование изображения
            self.grid_ctrl.draw()
            self.grid_ctrl.draw_hide(self.is_paused, pg.mouse.get_pos()[0] // TILE_SIZE, pg.mouse.get_pos()[1] // TILE_SIZE, self.draw_hide_list)
            self.group_ui.update()

            pg.display.flip()

        pg.quit()


if __name__ == "__main__":
    Game().run()
