"""
Syntax analysis is the second part of compiler frontend.
The main aim of that step is creating an abstract syntax tree from a list of tokens.

First, we get a list of tokens from lexical analysis.
A parser reads these tokens one by one according to grammar rules.

While reading tokens, we save parser states in a stack.
Each state describes what part of the program we have found.

After this we use these states to build an abstract syntax tree.
The tree shows the structure of our source code and relations between its parts.

The result of syntax analysis is an abstract syntax tree for semantic analysis.
But that’s the theme of my other videos.
"""


from cmanim import (
    SceneBase,
    SceneFormat,
    PALETTES,
    Title,
    Conveyor,
    TextStep,
    FigureTypesForText,
    Exploration,
    VerticalSteps,
    Graph
)


class ParserAnimation(SceneBase):
    palette_colors = PALETTES.get('dark')

    def __init__(self, scene_format=SceneFormat.FULL_HD, **kwargs):
        super().__init__(
            scene_format=scene_format,
            **kwargs
        )

    def construct(self):
        tokens = [
            'NAME(max)', 'PAREN_O', 'VAR(a)',
            'OPER(+)', 'VAR(b)', 'COMMA',
            'VALUE(42)', 'PAREN_C'
        ]

        grammar_rules = [
            'CALL -> NAME ( ARGS )',
            'ARGS -> EXPR , EXPR',
            'EXPR -> EXPR + EXPR',
            'EXPR -> VAR | VALUE'
        ]

        stack = [
            'function max found',
            'start max params',
            'variable a found',
            'plus operator found',
            'variable b found',
            'first param complete',
            'value 42 found',
            'function call complete'
        ]

        conveyor_tokens_data = [
            TextStep(
                text=token,
                text_font_size=23,
                text_color=self.palette_colors.text,
                figure_width=2.0,
                figure_color=self.palette_colors.secondary,
            ) for token in tokens
        ]

        conveyor_stack_data = [
            TextStep(
                text=state,
                text_font_size=30,
                text_color=self.palette_colors.text,
                figure_width=6.0,
                figure_color=self.palette_colors.accent,
            ) for state in stack
        ]

        # Preview

        title = Title(
            title='Syntax Analysis',
            description='How does a compiler build an AST?',
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

        self.wait(1.0)

        graph.animate_out(self, run_time=0.5, lag_ratio=0.1)
        title.animate_out(self, run_time=0.5, lag_ratio=0.1)

        # Step 1: Get a list of tokens

        title = Title(
            title='List of Tokens',
            description='Getting tokens from lexical analysis',
            title_font_size=50,
            title_color=self.palette_colors.accent,
            description_font_size=30,
            description_color=self.palette_colors.text,
        ).create()
        title.animate_in(self, run_time=1)

        exp = Exploration(
            text="Syntax analysis starts with prepared tokens",
            text_font_size=25,
            text_color=self.palette_colors.text,
            is_top=False,
        ).create()
        exp.animate_in(self, run_time=0.5)

        conveyor_tokens = Conveyor(
            items=conveyor_tokens_data,
            figure_height=1.5,
            figure_color=self.palette_colors.success,
            visible_count=3,
            shape=FigureTypesForText.rounded,
        ).create()
        conveyor_tokens.animate_in(self, run_time=1.0, is_fast=True)

        self.wait(1.0)

        exp.animate_out(self, run_time=0.5)
        conveyor_tokens.animate_out(self, run_time=0.5)
        title.animate_out(self, run_time=0.5)

        # Step 2: Grammar rules

        title = Title(
            title='Grammar Rules',
            description='Rules for understanding token structure',
            title_font_size=50,
            title_color=self.palette_colors.accent,
            description_font_size=30,
            description_color=self.palette_colors.text,
        ).create()
        title.animate_in(self, run_time=1)

        exp = Exploration(
            text="A parser checks tokens according to grammar rules",
            text_font_size=25,
            text_color=self.palette_colors.text,
            is_top=False,
        ).create()
        exp.animate_in(self, run_time=0.5)

        rule_steps = [
            TextStep(
                text=rule,
                text_font_size=30,
                text_color=self.palette_colors.text,
                figure_width=8.0,
                figure_color=self.palette_colors.accent,
            ) for rule in grammar_rules
        ]

        steps = VerticalSteps(
            steps=rule_steps,
            figure_height=0.8,
            figure_color=self.palette_colors.warning,
            arrow_color=self.palette_colors.danger,
            shape=FigureTypesForText.rounded,
        ).create()
        steps.animate_in(self, run_time=0.5)

        self.wait(2.0)

        exp.animate_out(self, run_time=0.5)
        steps.animate_out(self, run_time=0.5)
        title.animate_out(self, run_time=0.5)

        # Step 3: Create parser states

        title = Title(
            title='Parser States',
            description='Walking through tokens step by step',
            title_font_size=50,
            title_color=self.palette_colors.accent,
            description_font_size=30,
            description_color=self.palette_colors.text,
        ).create()
        title.animate_in(self, run_time=1)

        exp = Exploration(
            text="For every token we update a current parser state",
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

        self.wait(1.0)

        conveyor_stack.animate_out(self, run_time=0.5)
        exp.animate_out(self, run_time=0.5)
        title.animate_out(self, run_time=0.5)

        # Step 4: Build an AST

        title = Title(
            title='Abstract Syntax Tree',
            description='Building a tree from parser states',
            title_font_size=50,
            title_color=self.palette_colors.accent,
            description_font_size=30,
            description_color=self.palette_colors.text,
        ).create()
        title.animate_in(self, run_time=1)

        exp = Exploration(
            text="Now we connect source code parts into a tree",
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
            max_iterations=500,
            TOP_LIMIT=1.0,
            RIGHT_LIMIT=2.0,
            LEFT_LIMIT=-2.0,
            BOTTOM_LIMIT=-2.0,
        ).create()
        graph.animate_in(self, run_time=2, lag_ratio=0.1)

        self.wait(1.0)

        exp.animate_out(self, run_time=0.5)
        title.animate_out(self, run_time=0.5)

        # The End

        exp = Exploration(
            text="That’s a result of syntax analysis",
            text_font_size=30,
            text_color=self.palette_colors.text,
            is_top=True,
        ).create()
        exp.animate_in(self, run_time=0.5)

        self.wait(1.0)

        exp.animate_out(self, run_time=0.5)
        graph.animate_out(self, run_time=0.5)


class ParserAnimationShorts(ParserAnimation):
    def __init__(self, **kwargs):
        super().__init__(
            scene_format=SceneFormat.SHORTS,
            **kwargs
        )
