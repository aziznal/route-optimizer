
from typing import Tuple

from BaseClasses.Arc import Arc


from PygameSettings import *
import pygame


import numpy as np


class Street(Arc):

    def __init__(
        self, *args,
        show_arrows: bool = True,
        color: Colors,
        width: int
    ) -> None:
        super().__init__(*args)

        self.color = color
        self.width = width

        self.show_arrows = show_arrows

        self.arrow_surface = self.create_arrow_surface()
        self.arrow_xy = self._adjust_line_end(*self.node2.rect.center)

        self.start_pos, self.end_pos = self._get_line_start_and_end()

    def create_arrow_surface(self) -> pygame.Surface:

        arrow_surface = pygame.image.load(Resources.ARROW_IMAGE_PATH)
        arrow_surface = pygame.transform.scale(arrow_surface, (10, 10))

        rotation_angle = self.angle

        arrow_surface = pygame.transform.rotate(arrow_surface, rotation_angle)

        return arrow_surface

    def draw_arrow(self, screen: pygame.Surface) -> None:

        screen.blit(self.arrow_surface, self.arrow_xy)

    def _adjust_line_end(self, end_x: int, end_y: int) -> Tuple[int, int]:

        d = NODE_RADIUS * 1.3

        alpha = (360 - self.angle) % 90
        beta = 90 - alpha
        
        # print(f"alpha: {alpha}\tbeta: {beta}\n")

        dx = np.sin(np.deg2rad(beta)) * d
        dy = np.sin(np.deg2rad(alpha)) * d

        quadrant = self.get_quadrant_of_node2()

        # print(f"angle: {self.angle}\tquadrant: {quadrant}\n\n")

        if quadrant == 1:
            end_x -= dx
            end_y += dy

        elif quadrant == 2:
            end_x += dx
            end_y += dy

        elif quadrant == 3:
            end_x += dx
            end_y -= dy

        elif quadrant == 4:
            end_x -= dx
            end_y -= dy

        return end_x, end_y

    def _get_line_start_and_end(self) -> Tuple[Tuple[int, int], Tuple[int, int]]:

        # start_x, start_y = self.node1.x + NODE_RADIUS//2, self.node1.y + NODE_RADIUS//2
        # end_x, end_y = self.node2.x + NODE_RADIUS//2, self.node2.y + NODE_RADIUS//2

        start_x, start_y = self.node1.x, self.node1.y
        end_x, end_y = self.node2.x, self.node2.y

        # Move end x and end y back along the line to place the arrows better
        # end_x, end_y = self._adjust_line_end(end_x, end_y)

        return (start_x, start_y), (end_x, end_y)

    def draw(self, screen: pygame.Surface) -> None:

        if self.width == 1:
            pygame.draw.aaline(
                screen,
                self.color,
                start_pos=self.start_pos,
                end_pos=self.end_pos
            )
        else:
            pygame.draw.line(
                screen,
                self.color,
                start_pos=self.start_pos,
                end_pos=self.end_pos,
                width=self.width
            )
