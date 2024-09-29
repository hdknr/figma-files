from .vector import Vector
from ..base.property_types import TypeStyle
from ..base.files import FigmaFile
from typing import Optional, List, Literal
from lxml import etree
from cssutils.css import CSSStyleRule as Rule
from .frame import Frame


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

    def tw_class_size(self, parent: etree._Element, file: FigmaFile) -> set:
        ret = set()
        ret.add(file.tw_w(self.absoluteBoundingBox.width))
        ret.add(file.tw_h(self.absoluteBoundingBox.height))

        return ret

    def to_element(
        self,
        parent: etree._Element,
        sheet,
        file: FigmaFile,
        tag="p",
        container: Frame = None,
    ):
        tag = self.resolve_tag(tag)

        classes = set()

        if parent is None:
            return

        if parent.tag == "a":
            tag = "span"

        # フォントカラー
        fill = self.styles and file.styles.get(self.styles.get("fill", None), None)
        if fill:
            color = file.tw_color("text", fill)
            if color:
                classes.add(color)
        # フォントスタイル
        if self.style:
            classes = classes | file.tw_font_styles(self.style)

        if tag == "div":
            classes = classes | self.tw_class_size(parent, file)

            # TODO: absolute  条件
            classes.add("absolute")
            if container:
                # https://tailwindcss.com/docs/position
                x = self.absoluteBoundingBox.x - container.absoluteBoundingBox.x
                y = self.absoluteBoundingBox.y - container.absoluteBoundingBox.y
                classes.add(file.tw_position("left", x))
                classes.add(file.tw_position("top", y))

        attrs = self.html_attrs
        if classes:
            attrs["class"] = " ".join(classes)
        if tag == "a":
            attrs["href"] = "#"

        elm: etree._Element = etree.SubElement(parent, tag, attrib=attrs)

        if not self.characterStyleOverrides:
            elm.text = self.characters
            return elm

        # 拡張スタイルがあれば、spanで切り替える
        chars = list(self.characters)
        overrides = self.characterStyleOverrides + ([0.0] * len(chars))

        span: etree.Element = None
        prev_o = -1.0
        for c, o in zip(chars, overrides):
            attrib = {}
            if prev_o != o:
                if o == 0.0:
                    span = etree.SubElement(elm, "span")
                else:
                    # テキストの拡張スタイル
                    style = self.styleOverrideTable.get(str(int(o)), None)
                    if style and "inheritFillStyleId" in style:
                        id = style["inheritFillStyleId"]
                        fill = file.styles.get(id)
                        name = file.tw_color("text", fill)
                        attrib["class"] = name

                    span = etree.SubElement(elm, "span", attrib=attrib)
            prev_o = o
            span.text = (span.text or "") + c
        return elm
