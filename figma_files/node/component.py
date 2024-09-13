from .frame import Frame
from typing import Optional


class Component(Frame):
    componentPropertyDefinitions: Optional[dict] = {}


class ComponentSet(Frame):
    componentPropertyDefinitions: Optional[dict] = {}
