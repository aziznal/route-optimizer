"""

A Node is a point on the graph that can be connected to other nodes
using an Arc

"""

from __future__ import annotations
from typing import List


class Node:
    def __init__(self, x: int, y: int, connections: List[Node]):

        self.x, self.y, self.connections = x, y, connections

    def __hash__(self) -> int:
        # TODO: MUST implement better hash algorithm here. There may be a chance of nodes having the same hash
        return hash((self.x) ** 2 + (self.y + 1) ** 2)

    def __str__(self) -> str:
        return f"Node({self.x}, {self.y})"
