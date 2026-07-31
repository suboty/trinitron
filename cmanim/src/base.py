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
