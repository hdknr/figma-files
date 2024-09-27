from .vector import Vector
from typing import Optional, List
from ..base.files import FigmaFile
from lxml import etree


class Rectangle(Vector):
    cornerRadius: Optional[float] = None
    rectangleCornerRadii: Optional[List[float]] = []
    cornerSmoothing: Optional[float] = None

    def to_element(self, parent, sheet, file: FigmaFile, tag="div"):
        attrs = {}
        tag = self.resolve_tag(tag)

        if tag == "img":
            img = next(filter(lambda i: i.type == "IMAGE", self.fills), None)
            if img:
                ref = img.imageRef
                attrs["src"] = file.images.get(ref, None) or "#"
                elm: etree._Element = etree.SubElement(parent, tag, attrib=attrs)
                return elm
