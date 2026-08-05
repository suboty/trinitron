from typing import List

from manim import *

from .base import ObjectBase
from .entities import TextStep, FigureTypesForText
from .text import (
    TextInSomething,
    TextInBox,
    TextInCircle,
    TextInRoundedRectangle,
    TextInEllipse
)


class VerticalSteps(ObjectBase):
    DEFAULT_FILL_OPACITY = 0.8
    TOP_LIMIT = 1.5
    BOTTOM_LIMIT = -2.0
    MIN_SPACING = 0.2
    DEFAULT_HEIGHT = 1.0
    MIN_STEPS_LEN = 2
    MAX_STEPS_LEN = 4
    DEFAULT_SHAPE = FigureTypesForText.box
    ELLIPSE_SCALE = 1.5
    CORNER_RADIUS_DEFAULT = 0.2
    DEFAULT_WIDTH = 3.0
    STROKE_DEFAULT = 8.0

    def __init__(
            self,
            steps: List[TextStep],
            figure_color: ManimColor | str, # noqa
            figure_height: int | float,
            arrow_color: ManimColor | str, # noqa
            shape: FigureTypesForText = FigureTypesForText.box,
            shape_params: dict = None,
            **kwargs
    ):
        super().__init__()

        if len(steps) > self.MAX_STEPS_LEN:
            raise ValueError(
                f"Steps can have at most {self.MAX_STEPS_LEN} steps"
            )
        elif len(steps) < self.MIN_STEPS_LEN:
            raise ValueError(
                f"Steps must have at least {self.MIN_STEPS_LEN} steps"
            )

        self.steps = steps
        self.arrow_color = (
            arrow_color
            if isinstance(arrow_color, ManimColor)
            else ManimColor(arrow_color)
        )

        self.figure_height = figure_height
        self.shape = shape
        self.shape_params = shape_params or {}
        self.figure_color = (
            figure_color
            if isinstance(figure_color, ManimColor)
            else ManimColor(figure_color)
        )

    def _get_step_width(self, step: TextStep) -> float:
        width = getattr(step, 'figure_width', None)
        if width is None:
            width = getattr(step, 'width', None)
        if width is None:
            width = getattr(step, 'box_width', None)
        if width is None:
            width = self.DEFAULT_WIDTH
        return width

    def _create_text_in_shape(
            self,
            step: TextStep,
            width: float | int,
            height: float | int,
    ) -> TextInSomething:
        match self.shape:
            case FigureTypesForText.circle:
                radius = self.shape_params.get('radius', min(width, height) / 2)
                return TextInCircle(
                    text=step.text,
                    text_font_size=step.text_font_size,
                    text_color=step.text_color,
                    figure_color=step.figure_color,
                    circle_radius=radius,
                ).create()

            case FigureTypesForText.rounded:
                corner_radius = self.shape_params.get('corner_radius', self.CORNER_RADIUS_DEFAULT)
                return TextInRoundedRectangle(
                    text=step.text,
                    text_font_size=step.text_font_size,
                    text_color=step.text_color,
                    figure_color=step.figure_color,
                    box_width=width,
                    box_height=height,
                    corner_radius=corner_radius,
                ).create()

            case FigureTypesForText.ellipse:
                ellipse_width = self.shape_params.get('ellipse_width', width)
                ellipse_height = self.shape_params.get('ellipse_height', height)
                return TextInEllipse(
                    text=step.text,
                    text_font_size=step.text_font_size,
                    text_color=step.text_color,
                    figure_color=step.figure_color,
                    ellipse_width=ellipse_width,
                    ellipse_height=ellipse_height,
                ).create()

            case _:
                return TextInBox(
                    text=step.text,
                    text_font_size=step.text_font_size,
                    text_color=step.text_color,
                    figure_color=step.figure_color,
                    box_width=width,
                    box_height=height,
                ).create()

    def create(self) -> 'VerticalSteps':
        objects: list[TextInSomething | Arrow] = []

        n = len(self.steps)

        available_height = self.TOP_LIMIT - self.BOTTOM_LIMIT
        total_spacing = (n - 1) * self.MIN_SPACING
        available_for_boxes = available_height - total_spacing
        optimal_height = available_for_boxes / n

        initial_width = self._get_step_width(self.steps[0])
        box_width = initial_width
        box_height = self.figure_height

        match self.shape:
            case FigureTypesForText.circle:
                size = min(optimal_height, self.DEFAULT_HEIGHT)
                size = max(self.figure_height, size)
                box_height = size
                box_width = size

            case FigureTypesForText.ellipse:
                box_height = min(self.figure_height, min(optimal_height, self.DEFAULT_HEIGHT))
                box_width = self.shape_params.get('ellipse_width', box_height * self.ELLIPSE_SCALE)

            case _:
                box_height = min(self.figure_height, min(optimal_height, self.DEFAULT_HEIGHT))

        boxes = []
        for step in self.steps:
            if self.shape in [FigureTypesForText.box, FigureTypesForText.rounded]:
                width = self._get_step_width(step)
            else:
                width = box_width

            box = self._create_text_in_shape(
                step=step,
                width=width,
                height=box_height,
            )
            boxes.append(box)

        total_height = n * box_height + (n - 1) * self.MIN_SPACING

        if total_height <= available_height:
            center_y = (self.TOP_LIMIT + self.BOTTOM_LIMIT) / 2
            start_y = center_y + total_height / 2 - box_height / 2
        else:
            total_height = n * box_height + (n - 1) * self.MIN_SPACING
            center_y = (self.TOP_LIMIT + self.BOTTOM_LIMIT) / 2
            start_y = center_y + total_height / 2 - box_height / 2

        for i, box in enumerate(boxes):
            y_pos = start_y - i * (box_height + self.MIN_SPACING)
            box.shift(UP * y_pos)

        for i in range(n - 1):
            objects.append(
                Arrow(
                    boxes[i].get_bottom(),
                    boxes[i + 1].get_top(),
                    color=self.arrow_color,
                    stroke_width=self.STROKE_DEFAULT,
                )
            )

        objects.extend(boxes)
        self.add(*objects)

        return self


class HorizontalSteps(VerticalSteps):
    LEFT_LIMIT = -5.0
    RIGHT_LIMIT = 5.0
    MIN_SPACING = 0.3
    DEFAULT_WIDTH = 2.0
    TOP_LIMIT = 0
    BOTTOM_LIMIT = 0
    ELLIPSE_SCALE = 0.7
    DEFAULT_HEIGHT = 1.0

    def _get_step_width(self, step: TextStep) -> float:
        width = getattr(step, 'figure_width', None)
        if width is None:
            width = getattr(step, 'width', None)
        if width is None:
            width = getattr(step, 'box_width', None)
        if width is None:
            width = self.DEFAULT_WIDTH
        return width

    def _create_text_in_shape(
            self,
            step: TextStep,
            width: float | int,
            height: float | int,
    ) -> TextInSomething:
        match self.shape:
            case FigureTypesForText.circle:
                radius = self.shape_params.get('radius', min(width, height) / 2)
                return TextInCircle(
                    text=step.text,
                    text_font_size=step.text_font_size,
                    text_color=step.text_color,
                    figure_color=step.figure_color,
                    circle_radius=radius,
                ).create()

            case FigureTypesForText.rounded:
                corner_radius = self.shape_params.get('corner_radius', self.CORNER_RADIUS_DEFAULT)
                return TextInRoundedRectangle(
                    text=step.text,
                    text_font_size=step.text_font_size,
                    text_color=step.text_color,
                    figure_color=step.figure_color,
                    box_width=width,
                    box_height=height,
                    corner_radius=corner_radius,
                ).create()

            case FigureTypesForText.ellipse:
                ellipse_width = self.shape_params.get('ellipse_width', width)
                ellipse_height = self.shape_params.get('ellipse_height', height)
                return TextInEllipse(
                    text=step.text,
                    text_font_size=step.text_font_size,
                    text_color=step.text_color,
                    figure_color=step.figure_color,
                    ellipse_width=ellipse_width,
                    ellipse_height=ellipse_height,
                ).create()

            case _:
                return TextInBox(
                    text=step.text,
                    text_font_size=step.text_font_size,
                    text_color=step.text_color,
                    figure_color=step.figure_color,
                    box_width=width,
                    box_height=height,
                ).create()

    def create(self) -> 'HorizontalSteps':
        objects: list[TextInSomething | Arrow] = []

        n = len(self.steps)

        available_width = self.RIGHT_LIMIT - self.LEFT_LIMIT
        total_spacing = (n - 1) * self.MIN_SPACING
        available_for_boxes = available_width - total_spacing
        optimal_width = available_for_boxes / n

        initial_width = self._get_step_width(self.steps[0])
        box_width = initial_width
        box_height = self.figure_height

        match self.shape:
            case FigureTypesForText.circle:
                size = min(optimal_width, self.DEFAULT_WIDTH)
                size = max(initial_width, size)
                box_width = size
                box_height = size

            case FigureTypesForText.ellipse:
                box_width = min(initial_width, min(optimal_width, self.DEFAULT_WIDTH))
                box_height = self.shape_params.get('ellipse_height', box_width * self.ELLIPSE_SCALE)

            case _:
                box_width = min(initial_width, min(optimal_width, self.DEFAULT_WIDTH))
                box_height = self.figure_height

        boxes = []
        for step in self.steps:
            if self.shape in [FigureTypesForText.box, FigureTypesForText.rounded]:
                width = self._get_step_width(step)
            else:
                width = box_width

            box = self._create_text_in_shape(
                step=step,
                width=width,
                height=box_height,
            )
            boxes.append(box)

        total_width = n * box_width + (n - 1) * self.MIN_SPACING

        if total_width <= available_width:
            center_x = (self.RIGHT_LIMIT + self.LEFT_LIMIT) / 2
            start_x = center_x - total_width / 2 + box_width / 2
        else:
            total_width = n * box_width + (n - 1) * self.MIN_SPACING
            center_x = (self.RIGHT_LIMIT + self.LEFT_LIMIT) / 2
            start_x = center_x - total_width / 2 + box_width / 2

        for i, box in enumerate(boxes):
            x_pos = start_x + i * (box_width + self.MIN_SPACING)
            box.shift(RIGHT * x_pos)

        for i in range(n - 1):
            objects.append(
                Arrow(
                    boxes[i].get_right(),
                    boxes[i + 1].get_left(),
                    color=self.arrow_color,
                    stroke_width=self.STROKE_DEFAULT,
                )
            )

        objects.extend(boxes)
        self.add(*objects)

        return self


class Conveyor(ObjectBase):
    LEFT_LIMIT = -5.0
    RIGHT_LIMIT = 5.0
    MIN_SPACING = 0.3
    DEFAULT_WIDTH = 2.0
    FADE_DURATION = 0.3
    MIN_LEN = 1
    DEFAULT_SHAPE = FigureTypesForText.box
    DEFAULT_VISIBLE_COUNT = 3
    CORNER_RADIUS_DEFAULT = 0.2

    def __init__(
            self,
            items: List[TextStep],
            figure_height: float | int,
            figure_color: ManimColor | str, # noqa
            visible_count: int = DEFAULT_VISIBLE_COUNT,
            shape: FigureTypesForText = FigureTypesForText.box,
            shape_params: dict = None,
    ):
        super().__init__()

        if visible_count < self.MIN_LEN:
            raise ValueError(
                f"visible_count must be at least {self.MIN_LEN}"
            )

        if len(items) < visible_count:
            raise ValueError(
                f"items count ({len(items)}) must be >= visible_count ({visible_count})"
            )

        self.items = items
        self.figure_height = figure_height
        self.figure_color = (
            figure_color
            if isinstance(figure_color, ManimColor)
            else ManimColor(figure_color)
        )

        self.visible_count = visible_count
        self.current_index = 0
        self.boxes: List[TextInSomething] = []

        first_item = items[0] if items else None
        if first_item:
            self.box_width = getattr(first_item, 'figure_width', None)
            if self.box_width is None:
                self.box_width = getattr(first_item, 'width', None)
            if self.box_width is None:
                self.box_width = getattr(first_item, 'box_width', None)
            if self.box_width is None:
                self.box_width = self.DEFAULT_WIDTH
        else:
            self.box_width = self.DEFAULT_WIDTH

        self.shape = shape
        self.shape_params = shape_params or {}

    def _get_item_width(self, item: TextStep) -> float:
        width = getattr(item, 'figure_width', None)
        if width is None:
            width = getattr(item, 'width', None)
        if width is None:
            width = getattr(item, 'box_width', None)
        if width is None:
            width = self.DEFAULT_WIDTH
        return width

    def _create_box(self, item: TextStep) -> TextInSomething:
        item_width = self._get_item_width(item)

        match self.shape:
            case FigureTypesForText.circle:
                radius = self.shape_params.get('radius', item_width / 2)
                return TextInCircle(
                    text=item.text,
                    text_font_size=item.text_font_size,
                    text_color=item.text_color,
                    figure_color=item.figure_color,
                    circle_radius=radius,
                ).create()

            case FigureTypesForText.rounded:
                corner_radius = self.shape_params.get('corner_radius', self.CORNER_RADIUS_DEFAULT)
                return TextInRoundedRectangle(
                    text=item.text,
                    text_font_size=item.text_font_size,
                    text_color=item.text_color,
                    figure_color=item.figure_color,
                    box_width=item_width,
                    box_height=self.figure_height,
                    corner_radius=corner_radius,
                ).create()

            case FigureTypesForText.ellipse:
                ellipse_width = self.shape_params.get('ellipse_width', item_width)
                ellipse_height = self.shape_params.get('ellipse_height', self.figure_height)
                return TextInEllipse(
                    text=item.text,
                    text_font_size=item.text_font_size,
                    text_color=item.text_color,
                    figure_color=item.figure_color,
                    ellipse_width=ellipse_width,
                    ellipse_height=ellipse_height,
                ).create()

            case _:
                return TextInBox(
                    text=item.text,
                    text_font_size=item.text_font_size,
                    text_color=item.text_color,
                    figure_color=item.figure_color,
                    box_width=item_width,
                    box_height=self.figure_height,
                ).create()

    def _get_positions(self, count: int) -> List[float]:
        total_width = count * self.box_width + (count - 1) * self.MIN_SPACING
        center_x = (self.RIGHT_LIMIT + self.LEFT_LIMIT) / 2
        start_x = center_x - total_width / 2 + self.box_width / 2

        positions = []
        for i in range(count):
            x_pos = start_x + i * (self.box_width + self.MIN_SPACING)
            positions.append(x_pos)

        return positions

    def create(self) -> 'Conveyor':
        visible_items = self.items[:self.visible_count]
        positions = self._get_positions(self.visible_count)

        self.boxes = []
        for i, item in enumerate(visible_items):
            box = self._create_box(item)
            box.shift(RIGHT * positions[i])
            self.boxes.append(box)

        self.add(*self.boxes)
        return self

    def step_forward(self, scene: Scene, run_time: float = 0.5) -> None:
        if self.current_index + self.visible_count >= len(self.items):
            return

        positions = self._get_positions(self.visible_count)

        first_box = self.boxes[0]
        scene.play(FadeOut(first_box, run_time=self.FADE_DURATION))
        scene.wait(0.1)

        animations = []
        for i in range(1, len(self.boxes)):
            new_index = i - 1
            target_x = positions[new_index]
            animations.append(
                self.boxes[i].animate.move_to(RIGHT * target_x)
            )

        if animations:
            scene.play(*animations, run_time=run_time)

        self.remove(first_box)
        self.boxes.pop(0)

        next_item = self.items[self.current_index + self.visible_count]
        new_box = self._create_box(next_item)

        last_position = positions[-1]
        new_box.shift(RIGHT * last_position)

        scene.play(FadeIn(new_box, run_time=self.FADE_DURATION))

        self.boxes.append(new_box)
        self.add(new_box)

        self.current_index += 1

    def step_forward_fast(self, scene: Scene, run_time: float = 0.5) -> None:
        if self.current_index + self.visible_count >= len(self.items):
            return

        positions = self._get_positions(self.visible_count)

        next_item = self.items[self.current_index + self.visible_count]
        new_box = self._create_box(next_item)
        last_position = positions[-1]
        new_box.shift(RIGHT * last_position)
        self.add(new_box)

        animations = []

        first_box = self.boxes[0]
        animations.append(FadeOut(first_box, run_time=self.FADE_DURATION))

        for i in range(1, len(self.boxes)):
            new_index = i - 1
            target_x = positions[new_index]
            animations.append(
                self.boxes[i].animate.move_to(RIGHT * target_x)
            )

        animations.append(FadeIn(new_box, run_time=self.FADE_DURATION))

        scene.play(*animations, run_time=max(run_time, self.FADE_DURATION))

        self.remove(first_box)
        self.boxes.pop(0)

        self.boxes.append(new_box)

        self.current_index += 1

    def animate_in(
            self,
            scene: Scene,
            run_time: float = ObjectBase.DEFAULT_DURATION,
            is_fast: bool = False,
            **kwargs
    ) -> None:
        scene.play(FadeIn(self, run_time=self.FADE_DURATION))
        while self.current_index + self.visible_count < len(self.items):
            if is_fast:
                self.step_forward_fast(scene, run_time)
            else:
                self.step_forward(scene, run_time)

    def animate_out(
            self,
            scene: Scene,
            run_time: float = ObjectBase.DEFAULT_DURATION,
            **kwargs
    ) -> None:
        scene.play(FadeOut(self, run_time=run_time))
        scene.remove(self)