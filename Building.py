import pygame


from PygameSettings import *

from BaseClasses.Node import Node

import utils



class Building(Node):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.rect = pygame.Rect(self.x, self.y, NODE_RADIUS, NODE_RADIUS)
        self.text = {"text":f"({self.rect.x}, {self.rect.y})", "font_size":11, "color":Colors.BLACK, "bold":True}

    def draw(self, screen: pygame.Surface) -> None:

        pygame.draw.ellipse(
            screen, Colors.RED, self.rect
        )

        screen.blit(utils.create_text(**self.text), (self.rect.centerx - 20, self.rect.centery - NODE_RADIUS*2))
