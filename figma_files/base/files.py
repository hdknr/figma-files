from typing import Dict, Optional
from pydantic import BaseModel
from .property_types import Style, Component, ComponentSet, TypeStyle


class TailwindConfig(BaseModel):
    theme: Optional[Dict] = {}

    def set_extennd(self, category, key, value):
        extend = self.theme.get("extend", {})
        data = extend.get(category, {})
        data[key] = value
        extend[category] = data
        self.theme["extend"] = extend


class FigmaFile(BaseModel):
    document: dict = {}  # docuemnt ノードデータソース
    styles: Optional[Dict[str, Style]] = {}  # スタイル
    conpotents: Optional[Dict[str, Component]] = {}  # コンポーネント
    componentSets: Optional[Dict[str, ComponentSet]] = {}  # コンポーネントセット
    tailwind_config: Optional[TailwindConfig] = TailwindConfig()  # tailwind
    images: Optional[Dict[str, str]] = {}  # image

    def tw_position(self, postion: str, value: float):
        # https://tailwindcss.com/docs/top-right-bottom-left
        if 1 == int(value):
            return f"{postion}-px"

        n = int(value / 4)
        if n > 96:
            # rem = int(n / 4)
            # TOOD: config 設定
            pass

        return f"{postion}-{n}"

    def tw_w(self, width):
        """高さ (h-)"""
        n = int(width / 4)
        if n > 96:
            rem = int(n / 4)
            self.tailwind_config.set_extennd("width", f"{n}", f"{rem}rem")
        return f"w-{n}"

    def tw_h(self, height):
        """幅 (w-)"""
        n = int(height / 4)
        if n > 96:
            rem = int(n / 4)
            self.tailwind_config.set_extennd("height", f"{n}", f"{rem}rem")
        return f"h-{n}"

    def tw_color(self, target, fill: Style):
        # fill スタイルのネーミングルールによる
        parts = fill.name.split("/")
        return "-".join([target] + parts[1:])

    def tw_bg(self, fill: Style):
        """背景色 (bg-)"""
        return self.tw_color("bg", fill)

    def tw_rounded(self, px):
        """Border Radius"""
        # https://tailwindcss.com/docs/border-radius
        name = "rounded"
        index = int(px / 2) * 2
        if index < 2:
            return ""
        if index == 2:
            return f"{name}-sm"
        if index == 4:
            return name
        if index == 6:
            return f"{name}-md"
        if index >= 8 and index < 12:
            return f"{name}-lg"
        if index >= 12 and index < 16:
            return f"{name}-xl"
        if index >= 16 and index < 24:
            return f"{name}-2xl"
        if index >= 99998:
            return f"{name}-full"

    def tw_font_styles(self, style: TypeStyle):
        """フォントスタイル"""
        # https://tailwindcss.com/docs/font-family
        # https://tailwindcss.com/docs/line-height

        res = set()
        # サイズ (https://tailwindcss.com/docs/font-size)
        px = int(style.fontSize)
        mp = {
            128: "9xl",
            96: "8xl",
            72: "7xl",
            60: "6xl",
            48: "5xl",
            36: "4xl",
            30: "3xl",
            24: "2xl",
            20: "xl",
            18: "lg",
            16: "base",
            14: "sm",
            12: "xs",
        }
        sz, sym = next(filter(lambda i: i[0] <= px, mp.items()), (None, None))
        if not sym:
            sym = mp.values()[-1]
        res.add(f"text-{sym}")

        # https://tailwindcss.com/docs/font-weight
        w = int(style.fontWeight)
        mp = {
            900: "black",
            800: "extrabold",
            700: "bold",
            600: "semibold",
            500: "medium",
            400: "normal",
            300: "light",
            200: "extraylight",
            100: "thin",
            0: "",
        }
        sz, sym = next(filter(lambda i: i[0] <= w, mp.items()), (None, None))
        if not sym:
            sym = mp.values()[-1]
        res.add(f"font-{sym}")

        return res
