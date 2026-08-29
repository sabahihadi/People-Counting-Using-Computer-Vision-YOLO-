"""
fence.py

Virtual Fence utilities.
"""

from shapely.geometry import Point
from shapely.geometry import Polygon


class VirtualFence:
    """
    Represents the virtual fence.

    The person's FOOT POINT is used to determine
    whether he/she is inside the fence.
    """

    def __init__(self, top_left, bottom_right):

        x1, y1 = top_left
        x2, y2 = bottom_right

        self.polygon = Polygon(
            [
                (x1, y1),
                (x2, y1),
                (x2, y2),
                (x1, y2)
            ]
        )

    def foot_point(self, bbox):
        """
        Compute the foot point of a person.

        Parameters
        ----------
        bbox : tuple
            (x1,y1,x2,y2)

        Returns
        -------
        tuple
            (foot_x, foot_y)
        """

        x1, y1, x2, y2 = bbox

        foot_x = (x1 + x2) // 2

        foot_y = y2

        return (foot_x, foot_y)

    def is_inside(self, bbox):
        """
        Check whether the foot point is inside.

        Returns
        -------
        bool
        """

        point = Point(self.foot_point(bbox))

        return self.polygon.contains(point)