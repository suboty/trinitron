from dataclasses import dataclass

from manim import *


@dataclass
class PaletteTheme:
    background: ManimColor | str # noqa
    text: ManimColor | str # noqa
    accent: ManimColor | str # noqa
    primary: ManimColor | str # noqa
    secondary: ManimColor | str # noqa
    success: ManimColor | str # noqa
    warning: ManimColor | str # noqa
    danger: ManimColor | str # noqa
    text_invert: ManimColor | str # noqa

    def __post_init__(self):
        self.background = self._to_color(self.background)
        self.text = self._to_color(self.text)
        self.accent = self._to_color(self.accent)
        self.primary = self._to_color(self.primary)
        self.secondary = self._to_color(self.secondary)
        self.success = self._to_color(self.success)
        self.warning = self._to_color(self.warning)
        self.danger = self._to_color(self.danger)
        self.text_invert = self._to_color(self.text_invert)

    @staticmethod
    def _to_color(
            color: ManimColor | str # noqa
    ) -> ManimColor:
        if isinstance(color, ManimColor):
            return color
        return ManimColor(color)


PALETTES = {
    'dark': PaletteTheme(
        background=BLACK,
        text=WHITE,
        text_invert=BLACK,
        accent=TEAL,
        primary=BLUE,
        secondary=PURPLE,
        success=GREEN,
        warning=YELLOW,
        danger=RED,
    ),
    # TODO: add new themes
}
