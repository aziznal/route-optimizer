import pygame
import utils
from PygameSettings import *
from EventHandler import handle_events
from MapMaker import MapMaker
from City import City
from algorithms import A_star, Dijkstra


# BUG: Bi-directional connections are not visualized until the map is reloaded


def get_screen() -> pygame.Surface:
    return pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


def run(city: City, draw_functions) -> None:
    screen = get_screen()

    while 1:
        handle_events(city)

        screen.fill(Colors.WHITE)

        # Call all draw methods
        for method in draw_functions:
            method(screen)

        pygame.display.flip()


if __name__ == "__main__":
    # path_to_map_file = "./assets/konya-map.json"
    path_to_map_file = "default-map.json"

    buildings_data = utils.load_map(to_filename=path_to_map_file)
    buildings = City.make_buildings_from_saved_file(buildings_data)

    konya = City(
        buildings=buildings,
        on_change=lambda: utils.save_changes(buildings, map_name=path_to_map_file),
    )

    # solution = Dijkstra(konya.buildings).find_shortest_path(
    #     source_node=konya.get_building_at_pos((518, 45)),
    #     destination_node=konya.get_building_at_pos((645, 772)),
    # )

    solution = A_star(konya.buildings).find_shortest_path(
        source_node=konya.get_building_at_pos((575, 1334)),
        destination_node=konya.get_building_at_pos((103, 78)),
    )

    konya.color_paths(solution)

    map_image = pygame.image.load(Resources.KONYA_MAP_IMAGE_PATH)
    mapmaker = MapMaker(map_image=map_image)

    run(
        city=konya,
        draw_functions=[
            # mapmaker.draw,
            konya.draw
        ],
    )
