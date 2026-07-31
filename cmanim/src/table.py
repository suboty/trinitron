from typing import List, Optional

from manim import *

from .base import ObjectBase
from .entities import TableCell
from .text import TextInBox


class Table(ObjectBase):
    DEFAULT_FILL_OPACITY = 0.8
    MAX_ROWS = 4
    MAX_COLS = 4
    DEFAULT_CELL_WIDTH = 2.0
    DEFAULT_CELL_HEIGHT = 1.0
    DEFAULT_SPACING = 0.2

    def __init__(
            self,
            data: List[List[TableCell]],
            cell_width: Optional[float | int] = None,
            cell_height: Optional[float | int] = None,
            spacing: Optional[float | int] = None,
            table_color: Optional[ManimColor | str] = None,
    ):
        super().__init__()

        self.data = data
        self.rows = len(data)
        self.cols = len(data[0]) if data else 0

        if self.rows > self.MAX_ROWS:
            raise ValueError(
                f"Table can have at most {self.MAX_ROWS} rows"
            )
        if self.cols > self.MAX_COLS:
            raise ValueError(
                f"Table can have at most {self.MAX_COLS} columns"
            )

        for row in data:
            if len(row) != self.cols:
                raise ValueError(
                    "All rows must have the same number of columns"
                )

        self.cell_width = cell_width or self.DEFAULT_CELL_WIDTH
        self.cell_height = cell_height or self.DEFAULT_CELL_HEIGHT
        self.spacing = spacing or self.DEFAULT_SPACING

        self.table_color = (
            table_color
            if isinstance(table_color, ManimColor)
            else ManimColor(table_color)
        ) if table_color else None

        self.cells: List[List[TextInBox]] = []

    def create(self) -> 'Table':
        self.cells = []

        total_width = self.cols * self.cell_width + (self.cols - 1) * self.spacing
        total_height = self.rows * self.cell_height + (self.rows - 1) * self.spacing

        start_x = -total_width / 2 + self.cell_width / 2
        start_y = total_height / 2 - self.cell_height / 2

        for row_idx, row_data in enumerate(self.data):
            row_cells = []
            for col_idx, cell_data in enumerate(row_data):
                x_pos = start_x + col_idx * (self.cell_width + self.spacing)
                y_pos = start_y - row_idx * (self.cell_height + self.spacing)

                cell = TextInBox(
                    text=cell_data.text,
                    text_font_size=cell_data.text_font_size,
                    text_color=cell_data.text_color,
                    figure_color=cell_data.box_color,
                    box_width=self.cell_width,
                    box_height=self.cell_height,
                ).create()

                cell.shift(RIGHT * x_pos + UP * y_pos)
                row_cells.append(cell)

            self.cells.append(row_cells)

        for row in self.cells:
            for cell in row:
                self.add(cell)

        return self

    def get_cell(self, row: int, col: int) -> Optional[TextInBox]:
        if 0 <= row < self.rows and 0 <= col < self.cols:
            return self.cells[row][col]
        return None

    def get_row(self, row: int) -> List[TextInBox]:
        if 0 <= row < self.rows:
            return self.cells[row]
        return []

    def get_col(self, col: int) -> List[TextInBox]:
        if 0 <= col < self.cols:
            return [self.cells[row][col] for row in range(self.rows)]
        return []

    def highlight_cell(
            self,
            row: int,
            col: int,
            color: ManimColor,
            scene: Scene
    ) -> None:
        cell = self.get_cell(row, col)
        if cell:
            scene.play(cell.animate.set_color(color))

    def highlight_row(
            self,
            row: int,
            color: ManimColor,
            scene: Scene
    ) -> None:
        cells = self.get_row(row)
        if cells:
            scene.play(*[cell.animate.set_color(color) for cell in cells])

    def highlight_col(
            self,
            col: int,
            color: ManimColor,
            scene: Scene
    ) -> None:
        cells = self.get_col(col)
        if cells:
            scene.play(*[cell.animate.set_color(color) for cell in cells])

    def animate_in(
            self,
            scene: Scene,
            run_time: float = ObjectBase.DEFAULT_DURATION,
            **kwargs,
    ) -> None:
        if not self.cells:
            self.create()

        all_cells = [cell for row in self.cells for cell in row]
        for cell in all_cells:
            cell.set_fill(opacity=0)
            cell.set_stroke(opacity=0)

        scene.add(self)

        animations = []
        for cell in all_cells:
            animations.append(
                cell.animate
                .set_fill(opacity=self.DEFAULT_FILL_OPACITY)
                .set_stroke(opacity=1)
            )

        scene.play(
            *animations,
            lag_ratio=self.DEFAULT_LAG_RATIO,
            run_time=run_time
        )

    def animate_out(
            self,
            scene: Scene,
            run_time: float = 1,
            **kwargs,
    ) -> None:
        if not self.cells:
            return

        all_cells = [cell for row in self.cells for cell in row]

        scene.play(
            AnimationGroup(
                *[
                    cell.animate
                    .set_fill(opacity=0)
                    .set_stroke(opacity=0)
                    for cell in all_cells
                ],
                lag_ratio=self.DEFAULT_LAG_RATIO,
            ),
            run_time=run_time,
        )

        scene.remove(self)
