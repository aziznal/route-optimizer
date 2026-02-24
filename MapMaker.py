"""
A Simple UI that takes an image and allows the user to create
a graph (nodes and arcs) on the map. the graph is saved a json file.
"""

import pygame

pygame.init()
pygame.font.init()


class MapMaker:
    def __init__(self, map_image: pygame.Surface) -> None:

        self.map_image = map_image

        self.textmaker = pygame.font.SysFont("arial", 18, bold=True)

    def draw(self, screen) -> None:
        screen.blit(self.map_image, (0, 0))
