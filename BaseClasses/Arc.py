"""

An Arc is a *directional* connection between two Nodes

"""

from numpy import arctan


class Arc:
    def __init__(self, node1, node2):

        self.node1, self.node2 = node1, node2

        self.slope = self.calculate_slope()

        self.angle = self.calculate_angle()

        self.length = self.calculate_length()

    
    def calculate_length(self):

        length_squared = (
            (self.node1.x - self.node2.x)**2 + (self.node1.y - self.node2.y)**2
        )

        return length_squared ** 0.5        


    def calculate_slope(self):

        x1, x2 = self.node1.x, self.node2.x
        y1, y2 = self.node1.y, self.node2.y

        delta_y = y2 - y1
        delta_x = x2 - x1

        return delta_y / delta_x


    def calculate_angle(self):

        """
        Note: angle is calculated according to positive x-axis
        """

        # Angle formula is the following:
        #   
        #       Angle = arctan(slope)

        return arctan(self.slope)        
