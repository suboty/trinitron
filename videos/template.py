"""
DESCRIPTION
"""


from cmanim import (
    SceneBase,
    SceneFormat,
    PALETTES,
)


class EPISODEAnimation(SceneBase):
    palette_colors = PALETTES.get('dark')

    def __init__(self, scene_format=SceneFormat.FULL_HD, **kwargs):
        super().__init__(
            scene_format=scene_format,
            **kwargs
        )

    def construct(self):
        pass


class EPISODEAnimationShorts(EPISODEAnimation):
    def __init__(self, **kwargs):
        super().__init__(
            scene_format=SceneFormat.SHORTS,
            **kwargs
        )
