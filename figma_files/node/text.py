from .vector import Vector
from ..base.property_types import TypeStyle
from ..base.files import FigmaFile
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

    def to_element(self, parent: etree._Element, sheet, file: FigmaFile, tag="p"):
        tag = self.resolve_tag(tag)

        classes = []

        if parent is None:
            return

        if parent.tag == "a":
            tag = "span"

        # フォントカラー
        fill = self.styles and file.styles.get(self.styles.get("fill", None), None)
        if fill:
            color = file.tw_color("text", fill)
            if color:
                classes.append(color)

        attrs = self.html_attrs
        if classes:
            attrs["class"] = " ".join(classes)
        if tag == "a":
            attrs["href"] = "#"

        elm: etree._Element = etree.SubElement(parent, tag, attrib=attrs)
        elm.text = self.characters
        return elm
