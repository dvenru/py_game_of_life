import pygame as pg

from settings import *


class UIGroup:
    def __init__(self) -> None:
        self.group_draw = []
        self.group_update = []

    def append(self, new_object, is_update: bool = False) -> None:
        self.group_draw.append(new_object)
        if is_update:
            self.group_update.append(new_object)

    def change_draw(self, changed_object, draw_state: bool) -> None:
        if draw_state and (changed_object not in self.group_draw):
            self.group_draw.append(changed_object)
        elif not draw_state and (changed_object in self.group_draw):
            self.group_draw.remove(changed_object)

    def update(self) -> None:
        for _object in self.group_draw:
            _object.draw()
        for _object in self.group_update:
            _object.update()


class Label:
    def __init__(self, surface, text: str, position: tuple = (int, int), size: int = 20, color = "white", timer: float = 0) -> None:
        self.surface = surface
        self.font = pg.font.SysFont("Arial", size)
        self.image = self.font.render(text, True, color)
        _, _, width, height = self.image.get_rect()
        self.rect = pg.Rect(position[0], position[1], width, height)
        self.text = text
        self.timer = timer

    def draw(self) -> None:
        self.surface.blit(self.image, self.rect)

    def set_center(self, new_pos: tuple = (int, int)) -> None:
        self.rect.center = new_pos

    def set_text(self, new_text: str, color = "white") -> None:
        self.image = self.font.render(new_text, True, color)

    def get_timer(self) -> float:
        return self.timer


class Button:
    def __init__(self, surface, rect: tuple = (int, int, int, int), button_text: str = "Button", click_function = None) -> None:
        self.surface = surface
        self.rect = pg.Rect(rect[0], rect[1], rect[2], rect[3])
        self.text = button_text
        self.click_function = click_function

        self.fill_color = {
            "normal": SOFT_RED,
            "pressed": GRAY_RED,
            "hover": LIGHT_RED
        }

    def draw(self) -> None:
        pass

    def update(self) -> None:
        pass


class OptionMenu:
    def __init__(self, surface, background_color = "white", title_color = "black", title_label = "Menu") -> None:
        self.surface = surface
        self.background_color = background_color
        self.title_label = title_label
        self.title_color = title_color
        self.button_list = []
        self.show = False

    def add_button(self, new_button) -> None:
        self.button_list.append(new_button)
        self.update_size()

    def update_size(self) -> None:
        pass

    def draw(self) -> None:
        pass

    def update(self) -> None:
        pass
