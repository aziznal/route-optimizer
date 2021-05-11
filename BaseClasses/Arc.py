"""

An Arc is a *directional* connection between two Nodes

"""


class Arc:
    def __init__(self, node1, node2):

        self.node1, self.node2 = node1, node2

        self.length = self.calculate_length()

    
    def calculate_length(self):

        length_squared = (
            (self.node1.x - self.node2.x)**2 + (self.node1.y - self.node2.y)**2
        )

        return length_squared ** 0.5        


