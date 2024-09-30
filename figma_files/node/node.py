# https://www.figma.com/developers/api#node-types

from pydantic import BaseModel
from typing import Optional
from lxml import etree
from .utils import to_snake
from ..base.files import FigmaFile
from ..base.utils import sanitize_id
import re


class Node(BaseModel):
    id: str
    name: str
    type: str
    visible: Optional[bool] = None
    rotation: Optional[float] = None

    @property
    def sanitized_id(self):
        return sanitize_id(self.id)

    @property
    def html_attrs(self):
        return {
            "id": self.sanitized_id,
            "name": self.name,
            "data-figma_type": to_snake(self.__class__.__name__),
        }

    def to_element(self, parent, sheet, file: FigmaFile, tag="div", **kwargs):
        elm: etree._Element = etree.SubElement(parent, tag, attrib=self.html_attrs)
        return elm

    def resolve_tag(self, default):
        ma = re.search(r"^(?P<tag>[^_]+)_?(?P<name>.*)$", self.name)
        ma = ma and ma.groupdict() or {}
        tag = ma.get("tag", None) or default
        tag = {"anchor": "a", "image": "img"}.get(tag, None) or tag
        return tag

    def tw_class_background(self, parent: etree._Element, file: FigmaFile) -> set:
        """背景色"""
        classes = set()
        # 背景色
        fill = self.styles and file.styles.get(self.styles.get("fill", None), None)
        if fill:
            bg = file.tw_bg(fill)
            if bg:
                classes.add(bg)
        return classes

    def tw_class_corner(self, parent: etree._Element, file: FigmaFile) -> set:
        """角丸"""
        classes = set()
        # 角丸
        if self.cornerRadius:
            rounded = file.tw_rounded(self.cornerRadius)
            if rounded:
                classes.add(rounded)
        return classes
