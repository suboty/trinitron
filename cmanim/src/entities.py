from typing import List
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
    ellipse = 'ellipse'
