"""
Semantic analysis is the third part of compiler frontend.
The main aim of that step is verifying an abstract syntax tree.

First, we get an AST from syntax analysis.
The structure can be correct, but its meaning can still be wrong.

For verification, we use information about identifiers and their types.
For example, variables a and b are integers, so the result of a + b is also an integer.

Then we check the function call.
If max accepts integer values, both arguments are correct and the result is also an integer.

The result of semantic analysis is a verified abstract syntax tree.
Now this tree is ready for the next compiler steps.
"""


from cmanim import (
    SceneBase,
    SceneFormat,
    PALETTES,
    Title,
    FigureTypesForText,
    Exploration,
    Graph,
    Table,
    TableCell,
    VerticalSteps,
    TextStep
)


class SemanticAnimation(SceneBase):
    palette_colors = PALETTES.get('dark')

    def __init__(self, scene_format=SceneFormat.FULL_HD, **kwargs):
        super().__init__(
            scene_format=scene_format,
            **kwargs
        )

    def construct(self):
        semantic_rules = [
            'a -> int',
            'b -> int',
            'a + b -> int',
            '42 -> int',
            'max(int, int) -> int'
        ]

        # Preview

        title = Title(
            title='Semantic Analysis',
            description='But is an AST really correct?',
            title_font_size=50,
            title_color=self.palette_colors.accent,
            description_font_size=30,
            description_color=self.palette_colors.text,
        ).create()
        title.animate_in(self, run_time=1)

        graph = Graph(
            nodes=["max", "+", "a", "b", "42"],
            edges=[(0, 1), (1, 2), (1, 3), (0, 4)],
            node_color=self.palette_colors.accent,
            node_radius=0.4,
            edge_color=self.palette_colors.success,
            shape=FigureTypesForText.circle,
            max_iterations=100,
            TOP_LIMIT=1.0,
            RIGHT_LIMIT=2.0,
            LEFT_LIMIT=-2.0,
            BOTTOM_LIMIT=-2.0,
        ).create()
        graph.animate_in(self, run_time=2, lag_ratio=0.1)

        graph.highlight_node(
            1,
            self.palette_colors.text_invert,
            self.palette_colors.secondary,
            self,
        )

        self.wait(1.0)

        graph.animate_out(self, run_time=0.5, lag_ratio=0.1)
        title.animate_out(self, run_time=0.5, lag_ratio=0.1)

        # Step 1: Get an AST

        title = Title(
            title='Abstract Syntax Tree',
            description='Getting an AST from syntax analysis',
            title_font_size=50,
            title_color=self.palette_colors.accent,
            description_font_size=30,
            description_color=self.palette_colors.text,
        ).create()
        title.animate_in(self, run_time=1)

        exp = Exploration(
            text="The AST structure is correct",
            text_font_size=25,
            text_color=self.palette_colors.text,
            is_top=False,
        ).create()
        exp.animate_in(self, run_time=0.5)

        graph = Graph(
            nodes=["max", "+", "a", "b", "42"],
            edges=[(0, 1), (1, 2), (1, 3), (0, 4)],
            node_color=self.palette_colors.accent,
            node_radius=0.4,
            edge_color=self.palette_colors.success,
            shape=FigureTypesForText.circle,
            max_iterations=100,
            TOP_LIMIT=1.0,
            RIGHT_LIMIT=2.0,
            LEFT_LIMIT=-2.0,
            BOTTOM_LIMIT=-2.0,
        ).create()
        graph.animate_in(self, run_time=2, lag_ratio=0.1)

        self.wait(1.0)

        exp.animate_out(self, run_time=0.5)

        exp = Exploration(
            text="But now we need to check its meaning",
            text_font_size=25,
            text_color=self.palette_colors.text,
            is_top=False,
        ).create()
        exp.animate_in(self, run_time=0.5)

        self.wait(1.0)

        exp.animate_out(self, run_time=0.5)
        graph.animate_out(self, run_time=0.5)
        title.animate_out(self, run_time=0.5)

        # Step 2: Get identifier types

        title = Title(
            title='Symbol Table',
            description='Getting information about identifiers',
            title_font_size=50,
            title_color=self.palette_colors.accent,
            description_font_size=30,
            description_color=self.palette_colors.text,
        ).create()
        title.animate_in(self, run_time=1)

        table_data = [
            [
                TableCell(
                    text="Name", text_font_size=25,
                    text_color=self.palette_colors.text,
                    box_color=self.palette_colors.secondary
                ),
                TableCell(
                    text="Type", text_font_size=25,
                    text_color=self.palette_colors.text,
                    box_color=self.palette_colors.secondary
                ),
            ],
            [
                TableCell(
                    text="a", text_font_size=30,
                    text_color=self.palette_colors.text,
                    box_color=self.palette_colors.accent
                ),
                TableCell(
                    text="int", text_font_size=30,
                    text_color=self.palette_colors.text,
                    box_color=self.palette_colors.accent
                ),
            ],
            [
                TableCell(
                    text="b", text_font_size=30,
                    text_color=self.palette_colors.text,
                    box_color=self.palette_colors.accent
                ),
                TableCell(
                    text="int", text_font_size=30,
                    text_color=self.palette_colors.text,
                    box_color=self.palette_colors.accent
                ),
            ],
            [
                TableCell(
                    text="max", text_font_size=30,
                    text_color=self.palette_colors.text,
                    box_color=self.palette_colors.accent
                ),
                TableCell(
                    text="int", text_font_size=30,
                    text_color=self.palette_colors.text,
                    box_color=self.palette_colors.accent
                ),
            ],
        ]

        table = Table(
            data=table_data,
            cell_width=3.0,
            cell_height=0.5,
            spacing=0.15,
            MAX_ROWS=5
        ).create()

        table.animate_in(self, run_time=1.5)

        exp = Exploration(
            text="Semantic analysis uses types from the symbol table",
            text_font_size=25,
            text_color=self.palette_colors.text,
            is_top=False,
        ).create()
        exp.animate_in(self, run_time=0.5)

        self.wait(1.0)

        exp.animate_out(self, run_time=0.5)
        table.animate_out(self, run_time=1.0)
        title.animate_out(self, run_time=0.5)

        # Step 3: Check expression types

        title = Title(
            title='Type Checking',
            description='Checking expression types step by step',
            title_font_size=50,
            title_color=self.palette_colors.accent,
            description_font_size=30,
            description_color=self.palette_colors.text,
        ).create()
        title.animate_in(self, run_time=1)

        graph = Graph(
            nodes=["max", "+", "a", "b", "42"],
            edges=[(0, 1), (1, 2), (1, 3), (0, 4)],
            node_color=self.palette_colors.accent,
            node_radius=0.4,
            edge_color=self.palette_colors.success,
            shape=FigureTypesForText.circle,
            max_iterations=100,
            TOP_LIMIT=1.0,
            RIGHT_LIMIT=2.0,
            LEFT_LIMIT=-2.0,
            BOTTOM_LIMIT=-2.0,
        ).create()
        graph.animate_in(self, run_time=2, lag_ratio=0.1)

        exp_bottom = Exploration(
            text="Variables a and b are integers",
            text_font_size=25,
            text_color=self.palette_colors.text,
            is_top=False,
        ).create()
        exp_bottom.animate_in(self, run_time=0.5)

        graph.highlight_node(
            2,
            self.palette_colors.text_invert,
            self.palette_colors.secondary,
            self,
        )

        graph.highlight_node(
            3,
            self.palette_colors.text_invert,
            self.palette_colors.secondary,
            self,
        )

        self.wait(0.5)

        exp_bottom.animate_out(self, run_time=0.5)

        exp_bottom = Exploration(
            text="So a + b must also be an integer",
            text_font_size=25,
            text_color=self.palette_colors.text,
            is_top=False,
        ).create()
        exp_bottom.animate_in(self, run_time=0.5)

        graph.highlight_node(
            1,
            self.palette_colors.text_invert,
            self.palette_colors.secondary,
            self,
        )

        self.wait(0.5)

        exp_bottom.animate_out(self, run_time=0.5)

        exp_bottom = Exploration(
            text="The second argument 42 is also an integer",
            text_font_size=25,
            text_color=self.palette_colors.text,
            is_top=False,
        ).create()
        exp_bottom.animate_in(self, run_time=0.5)

        graph.highlight_node(
            4,
            self.palette_colors.text_invert,
            self.palette_colors.secondary,
            self,
        )

        self.wait(0.5)

        exp_bottom.animate_out(self, run_time=0.5)

        exp_bottom = Exploration(
            text="So max gets two integer arguments",
            text_font_size=25,
            text_color=self.palette_colors.text,
            is_top=False,
        ).create()
        exp_bottom.animate_in(self, run_time=0.5)

        graph.highlight_node(
            0,
            self.palette_colors.text_invert,
            self.palette_colors.secondary,
            self,
        )

        self.wait(1.0)

        exp_bottom.animate_out(self, run_time=0.5)
        graph.animate_out(self, run_time=0.5)
        title.animate_out(self, run_time=0.5)

        # Step 4: Semantic rules

        title = Title(
            title='Semantic Rules',
            description='The types must be compatible',
            title_font_size=50,
            title_color=self.palette_colors.accent,
            description_font_size=30,
            description_color=self.palette_colors.text,
        ).create()
        title.animate_in(self, run_time=1)

        rule_steps = [
            TextStep(
                text=rule,
                text_font_size=30,
                text_color=self.palette_colors.text,
                figure_width=8.0,
                figure_color=self.palette_colors.accent,
            ) for rule in semantic_rules
        ]

        steps = VerticalSteps(
            steps=rule_steps,
            figure_height=0.8,
            figure_color=self.palette_colors.warning,
            arrow_color=self.palette_colors.danger,
            shape=FigureTypesForText.rounded,
            MAX_STEPS_LEN=5
        ).create()
        steps.animate_in(self, run_time=0.5)

        exp = Exploration(
            text="Every expression must follow these type rules",
            text_font_size=25,
            text_color=self.palette_colors.text,
            is_top=False,
        ).create()
        exp.animate_in(self, run_time=0.5)

        self.wait(1.0)

        exp.animate_out(self, run_time=0.5)
        steps.animate_out(self, run_time=0.5)
        title.animate_out(self, run_time=0.5)

        # The End

        title = Title(
            title='Verified AST',
            description='The tree is ready for next compiler steps',
            title_font_size=50,
            title_color=self.palette_colors.accent,
            description_font_size=30,
            description_color=self.palette_colors.text,
        ).create()
        title.animate_in(self, run_time=1)

        graph = Graph(
            nodes=["max", "+", "a", "b", "42"],
            edges=[(0, 1), (1, 2), (1, 3), (0, 4)],
            node_color=self.palette_colors.secondary,
            node_radius=0.4,
            edge_color=self.palette_colors.success,
            shape=FigureTypesForText.circle,
            max_iterations=100,
            TOP_LIMIT=1.0,
            RIGHT_LIMIT=2.0,
            LEFT_LIMIT=-2.0,
            BOTTOM_LIMIT=-2.0,
        ).create()
        graph.animate_in(self, run_time=2, lag_ratio=0.1)

        title.animate_out(self, run_time=0.5)

        exp = Exploration(
            text="That’s a result of semantic analysis",
            text_font_size=30,
            text_color=self.palette_colors.text,
            is_top=False,
        ).create()
        exp.animate_in(self, run_time=0.5)

        self.wait(1.0)

        exp.animate_out(self, run_time=0.5)
        graph.animate_out(self, run_time=0.5)
        title.animate_out(self, run_time=0.5)


class SemanticAnimationShorts(SemanticAnimation):
    def __init__(self, **kwargs):
        super().__init__(
            scene_format=SceneFormat.SHORTS,
            **kwargs
        )
