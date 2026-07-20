from __future__ import annotations

import yaml
from pathlib import Path

from manim import *


def load_config(
        config_path: str = Path('videos', 'config.yaml')
) -> dict:
    with open(config_path, "r") as f:
        return yaml.safe_load(f)


CONFIG = load_config()

# Video settings
config.pixel_width = CONFIG["video"]["pixel_width"]
config.pixel_height = CONFIG["video"]["pixel_height"]
config.frame_width = CONFIG["video"]["frame_width"]
config.frame_height = config.frame_width * CONFIG["video"]["frame_height_ratio"] / 9
config.frame_rate = CONFIG["video"]["frame_rate"]

# Colors
BACKGROUND = CONFIG["colors"]["background"]
config.background_color = BACKGROUND

TEXT_COLOR = CONFIG["colors"]["text"]
MUTED_COLOR = CONFIG["colors"]["muted"]
BORDER_COLOR = CONFIG["colors"]["border"]
BELT_COLOR = CONFIG["colors"]["belt"]

KEYWORD_COLOR = CONFIG["colors"]["keyword"]
IDENTIFIER_COLOR = CONFIG["colors"]["identifier"]
OPERATOR_COLOR = CONFIG["colors"]["operator"]
NUMBER_COLOR = CONFIG["colors"]["number"]
PUNCTUATION_COLOR = CONFIG["colors"]["punctuation"]

ACCENT_COLOR = KEYWORD_COLOR


class CharacterCell(VGroup):
    def __init__(
            self,
            character: str,
            width: float = None,
            height: float = None,
    ) -> None:
        super().__init__()

        if width is None:
            width = CONFIG["character_cell"]["default_width"]
        if height is None:
            height = CONFIG["character_cell"]["default_height"]

        self.character = character

        box = RoundedRectangle(
            width=width,
            height=height,
            corner_radius=CONFIG["character_cell"]["corner_radius"],
            stroke_color=BORDER_COLOR,
            stroke_width=CONFIG["character_cell"]["stroke_width"],
            fill_color=BACKGROUND,
            fill_opacity=1,
        )

        displayed_character = "·" if character == " " else character

        glyph = Text(
            displayed_character,
            font="Menlo",
            font_size=CONFIG["character_cell"]["font_size"],
            color=MUTED_COLOR if character == " " else TEXT_COLOR,
        )
        glyph.move_to(box)

        self.box = box
        self.glyph = glyph

        self.add(box, glyph)

    def highlight(self, color: str) -> AnimationGroup:
        return AnimationGroup(
            self.box.animate.set_stroke(
                color,
                width=CONFIG["character_cell"]["highlight_stroke_width"]
            ),
            self.glyph.animate.set_color(color).set_opacity(1),
        )

    def reset_style(self) -> AnimationGroup:
        normal_color = (
            MUTED_COLOR
            if self.character == " "
            else TEXT_COLOR
        )

        return AnimationGroup(
            self.box.animate
            .set_stroke(BORDER_COLOR, width=CONFIG["character_cell"]["stroke_width"])
            .set_opacity(1),
            self.glyph.animate
            .set_color(normal_color)
            .set_opacity(1),
        )

    def consume(self) -> AnimationGroup:
        return AnimationGroup(
            self.box.animate
            .set_stroke(BORDER_COLOR, width=CONFIG["character_cell"]["stroke_width"])
            .set_opacity(CONFIG["character_cell"]["consumed_opacity"]),
            self.glyph.animate
            .set_color(MUTED_COLOR)
            .set_opacity(CONFIG["character_cell"]["consumed_glyph_opacity"]),
        )


class TokenCard(VGroup):
    def __init__(
            self,
            token_type: str,
            value: str,
            color: str,
            width: float = None,
            height: float = None,
            font_size: int = None,
    ) -> None:
        super().__init__()

        if width is None:
            width = CONFIG["token_card"]["default_width"]
        if height is None:
            height = CONFIG["token_card"]["default_height"]
        if font_size is None:
            font_size = CONFIG["token_card"]["font_size"]

        box = RoundedRectangle(
            width=width,
            height=height,
            corner_radius=CONFIG["token_card"]["corner_radius"],
            stroke_color=color,
            stroke_width=CONFIG["token_card"]["stroke_width"],
            fill_color=color,
            fill_opacity=CONFIG["token_card"]["fill_opacity"],
        )

        type_label = Text(
            token_type,
            font="Menlo",
            font_size=font_size - CONFIG["token_card"]["type_label_font_size_offset"],
            color=color,
        )

        value_label = Text(
            value,
            font="Menlo",
            font_size=font_size,
            color=TEXT_COLOR,
        )

        labels = VGroup(type_label, value_label)
        labels.arrange(DOWN, buff=CONFIG["token_card"]["labels_buff"])
        labels.move_to(box)

        self.add(box, labels)


class StationTitle(VGroup):
    def __init__(
            self,
            number: str,
            title: str,
            subtitle: str,
            color: str,
    ) -> None:
        super().__init__()

        number_text = Text(
            number,
            font="Menlo",
            font_size=CONFIG["station_title"]["number_font_size"],
            color=color,
        )

        title_text = Text(
            title,
            font="Menlo",
            font_size=CONFIG["station_title"]["title_font_size"],
            weight=BOLD,
            color=TEXT_COLOR,
        )

        subtitle_text = Text(
            subtitle,
            font="Menlo",
            font_size=CONFIG["station_title"]["subtitle_font_size"],
            color=MUTED_COLOR,
        )

        heading = VGroup(number_text, title_text)
        heading.arrange(RIGHT, buff=CONFIG["station_title"]["heading_buff"])

        content = VGroup(heading, subtitle_text)
        content.arrange(
            DOWN,
            aligned_edge=LEFT,
            buff=CONFIG["station_title"]["content_buff"],
        )

        underline = Line(
            LEFT,
            RIGHT,
            color=color,
            stroke_width=CONFIG["station_title"]["underline_stroke_width"],
        )
        underline.width = min(
            content.width,
            CONFIG["station_title"]["max_underline_width"]
        )
        underline.next_to(content, DOWN, buff=CONFIG["station_title"]["underline_buff"])

        self.add(content, underline)
