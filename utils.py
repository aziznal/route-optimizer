from typing import List
import pygame

pygame.init()
pygame.font.init()



def create_text(text, font_size, color, bold=False):
    """
    Returns a pygame surface with the desired text in it
    """

    font_obj = pygame.font.SysFont("arial", font_size, bold=bold)

    return font_obj.render(text, True, color)



def confirm_hashes_are_unique(buildings: List):

    hashes = [ hash(building) for building in buildings ]

    if len(set(hashes)) != len(hashes):
        raise KeyError("Found two matching hashes!")
