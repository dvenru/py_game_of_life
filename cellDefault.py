from cellAbstract import CellAbstract
from settings import COLOR_CELL_DEFAULT


class CellDefault(CellAbstract):

    def __init__(self, present_map, rule: str):
        self.rule = rule
        self.color = COLOR_CELL_DEFAULT
        self.present_map = present_map

    def search_neighbors(self, line_position: int, tile_position: int) -> list:
        neighbors = [self.present_map[l_pos][t_pos] for l_pos in range(line_position - 1, line_position + 2)
                     for t_pos in range(tile_position - 1, tile_position + 2) if
                     -1 < line_position <= len(self.present_map) and
                     -1 < tile_position <= len(self.present_map[0]) and
                     (line_position != l_pos or tile_position != t_pos) and
                     (0 <= l_pos < len(self.present_map)) and
                     (0 <= t_pos < len(self.present_map[0]))]
        neighbors_count = neighbors.count("1")
        return [neighbors, neighbors_count]

    def set_rule(self, rule: str) -> None:
        self.rule = rule
