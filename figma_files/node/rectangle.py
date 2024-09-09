from .vector import Vector
from typing import Optional, List


class Rectangle(Vector):
    cornerRadius: Optional[float] = None
    rectangleCornerRadii: Optional[List[float]] = []
    cornerSmoothing: Optional[float] = None
