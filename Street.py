

from BaseClasses.Arc import Arc


from PygameSettings import *
import pygame




class Street(Arc):

    def __init__(self, *args, show_arrows=True):
        super().__init__(*args)
        self.show_arrows = show_arrows

    def draw_arrow(self, screen):
        """
        arrows will be drawn 
        """
        
        points = [
            (self.node2.x, self.node2.y),
            (self.node2.x + 10, self.node2.y + 10),
            (self.node2.x - 10, self.node2.y - 10)
        ]

        # An arrow is just a triangle. That's easy enough to draw
        pygame.draw.polygon(screen, Colors.BLUE, points)


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
