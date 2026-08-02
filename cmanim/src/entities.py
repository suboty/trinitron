from typing import List, Tuple
from dataclasses import dataclass
from enum import Enum

from manim import *


@dataclass
class TextStep:
    text: List[str] | str
    text_font_size: List[float | int] | float | int
    text_color: List[ManimColor | str] | ManimColor | str
    figure_width: float | int
    figure_color: ManimColor | str # noqa


@dataclass
class TableCell:
    text: List[str] | str
    text_font_size: List[float | int] | float | int
    text_color: List[ManimColor | str] | ManimColor | str
    box_color: ManimColor | str # noqa


class FigureTypesForText(Enum):
    box = "box"
    circle = "circle"
    rounded = "rounded"
    ellipse = "ellipse"


@dataclass
class NodeData:
    name: str
    pos_x: float = None
    pos_y: float = None


@dataclass
class GraphData:
    nodes: List[NodeData]
    edges: List[Tuple[int, int]]
