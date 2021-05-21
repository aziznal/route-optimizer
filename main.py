from Building import Building
from MapMaker import MapMaker

from City import City

from BuildingManager import BuildingManager


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


def run(building_manager, *draw_functions) -> None:

    screen = get_screen()

    while 1:
        handle_events(
            on_mouse_left_click=building_manager.make_building,
            on_mouse_right_click=building_manager.connect_buildings,
            on_mouse_middle_click=building_manager.remove_building,
            on_mouse_scroll=lambda dir, pos: print(f"scroll {dir}"),
        )

        screen.fill(Colors.WHITE)

        # Call all draw methods
        for method in draw_functions:
            method(screen)

        pygame.display.flip()


if __name__ == '__main__':

    buildings = utils.load_map()

    building_manager = BuildingManager(
        buildings,
        streets,
        lambda: utils.save_changes(buildings)
    )
    building_manager.create_streets_between_buildings()

    img = pygame.image.load(Resources.KONYA_MAP_PATH)
    mapmaker = MapMaker(map_image=img)

    konya = City(buildings=buildings, streets=streets)

    run(

        building_manager,

        # Drawing methods below here

        # mapmaker.draw,
        konya.draw

    )
