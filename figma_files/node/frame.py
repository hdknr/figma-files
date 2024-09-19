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
    layoutAlign: Optional[
        Literal["INHERIT", "STRETCH", "MIN", "CENTER", "MAX", "STRETCH"]
    ] = None
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

    # Whether this layer uses auto-layout to position its children.
    # auto-layout :"HORIZONTAL", "VERTICAL"
    layoutMode: Optional[Literal["NONE", "HORIZONTAL", "VERTICAL"]] = "NONE"

    layoutSizingHorizontal: Optional[Literal["FIXED", "HUG", "FILL"]] = None
    layoutSizingVertical: Optional[Literal["FIXED", "HUG", "FILL"]] = None
    layoutWrap: Optional[Literal["NO_WRAP", "WRAP"]] = "NO_WRAP"

    # Whether the primary axis has a fixed length (determined by the user)
    # or an automatic length (determined by the layout engine).
    # This property is only applicable for auto-layout frames.
    primaryAxisSizingMode: Optional[Literal["FIXED", "AUTO"]] = "AUTO"

    # Whether the counter axis has a fixed length (determined by the user)
    # or an automatic length (determined by the layout engine).
    # This property is only applicable for auto-layout frames.
    counterAxisSizingMode: Optional[Literal["FIXED", "AUTO"]] = "AUTO"

    # MIN: 左揃え(HORIZONTAL), 上揃え(VERTICAL)
    # MAX: 右揃え(HORIZONTAL), 下揃え(VERTICAL)
    # SPACE_BETWEEN: 均等
    # BASELINE: 下揃え (HORIZONTALの場合のみ)
    primaryAxisAlignItems: Optional[
        Literal["MIN", "CENTER", "MAX", "SPACE_BETWEEN"]
    ] = "MIN"
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

    def tw_class_size(self, parent: etree._Element, file: FigmaFile) -> set:
        """サイズ"""
        classes = set()

        if self.layoutSizingVertical == "FIXED":
            if self.absoluteBoundingBox:
                classes.add(file.tw_h(self.absoluteBoundingBox.height))
        elif self.layoutSizingVertical == "FILL":
            classes.add("h-full")

        if self.layoutSizingHorizontal == "FIXED":
            if self.absoluteBoundingBox:
                classes.add(file.tw_w(self.absoluteBoundingBox.width))
        elif self.layoutSizingVertical == "FILL":
            classes.add("w-full")

        return classes

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

    def tw_class_align(self, parent: etree._Element, file: FigmaFile) -> set:
        """アライン"""
        classes = set()

        mp = {
            "CENTER": "center",
            "MIN": "start",
            "MAX": "end",
            "SPACE_BETWEEN": "between",
            "BASELINE": "baseline",
        }

        if self.layoutMode == "HORIZONTAL":  # 水平方向オートレイアウト
            classes.add("flex")  # オートレイアウト

            # 水平方向
            x = mp.get(self.primaryAxisAlignItems, None)
            if x:
                classes.add(f"justify-{x}")

            # 垂直方向
            y = mp.get(self.counterAxisAlignItems, None)
            if y:
                classes.add(f"items-{y}")

        return classes

    def tailwind_css(self, parent, file: FigmaFile):
        classes = set()

        # サイズ, 背景色
        classes = (
            classes
            | self.tw_class_size(parent, file)
            | self.tw_class_background(parent, file)
            | self.tw_class_align(parent, file)
        )

        # flex box
        if self.layoutPositioning == "AUTO":
            classes.add("flex")

        if "h-full" in classes and "w-full" in classes:
            # classes.append("grow")
            classes.add("flex-auto")

        return classes

    def to_element(self, parent, sheet, file: FigmaFile, tag="div"):
        attrs = self.html_attrs
        classes = ["relative"]

        # 構造タグ
        if parent.tag == "body":
            tag = "section"
            classes += ["min-h-screen flex-col"]
        else:
            names = self.name.split("_")
            # semantic structure
            if names[0] in ["section", "header", "nav", "aside", "main", "footer"]:
                tag = names[0]

        # クラス
        classes += self.tailwind_css(parent, file)
        if classes:
            attrs["class"] = " ".join(classes)

        elm: etree._Element = etree.SubElement(parent, tag, attrib=attrs)
        return elm
