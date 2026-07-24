from typing import Any

import yaml
from pathlib import Path

from manim import *


def load_config(
        config_path: str = Path('videos', '_base_animation', 'config.yaml')
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

SAFE_ZONES = CONFIG.get("safe_zones", {})
SAFE_TOP = SAFE_ZONES.get("top", 0.12)
SAFE_BOTTOM = SAFE_ZONES.get("bottom", 0.08)
SAFE_LEFT = SAFE_ZONES.get("left", 0.05)
SAFE_RIGHT = SAFE_ZONES.get("right", 0.08)
FRAME_WIDTH = config.frame_width
FRAME_HEIGHT = config.frame_height
SAFE_X_MIN = -FRAME_WIDTH/2 + FRAME_WIDTH * SAFE_LEFT
SAFE_X_MAX = FRAME_WIDTH/2 - FRAME_WIDTH * SAFE_RIGHT
SAFE_Y_MIN = -FRAME_HEIGHT/2 + FRAME_HEIGHT * SAFE_BOTTOM
SAFE_Y_MAX = FRAME_HEIGHT/2 - FRAME_HEIGHT * SAFE_TOP

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


class BaseAnimation(MovingCameraScene):
    """
    General geometry of the four zones.
    """

    def __init__(
            self, camera_class: type[Camera] = MovingCamera, **kwargs: Any
    ):
        super().__init__(camera_class, **kwargs)
        self.explanation = None
        self.subtitle = None
        self.config = None

    def station_center(self, camera_key: str) -> np.ndarray:
        """
        The center of the station is vertical.
        Each station is lower than the previous one.
        """
        return UP * self.config["camera"][camera_key]

    def zone_center(
            self,
            station_center: np.ndarray,
            top_key: str,
            bottom_key: str,
    ) -> np.ndarray:
        """
        Returns the center of a specific zone relative to the station center.
        """
        layout = self.config["layout"]

        center_x = (layout["content_left"] + layout["content_right"]) / 2
        center_x += layout["content_offset_x"]

        center_y = (layout[top_key] + layout[bottom_key]) / 2

        return station_center + RIGHT * center_x + UP * center_y

    def create_station_title(
            self,
            station_key: str,
            center: np.ndarray,
    ) -> StationTitle:
        station = self.config["stations"][station_key]

        title = StationTitle(
            station["number"],
            station["name"],
            station["description"],
            station["color"],
        )

        title.move_to(
            self.zone_center(
                center,
                "title_top",
                "title_bottom",
            )
            + RIGHT * self.config["layout"]["title_offset_x"]
        )

        return title

    def create_text(
            self,
            text: str,
            center: np.ndarray,
            font_size: int,
            color: str = TEXT_COLOR,  # noqa
            line_spacing: float | None = None,
    ) -> Text:
        kwargs: dict[str, Any] = {
            "text": text,
            "font": self.config["typography"]["font"],
            "font_size": font_size,
            "color": color,
        }

        if line_spacing is not None:
            kwargs["line_spacing"] = line_spacing

        return Text(**kwargs).move_to(center)

    def set_explanation(self, key: str, center: np.ndarray) -> None:
        """
        Shows a short thought only inside the Text Area.
        """
        cfg = self.config["text_area"]
        new_text = self.create_text(
            cfg["lines"][key],
            self.zone_center(center, "text_top", "text_bottom"),
            cfg["font_size"],
            MUTED_COLOR,
            cfg["line_spacing"],
        )
        new_text.scale_to_fit_width(cfg["max_width"])

        if self.explanation is None:
            self.explanation = new_text
            self.play(FadeIn(new_text), run_time=self.config["timing"]["text_change"])
            return

        self.play(
            ReplacementTransform(self.explanation, new_text),
            run_time=self.config["timing"]["text_change"],
        )
        self.explanation = new_text

    def set_subtitle(self, key: str, center: np.ndarray) -> None:
        """
        Shows the replica only inside the Subtitle Area.
        """
        cfg = self.config["subtitles"]
        new_text = self.create_text(
            cfg["lines"][key],
            self.zone_center(center, "subtitles_top", "subtitles_bottom"),
            cfg["font_size"],
            TEXT_COLOR,
            cfg["line_spacing"],
        )
        new_text.scale_to_fit_width(cfg["max_width"])

        if self.subtitle is None:
            self.subtitle = new_text
            self.play(FadeIn(new_text), run_time=self.config["timing"]["subtitle_change"])
            return

        self.play(
            ReplacementTransform(self.subtitle, new_text),
            run_time=self.config["timing"]["subtitle_change"],
        )
        self.subtitle = new_text

    def clear_station_text(self) -> None:
        animations: list[Animation] = []

        if self.subtitle is not None:
            animations.append(FadeOut(self.subtitle))
            self.subtitle = None

        if self.explanation is not None:
            animations.append(FadeOut(self.explanation))
            self.explanation = None

        if animations:
            self.play(*animations, run_time=self.config["timing"]["station_fade"])

    def move_to_station(self, camera_key: str) -> None:
        self.clear_station_text()
        self.play(
            self.camera.frame.animate.move_to(self.station_center(camera_key)),  # noqa
            run_time=self.config["camera"]["move_duration"],
            rate_func=smooth,
        )
