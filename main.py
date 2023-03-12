import pygame as pg
import sys

from settings import *
from life import Life
from gameui import UIGroup, Label, CursorRule
from gameui import Button, Edit


class Game:

    def __init__(self) -> None:
        pg.init()

        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption("Game of Life")
        pg.display.set_icon(pg.image.load("resources/pyGLicon.png"))
        self.clock = pg.time.Clock()

        self.life = Life(self.screen)
        self.life.set_rule_str(DEFAULT_LIFE_RULE)
        self.group_ui = UIGroup()

        self.option_menu_opened = False
        self.rule_menu_opened = False
        self.is_paused = False
        self.select_speed = 1

        # Вывод скорости и текущих правил
        self.speed_label = Label(self.screen, "SPEED: " + ">" * int(self.select_speed + 1), (10, 10), 23)
        self.rule_label = Label(self.screen, "RULE: " + self.life.get_rule(), (10, 40), 23)
        self.group_ui.change_group([self.speed_label, self.rule_label], True, False)

        # Вывод информации о действиях и ошибках
        self.system_label = Label(self.screen, "! NONE !", (0, 0), 23, "red", 0.5)
        self.system_label.set_center((WIDTH // 2, HEIGHT - 30))
        self.group_ui.change_group([self.system_label], True, False)

        # Линейка
        self.mouse_rule = CursorRule(self.screen, "0-0", (0, 0), 20, SOFT_RED)

        # Меню // Главная
        set_rule_button = Button(self.screen, (0, 0, 150, 40), "RULES", 20, lambda: self.control_menu("rule"))
        set_rule_button.rect.center = (WIDTH // 2, HEIGHT // 2 - 50)
        set_color_button = Button(self.screen, (0, 0, 150, 40), "COLOR")
        set_color_button.rect.center = (WIDTH // 2, HEIGHT // 2)
        quit_button = Button(self.screen, (0, 0, 150, 40), "QUIT", 20, lambda: sys.exit())
        quit_button.rect.center = (WIDTH // 2, HEIGHT // 2 + 50)
        self.menu_elements = [set_rule_button, set_color_button, quit_button]

        # Меню // Запись правил
        rule_life_label = Label(self.screen, "LIFE:", (0, 0), 23)
        rule_life_label.rect.center = (WIDTH // 2 - 85, HEIGHT // 2 - 50)
        rule_life_edit = Edit(self.screen, (0, 0, 130, 40))
        rule_life_edit.rect.center = (WIDTH // 2 + 40, HEIGHT // 2 - 50)
        rule_birth_label = Label(self.screen, "BIRTH:", (0, 0), 23)
        rule_birth_label.rect.center = (WIDTH // 2 - 75, HEIGHT // 2)
        rule_birth_edit = Edit(self.screen, (0, 0, 130, 40))
        rule_birth_edit.rect.center = (WIDTH // 2 + 40, HEIGHT // 2)
        rule_default_button = Button(self.screen, (0, 0, 100, 40), "DEFAULT", 20, lambda: self.set_rule_click(True))
        rule_default_button.rect.center = (WIDTH // 2 - 55, HEIGHT // 2 + 50)
        rule_set_button = Button(self.screen, (0, 0, 100, 40), "SET", 20, lambda: self.set_rule_click(False))
        rule_set_button.rect.center = (WIDTH // 2 + 55, HEIGHT // 2 + 50)
        self.rule_edit_elements = [rule_life_label, rule_birth_label, rule_life_edit, rule_birth_edit, rule_default_button, rule_set_button]

        # События
        self.new_generation = pg.USEREVENT + 1
        self.system_label_hide = pg.USEREVENT + 2
        pg.time.set_timer(self.new_generation, int(WAIT_LIST[self.select_speed] * 1000))
        pg.time.set_timer(self.system_label_hide, int(self.system_label.get_timer() * 1000), 1)

        self.draw_area_list = []

    def control_menu(self, menu_type: str) -> None:
        match menu_type:
            case "option":
                self.rule_menu_opened = False
                self.option_menu_opened = not self.option_menu_opened
            case "rule":
                self.rule_menu_opened = not self.rule_menu_opened
                self.option_menu_opened = False

        self.group_ui.change_group(self.menu_elements, self.option_menu_opened, self.option_menu_opened)
        self.group_ui.change_group(self.rule_edit_elements, self.rule_menu_opened, self.rule_menu_opened)

    def set_rule_click(self, is_default: bool) -> None:
        if (len(self.rule_edit_elements[2].text) == 0 or len(self.rule_edit_elements[3].text) == 0) and not is_default:
            self.system_label.set_text("Неправильный ввод правил!")
            self.system_label.set_center((WIDTH // 2, HEIGHT - 30))
            pg.time.set_timer(self.system_label_hide, 3000, 1)
        else:
            self.rule_label.set_text("RULE: " + DEFAULT_LIFE_RULE if is_default else "RULE: " + self.rule_edit_elements[2].text + "/" + self.rule_edit_elements[3].text)
            self.life.set_rule_str(DEFAULT_LIFE_RULE if is_default else self.rule_edit_elements[2].text + "/" + self.rule_edit_elements[3].text)
            self.control_menu("rule")

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

        self.draw_area_list = [(x, y) for x in range(end_position[0], start_position[0] + x_step, x_step)
                               for y in range(end_position[1], start_position[1] + y_step, y_step)
                               if fill or ((x == end_position[0] or x == start_position[0])
                               or (y == end_position[1] or y == start_position[1]))]

    def draw_pattern(self) -> None:
        pass

    def run(self) -> None:
        # Локальный переменные
        drawing = False
        start_position = (0, 0)

        while True:
            self.clock.tick(FPS)

            for event in pg.event.get():
                # Обновляем события интерфейса
                self.group_ui.update(event)

                # Обработка основных событий
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                if event.type == self.new_generation:
                    self.life.new_generation()
                if event.type == self.system_label_hide:
                    self.group_ui.change_group([self.system_label], False, False)

                # Обработка нажатий клавиш
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        self.control_menu("option")
                    if event.key == pg.K_r and pg.key.get_mods() & pg.KMOD_CTRL:
                        self.control_menu("rule")
                    if event.key == pg.K_TAB:
                        self.life.set_grid_visible()
                    if event.key == pg.K_RIGHT:
                        self.update_event_wait(1)
                    if event.key == pg.K_LEFT:
                        self.update_event_wait(-1)
                    if event.key == pg.K_SPACE:
                        self.update_event_wait()
                    if event.key == pg.K_DELETE:
                        self.life.clear()

                # Одна из вариаций паузы (неудобно)
                # if event.type == pg.MOUSEBUTTONDOWN:
                #     self.update_event_wait(0)
                # if event.type == pg.MOUSEBUTTONUP:
                #     self.update_event_wait(0)

                if not self.option_menu_opened and not self.rule_menu_opened:

                    if pg.key.get_pressed()[pg.K_LCTRL]:

                        if event.type == pg.MOUSEBUTTONDOWN:
                            start_position = (pg.mouse.get_pos()[0] // TILE_SIZE, pg.mouse.get_pos()[1] // TILE_SIZE)
                            drawing = True
                            self.group_ui.change_group([self.mouse_rule], True, False)

                        if event.type == pg.MOUSEMOTION and drawing:
                            end_position = (pg.mouse.get_pos()[0] // TILE_SIZE, pg.mouse.get_pos()[1] // TILE_SIZE)
                            self.draw_rect(start_position, end_position, True if pg.key.get_pressed()[pg.K_LSHIFT] else False)
                            self.mouse_rule.set_text(str(max([x[0] for x in self.draw_area_list])
                                                         - min([x[0] for x in self.draw_area_list]) + 1) + " | " +
                                                     str(max([y[1] for y in self.draw_area_list])
                                                         - min([y[1] for y in self.draw_area_list]) + 1), SOFT_RED)

                        if event.type == pg.MOUSEBUTTONUP:
                            drawing = False
                            self.group_ui.change_group([self.mouse_rule], False, False)
                            if event.button == 1:
                                self.life.set_life(0, 0, '1', self.draw_area_list)
                            if event.button == 3:
                                self.life.set_life(0, 0, '0', self.draw_area_list)
                            self.draw_area_list = []

                    # Рисование точек
                    else:
                        if pg.mouse.get_pressed()[0]:
                            self.life.set_life(pg.mouse.get_pos()[0] // TILE_SIZE, pg.mouse.get_pos()[1] // TILE_SIZE, '1')
                        elif pg.mouse.get_pressed()[2]:
                            self.life.set_life(pg.mouse.get_pos()[0] // TILE_SIZE, pg.mouse.get_pos()[1] // TILE_SIZE, '0')
                        self.draw_area_list = []

            # Рисование изображения
            self.life.draw()
            self.life.draw_area(self.is_paused, pg.mouse.get_pos()[0] // TILE_SIZE, pg.mouse.get_pos()[1] // TILE_SIZE, self.draw_area_list)
            self.group_ui.update()

            pg.display.flip()


if __name__ == "__main__":
    Game().run()
