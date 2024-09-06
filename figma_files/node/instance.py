from .frame import Frame
from typing import Optional, List
from .primitives import Overrides


class Instance(Frame):
    componentId: str
    isExposedInstance: Optional[bool] = False
    exposedInstances: Optional[List[str]] = []
    overrides: Optional[List[Overrides]] = []
