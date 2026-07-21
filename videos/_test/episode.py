from typing import Any

from common import *


def load_scene_config(
    config_path: str = Path("videos", "_test", "config.yaml"),
) -> dict:
    with open(config_path, "r", encoding="utf-8") as file:
        return yaml.safe_load(file)


SCENE_CONFIG = load_scene_config()


class TestAnimation(MovingCameraScene):
    def __init__(
        self,
        camera_class: type[Camera] = MovingCamera,
        **kwargs: Any,
    ) -> None:
        super().__init__(camera_class, **kwargs)

        self.config = SCENE_CONFIG["test"]

    def construct(self) -> None:
        camera_config = self.config["camera"]

        self.camera.background_color = BACKGROUND
        self.camera.frame.width = camera_config["frame_width"] # noqa

        scenes = self.create_scene_definitions()

        first_scene = scenes[0]

        self.camera.frame.move_to( # noqa
            UP * first_scene["y_position"]
        )

        for scene in scenes:
            overlay = self.create_overlay(
                center=UP * scene["y_position"],
                scene_number=scene["number"],
                scene_name=scene["name"],
                scene_color=scene["color"],
            )

            self.add(overlay)

        self.wait(
            camera_config["initial_wait_duration"]
        )

        for scene in scenes[1:]:
            self.play(
                self.camera.frame.animate.move_to( # noqa
                    UP * scene["y_position"]
                ),
                run_time=camera_config["move_duration"],
                rate_func=smooth,
            )

        self.wait(
            camera_config["final_wait_duration"]
        )

    def create_scene_definitions(self) -> list[dict]:
        camera_config = self.config["camera"]

        scenes = []

        for scene_config in self.config["scenes"]:
            camera_position_key = scene_config["camera_position"]

            scenes.append({
                "number": scene_config["number"],
                "name": scene_config["name"],
                "y_position": camera_config[camera_position_key],
                "color": scene_config["color"],
            })

        return scenes

    def create_overlay(
        self,
        center: np.ndarray,
        scene_number: str,
        scene_name: str,
        scene_color: str,
    ) -> VGroup:
        content_config = self.config["content"]

        content_left = content_config["left"]
        content_right = content_config["right"]

        content_width = content_right - content_left
        content_center_x = (content_left + content_right) / 2

        frame = self.create_frame(center)

        title_zone = self.create_zone(
            center=center,
            center_x=content_center_x,
            width=content_width,
            zone_config=self.config["title_zone"],
        )

        animation_zone = self.create_zone(
            center=center,
            center_x=content_center_x,
            width=content_width,
            zone_config=self.config["animation_zone"],
        )

        text_zone = self.create_zone(
            center=center,
            center_x=content_center_x,
            width=content_width,
            zone_config=self.config["text_zone"],
        )

        subtitles_zone = self.create_zone(
            center=center,
            center_x=content_center_x,
            width=content_width,
            zone_config=self.config["subtitles_zone"],
        )

        station_title = self.create_station_title(
            zone=title_zone,
            scene_number=scene_number,
            scene_name=scene_name,
            scene_color=scene_color,
        )

        animation_content = self.create_zone_content(
            zone=animation_zone,
            content_config=self.config["animation_zone"]["content"],
        )

        text_content = self.create_zone_content(
            zone=text_zone,
            content_config=self.config["text_zone"]["content"],
        )

        subtitles_content = self.create_zone_content(
            zone=subtitles_zone,
            content_config=self.config["subtitles_zone"]["content"],
        )

        title_label = self.create_zone_label(
            zone=title_zone,
            label_config=self.config["title_zone"]["label"],
        )

        animation_label = self.create_zone_label(
            zone=animation_zone,
            label_config=self.config["animation_zone"]["label"],
        )

        text_label = self.create_zone_label(
            zone=text_zone,
            label_config=self.config["text_zone"]["label"],
        )

        subtitles_label = self.create_zone_label(
            zone=subtitles_zone,
            label_config=self.config["subtitles_zone"]["label"],
        )

        return VGroup(
            frame,
            title_zone,
            title_label,
            station_title,
            animation_zone,
            animation_label,
            animation_content,
            text_zone,
            text_label,
            text_content,
            subtitles_zone,
            subtitles_label,
            subtitles_content,
        )

    def create_frame(
        self,
        center: np.ndarray,
    ) -> Rectangle:
        camera_config = self.config["camera"]
        frame_config = self.config["frame"]

        frame = Rectangle( # noqa
            width=camera_config["frame_width"],
            height=camera_config["frame_height"],
            stroke_color=frame_config["stroke_color"],
            stroke_width=frame_config["stroke_width"],
            fill_opacity=0,
        )

        frame.move_to(center)

        return frame

    def create_station_title(
        self,
        zone: Mobject,
        scene_number: str,
        scene_name: str,
        scene_color: str,
    ) -> StationTitle:
        title_config = self.config["title_zone"]["station_title"]

        station_title = StationTitle(
            scene_number,
            scene_name,
            title_config["subtitle"],
            scene_color,
        )

        station_title.move_to(zone)

        return station_title

    @staticmethod
    def create_zone(
        center: np.ndarray,
        center_x: float,
        width: float,
        zone_config: dict,
    ) -> RoundedRectangle:
        top = zone_config["top"]
        bottom = zone_config["bottom"]

        zone = RoundedRectangle(
            width=width,
            height=top - bottom,
            corner_radius=zone_config["corner_radius"],
            stroke_color=zone_config["color"],
            stroke_width=zone_config["stroke_width"],
            fill_color=zone_config["color"],
            fill_opacity=zone_config["fill_opacity"],
        )

        zone.move_to(
            np.array([
                center_x,
                center[1] + (top + bottom) / 2,
                0,
            ])
        )

        return zone

    @staticmethod
    def create_zone_content(
        zone: Mobject,
        content_config: dict,
    ) -> Text:
        content = Text(
            content_config["text"],
            font=content_config["font"],
            font_size=content_config["font_size"],
            color=content_config["color"],
        )

        content.move_to(zone)

        return content

    @staticmethod
    def create_zone_label(
        zone: Mobject,
        label_config: dict,
    ) -> Text:
        label = Text(
            label_config["text"],
            font=label_config["font"],
            font_size=label_config["font_size"],
            color=label_config["color"],
        )

        upper_left_corner = zone.get_corner(UL)

        label.move_to(
            upper_left_corner
            + RIGHT * label_config["offset_x"]
            + DOWN * abs(label_config["offset_y"]),
            aligned_edge=UL,
        )

        return label
