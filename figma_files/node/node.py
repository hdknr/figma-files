# https://www.figma.com/developers/api#node-types

from pydantic import BaseModel


class Node(BaseModel):
    id: str
    name: str
    visible: bool
    type: str
    rotation: int
