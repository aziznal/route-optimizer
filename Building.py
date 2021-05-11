

from typing import List


from BaseClasses.Node import Node


import pygame

from PygameSettings import *


class Building(Node):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.rect = pygame.Rect(self.x, self.y, NODE_RADIUS, NODE_RADIUS)

    def draw(self, screen: pygame.Surface):

        pygame.draw.ellipse(
            screen, Colors.RED, self.rect
        )

