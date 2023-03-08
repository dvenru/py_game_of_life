import pygame as pg


class UIGroup:
    def __init__(self) -> None:
        self.group_ui = []

    def append(self, new_object) -> None:
        self.group_ui.append(new_object)

    def update(self) -> None:
        for _object in self.group_ui:
            _object.draw()


class Label:
    def __init__(self, surface, text: str, position: tuple = (int, int), group_ui = None, size: int = 20, color = "white") -> None:
        self.surface = surface
        self.font = pg.font.SysFont("Arial", size)
        self.image = self.font.render(text, True, color)
        _, _, width, height = self.image.get_rect()
        self.rect = pg.Rect(position[0], position[1], width, height)
        self.text = text
        group_ui.append(self)

    def draw(self) -> None:
        self.surface.blit(self.image, self.rect)

    def set_text(self, new_text: str, color = "white") -> None:
        self.image = self.font.render(new_text, True, color)
