# https://www.figma.com/developers/api#node-types

from pydantic import BaseModel
from typing import Optional
from lxml import etree
from .utils import to_snake
from ..base.files import FigmaFile
from ..base.utils import sanitize_id


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

    def to_element(self, parent, sheet, file: FigmaFile, tag="div"):
        elm: etree._Element = etree.SubElement(parent, tag, attrib=self.html_attrs)
        return elm
