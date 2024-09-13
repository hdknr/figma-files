from .node import Node
from ..base.files import FigmaFile
from ..base.property_types import (
    Paint,
    Color,
    ExportSetting,
    BlendMode,
    LayoutConstraint,
    Rectangle,
    Vector,
    Transform,
    LayoutGrid,
    Effect,
    DevStatus,
    Annotation,
    EasingType,
)
from typing import Optional, List, Literal
from lxml import etree


class Frame(Node):
    locked: Optional[bool] = False
    background: Optional[List[Paint]] = []
    backgroundColor: Color
    fills: Optional[List[Paint]] = []
    #
    strokes: Optional[List[Paint]] = []
    strokeWeight: Optional[float] = None
    strokeAlign: Optional[Literal["INSIDE", "OUTSIDE", "CENTER"]] = None
    strokeDashes: Optional[List[float]] = []
    #
    cornerRadius: Optional[float] = None
    rectangleCornerRadii: Optional[List[float]] = []
    cornerSmoothing: Optional[float] = None
    #
    exportSettings: Optional[list[ExportSetting]] = []
    blendMode: BlendMode
    preserveRatio: Optional[bool] = False
    constraints: Optional[LayoutConstraint] = None
    layoutAlign: Optional[Literal["INHERIT", "STRETCH", "MIN", "CENTER", "MAX", "STRETCH"]] = None
    #
    transitionNodeID: Optional[str] = None
    transitionDuration: Optional[float] = None
    transitionEasing: Optional[EasingType] = None
    #
    opacity: Optional[float] = 1
    absoluteBoundingBox: Optional[Rectangle] = None
    absoluteRenderBounds: Optional[Rectangle] = None
    #
    size: Optional[Vector] = None
    minWidth: Optional[float] = None
    maxWidth: Optional[float] = None
    minHeight: Optional[float] = None
    maxHeight: Optional[float] = None
    #
    relativeTransform: Optional[Transform] = None
    #
    clipsContent: bool
    #
    layoutMode: Optional[Literal["NONE", "HORIZONTAL", "VERTICAL"]] = "NONE"
    layoutSizingHorizontal: Optional[Literal["FIXED", "HUG", "FILL"]] = None
    layoutSizingVertical: Optional[Literal["FIXED", "HUG", "FILL"]] = None
    layoutWrap: Optional[Literal["NO_WRAP", "WRAP"]] = "NO_WRAP"
    primaryAxisSizingMode: Optional[Literal["FIXED", "AUTO"]] = "AUTO"
    counterAxisSizingMode: Optional[Literal["FIXED", "AUTO"]] = "AUTO"
    primaryAxisAlignItems: Optional[Literal["MIN", "CENTER", "MAX", "SPACE_BETWEEN"]] = "MIN"
    counterAxisAlignItems: Optional[Literal["MIN", "CENTER", "MAX", "BASELINE"]] = "MIN"
    counterAxisAlignContent: Optional[Literal["AUTO", "SPACE_BETWEEN"]] = "AUTO"
    #
    paddingLeft: Optional[float] = 0
    paddingRight: Optional[float] = 0
    paddingTop: Optional[float] = 0
    paddingBottom: Optional[float] = 0
    #
    horizontalPadding: Optional[float] = 0
    verticalPadding: Optional[float] = 0
    #
    itemSpacing: Optional[float] = 0
    counterAxisSpacing: Optional[float] = 0
    #
    layoutPositioning: Optional[Literal["AUTO", "ABSOLUTE"]] = "AUTO"
    #
    itemReverseZIndex: Optional[bool] = False
    strokesIncludedInLayout: Optional[bool] = False
    layoutGrids: Optional[List[LayoutGrid]] = []
    overflowDirection: Optional[
        Literal[
            "NONE",
            "HORIZONTAL_SCROLLING",
            "VERTICAL_SCROLLING",
            "HORIZONTAL_AND_VERTICAL_SCROLLING",
        ]
    ] = "NONE"

    effects: Optional[List[Effect]] = []
    isMask: Optional[bool] = False
    isMaskOutline: Optional[bool] = False
    maskType: Optional[Literal["ALPHA", "VECTOR", "LUMINANCE"]] = None
    styles: Optional[dict] = None
    devStatus: Optional[DevStatus] = None
    annotations: Optional[List[Annotation]] = []

    def to_element(self, parent, sheet, file: FigmaFile, tag="div"):
        if parent.tag == "body":
            tag = "section"
        else:
            names = self.name.split("_")
            # semantic structure
            if names[0] in ["section", "header", "nav", "aside", "main", "footer"]:
                tag = names[0]

        classes = []

        # flex
        if self.layoutPositioning == "AUTO":
            classes.append("flex")

        # flex
        if "class" in parent.attrib and "flex" in parent.attrib["class"].split(" "):
            classes.append("flex-auto")

        # 背景色
        if self.styles and "fill" in self.styles:
            style = file.styles.get(self.styles["fill"], None)
            if style:
                prefix, color, grade = style.name.split("/")
                bg = f"bg-{color}-{grade}"
                classes.append(bg)

        attrs = self.html_attrs
        if classes:
            attrs["class"] = " ".join(classes)

        elm: etree._Element = etree.SubElement(parent, tag, attrib=attrs)
        return elm
