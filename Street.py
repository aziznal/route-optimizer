
from typing import Tuple

from BaseClasses.Arc import Arc


from PygameSettings import *
import pygame


import numpy as np


class Street(Arc):

    def __init__(self, *args, show_arrows: bool = True) -> None:
        super().__init__(*args)

        self.show_arrows = show_arrows

        self.arrow_surface = self.create_arrow_surface()

        self.start_pos, self.end_pos = self._get_line_start_and_end()

    def create_arrow_surface(self) -> pygame.Surface:

        arrow_surface = pygame.image.load(Resources.ARROW_IMAGE_PATH)
        arrow_surface = pygame.transform.scale(arrow_surface, (10, 10))

        rotation_angle = self.angle

        arrow_surface = pygame.transform.rotate(arrow_surface, rotation_angle)

        return arrow_surface

    def draw_arrow(self, screen: pygame.Surface) -> None:
        screen.blit(self.arrow_surface, (self.node2.x, self.node2.y))

    def _adjust_line_end(self, end_x: int, end_y: int) -> Tuple[int, int]:

        dx = NODE_RADIUS * np.cos(self.angle)
        dy = NODE_RADIUS * np.sin(self.angle)

        quadrant = self.get_quadrant_of_node2()

        print(f"angle: {self.angle}\tquadrant: {quadrant}\n\n")

        if quadrant == 1:
            end_x -= dx
            end_y += dy

        elif quadrant == 2:
            end_x -= dx
            end_y += dy

        elif quadrant == 3:
            end_x -= dx
            end_y += dy

        elif quadrant == 4:
            end_x -= dx
            end_y += dy

        return end_x, end_y

    def _get_line_start_and_end(self) -> Tuple[Tuple[int, int], Tuple[int, int]]:

        start_x, start_y = self.node1.x + NODE_RADIUS//2, self.node1.y + NODE_RADIUS//2
        end_x, end_y = self.node2.x + NODE_RADIUS//2, self.node2.y + NODE_RADIUS//2

        # Move end x and end y back along the line to place the arrows better
        # end_x, end_y = self._adjust_line_end(end_x, end_y)

        return (start_x, start_y), (end_x, end_y)

    def draw(self, screen: pygame.Surface) -> None:

        pygame.draw.aaline(
            screen,
            Colors.BLACK,
            start_pos=self.start_pos,
            end_pos=self.end_pos
        )

        if self.show_arrows:
            self.draw_arrow(screen)
