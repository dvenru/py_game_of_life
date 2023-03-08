import pygame as pg

from settings import *


class Life:
    def __init__(self, surface) -> None:
        self.surface = surface
        self.present_map = [['0' for i in range(HEIGHT // TILE_SIZE)] for i in range(WIDTH // TILE_SIZE)]
        self.tile_size = TILE_SIZE
        self.colors = [SOFT_BLACK, SOFT_RED]

        self.grid_visible = False

    def draw(self, is_setting: bool = False, line_position: int = 0, tile_position: int = 0) -> None:
        for num_line, line in enumerate(self.present_map):
            for num_tile, tile in enumerate(line):
                pg.draw.rect(self.surface, self.colors[int(tile)], (
                    (num_line * self.tile_size), (num_tile * self.tile_size), self.tile_size, self.tile_size))

                if self.grid_visible:
                    pg.draw.rect(self.surface, (61, 66, 65), (
                        (num_line * self.tile_size), (num_tile * self.tile_size), self.tile_size, self.tile_size), 1)

                if is_setting:
                    pg.draw.rect(self.surface, (223, 244, 243), (
                        (line_position * self.tile_size), (tile_position * self.tile_size), self.tile_size, self.tile_size))

    def clear(self) -> None:
        for num_line, line in enumerate(self.present_map):
            for num_tile, tile in enumerate(line):
                self.present_map[num_line][num_tile] = '0'

    def set_life(self, line_position: int, tile_position: int, state: str) -> None:
        self.present_map[line_position][tile_position] = state

    def set_grid_visible(self) -> None:
        self.grid_visible = not self.grid_visible

    def new_generation(self) -> None:
        future_map = [['0' for i in range(HEIGHT // TILE_SIZE)] for i in range(WIDTH // TILE_SIZE)]
        for num_line, line in enumerate(self.present_map):
            for num_tile, tile in enumerate(line):
                neighbors = self.search_neighbors(num_line, num_tile)
                match tile:
                    case '0':
                        future_map[num_line][num_tile] = '1' if neighbors[1] == 3 else '0'
                    case '1':
                        future_map[num_line][num_tile] = '1' if 2 <= neighbors[1] <= 3 else '0'

        self.present_map = future_map.copy()

    def search_neighbors(self, line_position: int, tile_position: int) -> list:
        neighbors = [self.present_map[l_pos][t_pos] for l_pos in range(line_position - 1, line_position + 2)
                     for t_pos in range(tile_position - 1, tile_position + 2) if
                     -1 < line_position <= len(self.present_map) and
                     -1 < tile_position <= len(self.present_map[0]) and
                     (line_position != l_pos or tile_position != t_pos) and
                     (0 <= l_pos < len(self.present_map)) and
                     (0 <= t_pos < len(self.present_map[0]))]
        neighbors_count = neighbors.count('1')
        return [neighbors, neighbors_count]
