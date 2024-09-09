from .node import Node
from typing import Optional
from ..base.primitives import ExportSetting, Rectangle, Vector, Transform


class Slice(Node):
    exportSettings: Optional[list[ExportSetting]] = []
    absoluteBoundingBox: Optional[Rectangle] = None
    absoluteRenderBounds: Optional[Rectangle] = None
    size: Vector
    relativeTransform: Optional[Transform] = None
