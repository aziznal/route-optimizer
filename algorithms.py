
from typing import Union, List

from City import City
from BaseClasses.Node import Node
from BaseClasses.Arc import Arc




class Algorithm:

    def __init__(self, nodes: List[Node]) -> None:
        self.nodes = nodes

    
    def find_shortest_path(self, first_point: Node, second_point: Node) -> List[Node]:
        raise NotImplementedError("Method has not been implemented yet.")



class A_star(Algorithm):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)


class Dijkstra(Algorithm):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)


class Johnson(Algorithm):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)


class TravelingSalesman(Algorithm):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)


    def find_shortest_path(self, starting_node: Node, nodes: List[Node]) -> List[Node]:
        pass

