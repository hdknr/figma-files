from .node import Node
from ..base.property_types import (
    ExportSetting,
    BlendMode,
    LayoutConstraint,
    Rectangle,
    Vector as PrimitiveVector,
    Transform,
    Paint,
    Annotation,
    EasingType,
)
from typing import Optional, List, Literal


class Vector(Node):
    locked: Optional[bool] = False
    exportSettings: Optional[list[ExportSetting]] = []
    blendMode: BlendMode
    preserveRatio: Optional[bool] = False
    layoutAlign: Optional[Literal["INHERIT", "STRETCH", "MIN", "CENTER", "MAX", "STRETCH"]] = None

    layoutGrow: Optional[float] = 0
    constraints: Optional[LayoutConstraint] = None
    #
    opacity: Optional[float] = 1
    absoluteBoundingBox: Optional[Rectangle] = None
    # Bounding box of the node in absolute space coordinates

    absoluteRenderBounds: Optional[Rectangle] = None
    # The actual bounds of a node accounting for drop shadows, thick strokes,
    # and anything else that may fall outside the node's regular bounding box defined in x, y, width, and height.
    # The x and y inside this property represent the absolute position of the node on the page.
    # This value will be null if the node is invisible.

    transitionNodeID: Optional[str] = None
    transitionDuration: Optional[float] = None
    transitionEasing: Optional[EasingType] = None
    #
    size: Optional[PrimitiveVector] = None
    relativeTransform: Optional[Transform] = None
    #
    isMask: Optional[bool] = False

    # fills: An array of fill paints applied to the node
    fills: Optional[List[Paint]] = []

    fillGeometry: Optional[List[Paint]] = []
    #
    fillOverrideTable: Optional[dict] = None
    strokes: Optional[List[Paint]] = []
    strokeWeight: Optional[float] = None
    strokeCap: Optional[
        Literal[
            "NONE",
            "ROUND",
            "SQUARE",
            "LINE_ARROW",
            "TRIANGLE_ARROW",
            "DIAMOND_FILLED",
            "CIRCLE_FILLED",
            "TRIANGLE_FILLED",
            "WASHI_TAPE_1",
            "WASHI_TAPE_2",
            "WASHI_TAPE_3",
            "WASHI_TAPE_4",
            "WASHI_TAPE_5",
            "WASHI_TAPE_6",
        ]
    ] = "NONE"
    strokeJoin: Optional[str] = "MITER"
    strokeDashes: Optional[List[float]] = []
    strokeMiterAngle: Optional[float] = 28.96
    strokeGeometry: Optional[List[Paint]] = []
    strokeAlign: Optional[Literal["INSIDE", "OUTSIDE", "CENTER"]] = None
    styles: Optional[dict] = None
    annotations: Optional[List[Annotation]] = []
