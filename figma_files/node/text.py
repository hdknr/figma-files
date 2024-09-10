from .vector import Vector
from ..base.primitives import TypeStyle
from typing import Optional, List, Literal
from lxml import etree


class Text(Vector):
    characters: str
    style: TypeStyle
    characterStyleOverrides: Optional[List[float]] = []
    styleOverrideTable: Optional[dict] = None
    lineTypes: Optional[List[Literal["ORDERED", "UNORDERED", "NONE"]]]
    lineIndentations: Optional[List[float]]

    @property
    def html_attrs(self):
        attrs = super().html_attrs
        attrs.pop("name")
        return attrs

    def to_element(self, parent, tag="p"):
        elm: etree._Element = etree.SubElement(parent, tag, attrib=self.html_attrs)
        elm.text = self.name
        return elm
