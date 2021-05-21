from Building import Building
from MapMaker import MapMaker

from City import City

from BuildingManager import CityManager


from PygameSettings import *
from EventHandler import handle_events

import utils

import pygame


buildings = []
streets = []


# BUG: Bi-directional connections are not visualized until the map is reloaded


def get_screen() -> pygame.Surface:

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    return screen


def run(city: City, *draw_functions) -> None:

    screen = get_screen()

    while 1:
        handle_events(
            on_mouse_left_click=city.create_building,
            on_mouse_right_click=city.connect_buildings,
            on_mouse_middle_click=city.remove_building,
            on_mouse_scroll=lambda dir, pos: print(f"scroll {dir}"),
        )

        screen.fill(Colors.WHITE)

        # Call all draw methods
        for method in draw_functions:
            method(screen)

        pygame.display.flip()


if __name__ == '__main__':

    buildings = utils.load_map()

    img = pygame.image.load(Resources.KONYA_MAP_PATH)
    mapmaker = MapMaker(map_image=img)

    konya = City(
        buildings=buildings,
        streets=streets,
        on_change=lambda: utils.save_changes(buildings)
    )
    konya.create_streets_between_buildings()

    run(

        konya,

        # Drawing methods below here

        # mapmaker.draw,
        konya.draw

    )
