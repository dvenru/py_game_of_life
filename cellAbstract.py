from abc import ABC, abstractmethod


class CellAbstract(ABC):

    @abstractmethod
    def search_neighbors(self, line_position: int, tile_position: int) -> list:
        pass

    def set_rule(self, rule: str):
        pass
