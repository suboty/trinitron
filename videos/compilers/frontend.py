"""
Any compiler consists of frontend and backend parts.
The frontend part is a pipeline for getting an abstract syntax tree.
Then an abstract syntax tree is put into the backend part for getting machine code.
The frontend part consists of three steps: lexical analysis, syntax analysis and semantic analysis.

The first step of a compiler frontend is lexical analysis. Firstly, we get a source code line.
Then we get a list of tokens according to our language rules.
Of course, we skip all unimportant gaps.

Secondly, we get an abstract syntax tree.
We walk through the list of tokens and create a stack with states.
After this we parse the stack and build an abstract syntax tree.

Thirdly, we start semantic analysis.
The main aim of semantic analysis is to verify an AST.
For example: one integer variable plus another integer variable.
Then our function max must be integer and so on.

That’s a compiler frontend result.
Based on it, we can get machine code via the compiler backend.
But that’s the theme of my other videos.
"""


from cmanim import (
    SceneBase,
    SceneFormat,
    FadeIn,
    FadeOut,
    Title,
    FigureTypesForText,
    TextInBox,
    Graph,
    PALETTES,
    VerticalSteps,
    TextStep,
    Exploration,
    Conveyor
)


class FrontendAnimation(SceneBase):
    palette_colors = PALETTES.get('dark')

    def __init__(self, scene_format=SceneFormat.FULL_HD, **kwargs):
        super().__init__(
            scene_format=scene_format,
            **kwargs
        )

    def construct(self):
        symbols = ['max', '(', 'a', '+', 'b', ',', '42', ')']
        tokens = [
            'NAME(max)', 'PAREN_O', 'VAR(a)',
            'OPERATOR(a)', 'VAR(b)', 'COMMA',
            'VALUE(42)', 'PAREN_C'
        ]
        stack = [
            'func max calling',
            'start max params',
            'variable a found',
            'plus operator found',
            'and so on ...'
        ]

        conveyor_data = [
            TextStep(
                text=symbol,
                text_font_size=40,
                text_color=self.palette_colors.text,
                figure_width=1.0,
                figure_color=self.palette_colors.accent,
            ) for symbol in symbols
        ]
        conveyor_tokens_data = [
            TextStep(
                text=token,
                text_font_size=20,
                text_color=self.palette_colors.text,
                figure_width=2.0,
                figure_color=self.palette_colors.secondary,
            ) for token in tokens
        ]
        conveyor_stack_data = [
            TextStep(
                text=rule,
                text_font_size=40,
                text_color=self.palette_colors.text,
                figure_width=6.0,
                figure_color=self.palette_colors.accent,
            ) for rule in stack
        ]

        # Preview

        title = Title(
            title='Compiler Frontend',
            description='How does a compiler get an AST?',
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
            BOTTOM_LIMIT=-5,
        ).create()
        graph.animate_in(self, run_time=2, lag_ratio=0.1)

        self.wait(1.0)

        graph.animate_out(self, run_time=0.5, lag_ratio=0.1)
        title.animate_out(self, run_time=0.5, lag_ratio=0.1)

        # Compiler Structure

        title = Title(
            title='Compiler Structure',
            description='Frontend and backend',
            title_font_size=50,
            title_color=self.palette_colors.accent,
            description_font_size=30,
            description_color=self.palette_colors.text,
        ).create()
        title.animate_in(self, run_time=1)

        shapes = [
            TextInBox(
                text=["Frontend", 'Getting an AST'],
                text_font_size=[40, 20],
                text_color=[self.palette_colors.text, self.palette_colors.text],
                figure_color=self.palette_colors.accent,
                box_width=3.0,
                box_height=2.0,
                shift_direction='left',
            ).create(),
            TextInBox(
                text=["Backend", 'Getting a machine code'],
                text_font_size=[40, 20],
                text_color=[self.palette_colors.text, self.palette_colors.text],
                figure_color=self.palette_colors.secondary,
                box_width=3.0,
                box_height=2.0,
                shift_direction='right',
            ).create(),
        ]
        self.play(*[FadeIn(shape) for shape in shapes])

        self.wait(1.0)

        self.play(*[FadeOut(shape) for shape in shapes])

        steps_data = [
            TextStep(
                text=['Lexical analysis', 'Getting tokens'],
                text_font_size=[35, 25],
                text_color=[self.palette_colors.text, self.palette_colors.text],
                figure_width=5.0,
                figure_color=self.palette_colors.accent,
            ),
            TextStep(
                text=['Syntax analysis', 'Getting an AST'],
                text_font_size=[35, 25],
                text_color=[self.palette_colors.text, self.palette_colors.text],
                figure_width=5.0,
                figure_color=self.palette_colors.accent,
            ),
            TextStep(
                text=['Semantic analysis', 'Getting an verified AST'],
                text_font_size=[35, 25],
                text_color=[self.palette_colors.text, self.palette_colors.text],
                figure_width=5.0,
                figure_color=self.palette_colors.accent,
            ),
        ]

        steps = VerticalSteps(
            steps=steps_data,
            figure_height=2.0,
            figure_color=self.palette_colors.warning,
            arrow_color=self.palette_colors.danger,
            shape=FigureTypesForText.box,
        ).create()
        steps.animate_in(self, run_time=1)

        self.wait(0.5)

        steps.animate_out(self, run_time=0.5)
        title.animate_out(self, run_time=0.5)

        # Lexical Analysis

        title = Title(
            title='A Lexical Analysis',
            description='Getting tokens',
            title_font_size=50,
            title_color=self.palette_colors.accent,
            description_font_size=30,
            description_color=self.palette_colors.text,
        ).create()
        title.animate_in(self, run_time=1)

        exp = Exploration(
            text="We getting a source code line",
            text_font_size=30,
            text_color=self.palette_colors.text,
            is_top=True,
        ).create()
        exp.animate_in(self, run_time=0.5)

        source_code = TextInBox(
            text="max(a + b, 42)",
            text_font_size=35,
            text_color=self.palette_colors.text,
            figure_color=self.palette_colors.accent,
            box_width=7.0,
            box_height=2.0,
            shift_direction='origin',
        ).create()
        source_code.animate_in(self, run_time=0.5)

        self.wait(1.0)

        exp.animate_out(self, run_time=0.5)
        source_code.animate_out(self, run_time=0.5)

        exp = Exploration(
            text="Then we get tokens by our rules",
            text_font_size=25,
            text_color=self.palette_colors.text,
            is_top=False,
        ).create()
        exp.animate_in(self, run_time=0.5)
        self.wait(0.5)
        exp.animate_out(self, run_time=0.5)

        conveyor = Conveyor(
            items=conveyor_data,
            figure_height=2.0,
            figure_color=self.palette_colors.success,
            visible_count=3,
            shape=FigureTypesForText.circle,
            shift_param='up',
        ).create()

        conveyor_tokens = Conveyor(
            items=conveyor_tokens_data,
            figure_height=1.5,
            figure_color=self.palette_colors.success,
            visible_count=3,
            shape=FigureTypesForText.rounded,
            shift_param='down',
        ).create()

        Conveyor.animate_in_two(
            scene=self,
            first=conveyor,
            second=conveyor_tokens,
            run_time=1.0,
        )

        self.wait(0.5)

        Conveyor.animate_out_two(
            scene=self,
            first=conveyor,
            second=conveyor_tokens,
            run_time=0.5,
        )

        title.animate_out(self, run_time=0.5)

        # Syntax Analysis
        title = Title(
            title='A Syntax Analysis',
            description='Getting an AST',
            title_font_size=50,
            title_color=self.palette_colors.accent,
            description_font_size=30,
            description_color=self.palette_colors.text,
        ).create()
        title.animate_in(self, run_time=1)

        exp = Exploration(
            text="We walk through the list of tokens ...",
            text_font_size=25,
            text_color=self.palette_colors.text,
            is_top=True,
        ).create()
        exp.animate_in(self, run_time=0.5)
        self.wait(0.5)
        exp.animate_out(self, run_time=0.5)

        exp = Exploration(
            text="... and create a stack with states",
            text_font_size=25,
            text_color=self.palette_colors.text,
            is_top=True,
        ).create()
        exp.animate_in(self, run_time=0.5)

        conveyor_stack = Conveyor(
            items=conveyor_stack_data,
            figure_height=2.0,
            figure_color=self.palette_colors.success,
            visible_count=1,
            shape=FigureTypesForText.box,
        ).create()
        conveyor_stack.animate_in(self, run_time=1.0, is_fast=True)

        self.wait(0.5)

        conveyor_stack.animate_out(self, run_time=0.5)
        exp.animate_out(self, run_time=0.5)

        exp = Exploration(
            text="After this we parse the stack and build an AST",
            text_font_size=25,
            text_color=self.palette_colors.text,
            is_top=True,
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
            BOTTOM_LIMIT=-5,
        ).create()
        graph.animate_in(self, run_time=2, lag_ratio=0.1)

        self.wait(1.0)

        exp.animate_out(self, run_time=0.5)
        title.animate_out(self, run_time=0.5)

        # Semantic Analysis

        title = Title(
            title='A Semantic Analysis',
            description='But Is an AST right?',
            title_font_size=50,
            title_color=self.palette_colors.accent,
            description_font_size=30,
            description_color=self.palette_colors.text,
        ).create()
        title.animate_in(self, run_time=1)

        exp = Exploration(
            text="Now we need to verify our AST",
            text_font_size=25,
            text_color=self.palette_colors.text,
            is_top=True,
        ).create()
        exp.animate_in(self, run_time=0.5)

        exp_bottom = Exploration(
            text="We have two integer variables: a and b",
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

        exp_bottom.animate_out(self, run_time=0.5)

        exp_bottom = Exploration(
            text="And their result must be an integer",
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

        graph.highlight_node(
            0, self.palette_colors.text_invert,
            self.palette_colors.accent, self
        )
        graph.highlight_node(
            0, self.palette_colors.text_invert,
            self.palette_colors.accent, self
        )

        exp_bottom.animate_out(self, run_time=0.5)
        exp.animate_out(self, run_time=0.5)
        title.animate_out(self, run_time=0.5)

        # The End

        exp = Exploration(
            text="That’s a compiler frontend result",
            text_font_size=30,
            text_color=self.palette_colors.text,
            is_top=True,
        ).create()
        exp.animate_in(self, run_time=0.5)

        self.wait(1.0)

        exp.animate_out(self, run_time=0.5)
        graph.animate_out(self, run_time=0.5)


class FrontendAnimationShorts(FrontendAnimation):
    def __init__(self, **kwargs):
        super().__init__(
            scene_format=SceneFormat.SHORTS,
            **kwargs
        )
