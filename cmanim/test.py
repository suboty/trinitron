from src.text import (
    Title,
    Exploration,
    TextInBox,
    TextInCircle,
    TextInRoundedRectangle,
    TextInEllipse
)
from src.colors import PALETTES
from src.base import SceneBase, SceneFormat, FadeIn, FadeOut
from src.objects import VerticalSteps, TextStep, HorizontalSteps, Conveyor
from src.entities import FigureTypesForText
from src.table import Table, TableCell
from src.graph import Graph


class TestScene(SceneBase):
    palette_colors = PALETTES.get('dark')

    def __init__(self, scene_format=SceneFormat.FULL_HD, **kwargs):
        super().__init__(
            scene_format=scene_format,
            **kwargs
        )

    def construct(self):
        title = Title(
            title="Test Title",
            title_font_size=40,
            title_color=self.palette_colors.primary,
            description="Test description",
            description_font_size=20,
            description_color=self.palette_colors.text,
            title_number="01",
            title_number_color=self.palette_colors.secondary,
        ).create()

        exp_top = Exploration(
            text="Test Exploration top",
            text_font_size=20,
            text_color=self.palette_colors.text,
            is_top=True,
        ).create()

        exp_down = Exploration(
            text="Test Exploration down",
            text_font_size=20,
            text_color=self.palette_colors.text,
            is_top=False,
        ).create()

        title.animate_in(self, run_time=2)
        exp_top.animate_in(self, run_time=2)
        exp_down.animate_in(self, run_time=2)
        self.wait(0.5)

        shapes = [
            TextInBox(
                text="Box",
                text_font_size=30,
                text_color=self.palette_colors.text,
                figure_color=self.palette_colors.accent,
                box_width=2.0,
                box_height=1.0,
                shift_direction='up',
            ).create(),
            TextInCircle(
                text="Circle",
                text_font_size=30,
                text_color=self.palette_colors.text,
                figure_color=self.palette_colors.accent,
                circle_radius=0.8,
                shift_direction='down',
            ).create(),
            TextInRoundedRectangle(
                text="Rounded",
                text_font_size=30,
                text_color=self.palette_colors.text,
                figure_color=self.palette_colors.accent,
                box_width=2.0,
                box_height=1.0,
                corner_radius=0.4,
                shift_direction='left',
            ).create(),
            TextInEllipse(
                text="Ellipse",
                text_font_size=30,
                text_color=self.palette_colors.text,
                figure_color=self.palette_colors.accent,
                ellipse_width=2.0,
                ellipse_height=1.2,
                shift_direction='right',
            ).create(),
        ]

        self.play(*[FadeIn(shape) for shape in shapes])
        self.wait(0.5)
        self.play(*[FadeOut(shape) for shape in shapes])
        self.wait(0.3)

        steps_data = [
            TextStep(
                text="Step 1",
                text_font_size=20,
                text_color=self.palette_colors.text,
                figure_width=2.0,
                figure_color=self.palette_colors.accent,
            ),
            TextStep(
                text=["Step 2", "sub"],
                text_font_size=[20, 14],
                text_color=[self.palette_colors.text, self.palette_colors.text],
                figure_width=2.0,
                figure_color=self.palette_colors.accent,
            ),
            TextStep(
                text="Step 3",
                text_font_size=20,
                text_color=self.palette_colors.text,
                figure_width=2.0,
                figure_color=self.palette_colors.accent,
            ),
            TextStep(
                text="Step 4",
                text_font_size=20,
                text_color=self.palette_colors.text,
                figure_width=2.0,
                figure_color=self.palette_colors.accent,
            ),
        ]

        for shape in [
            FigureTypesForText.box,
            FigureTypesForText.circle,
            FigureTypesForText.rounded,
            FigureTypesForText.ellipse,
        ]:
            params = {"corner_radius": 0.2} if shape == FigureTypesForText.rounded else {}
            steps = VerticalSteps(
                steps=steps_data[:3],
                figure_height=0.8,
                figure_color=self.palette_colors.warning,
                arrow_color=self.palette_colors.danger,
                shape=shape,
                shape_params=params,
            ).create()
            steps.animate_in(self, run_time=1)
            self.wait(0.2)
            steps.animate_out(self, run_time=0.5)

        # For SHORTS 4 steps are not recommended
        for count in [2, 3, 4]:
            steps = HorizontalSteps(
                steps=steps_data[:count],
                figure_height=0.8,
                figure_color=self.palette_colors.accent,
                arrow_color=self.palette_colors.secondary,
                shape=FigureTypesForText.rounded,
                shape_params={"corner_radius": 0.3},
            ).create()
            steps.animate_in(self, run_time=0.8)
            self.wait(0.2)
            steps.animate_out(self, run_time=0.4)

        conveyor_data = [
            TextStep(
                text=f"Item {i+1}",
                text_font_size=24,
                text_color=self.palette_colors.text,
                figure_width=2.0,
                figure_color=self.palette_colors.accent,
            ) for i in range(6)
        ]

        for shape in [
            FigureTypesForText.box,
            FigureTypesForText.circle,
            FigureTypesForText.ellipse,
        ]:
            params = {"radius": 0.6} if shape == FigureTypesForText.circle else {}
            conveyor = Conveyor(
                items=conveyor_data,
                figure_height=1.0,
                figure_color=self.palette_colors.success,
                visible_count=3,
                shape=shape,
                shape_params=params,
            ).create()
            conveyor.animate_in(self, run_time=1.0, is_fast=True)
            self.wait(0.3)
            conveyor.animate_out(self, run_time=0.8)

        table_data = [
            [
                TableCell(
                    text="Header", text_font_size=24,
                    text_color=self.palette_colors.text, box_color=self.palette_colors.accent
                ),
                TableCell(
                    text="Col1", text_font_size=24,
                    text_color=self.palette_colors.text, box_color=self.palette_colors.accent
                ),
                TableCell(
                    text="Col2", text_font_size=24,
                    text_color=self.palette_colors.text, box_color=self.palette_colors.accent
                ),
            ],
            [
                TableCell(
                    text="Row1", text_font_size=20,
                    text_color=self.palette_colors.text, box_color=self.palette_colors.accent
                ),
                TableCell(
                    text="Data1", text_font_size=20,
                    text_color=self.palette_colors.text, box_color=self.palette_colors.accent
                ),
                TableCell(
                    text="Data2", text_font_size=20,
                    text_color=self.palette_colors.text, box_color=self.palette_colors.accent
                ),
            ],
            [
                TableCell(
                    text="Row2", text_font_size=20,
                    text_color=self.palette_colors.text, box_color=self.palette_colors.accent
                ),
                TableCell(
                    text="Data3", text_font_size=20,
                    text_color=self.palette_colors.text, box_color=self.palette_colors.accent
                ),
                TableCell(
                    text="Data4", text_font_size=20,
                    text_color=self.palette_colors.text, box_color=self.palette_colors.accent
                ),
            ],
            [
                TableCell(
                    text="Row3", text_font_size=20,
                    text_color=self.palette_colors.text, box_color=self.palette_colors.accent
                ),
                TableCell(
                    text="Data5", text_font_size=20,
                    text_color=self.palette_colors.text, box_color=self.palette_colors.accent
                ),
                TableCell(
                    text="Data6", text_font_size=20,
                    text_color=self.palette_colors.text, box_color=self.palette_colors.accent
                ),
            ],
        ]

        table = Table(
            data=table_data,
            cell_width=2.0,
            cell_height=0.5,
            spacing=0.15,
        ).create()

        table.animate_in(self, run_time=1.5)
        self.wait(0.5)

        table.highlight_cell(
            row=1, col=1,
            text_color=self.palette_colors.text_invert,
            color=self.palette_colors.warning, scene=self
        )
        self.wait(0.3)
        table.highlight_row(
            row=2, color=self.palette_colors.success,
            text_color=self.palette_colors.text_invert, scene=self
        )
        self.wait(0.3)
        table.highlight_col(
            col=2, color=self.palette_colors.danger,
            text_color=self.palette_colors.text_invert, scene=self
        )
        self.wait(0.5)

        table.animate_out(self, run_time=0.8)

        graph = Graph(
            nodes=["A", "B", "C", "D", "E"],
            edges=[(0, 1), (1, 2), (2, 3), (3, 4), (4, 0), (0, 2)],
            node_color=self.palette_colors.accent,
            node_radius=0.4,
            edge_color=self.palette_colors.success,
            shape=FigureTypesForText.circle,
            max_iterations=100,
        ).create()

        graph.animate_in(self, run_time=2, lag_ratio=0.1)
        self.wait(1)

        graph.highlight_node(
            0, self.palette_colors.text_invert,
            self.palette_colors.secondary, self
        )
        self.wait(0.5)
        graph.highlight_edge(0, self.palette_colors.danger, self)
        self.wait(1)

        graph.animate_out(self, run_time=1)

        exp_top.animate_out(self, run_time=2)
        exp_down.animate_out(self, run_time=2)
        title.animate_out(self, run_time=2)


class TestSceneShorts(TestScene):
    def __init__(self, **kwargs):
        super().__init__(
            scene_format=SceneFormat.SHORTS,
            **kwargs
        )
