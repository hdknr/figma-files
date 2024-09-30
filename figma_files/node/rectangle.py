from .vector import Vector
from typing import Optional, List
from ..base.files import FigmaFile
from lxml import etree
from .frame import Frame


class Rectangle(Vector):
    cornerRadius: Optional[float] = None
    rectangleCornerRadii: Optional[List[float]] = []
    cornerSmoothing: Optional[float] = None

    def get_image(self, file: FigmaFile):
        img = next(filter(lambda i: i.type == "IMAGE", self.fills), None)
        if img:
            ref = img.imageRef
            return file.images.get(ref, None)

    def to_element(
        self,
        parent: etree._Element,
        sheet,
        file: FigmaFile,
        tag="div",
        container: Frame = None,
    ):
        attrs = {}
        tag = self.resolve_tag(tag)

        if tag == "img":
            src = self.get_image(file)
            if src:
                attrs["src"] = src
                elm: etree._Element = etree.SubElement(parent, tag, attrib=attrs)
                return elm

        if tag == "bg":
            # 背景イメージ
            src = self.get_image(file)
            if src:
                klass = parent.attrib["class"] or ""
                klass += f" bg-[url('{src}')] bg-cover"
                parent.attrib["class"] = klass
                return parent
