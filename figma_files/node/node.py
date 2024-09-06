# https://www.figma.com/developers/api#node-types

from pydantic import BaseModel
from typing import Optional
from .primitives import EasingType


class Node(BaseModel):
    id: str
    name: str
    visible: bool
    type: str
    rotation: int


class AbstractTransition(BaseModel):
    transitionNodeID: Optional[str] = None
    transitionDuration: Optional[float] = None
    transitionEasing: Optional[EasingType] = None
