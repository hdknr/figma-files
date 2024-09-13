from typing import Dict, Optional
from pydantic import BaseModel
from .property_types import Style, Component, ComponentSet


class FigmaFile(BaseModel):
    document: dict = {}  # docuemnt ノードデータソース
    styles: Optional[Dict[str, Style]] = {}  # スタイル
    conpotents: Optional[Dict[str, Component]] = {}  # コンポーネント
    componentSets: Optional[Dict[str, ComponentSet]] = {}  # コンポーネントセット
