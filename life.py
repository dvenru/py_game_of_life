import pygame as pg

from settings import *


class Life:
    def __init__(self, surface) -> None:
        self.surface = surface
        self.present_map = [['0' for _i in range(HEIGHT // TILE_SIZE)] for _i in range(WIDTH // TILE_SIZE)]
        self.tile_size = TILE_SIZE
        self.colors = [SOFT_BLACK, SOFT_RED]
        self.rule_life = None
        self.rule_birth = None

        self.grid_visible = False

    def draw(self) -> None:
        for num_line, line in enumerate(self.present_map):
            for num_tile, tile in enumerate(line):
                pg.draw.rect(self.surface, self.colors[int(tile)], (
                    (num_line * self.tile_size), (num_tile * self.tile_size), self.tile_size, self.tile_size))

                if self.grid_visible:
                    pg.draw.rect(self.surface, (61, 66, 65), (
                        (num_line * self.tile_size), (num_tile * self.tile_size), self.tile_size, self.tile_size), 1)

    def draw_area(self, is_paused: bool, line_position: int = 0, tile_position: int = 0, draw_list = None) -> None:
        pg.draw.rect(self.surface, (223, 244, 243) if is_paused else (57, 62, 70), ((line_position * self.tile_size), (tile_position * self.tile_size), self.tile_size, self.tile_size))

        if draw_list is not None:
            for tile in draw_list:
                pg.draw.rect(self.surface, (223, 244, 243), (
                    (tile[0] * self.tile_size), (tile[1] * self.tile_size), self.tile_size,
                    self.tile_size))

    def clear(self) -> None:
        for num_line, line in enumerate(self.present_map):
            for num_tile, tile in enumerate(line):
                self.present_map[num_line][num_tile] = '0'

    def set_life(self, line_position: int, tile_position: int, state: str, draw_list: list = None) -> None:
        if draw_list is None:
            if 0 <= line_position < len(self.present_map) and 0 <= tile_position < len(self.present_map[0]):
                self.present_map[line_position][tile_position] = state
        else:
            for tile in draw_list:
                if 0 <= tile[0] < len(self.present_map) and 0 <= tile[1] < len(self.present_map[0]):
                    self.present_map[tile[0]][tile[1]] = state

    def set_grid_visible(self) -> None:
        self.grid_visible = not self.grid_visible

    def set_rule(self, new_rule_life: str, new_rule_birth: str) -> None:
        self.rule_life = new_rule_life
        self.rule_birth = new_rule_birth

    def set_rule_str(self, new_rule: str) -> None:
        self.rule_life = list(new_rule[:new_rule.find("/")])
        self.rule_birth = list(new_rule[new_rule.find("/") + 1:])

    def get_rule(self) -> str:
        return "".join(self.rule_life) + "/" + "".join(self.rule_birth)

    def new_generation(self) -> None:
        future_map = [['0' for _i in range(HEIGHT // TILE_SIZE)] for _i in range(WIDTH // TILE_SIZE)]
        for num_line, line in enumerate(self.present_map):
            for num_tile, tile in enumerate(line):
                neighbors = self.search_neighbors(num_line, num_tile)
                match tile:
                    case '0':
                        future_map[num_line][num_tile] = '1' if str(neighbors[1]) in list(self.rule_birth) else '0'
                    case '1':
                        future_map[num_line][num_tile] = '1' if str(neighbors[1]) in list(self.rule_life) else '0'

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
