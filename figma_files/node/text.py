from .vector import Vector
from .primitives import TypeStyle
from typing import Optional, List, Literal


class Text(Vector):
    characters: str
    styles: TypeStyle
    characterStyleOverrides: Optional[List[float]] = []
    styleOverrideTable: Optional[dict] = None
    lineTypes: Optional[List[Literal["ORDERED", "UNORDERED", "NONE"]]]
    lineIndentations: Optional[List[float]]
