"""

An Arc is a *directional* connection between two Nodes

"""

import numpy as np
from .Node import Node

from typing import Literal, Union

class Arc:
    def __init__(self, node1: Node, node2: Node) -> None:

        self.node1, self.node2 = node1, node2

        self.slope = self.calculate_slope()

        self.angle = self.calculate_angle(in_radians=False)
        self.angle_in_radians = self.calculate_angle(in_radians=True)

        self.length = self.calculate_length()

    
    def calculate_length(self) -> float:
        """
        Returns length of Arc connecting the two nodes
        """

        length_squared = (
            (self.node1.x - self.node2.x)**2 + (self.node1.y - self.node2.y)**2
        )

        return length_squared ** 0.5        


    def calculate_slope(self) -> Union[float]:
        """
        Calculates and retuns slope of line connecting the two nodes
        """

        x1, x2 = self.node1.x, self.node2.x
        y1, y2 = self.node1.y, self.node2.y

        delta_y = y2 - y1
        delta_x = x2 - x1


        if delta_x == 0:
            return np.inf


        return -delta_y / delta_x


    def get_quadrant_of_node2(self) -> Literal[1, 2, 3, 4]:
        """
        Returns quadrant of node2 in reference to node1 based on the unit circle.
        Note: This takes into account the pygame cartesian coordinate system behavior.
        """
        
        # TODO: check behavior of edge cases: x1 == x2 | y1 == y2

        x1, y1, x2, y2 = self.node1.x, self.node1.y, self.node2.x, self.node2.y

        # Left
        if x2 < x1:
            
            # Top
            if y2 < y1:
                return 2

            # Bottom or center
            else:
                return 3

        # Right or center
        else:

            # Top
            if y2 < y1:
                return 1

            # Bottom or center
            else: 
                return 4



    def _adjust_for_quadrant(self, angle_in_radians: float) -> float:

        quadrant = self.get_quadrant_of_node2()

        if quadrant == 2:
            angle_in_radians += 2 * np.pi/2

        elif quadrant == 3:
            angle_in_radians = -angle_in_radians + 3 * np.pi/2

        elif quadrant == 4:
            angle_in_radians += 4 * np.pi/2

        return angle_in_radians

    def calculate_angle(self, in_radians=False) -> float:

        """
        Note: angle is calculated according to positive x-axis
        """

        # Angle formula is the following:
        #   
        #       Angle = arctan(slope)

        angle_in_radians = np.arctan(self.slope)

        angle_in_radians = self._adjust_for_quadrant(angle_in_radians)


        if in_radians:
            
            return angle_in_radians

        else:

            angle_in_degrees = angle_in_radians * 180 / np.pi
            return angle_in_degrees
