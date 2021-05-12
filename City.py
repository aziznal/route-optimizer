"""

A City is a graph made of Buildings (nodes) which are connected by Streets (arcs)

"""

from typing import List


from Building import Building
from Street import Street

import pygame


class City:

    def __init__(self, buildings: List[Building], streets: List[Street]):

        self.buildings = buildings
        self.streets = streets

    def draw(self, screen: pygame.Surface):

        for building in self.buildings:
            building.draw(screen)

        for street in self.streets:
            street.draw(screen)
