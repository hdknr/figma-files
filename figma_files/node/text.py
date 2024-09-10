from .vector import Vector
from ..base.primitives import TypeStyle
from typing import Optional, List, Literal
from lxml import etree
from cssutils.css import CSSStyleRule as Rule


class Text(Vector):
    characters: str
    style: TypeStyle
    characterStyleOverrides: Optional[List[float]] = []
    styleOverrideTable: Optional[dict] = None
    lineTypes: Optional[List[Literal["ORDERED", "UNORDERED", "NONE"]]]
    lineIndentations: Optional[List[float]]

    def css(self, sheet, tag):
        if not self.style:
            return

        sel = f"{tag}#{self.sanitized_id}"
        rule = Rule(selectorText=sel)
        self.style.set_rule(rule)
        sheet.cssRules.append(rule)

    @property
    def html_attrs(self):
        attrs = super().html_attrs
        attrs.pop("name")
        return attrs

    def to_element(self, parent, sheet, tag="p"):
        elm: etree._Element = etree.SubElement(parent, tag, attrib=self.html_attrs)
        elm.text = self.name
        # self.css(sheet, tag)
        return elm
