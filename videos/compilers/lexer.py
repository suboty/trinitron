"""
A lexical analysis is the first part of compiler frontend.
The main aim of that step is a creating a list of tokens of your source code.

For token getting we need prepare special rules for token understanding.
One of the most popular way for it is a sorting of known tokens by length.

First, we get a line of source code. We start working with symbols - step by step.
While working, we save a current state of our lexer.
If we find a separator we add a token to a list and update a current state.

One of the most important duty of a lexical analysis is saving data in symbols table.
In this table we save all identifiers - names of variables, classes and functions.
That`s needed for next steps of compiler frontend.

The result of lexical analysis work is a list of prepared tokens for next steps.
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
    TextInBox,
    Exploration,
    Table,
    TableCell,
    VerticalSteps
)


class LexerAnimation(SceneBase):
    palette_colors = PALETTES.get('dark')

    def __init__(self, scene_format=SceneFormat.FULL_HD, **kwargs):
        super().__init__(
            scene_format=scene_format,
            **kwargs
        )

    def construct(self):
        symbols = ['int', 'res', '=', 'max', '(', 'a', '+', 'b', ',', '42', ')', ';']
        tokens = [
            'TYPE(int)', 'VAR(res)', 'OPER(=)',
            'NAME(max)', 'PAREN_O', 'VAR(a)',
            'OPER(+)', 'VAR(b)', 'COMMA',
            'VALUE(42)', 'PAREN_C', 'TERM'
        ]

        rules_for_tokens = [
            'Function name MAX -> 3 symbols',
            'Function name MIN -> 3 symbols',
            'Operator = -> 1 symbol',
            'Operator + -> 1 symbol'
        ]

        conveyor_data = [
            TextStep(
                text=symbol,
                text_font_size=25,
                text_color=self.palette_colors.text,
                figure_width=1.0,
                figure_color=self.palette_colors.accent,
            ) for symbol in symbols
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

        # Preview

        title = Title(
            title='Lexical Analysis',
            description='How does a compiler understand a source code?',
            title_font_size=50,
            title_color=self.palette_colors.accent,
            description_font_size=30,
            description_color=self.palette_colors.text,
        ).create()
        title.animate_in(self, run_time=1)

        conveyor_tokens_data_preview = conveyor_tokens_data[:2]
        conveyor_tokens_data_preview.append(
            TextStep(
                text='...',
                text_font_size=30,
                text_color=self.palette_colors.text,
                figure_width=2.0,
                figure_color=self.palette_colors.accent,
            )
        )

        conveyor_tokens = Conveyor(
            items=conveyor_tokens_data_preview,
            figure_height=1.5,
            figure_color=self.palette_colors.success,
            visible_count=3,
            shape=FigureTypesForText.rounded,
            shift_param='down',
        ).create()
        conveyor_tokens.animate_in(self, run_time=1.0, is_fast=True)

        self.wait(1.0)

        title.animate_out(self, run_time=0.5)
        conveyor_tokens.animate_out(self, run_time=0.5)

        # Step 1: Read a source code

        title = Title(
            title='Source Code',
            description='Getting a line of source code',
            title_font_size=50,
            title_color=self.palette_colors.accent,
            description_font_size=30,
            description_color=self.palette_colors.text,
        ).create()
        title.animate_in(self, run_time=1)

        source_code = TextInBox(
            text="int result = max(a + b, 42)",
            text_font_size=35,
            text_color=self.palette_colors.text,
            figure_color=self.palette_colors.accent,
            box_width=7.0,
            box_height=2.0,
            shift_direction='origin',
        ).create()
        source_code.animate_in(self, run_time=0.5)

        self.wait(1.0)

        source_code.animate_out(self, run_time=0.5)

        title.animate_out(self, run_time=0.5)

        # Step 2: Rules of token getting

        title = Title(
            title='Token getting rules',
            description='Special rules for token understanding',
            title_font_size=50,
            title_color=self.palette_colors.accent,
            description_font_size=30,
            description_color=self.palette_colors.text,
        ).create()
        title.animate_in(self, run_time=1)

        rule_exp = Exploration(
            text="Sorting by length",
            text_font_size=30,
            text_color=self.palette_colors.text,
            is_top=False,
        ).create()
        rule_exp.animate_in(self, run_time=0.5)

        rule_steps = [
            TextStep(
                text=rule,
                text_font_size=30,
                text_color=self.palette_colors.text,
                figure_width=8.0 if i in (0, 1) else 5.0,
                figure_color=self.palette_colors.accent,
            ) for i, rule in enumerate(rules_for_tokens)
        ]
        steps = VerticalSteps(
            steps=rule_steps,
            figure_height=0.8,
            figure_color=self.palette_colors.warning,
            arrow_color=self.palette_colors.danger,
            shape=FigureTypesForText.rounded,
        ).create()
        steps.animate_in(self, run_time=0.5)

        rule_exp.animate_out(self, run_time=0.5)

        exp = Exploration(
            text="Firstly we work with most length tokens",
            text_font_size=30,
            text_color=self.palette_colors.text,
            is_top=False,
        ).create()
        exp.animate_in(self, run_time=0.5)

        self.wait(1.0)

        exp.animate_out(self, run_time=0.5)
        steps.animate_out(self, run_time=0.5)
        title.animate_out(self, run_time=0.5)

        # Step 3: Getting a list of tokens

        title = Title(
            title='List of tokens',
            description='Getting a list of tokens by rules',
            title_font_size=50,
            title_color=self.palette_colors.accent,
            description_font_size=30,
            description_color=self.palette_colors.text,
        ).create()
        title.animate_in(self, run_time=1)

        exp = Exploration(
            text="Then we get tokens by our rules",
            text_font_size=25,
            text_color=self.palette_colors.text,
            is_top=False,
        ).create()
        exp_bottom = Exploration(
            text="We skip all gaps",
            text_font_size=25,
            text_color=self.palette_colors.text,
            is_top=False,
        ).create()

        exp.animate_in(self, run_time=0.5)
        self.wait(0.5)
        exp.animate_out(self, run_time=0.5)

        exp_bottom.animate_in(self, run_time=0.5)

        conveyor = Conveyor(
            items=conveyor_data,
            figure_height=1.0,
            figure_color=self.palette_colors.success,
            visible_count=3,
            shape=FigureTypesForText.circle,
            shift_param='up',
        ).create()

        conveyor_tokens = Conveyor(
            items=conveyor_tokens_data,
            figure_height=1.3,
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

        self.wait(1.0)

        exp_bottom.animate_out(self, run_time=0.5)

        Conveyor.animate_out_two(
            scene=self,
            first=conveyor,
            second=conveyor_tokens,
            run_time=0.5,
        )

        title.animate_out(self, run_time=0.5)

        # Step 4: Create a symbol table

        title = Title(
            title='Symbol Table',
            description='Create a symbol table',
            title_font_size=50,
            title_color=self.palette_colors.accent,
            description_font_size=30,
            description_color=self.palette_colors.text,
        ).create()
        title.animate_in(self, run_time=1)

        table_data = [
            [
                TableCell(
                    text="Identifier", text_font_size=25,
                    text_color=self.palette_colors.text, box_color=self.palette_colors.secondary
                ),
                TableCell(
                    text="Name", text_font_size=25,
                    text_color=self.palette_colors.text, box_color=self.palette_colors.secondary
                ),
            ],
            [
                TableCell(
                    text="ID 1", text_font_size=30,
                    text_color=self.palette_colors.text, box_color=self.palette_colors.accent
                ),
                TableCell(
                    text="res", text_font_size=30,
                    text_color=self.palette_colors.text, box_color=self.palette_colors.accent
                ),
            ],
            [
                TableCell(
                    text="ID 2", text_font_size=30,
                    text_color=self.palette_colors.text, box_color=self.palette_colors.accent
                ),
                TableCell(
                    text="max", text_font_size=30,
                    text_color=self.palette_colors.text, box_color=self.palette_colors.accent
                ),
            ],
            [
                TableCell(
                    text="ID 3", text_font_size=30,
                    text_color=self.palette_colors.text, box_color=self.palette_colors.accent
                ),
                TableCell(
                    text="a", text_font_size=30,
                    text_color=self.palette_colors.text, box_color=self.palette_colors.accent
                ),
            ],
            [
                TableCell(
                    text="ID 4", text_font_size=30,
                    text_color=self.palette_colors.text, box_color=self.palette_colors.accent
                ),
                TableCell(
                    text="b", text_font_size=30,
                    text_color=self.palette_colors.text, box_color=self.palette_colors.accent
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

        exp_bottom = Exploration(
            text="That`s needed for next steps of compiler frontend",
            text_font_size=25,
            text_color=self.palette_colors.text,
            is_top=False,
        ).create()
        exp_bottom.animate_in(self, run_time=0.5)

        self.wait(1.5)

        exp_bottom.animate_out(self, run_time=0.5)
        table.animate_out(self, run_time=1.0)
        title.animate_out(self, run_time=1.0)

        # The End

        table_data_tokens = [
            [
                TableCell(
                    text="TYPE(int)", text_font_size=24,
                    text_color=self.palette_colors.text, box_color=self.palette_colors.accent
                ),
                TableCell(
                    text="VAR(res)", text_font_size=24,
                    text_color=self.palette_colors.text, box_color=self.palette_colors.accent
                ),
                TableCell(
                    text="OPER(=)", text_font_size=24,
                    text_color=self.palette_colors.text, box_color=self.palette_colors.accent
                ),
            ],
            [
                TableCell(
                    text="NAME(max)", text_font_size=24,
                    text_color=self.palette_colors.text, box_color=self.palette_colors.accent
                ),
                TableCell(
                    text="PAREN_O", text_font_size=24,
                    text_color=self.palette_colors.text, box_color=self.palette_colors.accent
                ),
                TableCell(
                    text="VAR(a)", text_font_size=24,
                    text_color=self.palette_colors.text, box_color=self.palette_colors.accent
                ),
            ],
            [
                TableCell(
                    text="OPER(+))", text_font_size=24,
                    text_color=self.palette_colors.text, box_color=self.palette_colors.accent
                ),
                TableCell(
                    text="VAR(b)", text_font_size=24,
                    text_color=self.palette_colors.text, box_color=self.palette_colors.accent
                ),
                TableCell(
                    text="COMMA", text_font_size=24,
                    text_color=self.palette_colors.text, box_color=self.palette_colors.accent
                ),
            ],
            [
                TableCell(
                    text="VALUE(42)", text_font_size=24,
                    text_color=self.palette_colors.text, box_color=self.palette_colors.accent
                ),
                TableCell(
                    text="PAREN_C", text_font_size=24,
                    text_color=self.palette_colors.text, box_color=self.palette_colors.accent
                ),
                TableCell(
                    text="TERM", text_font_size=24,
                    text_color=self.palette_colors.text, box_color=self.palette_colors.accent
                ),
            ],
        ]

        table_tokens = Table(
            data=table_data_tokens,
            cell_width=2.0,
            cell_height=0.5,
            spacing=0.15,
        ).create()

        exp = Exploration(
            text="That`s a result of a lexical analysis",
            text_font_size=25,
            text_color=self.palette_colors.text,
            is_top=False,
        ).create()

        table_tokens.animate_in(self, run_time=1.5)
        exp.animate_in(self, run_time=0.5)

        self.wait(1.0)

        table_tokens.animate_out(self, run_time=0.5)
        exp.animate_out(self, run_time=0.5)


class LexerAnimationShorts(LexerAnimation):
    def __init__(self, **kwargs):
        super().__init__(
            scene_format=SceneFormat.SHORTS,
            **kwargs
        )
