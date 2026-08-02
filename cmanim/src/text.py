from typing import List

from manim import *

from .base import ObjectBase


class Title(ObjectBase):
    obj_pos = [
        UP * 3 + LEFT * 1.5,
        UP * 3,
        UP * 2.5,
    ]

    def __init__(
        self,
        title: str,
        description: str,
        title_font_size: float | int,
        title_color: ManimColor | str, # noqa
        description_font_size: float | int,
        description_color: ManimColor | str, # noqa
        title_number: str | int | None = None,
        title_number_color: ManimColor | str | None = None, # noqa
    ):
        super().__init__()

        self.title = title
        self.title_font_size = title_font_size
        self.title_color = (
            title_color
            if isinstance(title_color, ManimColor)
            else ManimColor(title_color)
        )

        self.description = description
        self.description_font_size = description_font_size
        self.description_color = (
            description_color
            if isinstance(description_color, ManimColor)
            else ManimColor(description_color)
        )

        self.title_number = title_number
        self.title_number_color = (
            title_number_color
            if isinstance(title_number_color, ManimColor)
            else ManimColor(title_number_color)
            if title_number_color is not None
            else None
        )

    def _position_objects(self, objects: list[Text]) -> None:
        if len(objects) > len(self.obj_pos):
            raise ValueError(
                f"Too many objects ({len(objects)}) for positions ({len(self.obj_pos)})"
            )
        for obj, position in zip(objects, self.obj_pos):
            obj.shift(position)

    def create(self) -> 'Title':
        objects: list[Text] = []

        if (
            self.title_number is not None
            and self.title_number_color is not None
        ):
            objects.append(
                Text(
                    str(self.title_number),
                    font_size=self.title_font_size,
                    color=self.title_number_color,
                    fill_opacity=self.DEFAULT_FILL_OPACITY,
                )
            )

        objects.extend(
            [
                Text(
                    self.title,
                    font_size=self.title_font_size,
                    color=self.title_color,
                    fill_opacity=self.DEFAULT_FILL_OPACITY,
                ),
                Text(
                    self.description,
                    font_size=self.description_font_size,
                    color=self.description_color,
                    fill_opacity=self.DEFAULT_FILL_OPACITY,
                ),
            ]
        )

        self._position_objects(objects)
        self.add(*objects)

        return self


class Exploration(ObjectBase):
    TOP_TEXT_POS = UP * 2
    DOWN_TEXT_POS = DOWN * 3

    def __init__(
            self,
            text: str,
            text_font_size: float | int,
            text_color: ManimColor | str, # noqa
            is_top: bool = True,
    ):
        super().__init__()

        self.text = text
        self.text_font_size = text_font_size
        self.text_color = (
            text_color
            if isinstance(text_color, ManimColor)
            else ManimColor(text_color)
        )
        self.text_pos = self.TOP_TEXT_POS if is_top else self.DOWN_TEXT_POS

    def create(self) -> 'Exploration':
        text_obj = Text(
            str(self.text),
            font_size=self.text_font_size,
            color=self.text_color,
            fill_opacity=self.DEFAULT_FILL_OPACITY,
        )
        text_obj.shift(self.text_pos)
        self.add(text_obj)
        return self


class TextInSomething(ObjectBase):
    DEFAULT_FILL_OPACITY = 0.8
    VERTICAL_SHIFT_SCALE = 1.0
    HORIZONTAL_SHIFT_SCALE = 2.0
    VALID_SHIFT_DIRECTIONS = {'left', 'right', 'up', 'down'}

    def __init__(
            self,
            text: List[str] | str,
            text_font_size: List[float | int] | float | int,
            text_color: List[ManimColor | str] | ManimColor | str,
            figure_color: ManimColor | str, # noqa
            shift_direction: str | None = None,
            **kwargs
    ):
        super().__init__()

        self.text = text if isinstance(text, list) else [text]
        if not self.text or not any(self.text):
            raise ValueError("Text cannot be empty")

        if isinstance(text_font_size, list):
            if len(text_font_size) != len(self.text):
                raise ValueError("text_font_size list must have the same length as text")
            self.text_font_size = text_font_size
        else:
            self.text_font_size = [text_font_size] * len(self.text)

        if isinstance(text_color, list):
            if len(text_color) != len(self.text):
                raise ValueError("text_color list must have the same length as text")
            self.text_color = [
                x if isinstance(x, ManimColor) else ManimColor(x)
                for x in text_color
            ]
        else:
            color = text_color if isinstance(text_color, ManimColor) else ManimColor(text_color)
            self.text_color = [color] * len(self.text)

        self.figure_color = (
            figure_color
            if isinstance(figure_color, ManimColor)
            else ManimColor(figure_color)
        )

        if shift_direction:
            shift_direction = shift_direction.lower()
            if shift_direction not in self.VALID_SHIFT_DIRECTIONS:
                raise ValueError(
                    f"Invalid shift_direction: {shift_direction}. "
                    f"Must be one of {self.VALID_SHIFT_DIRECTIONS}"
                )
        self.shift_direction = shift_direction

        self._process_kwargs(kwargs)

    def _process_kwargs(self, kwargs):
        pass

    def get_figure_object(self):
        raise NotImplementedError("Subclasses must implement get_figure_object()")

    def create(self) -> 'TextInSomething':
        objects = []

        figure = self.get_figure_object()
        objects.append(figure)

        text_objects = []
        for text, font_size, color in zip(
                self.text, self.text_font_size, self.text_color
        ):
            text_obj = Text(
                text,
                font_size=font_size,
                color=color,
            )
            text_objects.append(text_obj)

        if len(text_objects) == 1:
            text_group = text_objects[0]
        else:
            text_group = VGroup(*text_objects).arrange(DOWN, buff=0.1)

        text_group.move_to(figure.get_center())

        self.add(figure, text_group)

        if self.shift_direction:
            match self.shift_direction:
                case 'left':
                    self.shift(self.HORIZONTAL_SHIFT_SCALE * LEFT)
                case 'right':
                    self.shift(self.HORIZONTAL_SHIFT_SCALE * RIGHT)
                case 'up':
                    self.shift(self.VERTICAL_SHIFT_SCALE * UP)
                case 'down':
                    self.shift(self.VERTICAL_SHIFT_SCALE * DOWN)

        return self


class TextInBox(TextInSomething):
    def __init__(
            self,
            text: List[str] | str,
            text_font_size: List[float | int] | float | int,
            text_color: List[ManimColor | str] | ManimColor | str,
            figure_color: ManimColor | str, # noqa
            box_width: float | int,
            box_height: float | int,
            shift_direction: str | None = None,
            **kwargs
    ):
        if box_width <= 0 or box_height <= 0:
            raise ValueError("box_width and box_height must be positive")
        self.box_width = box_width
        self.box_height = box_height

        super().__init__(
            text=text,
            text_font_size=text_font_size,
            text_color=text_color,
            figure_color=figure_color,
            shift_direction=shift_direction,
            **kwargs
        )

    def get_figure_object(self):
        return Rectangle(
            height=self.box_height,
            width=self.box_width,
            fill_color=self.figure_color,
            fill_opacity=self.DEFAULT_FILL_OPACITY,
            stroke_color=self.figure_color,
        )


class TextInCircle(TextInSomething):
    def __init__(
            self,
            text: List[str] | str,
            text_font_size: List[float | int] | float | int,
            text_color: List[ManimColor | str] | ManimColor | str,
            figure_color: ManimColor | str, # noqa
            circle_radius: float | int,
            shift_direction: str | None = None,
            **kwargs
    ):
        if circle_radius <= 0:
            raise ValueError("circle_radius must be positive")
        self.circle_radius = circle_radius

        super().__init__(
            text=text,
            text_font_size=text_font_size,
            text_color=text_color,
            figure_color=figure_color,
            shift_direction=shift_direction,
            **kwargs
        )

    def get_figure_object(self):
        return Circle(
            radius=self.circle_radius,
            fill_color=self.figure_color,
            fill_opacity=self.DEFAULT_FILL_OPACITY,
            stroke_color=self.figure_color,
        )


class TextInRoundedRectangle(TextInSomething):
    DEFAULT_CORNER_RADIUS = 0.2

    def __init__(
            self,
            text: List[str] | str,
            text_font_size: List[float | int] | float | int,
            text_color: List[ManimColor | str] | ManimColor | str,
            figure_color: ManimColor | str, # noqa
            box_width: float | int,
            box_height: float | int,
            corner_radius: float | int = DEFAULT_CORNER_RADIUS,
            shift_direction: str | None = None,
            **kwargs
    ):
        if box_width <= 0 or box_height <= 0:
            raise ValueError("box_width and box_height must be positive")
        if corner_radius <= 0:
            raise ValueError("corner_radius must be positive")
        self.box_width = box_width
        self.box_height = box_height
        self.corner_radius = corner_radius

        super().__init__(
            text=text,
            text_font_size=text_font_size,
            text_color=text_color,
            figure_color=figure_color,
            shift_direction=shift_direction,
            **kwargs
        )

    def get_figure_object(self):
        return RoundedRectangle(
            height=self.box_height,
            width=self.box_width,
            corner_radius=self.corner_radius,
            fill_color=self.figure_color,
            fill_opacity=self.DEFAULT_FILL_OPACITY,
            stroke_color=self.figure_color,
        )


class TextInEllipse(TextInSomething):
    def __init__(
            self,
            text: List[str] | str,
            text_font_size: List[float | int] | float | int,
            text_color: List[ManimColor | str] | ManimColor | str,
            figure_color: ManimColor | str, # noqa
            ellipse_width: float | int,
            ellipse_height: float | int,
            shift_direction: str | None = None,
            **kwargs
    ):
        if ellipse_width <= 0 or ellipse_height <= 0:
            raise ValueError("ellipse_width and ellipse_height must be positive")
        self.ellipse_width = ellipse_width
        self.ellipse_height = ellipse_height

        super().__init__(
            text=text,
            text_font_size=text_font_size,
            text_color=text_color,
            figure_color=figure_color,
            shift_direction=shift_direction,
            **kwargs
        )

    def get_figure_object(self):
        return Ellipse(
            width=self.ellipse_width,
            height=self.ellipse_height,
            fill_color=self.figure_color,
            fill_opacity=self.DEFAULT_FILL_OPACITY,
            stroke_color=self.figure_color,
        )
