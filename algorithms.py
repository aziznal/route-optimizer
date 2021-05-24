
from Street import Street
from Building import Building
from typing import Union, List, Dict

from City import City
from BaseClasses.Node import Node
from BaseClasses.Arc import Arc

import numpy as np


class Algorithm:

    def __init__(self, nodes: List[Node]) -> None:
        self.nodes = nodes

    
    def find_shortest_path(self, source_node: Node, destination_node: Node) -> List[Node]:
        raise NotImplementedError("Method has not been implemented yet.")



class A_star(Algorithm):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def find_shortest_path(self, source_node: Node, destination_node: Node) -> List[Node]:

        self.source_node = source_node
        self.destination_node = destination_node

        # To help with returning the result of the algorithm (TODO: give better explanation)
        self.prev_node: Dict[Node, Node] = {}
        
        self.open_set: List[Node] = []
        # self.unvisited: List[Node] = [node for node in self.nodes if node != self.source_node]

        # Starting node is present in visited list from the start
        self.open_set.append(self.source_node)
        self.current_node = self.source_node

        # No node comes before the starting node, so set it to none
        self.prev_node[self.source_node] = None

        
        # To save distance from source node to current node:
        self.g_scores = self.get_initial_distances()
        
        self.f_scores = self.get_initial_distances()
        self.f_scores[self.source_node] = self.h_cost(self.source_node)


        while True:

            if self.check_satisfies_exit_condition():
                break

            self.open_set.remove(self.current_node)

            for neighbor in self.current_node.connections:

                neighbor_new_g_score = self.g_scores[self.current_node] + A_star.get_distance_between_nodes(self.current_node, neighbor)

                if neighbor_new_g_score < self.g_scores[neighbor]:

                    self.prev_node[neighbor] = self.current_node

                    self.g_scores[neighbor] = neighbor_new_g_score
                    self.f_scores[neighbor] = self.g_scores[neighbor] + self.h_cost(neighbor)

                    if neighbor not in self.open_set:
                        self.open_set.append(neighbor)

            self.current_node = self.get_node_with_lowest_f_score()


        return self.construct_path()
    
    def f_cost(self, node):
        pass

    def g_cost(self):
        """
        length of path from starting node to current node
        """
        pass

    def h_cost(self, node: Node):
        """
        length of 'direct' path from given node to destination node
        """
        return A_star.get_distance_between_nodes(node, self.destination_node, connected=False)


    def get_initial_distances(self) -> Dict[Node, Union[float, int]]:
        """
        Returns a map of distances from initial node, all set to
        infinity except for the source node
        """
        distances = { node: np.inf for node in self.nodes }

        # Source Node has distance 0 with itself
        distances[self.source_node] = 0
        
        return distances


    def get_node_with_lowest_f_score(self):
        """
        Return the current node's neighboring node with the least f_cost
        """

        open_set_f_scores = { node: self.f_scores[node] for node in self.open_set }

        return min(open_set_f_scores, key=open_set_f_scores.get)


    def check_satisfies_exit_condition(self):

        return any([

            self.current_node == self.destination_node,

            len(self.open_set) == 0

        ])

    @staticmethod
    def get_distance_between_nodes(node1: Node, node2: Node, connected=True) -> float:

        if connected:
            assert node2 in node1.connections

        return Arc(node1, node2).calculate_length()


    def construct_path(self):

        shortest_path: List[Node] = []
        u = self.destination_node

        while u is not None:
            shortest_path.append(u)
            u = self.prev_node[u]

        shortest_path.reverse()

        return shortest_path
        



class Dijkstra(Algorithm):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)


    def find_shortest_path(self, source_node: Node, destination_node: Node) -> List[Node]:
        """
        Applies Dijkstra's shortest path algorithm and tries to find
        a path between source and destination, if any exists.

        Returns an ordered list of nodes that will be traversed starting with the source node
        and ending with the destination node

        Algorithm was implemented from https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm
        """
        
        self.source_node = source_node
        self.destination_node = destination_node

        # <Node, Node> Dict that points to the node that leads to current node with the shortest path
        self.prev_node: Dict[Node, Union[Node, None]] = {}

        ### Step 1
        self.unvisited_nodes = [node for node in self.nodes]
        self.visited_nodes: List[Node] = []

        ### Step 2 - Distance from source to all others is set to Infinity initially
        self.distances = self.get_initial_distances(source_node)
        self.current_node = source_node

        # We don't care about nodes that lead back to source
        self.prev_node[source_node] = None

        # Loop from step 3 till condition is satisfied in step 5
        while 1:
            
            ### Step 3
            current_node_tentative_distances = self.get_current_node_tentative_distances()

            for node, distance in current_node_tentative_distances.items():
                if distance < self.distances[node]:
                    self.distances[node] = distance
                    self.prev_node[node] = self.current_node


            ### Step 4
            self.unvisited_nodes.remove(self.current_node)
            self.visited_nodes.append(self.current_node)

            ### Check if Step 5    
            if self.check_exit_conditions():
                break
            
            ### Otherwise, Step 6
            # Get node with least tentative distance and set it as current node
            print(f"Prev. Node: {self.current_node}")
            self.current_node = self.get_unvisited_node_with_least_tentative_distance()
            print(f"Current. Node: {self.current_node}", end="\n\n")

        # [print(f"{key}: {val}") for key, val in self.distances.items()]

        print("\n\nVisited Nodes:")
        [print(node) for node in self.visited_nodes]
        
        return self.return_shortest_path()


    
    def get_initial_distances(self, source_node) -> Dict[Node, Union[float, int]]:
        """
        Returns a map of distances from initial node, all set to
        infinity except for the source node
        """
        distances = { node: np.inf for node in self.nodes }

        # Source Node has distance 0 with itself
        distances[source_node] = 0
        
        return distances

    def get_current_node_tentative_distances(self) -> Dict[Node, Union[float, int]]:

        distances: Dict[Node, Union[float, int]] = {}

        for neighbor_node in self.current_node.connections:
            distance_to_neighbor = self.get_distance_between_nodes(self.current_node, neighbor_node)

            # Add distance from source node to current node as well. This is what makes it 'Tentative'
            distances[neighbor_node] = distance_to_neighbor + self.distances[self.current_node]

        return distances

    def get_distance_between_nodes(self, node1: Node, node2: Node) -> float:

        assert node2 in node1.connections

        return Arc(node1, node2).calculate_length()

    def check_exit_conditions(self) -> bool:
        
        # Either destination node has been visited
        if self.destination_node in self.visited_nodes:
            # print("Reached Destination Node")
            return True

        # Or the smallest distance between source and any unvisited node is Infinity (i.e unreacheable)
        # NOTE: This condition's code is untested
        unvisited_nodes_dict = { node: self.distances[node] for node in self.unvisited_nodes }
        current_min_distance = min(unvisited_nodes_dict, key=unvisited_nodes_dict.get)

        if current_min_distance == np.inf:
            print("No more nodes are reacheable")
            return True

        return False

    def get_unvisited_node_with_least_tentative_distance(self) -> Node:

        # Subset dict of all distances for only unvisited nodes
        unvisited_nodes_dict = { node: self.distances[node] for node in self.unvisited_nodes }

        return min(unvisited_nodes_dict, key=unvisited_nodes_dict.get)

    def return_shortest_path(self):
        # shortest_path: List[Node] = []

        # if self.destination_node not in self.visited_nodes:
        #     return []

        # current_node = self.source_node
        # shortest_path.append(current_node)

        # next_node = None

        # while next_node != self.destination_node:
        #     next_node = self.get_closest_connected_node(current_node)
        #     shortest_path.append(next_node)
        #     current_node = next_node

        # return shortest_path

        shortest_path: List[Node] = []
        u = self.destination_node

        while u is not None:
            shortest_path.append(u)
            u = self.prev_node[u]

        shortest_path.reverse()

        return shortest_path



    def get_closest_connected_node(self, neighbor_node: Node) -> Node:
        dict_subset = { node: self.distances[node] for node in neighbor_node.connections }
        return min( dict_subset, key=dict_subset.get )


class Johnson(Algorithm):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)


class TravelingSalesman(Algorithm):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)


    def find_shortest_path(self, starting_node: Node, nodes: List[Node]) -> List[Node]:
        pass

