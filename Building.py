import pygame


import utils
from PygameSettings import *

from BaseClasses.Node import Node


class Building(Node):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.rect = pygame.Rect(self.x, self.y, NODE_RADIUS, NODE_RADIUS)
        self.coordinates_text = self.get_coordinates_as_text()

    def get_coordinates_as_text(self) -> pygame.Surface:
        """
        Returns text containing this building's coordinates as a pygame.Surface
        """
        return utils.create_text(
            text=f"({self.rect.x}, {self.rect.y})",
            font_size=11,
            color=Colors.BLACK,
            bold=True
        )

    def draw(self, screen: pygame.Surface) -> None:
        pygame.draw.ellipse(
            screen, Colors.RED, self.rect
        )

        screen.blit(
            self.coordinates_text,
            (self.rect.centerx - 20, self.rect.centery - NODE_RADIUS*2)
        )
