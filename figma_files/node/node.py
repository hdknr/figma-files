# https://www.figma.com/developers/api#node-types

from pydantic import BaseModel
from typing import Optional


class Node(BaseModel):
    id: str
    name: str
    type: str
    visible: Optional[bool] = None
    rotation: Optional[float] = None
