"""

A City is a graph made of Buildings (nodes) which are connected by Streets (arcs)

"""

from typing import Callable, List, Tuple, Union, Dict
import traceback

import pygame

from PygameSettings import *

from Building import Building
from Street import Street


class City:

    def __init__(
        self,
        buildings: List[Building],
        on_change: Callable[[], None],
        create_streets_between_buildings: bool = True
    ) -> None:

        self.buildings = buildings
        self.streets: List[Street] = []
        self.on_change = on_change

        if create_streets_between_buildings:
            self.create_streets_between_buildings()

    def draw(self, screen: pygame.Surface) -> None:

        for building in self.buildings:
            building.draw(screen)

        for street in self.streets:
            street.draw(screen)

    def get_building_at_pos(self, pos: Tuple[int, int]) -> Union[Building, None]:
        """
        Returns building at given position, if any exists. Otherwise returns None
        """
        for building in self.buildings:

            if pos[0] - NODE_RADIUS < building.x < pos[0] + NODE_RADIUS:
                if pos[1] - NODE_RADIUS < building.y < pos[1] + NODE_RADIUS:
                    return building

    def create_building(self, pos: Tuple[int, int]) -> None:
        """
        Creates a building at the given position
        """

        new_building_pos = (pos[0] - NODE_RADIUS//2, pos[1] - NODE_RADIUS//2)

        new_building = Building(*new_building_pos, connections=[])

        self.buildings.append(new_building)

        self.on_change()

    def _remove_connections(self, building_to_remove: Building) -> None:
        """
        Removes all connections to / from given building
        """

        # Remove connections FROM building_to_delete
        for connected_building in building_to_remove.connections:
            try:
                # BUG: sometimes getting error ('list.remove(x): x not in list')
                connected_building.connections.remove(building_to_remove)

            except ValueError:
                traceback.print_exc()

        # Remove connections TO building_to_delete
        for potentailly_connected_building in self.buildings:
            try:
                if building_to_remove in potentailly_connected_building.connections:
                    potentailly_connected_building.connections.remove(
                        building_to_remove)

            except ValueError:
                traceback.print_exc()

    def remove_building(self, pos: Tuple[int, int]) -> None:
        """
        Removes building at given position (if any exists) and cuts off all connections
        to / from it
        """

        building_to_remove = self.get_building_at_pos(pos)

        if building_to_remove is None:
            print(f"No building to remove at {pos}")
            return

        self._remove_connections(building_to_remove)

        self.buildings.remove(building_to_remove)

        # REFACTOR
        # IMPORTANT: This may cause performance issues in large maps

        # This resets the streets list after any buildings are removed in order to keep from having 'floating' streets
        # for _ in range(len(self.streets)):
        #     del self.streets[0]

        self.streets.clear()

        self.create_streets_between_buildings()

        self.on_change()

    def connect_buildings(
        self,
        pos1: Tuple[int, int],
        pos2: Tuple[int, int],
        bidirectional=False,
        verbose=True
    ) -> None:
        """
        Create a connection between nodes at pos1 and pos2
        """
        building1 = self.get_building_at_pos(pos1)
        building2 = self.get_building_at_pos(pos2)

        if building1 is None or building2 is None:
            print(
                f"Couldn't find one of the buildings: {building1}, {building2}")
            return

        # TODO: check whether building are already connected before doing this step

        # Connect first to second
        building1.connections.append(building2)
        self.draw_street(building1, building2)

        if bidirectional:
            # Connect second to first as well
            building2.connections.append(building1)
            self.draw_street(building1, building2)

        self.on_change()

        if verbose:
            print(f"Connected two buildings together at {pos1} and {pos2}")

            print(f"First building connections: {building1.connections}")
            print(f"Second building connections: {building2.connections}")

    def create_streets_between_buildings(self) -> None:
        """
        Creates directed Arcs between all connected buildings
        """

        # BUG: Bi-directional connections aren't being drawn until the map is reloaded

        for building in self.buildings:

            for connected_building in building.connections:

                self.streets.append(
                    Street(
                        building, connected_building, show_arrows=True, color=Colors.BLACK, width=1
                    )
                )

    def draw_street(
            self,
            building1: Building,
            building2: Building,
            color: Colors = Colors.BLACK,
            width: int = 1
    ) -> None:
        """
        Creates an Arc between the two given buildings
        """

        new_street = Street(building1, building2,
                            show_arrows=True, color=color, width=width)

        self.streets.append(new_street)

        self.on_change()

    def color_paths(self, nodes: List[Building]) -> None:
        """
        Colors a path starting from first node until last node in the
        given list
        """
        for node1, node2 in zip(nodes[:-1], nodes[1:]):
            self.draw_street(node1, node2, Colors.YELLOW, width=3)

    @staticmethod
    def make_buildings_from_saved_file(
        building_data: Dict[str, List]
    ) -> List[Building]:

        buildings: List[Building] = []

        # First, create buildings without their connections
        for building_data in building_data["data"]:
            buildings.append(
                Building(**building_data)
            )

        # then connect them all
        temp_city = City(
            buildings,
            on_change=lambda: None,
            create_streets_between_buildings=False
        )

        def get_building_at_pos(x, y):
            return temp_city.get_building_at_pos((x, y))

        # Convert each building's connections from coordinates to Building objects
        for building in buildings:
            building.connections = [
                get_building_at_pos(*coords) for coords in building.connections
            ]

        return buildings
