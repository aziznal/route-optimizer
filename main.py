
from MapMaker import MapMaker
from typing import List

from City import City
from Building import Building
from Street import Street

from BuildingManager import BuildingManager

import pickle

import traceback


import pygame
from pygame.locals import *

from PygameSettings import *
from EventHandler import handle_events


pygame.init()
pygame.font.init()


buildings = []
streets = []


# BUG: all connections between buildings are becoming bidirectional after loading a saved map


def create_text(text, font_size, color, bold=False):

    font_obj = pygame.font.SysFont("arial", font_size, bold=bold)

    return font_obj.render(text, True, color)


def get_screen():

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    return screen




def save_changes(map_name="default-map-buildings.p"):
    
    global buildings

    with open(map_name, "wb") as save_file:
        pickle.dump(buildings, save_file)


def load_map(to_filename="default-map-buildings.p"):

    try:

        with open(to_filename, 'rb') as map_file:
            return pickle.load(map_file)

    except Exception as e:
        print(f"WARNING! Couldn't find file ({to_filename}).")
        traceback.print_exc()
        return []


def run(*draw_functions):

    global building_manager

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


def create_konya():

    buildings = [

        Building(78, 200, connections=[1, 2]),

        Building(135, 300, connections=[0, 2]),

        Building(275, 400, connections=[0, 1]),

        Building(360, 135, connections=[0, 1, 2]),

    ]

    streets = building_manager.create_streets_between_buildings(buildings)

    konya = City(buildings, streets)

    return konya


if __name__ == '__main__':


    buildings = load_map()

    building_manager = BuildingManager(buildings, streets, save_changes)

    building_manager.create_streets_between_buildings()



    img = pygame.image.load("./konya_map.png")

    mapmaker = MapMaker(map_image=img)


    konya = City(buildings=buildings, streets=streets)


    run(
        # mapmaker.draw,
        konya.draw
    )
