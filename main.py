from Building import Building
from MapMaker import MapMaker

from City import City


from PygameSettings import *
from EventHandler import handle_events

import utils

import pygame


buildings = []
streets = []


# BUG: Bi-directional connections are not visualized until the map is reloaded
# TODO: Stop pickling maps. Load data and re-instantiate nodes from it instead.


def get_screen() -> pygame.Surface:

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    return screen


def run(city: City, draw_functions) -> None:

    screen = get_screen()

    while 1:
        handle_events(city)

        screen.fill(Colors.WHITE)

        # Call all draw methods
        for method in draw_functions:
            method(screen)

        pygame.display.flip()


if __name__ == '__main__':

    buildings = utils.load_map()

    konya = City(
        buildings=buildings,
        streets=streets,
        on_change=lambda: utils.save_changes(buildings)
    )
    konya.create_streets_between_buildings()

    map_image = pygame.image.load(Resources.KONYA_MAP_IMAGE_PATH)
    mapmaker = MapMaker(map_image=map_image)

    run(

        city=konya,

        draw_functions=[
            # mapmaker.draw,
            konya.draw
        ]

    )
