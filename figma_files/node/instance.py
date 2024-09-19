from .frame import Frame
from typing import Optional, List
from ..base.property_types import Overrides
from ..base.files import FigmaFile
from lxml import etree


class Instance(Frame):
    componentId: str
    # ID of component that this instance came from, refers to components table (see endpoints section below)

    isExposedInstance: Optional[bool] = False
    # If true, this node has been marked as exposed to its containing component or component set

    exposedInstances: Optional[List[str]] = []
    # IDs of instances that have been exposed to this node's level

    overrides: Optional[List[Overrides]] = []
    # An array of all of the fields directly overridden on this instance. Inherited overrides are not included.

    def to_element(self, parent, sheet, file: FigmaFile, tag="div"):
        if self.name.startswith("anchor_"):
            return self.to_anchor(parent, sheet, file)

    def to_anchor(self, parent, sheet, file: FigmaFile, tag="a"):
        """<a>"""
        classes = set()
        classes = (
            classes
            | self.tw_class_size(parent, file)
            | self.tw_class_background(parent, file)
            | self.tw_class_corner(parent, file)
            | self.tw_class_align(parent, file)
        )

        attrs = self.html_attrs
        if classes:
            attrs["class"] = " ".join(classes)
        elm: etree._Element = etree.SubElement(parent, tag, attrib=attrs)
        return elm
