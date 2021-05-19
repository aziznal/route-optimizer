"""

A Node is a point on the graph that can be connected to other nodes
using the Arc

"""

from __future__ import annotations
from typing import List


class Node:
    def __init__(self, x: float, y: float, connections: List[Node]):

        self.x, self.y, self.connections = x, y, connections
