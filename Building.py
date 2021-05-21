import pygame


from PygameSettings import *

from BaseClasses.Node import Node


# TODO: Add method to draw node index or coordinates on top of node

class Building(Node):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.rect = pygame.Rect(self.x, self.y, NODE_RADIUS, NODE_RADIUS)

    def draw(self, screen: pygame.Surface) -> None:

        pygame.draw.ellipse(
            screen, Colors.RED, self.rect
        )
