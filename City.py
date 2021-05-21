"""

A City is a graph made of Buildings (nodes) which are connected by Streets (arcs)

"""

import traceback

from typing import Callable, List, Tuple, Union

import pygame

from PygameSettings import *

from Building import Building
from Street import Street


class City:

    def __init__(self, buildings: List[Building], streets: List[Street], on_change: Callable) -> None:

        self.buildings = buildings
        self.streets = streets
        self.on_change = on_change

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

    def connect_buildings(self, pos1: Tuple[int, int], pos2: Tuple[int, int], bidirectional=False, verbose=True) -> None:
        """
        Create a one-way or two-way connection between nodes at pos1 and pos2
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
                        building, connected_building
                    )
                )

    def draw_street(self, building1: Building, building2: Building) -> None:
        """
        Creates an Arc between the two given buildings
        """

        new_street = Street(building1, building2)

        self.streets.append(new_street)

        self.on_change()
