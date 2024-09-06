from .vector import Vector
from typing import Optional, List


class Rectangle(Vector):
    cornerRadius: float
    rectangleCornerRadii: Optional[List[float]] = []
    cornerSmoothing: float
