
import traceback

from PygameSettings import *


from Building import Building
from Street import Street


# REFACTOR: tidy up before you get further in the project

class BuildingManager:
    def __init__(self, buildings_list, streets, on_change):

        self.buildings = buildings_list
        self.streets = streets

        self.on_change = on_change



    def get_building_at_pos(self, pos):
        """
        Returns building at given position, if any exists. Otherwise returns None
        """
        for building in self.buildings:

            if pos[0] - NODE_RADIUS < building.x < pos[0] + NODE_RADIUS:
                if pos[1] - NODE_RADIUS < building.y < pos[1] + NODE_RADIUS:
                    return building



    def make_building(self, pos):

        new_building_pos = (pos[0] - NODE_RADIUS//2, pos[1] - NODE_RADIUS//2)

        new_building = Building(*new_building_pos, connections=[])

        self.buildings.append(new_building)

        self.on_change()



    def _remove_connections(self, building_to_remove):

        # Remove connections FROM building_to_delete
        for connected_building in building_to_remove.connections:
            try:
                connected_building.connections.remove(building_to_remove)

            except ValueError:
                traceback.print_exc()

        # Remove connections TO building_to_delete
        for potentailly_connected_building in self.buildings:
            try:
                if building_to_remove in potentailly_connected_building.connections:
                    potentailly_connected_building.connections.remove(building_to_remove)

            except ValueError:
                traceback.print_exc()


                

    def remove_building(self, pos):

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



    def connect_buildings(self, pos1, pos2, bidirectional=False, verbose=True):
        """
        Create a one-way or two-way connection between nodes at pos1 and pos2
        """
        building1 = self.get_building_at_pos(pos1)
        building2 = self.get_building_at_pos(pos2)

        if building1 is None or building2 is None:
            print(f"Couldn't find one of the buildings: {building1}, {building2}")
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



    def create_streets_between_buildings(self):
        
        # BUG: Bi-directional connections aren't being drawn until the map is reloaded

        for building in self.buildings:

            for connected_building in building.connections:

                self.streets.append(
                    Street(
                        building, connected_building
                    )
                )




    def draw_street(self, building1, building2):
        
        new_street = Street(building1, building2)

        self.streets.append(new_street)

        self.on_change()

