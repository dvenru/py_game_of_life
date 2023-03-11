import pygame as pg

from settings import *


class UIGroup:
    def __init__(self) -> None:
        self.group_draw = []
        self.group_update = []

    def change_group(self, changed_objects: list, draw_state: bool = True, update_state: bool = False) -> None:
        for changed_object in changed_objects:
            if draw_state and (changed_object not in self.group_draw):
                self.group_draw.append(changed_object)
            elif not draw_state and (changed_object in self.group_draw):
                self.group_draw.remove(changed_object)

            if update_state and (changed_object not in self.group_update):
                self.group_update.append(changed_object)
            elif not update_state and (changed_object in self.group_update):
                self.group_update.remove(changed_object)

    def update(self, event = None) -> None:
        if event is None:
            for _object in self.group_draw:
                _object.draw()
        else:
            for _object in self.group_update:
                if callable(getattr(_object, "update", None)):
                    _object.update(event)

    def get_group(self, group_type: str = "draw") -> list:
        return self.group_draw if group_type == "draw" else self.group_update if group_type == "update" else None


class Label:
    def __init__(self, surface, text: str, position: tuple = (int, int), size: int = 20, color = "white", timer: float = 0) -> None:
        self.surface = surface
        self.font = pg.font.SysFont(DEFAULT_FONT, size)
        self.render_text = self.font.render(text, True, color)
        _, _, width, height = self.render_text.get_rect()
        self.rect = pg.Rect(position[0], position[1], width, height)
        self.text = text
        self.timer = timer

    def draw(self) -> None:
        self.surface.blit(self.render_text, self.rect)

    def set_center(self, new_pos: tuple = (int, int)) -> None:
        self.rect.center = new_pos

    def set_text(self, new_text: str, color = "white") -> None:
        self.render_text = self.font.render(new_text, True, color)

    def get_timer(self) -> float:
        return self.timer


class CursorRule(Label):
    def __init__(self, surface, text: str, position: tuple = (int, int), size: int = 20, color = "white", timer: float = 0) -> None:
        super().__init__(surface, text, position, size, color, timer)

    def draw(self) -> None:
        self.rect.center = (pg.mouse.get_pos()[0] + 10, pg.mouse.get_pos()[1] - 10)
        self.surface.blit(self.render_text, self.rect)


class Button:
    def __init__(self, surface, rect: tuple = (int, int, int, int), button_text: str = "Button", size: int = 20, click_function = None) -> None:
        self.surface = surface
        self.font = pg.font.SysFont(DEFAULT_FONT, size)
        self.text = button_text
        self.click_function = click_function
        self.rect = pg.Rect(rect)
        self.background = pg.Surface((rect[2], rect[3]))
        self.render_text = self.font.render(self.text, False, "white")

        self.fill_color = {
            "normal": SOFT_RED,
            "pressed": GRAY_RED,
            "hover": LIGHT_RED
        }

    def draw(self) -> None:
        self.background.blit(self.render_text, [
            self.rect.width // 2 - self.render_text.get_rect().width // 2,
            self.rect.height // 2 - self.render_text.get_rect().height // 2
        ])
        self.surface.blit(self.background, self.rect)

    def update(self, _event) -> None:
        mouse_position = pg.mouse.get_pos()
        self.background.fill(self.fill_color['normal'])
        if self.rect.collidepoint(mouse_position):
            self.background.fill(self.fill_color['hover'])
            if pg.mouse.get_pressed()[0] and self.click_function is not None:
                self.background.fill(self.fill_color['pressed'])
                self.click_function()


class Edit:
    def __init__(self, surface, rect: tuple = (int, int, int, int), size: int = 23, text: str = "") -> None:
        self.surface = surface
        self.rect = pg.Rect(rect)
        self.background = pg.Surface((rect[2], rect[3]))
        self.font = pg.font.SysFont("Arial", size)
        self.text = text
        self.render_text = self.font.render(self.text, False, "white")
        self.is_selected = False

        self.fill_color = {
            "normal": SOFT_BLUE,
            "pressed": GRAY_BLUE,
            "hover": LIGHT_BLUE
        }

    def draw(self) -> None:
        self.background.blit(self.render_text, [
            self.rect.width // 2 - self.render_text.get_rect().width // 2,
            self.rect.height // 2 - self.render_text.get_rect().height // 2
        ])
        self.surface.blit(self.background, self.rect)

    def update(self, event) -> None:
        mouse_position = pg.mouse.get_pos()
        self.background.fill(self.fill_color["normal"])
        if self.rect.collidepoint(mouse_position):
            self.background.fill(self.fill_color["hover"])
        if self.is_selected:
            self.background.fill(self.fill_color["pressed"])

        if event.type == pg.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(mouse_position):
                self.is_selected = not self.is_selected
            else:
                self.is_selected = False

        if event.type == pg.KEYDOWN:
            if self.is_selected:
                match event.key:
                    case pg.K_RETURN:
                        self.text = ""
                    case pg.K_BACKSPACE:
                        self.text = self.text[:-1]
                    case _:
                        self.text += event.unicode
            self.render_text = self.font.render(self.text, False, "white")
