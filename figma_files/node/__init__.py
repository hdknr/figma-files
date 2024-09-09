from .boolean import BooleanOperation  # NOQA
from .canvas import Canvas  # NOQA
from .component import Component, ComponentSet  # NOQA
from .document import Document  # NOQA
from .ellipse import Ellipse  # NOQA
from .frame import Frame  # NOQA
from .group import Group  # NOQA
from .instance import Instance  # NOQA
from .line import Line  # NOQA
from .node import Node  # NOQA
from .polygon import RegularPolygon  # NOQA
from .rectangle import Rectangle  # NOQA
from .section import Section  # NOQA
from .slice import Slice  # NOQA
from .text import Text  # NOQA
from .vector import Vector  # NOQA
from .washi import WashiTape  # NOQA
import re
import inspect


def to_snake(src: str) -> str:
    return re.sub(r"(?<!^)(?=[A-Z])", "_", src).upper()


target = list(filter(lambda i: inspect.isclass(i[1]) and issubclass(i[1], Node), globals().items()))
mapper = dict(map(lambda i: (to_snake(i[0]), i[1]), target))
