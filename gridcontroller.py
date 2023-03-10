import pygame as pg

from settings import *


class gridcontroller:

    def __int__(self, surface) -> None:
        self.surface = surface # Задаем поле
        self.present_map = [[None for i in range(HEIGHT // TILE_SIZE)] for i in range(WIDTH // TILE_SIZE)] # Создаем пустую матрицу
        self.tile_size = TILE_SIZE
        self.colors = [SOFT_BLACK, SOFT_RED]
        self.rule_life = None
        self.rule_birth = None

        self.grid_visible = False
