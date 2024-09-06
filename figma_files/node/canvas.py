from .node import Node
from ..base.primitives import Color, FlowStartingPoint, ExportSetting, Measurement
from typing import Optional


class Canvas(Node):
    backgroundColor: Color
    prototypeStartNodeID: Optional[str] = None
    flowStartingPoints: Optional[list[FlowStartingPoint]] = None
    exportSettings = Optional[list[ExportSetting]] = []
    measurements = Optional[list[Measurement]] = []
