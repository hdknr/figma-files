from .node import Node
from .primitives import Paint, Rectangle, DevStatus
from typing import Optional, List, Literal


class Section(Node):
    sectionContentsHidden: Optional[bool] = False
    devStatus = Optional[DevStatus] = None
    fills: Optional[List[Paint]] = []
    strokes: Optional[List[Paint]] = []
    strokeAlign: Optional[Literal["INSIDE", "OUTSIDE", "CENTER"]] = None
    absoluteBoundingBox: Optional[Rectangle] = None
    absoluteRenderBounds: Optional[Rectangle] = None
