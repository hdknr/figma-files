from typing import Dict, Optional
from pydantic import BaseModel
from .property_types import Style, Component, ComponentSet


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
