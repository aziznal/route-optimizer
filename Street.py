

from BaseClasses.Arc import Arc


from PygameSettings import *
import pygame


import numpy as np



class Street(Arc):

    def __init__(self, *args, show_arrows=True):
        super().__init__(*args)

        self.show_arrows = show_arrows

        self.arrow_surface = self.create_arrow_surface()


    def create_arrow_surface(self):
        
        # TODO: replace this f**kery with a simple image of an arrow instead

        arrow_surface = pygame.Surface((20, 20), pygame.SRCALPHA)
        arrow_surface.fill((255, 255, 255))


        x, y = self.node2.x, self.node2.y

        norm_x, norm_y = x * 20 / SCREEN_WIDTH, y * 20 / SCREEN_HEIGHT
        
        scale = 10


        rotation_angle = self.angle
        rotation_coef = scale * (2**0.5 / 2)

        print(f"Rotation Angle: {rotation_angle}")

        points = [
            
            (norm_x - rotation_coef, norm_y + rotation_coef),
            (norm_x, norm_y),
            (norm_x - rotation_coef, norm_y - rotation_coef)

        ]

        # An arrow is just a triangle. That's easy enough to draw
        pygame.draw.polygon(arrow_surface, Colors.BLUE, points)
        arrow_surface = pygame.transform.rotate(arrow_surface, rotation_angle)

        return arrow_surface


    def draw_arrow(self, screen):
        screen.blit(self.arrow_surface, (self.node2.x, self.node2.y))


    def draw(self, screen: pygame.Surface):

        pygame.draw.line(
            screen,
            Colors.BLACK,
            start_pos=(self.node1.x + NODE_RADIUS//2, self.node1.y + NODE_RADIUS//2),
            end_pos=(self.node2.x + NODE_RADIUS//2, self.node2.y + NODE_RADIUS//2),
            width=2
        )

        if self.show_arrows:
            self.draw_arrow(screen)
