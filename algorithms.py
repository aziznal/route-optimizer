from typing import Union, List, Dict

import numpy as np

from BaseClasses.Node import Node
from BaseClasses.Arc import Arc


class Algorithm:
    def __init__(self, nodes: List[Node]) -> None:
        self.nodes = nodes

    def find_shortest_path(
        self, source_node: Node, destination_node: Node
    ) -> List[Node]:
        raise NotImplementedError("Method has not been implemented yet.")

    @staticmethod
    def get_direct_distance_between_nodes(node1: Node, node2: Node) -> float:
        """
        Returns distance between given nodes as a straight line.
        """

        return Arc(node1, node2).calculate_length()


class A_star(Algorithm):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def find_shortest_path(
        self, source_node: Node, destination_node: Node
    ) -> List[Node]:

        print("\nApplying A* Algorithm ...\n")

        self.source_node = source_node
        self.destination_node = destination_node

        # This dict is where the final shortest path is saved.
        # It maps current node to the node that should preceed it in a shortest path.
        self.prev_node: Dict[Node, Node] = {}

        self.open_set: List[Node] = []

        # source node is present in visited list from the beginning
        self.open_set.append(self.source_node)
        self.current_node = self.source_node

        # No node comes before the source node
        self.prev_node[self.source_node] = None

        # This dict saves distances from source node to current node
        # It maps node to distance
        self.g_scores = self.get_initial_distances()

        # This dict stores result of objective function
        self.f_scores = self.get_initial_distances()
        self.f_scores[self.source_node] = self.h_cost(self.source_node)

        while True:
            if self.check_satisfies_exit_condition():
                break

            self.open_set.remove(self.current_node)

            for neighbor in self.current_node.connections:
                neighbor_new_g_score = self.g_scores[
                    self.current_node
                ] + Algorithm.get_direct_distance_between_nodes(
                    self.current_node, neighbor
                )

                if neighbor_new_g_score < self.g_scores[neighbor]:
                    self.prev_node[neighbor] = self.current_node

                    self.g_scores[neighbor] = neighbor_new_g_score
                    self.f_scores[neighbor] = self.g_scores[neighbor] + self.h_cost(
                        neighbor
                    )

                    if neighbor not in self.open_set:
                        self.open_set.append(neighbor)

            self.current_node = self.get_node_with_lowest_f_score()

        return self.construct_path()

    def h_cost(self, node: Node) -> float:
        """
        length of 'direct' path from given node to destination node
        """
        return Algorithm.get_direct_distance_between_nodes(node, self.destination_node)

    def get_initial_distances(self) -> Dict[Node, Union[float, int]]:
        """
        Returns a map of distances from initial node, all set to
        infinity except for the source node
        """
        distances = {node: np.inf for node in self.nodes}

        # Source Node has distance 0 with itself
        distances[self.source_node] = 0

        return distances

    def get_node_with_lowest_f_score(self) -> Node:
        """
        Return the current node's neighboring node with the least f_cost
        """

        f_scores_of_nodes_in_open_setopen_set = {
            node: self.f_scores[node] for node in self.open_set
        }

        return min(
            f_scores_of_nodes_in_open_setopen_set,
            key=f_scores_of_nodes_in_open_setopen_set.get,
        )

    def check_satisfies_exit_condition(self) -> bool:

        return any(
            [self.current_node == self.destination_node, len(self.open_set) == 0]
        )

    def construct_path(self) -> List[Node]:

        shortest_path: List[Node] = []
        current_node = self.destination_node

        while current_node is not None:
            shortest_path.append(current_node)
            current_node = self.prev_node[current_node]

        shortest_path.reverse()

        return shortest_path


class Dijkstra(Algorithm):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def find_shortest_path(
        self, source_node: Node, destination_node: Node
    ) -> List[Node]:
        """
        Applies Dijkstra's shortest path algorithm and tries to find
        a path between source and destination, if any exists.

        Returns an ordered list of nodes that will be traversed starting with the source node
        and ending with the destination node

        Algorithm was implemented from https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm
        """

        print("\nApplying Dijkstra's Algorithm ...\n")

        self.source_node = source_node
        self.destination_node = destination_node

        # <Node, Node> Dict that points to the node that
        #  leads to current node with the shortest path
        self.prev_node: Dict[Node, Union[Node, None]] = {}

        ### Step 1
        self.unvisited_nodes = [node for node in self.nodes]
        self.visited_nodes: List[Node] = []

        ### Step 2 - Distance from source to all others is set to Infinity initially
        self.distances = self.get_initial_distances(source_node)
        self.current_node = source_node

        # no node comes before source
        self.prev_node[source_node] = None

        # Loop from step 3 till condition is satisfied in step 5
        while 1:
            ### Step 3
            current_node_tentative_distances = (
                self.get_current_node_tentative_distances()
            )

            for node, distance in current_node_tentative_distances.items():
                if distance < self.distances[node]:
                    self.distances[node] = distance
                    self.prev_node[node] = self.current_node

            ### Step 4
            self.unvisited_nodes.remove(self.current_node)
            self.visited_nodes.append(self.current_node)

            ### if Step 5, then algorithm is done
            if self.check_any_exit_conditions_satisfy():
                break

            ### Otherwise, Step 6
            self.current_node = self.get_unvisited_node_with_least_tentative_distance()

        return self.return_shortest_path()

    def get_initial_distances(self, source_node) -> Dict[Node, Union[float, int]]:
        """
        Returns a map of distances from initial node, all set to
        infinity except for the source node
        """
        distances = {node: np.inf for node in self.nodes}

        # Source Node has distance 0 with itself
        distances[source_node] = 0

        return distances

    def get_current_node_tentative_distances(self) -> Dict[Node, Union[float, int]]:
        """
        Tentative distance is the length of path starting at source node and ending at current node
        """

        distances: Dict[Node, Union[float, int]] = {}

        for neighbor_node in self.current_node.connections:
            distance_to_neighbor = Algorithm.get_direct_distance_between_nodes(
                self.current_node, neighbor_node
            )

            # Add distance from source node to current node as well. This is what makes it 'Tentative'
            distances[neighbor_node] = (
                distance_to_neighbor + self.distances[self.current_node]
            )

        return distances

    def check_any_exit_conditions_satisfy(self) -> bool:

        # Either destination node has been visited
        if self.destination_node in self.visited_nodes:
            # print("Reached Destination Node")
            return True

        # Or the smallest distance between source and any unvisited node is Infinity (i.e unreacheable)
        # NOTE: This condition's code is untested
        unvisited_nodes_dict = {
            node: self.distances[node] for node in self.unvisited_nodes
        }
        current_min_distance = min(unvisited_nodes_dict, key=unvisited_nodes_dict.get)

        if current_min_distance == np.inf:
            print("No more nodes are reacheable")
            return True

        return False

    def get_unvisited_node_with_least_tentative_distance(self) -> Node:

        # Subset dict of all distances for only unvisited nodes
        distances_of_unvisited_nodes = {
            node: self.distances[node] for node in self.unvisited_nodes
        }

        return min(distances_of_unvisited_nodes, key=distances_of_unvisited_nodes.get)

    def get_closest_connected_node(self, neighbor_node: Node) -> Node:

        distances_of_connected_nodes = {
            node: self.distances[node] for node in neighbor_node.connections
        }

        return min(distances_of_connected_nodes, key=distances_of_connected_nodes.get)

    def return_shortest_path(self) -> List[Node]:

        shortest_path: List[Node] = []
        current_node = self.destination_node

        while current_node is not None:
            shortest_path.append(current_node)
            current_node = self.prev_node[current_node]

        shortest_path.reverse()

        return shortest_path


class Johnson(Algorithm):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)


class TravelingSalesman(Algorithm):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def find_shortest_path(self, starting_node: Node, nodes: List[Node]) -> List[Node]:
        pass
