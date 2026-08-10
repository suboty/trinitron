from typing import List, Tuple, Optional
from dataclasses import dataclass, field
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
    children: List['NodeData'] = field(default_factory=list)
    parent: Optional['NodeData'] = None

    pos_x: float | None = 0.0
    pos_y: float | None = 0.0

    mod: float | None = None
    thread: Optional['NodeData'] = None
    ancestor: Optional['NodeData'] = None


@dataclass
class GraphData:
    nodes: List[NodeData]
    edges: List[Tuple[int, int]]

    def build_tree(self) -> None:
        for node in self.nodes:
            node.children = []
            node.parent = None

        for parent_idx, child_idx in self.edges:
            parent = self.nodes[parent_idx]
            child = self.nodes[child_idx]

            if child not in parent.children:
                parent.children.append(child)

            if child.parent is not None:
                raise ValueError(f"Node {child.name} already has a parent!")
            child.parent = parent
