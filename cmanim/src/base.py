from enum import Enum
from dataclasses import dataclass

from manim import *


class ObjectBase(VGroup):
    DEFAULT_FILL_OPACITY = 0.75
    DEFAULT_DURATION = 2.0
    DEFAULT_LAG_RATIO = 0.15

    def animate_in(
            self,
            scene: Scene,
            run_time: float = DEFAULT_DURATION,
            **kwargs,
    ) -> None:
        if not self.submobjects:
            return

        for obj in self:
            obj.set_fill(opacity=0)
            obj.set_stroke(opacity=0)

        scene.add(self)

        scene.play(
            AnimationGroup(
                *[
                    obj.animate
                    .set_fill(opacity=self.DEFAULT_FILL_OPACITY)
                    .set_stroke(opacity=1)
                    for obj in self
                ],
                lag_ratio=self.DEFAULT_LAG_RATIO,
            ),
            run_time=run_time,
        )

    def animate_out(
            self,
            scene: Scene,
            run_time: float = 1,
            **kwargs,
    ) -> None:
        if not self.submobjects:
            return

        scene.play(
            AnimationGroup(
                *[
                    obj.animate
                    .set_fill(opacity=0)
                    .set_stroke(opacity=0)
                    for obj in self
                ],
                lag_ratio=self.DEFAULT_LAG_RATIO,
            ),
            run_time=run_time,
        )

        scene.remove(self)


class SceneFormat(Enum):
    FULL_HD = "full_hd"  # 1920x1080 (16:9)
    SHORTS = "shorts"  # 1080x1920 (9:16)


@dataclass
class SceneSettings:
    frame_width: float
    frame_height: float
    top_limit: float
    bottom_limit: float
    left_limit: float
    right_limit: float
    pixel_width: int
    pixel_height: int


class SceneBase(Scene):
    FORMAT_CONFIGS = {
        SceneFormat.FULL_HD: SceneSettings(
            frame_width=16.0,
            frame_height=9.0,
            top_limit=2.25,
            bottom_limit=-2.25,
            left_limit=-4.0,
            right_limit=4.0,
            pixel_width=1920,
            pixel_height=1080,
        ),
        SceneFormat.SHORTS: SceneSettings(
            frame_width=9.0,
            frame_height=16.0,
            top_limit=4.0,
            bottom_limit=-4.0,
            left_limit=-2.25,
            right_limit=2.25,
            pixel_width=1080,
            pixel_height=1920,
        ),
    }

    def __init__(
            self,
            scene_format: SceneFormat = SceneFormat.FULL_HD,
            **kwargs
    ):
        scene_config = self.FORMAT_CONFIGS[scene_format]

        from manim import config
        config.pixel_width = scene_config.pixel_width
        config.pixel_height = scene_config.pixel_height
        config.frame_width = scene_config.frame_width
        config.frame_height = scene_config.frame_height

        super().__init__(**kwargs)

        self.RIGHT_LIMIT = None
        self.LEFT_LIMIT = None
        self.BOTTOM_LIMIT = None
        self.TOP_LIMIT = None
        self.scene_config = None
        self.scene_format = scene_format
        self._setup_format()

    def _setup_format(self):
        scene_config = self.FORMAT_CONFIGS[self.scene_format]

        self.frame_width = scene_config.frame_width
        self.frame_height = scene_config.frame_height
        self.TOP_LIMIT = scene_config.top_limit
        self.BOTTOM_LIMIT = scene_config.bottom_limit
        self.LEFT_LIMIT = scene_config.left_limit
        self.RIGHT_LIMIT = scene_config.right_limit

        self.camera.frame_width = self.frame_width
        self.camera.frame_height = self.frame_height

        if hasattr(self.camera, 'aspect_ratio'):
            self.camera.aspect_ratio = self.frame_width / self.frame_height

    def set_scene_settings(
            self,
            scene_config: SceneFormat = None,
            top_limit: float = None,
            bottom_limit: float = None,
            left_limit: float = None,
            right_limit: float = None,
    ) -> None:
        if scene_config:
            self.scene_config = scene_config
            self._setup_format()

        if top_limit is not None:
            self.TOP_LIMIT = top_limit
        if bottom_limit is not None:
            self.BOTTOM_LIMIT = bottom_limit
        if left_limit is not None:
            self.LEFT_LIMIT = left_limit
        if right_limit is not None:
            self.RIGHT_LIMIT = right_limit

        if any([top_limit, bottom_limit, left_limit, right_limit]):
            self.camera.frame_width = self.RIGHT_LIMIT - self.LEFT_LIMIT
            self.camera.frame_height = self.TOP_LIMIT - self.BOTTOM_LIMIT
            if hasattr(self.camera, 'aspect_ratio'):
                self.camera.aspect_ratio = self.camera.frame_width / self.camera.frame_height


class FadeIn(FadeIn):
    ...


class FadeOut(FadeOut):
    ...
