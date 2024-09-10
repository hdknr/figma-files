# https://www.figma.com/developers/api#node-types

from pydantic import BaseModel
from typing import Optional
from lxml import etree


class Node(BaseModel):
    id: str
    name: str
    type: str
    visible: Optional[bool] = None
    rotation: Optional[float] = None

    def to_element(self, parent, tag="div"):
        attrib = {
            "id": self.id,
            "name": self.name,
        }
        elm: etree._Element = etree.SubElement(parent, tag, attrib=attrib)
        return elm
