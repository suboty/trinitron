from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from common import *


def load_scene_config(
        config_path: str = Path('videos', 'lexer', 'config.yaml')
) -> dict:
    with open(config_path, "r") as f:
        return yaml.safe_load(f)


SCENE_CONFIG = load_scene_config()


@dataclass(frozen=True)
class TokenSpec:
    lexeme: str
    token_type: str
    color: str


def _get_color_for_token_type(token_type: str) -> str:
    color_map = {
        "KEYWORD": KEYWORD_COLOR,
        "IDENTIFIER": IDENTIFIER_COLOR,
        "OPERATOR": OPERATOR_COLOR,
        "NUMBER": NUMBER_COLOR,
        "PAREN": PUNCTUATION_COLOR,
        "SEPARATOR": PUNCTUATION_COLOR,
        "TERMINATOR": PUNCTUATION_COLOR,
    }
    return color_map.get(token_type, TEXT_COLOR)


def create_symbol_row(
        name: str,
        category: str,
        config: dict, # noqa
) -> VGroup:
    background = RoundedRectangle(
        width=config["row_width"],
        height=config["row_height"],
        corner_radius=config["row_corner_radius"],
        stroke_color=BORDER_COLOR,
        stroke_width=config["row_stroke_width"],
        fill_color=BORDER_COLOR,
        fill_opacity=config["row_fill_opacity"],
    )

    name_text = Text(
        name,
        font="Menlo",
        font_size=config["row_name_font_size"],
        color=TEXT_COLOR,
    )

    category_text = Text(
        category,
        font="Menlo",
        font_size=config["row_category_font_size"],
        color=MUTED_COLOR,
    )

    content = VGroup(name_text, category_text)
    content.arrange(DOWN, buff=config["row_buff"])
    content.move_to(background)

    return VGroup(background, content)


def create_vertical_ast(
        center: np.ndarray,
        config: dict, # noqa
) -> tuple[VGroup, VGroup]:
    positions = {}
    for label, coords in config["ast_positions"].items():
        positions[label] = center + RIGHT * coords[0] + UP * coords[1]

    colors = {
        "=": OPERATOR_COLOR,
        "result": IDENTIFIER_COLOR,
        "max": IDENTIFIER_COLOR,
        "+": OPERATOR_COLOR,
        "42": NUMBER_COLOR,
        "a": IDENTIFIER_COLOR,
        "b": IDENTIFIER_COLOR,
    }

    nodes_by_name: dict[str, VGroup] = {}

    for label, position in positions.items():
        radius = config["ast_radius_result"] if label == "result" \
            else config["ast_radius_default"]

        circle = Circle(
            radius=radius,
            stroke_color=colors[label],
            stroke_width=config["ast_stroke_width"],
            fill_color=colors[label],
            fill_opacity=config["ast_fill_opacity"],
        )

        text = Text(
            label,
            font="Menlo",
            font_size=config["ast_font_size_result"] if label == "result"
            else config["ast_font_size_default"],
            color=TEXT_COLOR,
        )
        text.move_to(circle)

        node = VGroup(circle, text)
        node.move_to(position)

        nodes_by_name[label] = node

    edges = VGroup()

    for parent_name, child_name in config["ast_edges"]:
        parent = nodes_by_name[parent_name]
        child = nodes_by_name[child_name]

        edge = Line(
            parent.get_center(),
            child.get_center(),
            color=BORDER_COLOR,
            stroke_width=config["ast_edge_stroke_width"],
        )

        edge.set_length(
            max(edge.get_length() - config["ast_edge_shorten"], 0.1)
        )

        edges.add(edge)

    nodes = VGroup(*nodes_by_name.values())

    return nodes, edges


class LexerAnimation(MovingCameraScene):
    def __init__(
            self, camera_class: type[Camera] = MovingCamera, **kwargs: Any
    ):
        super().__init__(camera_class, **kwargs)

        self.config = SCENE_CONFIG["lexer"]
        self.source_code = self.config["source_code"]

        # Create tokens from config
        self.token_specs = []
        for token_data in self.config["tokens"]:
            color = _get_color_for_token_type(token_data["token_type"]) # noqa
            self.token_specs.append(
                TokenSpec(
                    token_data["lexeme"],
                    token_data["token_type"],
                    color
                )
            )

        self.after_label = None
        self.token_summary = None
        self.final_token_cards = None
        self.next_video = None
        self.final_caption = None
        self.token_arrow = None
        self.before_stream = None
        self.before_label = None
        self.ast_edges = None
        self.ast_nodes = None
        self.parser_arrow = None
        self.output_label = None
        self.token_title = None
        self.stream_label = None
        self.compiler_arrow = None
        self.compiler_label = None
        self.code = None
        self.status_text = None
        self.code_box = None
        self.parser_question = None
        self.scanner = None
        self.intro_line_2 = None
        self.buffer_value = None
        self.buffer = None
        self.lower_rail = None
        self.buffer_label = None
        self.intro_line_1 = None
        self.parser_title = None
        self.intro_title = None
        self.emitted_cards = None
        self.token_spans = None
        self.character_cells = None
        self.lexer_title = None
        self.upper_rail = None

    def construct(self) -> None:
        self.camera.background_color = BACKGROUND
        self.camera.frame.width = self.config["camera"]["frame_width"] # noqa
        self.camera.frame.move_to(UP * self.config["camera"]["intro_y"]) # noqa

        self.character_cells: VGroup | None = None
        self.token_spans: list[tuple[int, int]] = []

        self.emitted_cards: list[TokenCard] = []

        self.build_world()

        self.animate_intro()
        self.animate_character_stream()
        self.animate_lexer()
        self.animate_token_stream()
        self.animate_symbol_table()
        self.animate_parser_preview()

    def build_world(self) -> None:
        self.build_intro_world()
        self.build_lexer_world()
        self.build_token_world()
        self.build_parser_world()

    def build_intro_world(self) -> None:
        center = UP * self.config["camera"]["intro_y"]
        intro_config = self.config["intro"]

        title = StationTitle(
            "01",
            "SOURCE CODE",
            "What you see",
            KEYWORD_COLOR,
        )
        title.move_to(center + UP * intro_config["title_y_offset"])

        intro_line_1 = Text(
            "You write code.",
            font="Menlo",
            font_size=intro_config["line1_font_size"],
            color=TEXT_COLOR,
        )
        intro_line_1.move_to(center + UP * intro_config["line1_y_offset"])

        intro_line_2 = Text(
            "The compiler sees\nsomething different.",
            font="Menlo",
            font_size=intro_config["line2_font_size"],
            color=MUTED_COLOR,
            line_spacing=intro_config["line2_line_spacing"],
        )
        intro_line_2.move_to(center + UP * intro_config["line2_y_offset"])

        code_box = RoundedRectangle(
            width=intro_config["code_box_width"],
            height=intro_config["code_box_height"],
            corner_radius=intro_config["code_box_corner_radius"],
            stroke_color=KEYWORD_COLOR,
            stroke_width=intro_config["code_box_stroke_width"],
            fill_color=KEYWORD_COLOR,
            fill_opacity=intro_config["code_box_fill_opacity"],
        )
        code_box.move_to(center + DOWN * 0.3)

        code_line_1 = Text(
            "int result =",
            font="Menlo",
            font_size=intro_config["code_font_size"],
            color=TEXT_COLOR,
        )

        code_line_2 = Text(
            "max(a + b, 42);",
            font="Menlo",
            font_size=intro_config["code_font_size"],
            color=TEXT_COLOR,
        )

        code = VGroup(code_line_1, code_line_2)
        code.arrange(DOWN, buff=intro_config["code_buff"])
        code.move_to(code_box)

        compiler_label = Text(
            "compiler view",
            font="Menlo",
            font_size=intro_config["compiler_label_font_size"],
            color=MUTED_COLOR,
        )
        compiler_label.move_to(center + DOWN * intro_config["compiler_label_y_offset"])

        compiler_arrow = Arrow(
            compiler_label.get_bottom(),
            center + DOWN * 3.6,
            buff=intro_config["compiler_arrow_buff"],
            stroke_width=intro_config["compiler_arrow_stroke_width"],
            color=MUTED_COLOR,
        )

        stream_label = Text(
            "a stream of characters",
            font="Menlo",
            font_size=intro_config["stream_label_font_size"],
            color=ACCENT_COLOR,
        )
        stream_label.move_to(center + DOWN * intro_config["stream_label_y_offset"])

        self.intro_title = title
        self.intro_line_1 = intro_line_1
        self.intro_line_2 = intro_line_2
        self.code_box = code_box
        self.code = code
        self.compiler_label = compiler_label
        self.compiler_arrow = compiler_arrow
        self.stream_label = stream_label

    def build_lexer_world(self) -> None:
        center = UP * self.config["camera"]["lexer_y"]
        lexer_config = self.config["lexer_scene"]

        title = StationTitle(
            "02",
            "LEXICAL ANALYSIS",
            "Characters become tokens",
            ACCENT_COLOR,
        )
        title.move_to(center + UP * lexer_config["title_y_offset"])

        # Current token buffer
        buffer = RoundedRectangle(
            width=lexer_config["buffer_width"],
            height=lexer_config["buffer_height"],
            corner_radius=lexer_config["buffer_corner_radius"],
            stroke_color=IDENTIFIER_COLOR,
            stroke_width=lexer_config["buffer_stroke_width"],
            fill_color=IDENTIFIER_COLOR,
            fill_opacity=lexer_config["buffer_fill_opacity"],
        )
        buffer.move_to(center + UP * lexer_config["buffer_y_offset"])

        buffer_label = Text(
            "CURRENT TOKEN",
            font="Menlo",
            font_size=lexer_config["buffer_label_font_size"],
            color=IDENTIFIER_COLOR,
        )
        buffer_label.next_to(
            buffer.get_top(),
            DOWN,
            buff=lexer_config["buffer_label_buff"],
        )

        buffer_value = Text(
            "—",
            font="Menlo",
            font_size=lexer_config["buffer_value_font_size"],
            color=TEXT_COLOR,
        )
        buffer_value.move_to(
            buffer.get_center() + DOWN * lexer_config["buffer_value_y_offset"]
        )

        # Conveyor
        upper_rail = Line(
            center + LEFT * lexer_config["rail_length"] + UP * lexer_config["rail_y_offset_upper"],
            center + RIGHT * lexer_config["rail_length"] + UP * lexer_config["rail_y_offset_upper"],
            color=BELT_COLOR,
            stroke_width=lexer_config["rail_stroke_width"],
        )

        lower_rail = Line(
            center + LEFT * lexer_config["rail_length"] + UP * lexer_config["rail_y_offset_lower"],
            center + RIGHT * lexer_config["rail_length"] + UP * lexer_config["rail_y_offset_lower"],
            color=BELT_COLOR,
            stroke_width=lexer_config["rail_stroke_width"],
        )

        scanner_line = Line(
            center + UP * lexer_config["scanner_line_y_start"],
            center + DOWN * lexer_config["scanner_line_y_end"],
            color=ACCENT_COLOR,
            stroke_width=lexer_config["scanner_line_stroke_width"],
        )

        scanner_label = Text(
            "READ",
            font="Menlo",
            font_size=lexer_config["scanner_label_font_size"],
            color=ACCENT_COLOR,
        )
        scanner_label.next_to(
            scanner_line,
            UP,
            buff=lexer_config["scanner_label_buff"],
        )

        scanner = VGroup(scanner_line, scanner_label)

        status = Text(
            "waiting for input",
            font="Menlo",
            font_size=lexer_config["status_font_size"],
            color=MUTED_COLOR,
        )
        status.move_to(center + DOWN * lexer_config["status_y_offset"])

        output_label = Text(
            "EMITTED TOKENS",
            font="Menlo",
            font_size=lexer_config["output_label_font_size"],
            color=OPERATOR_COLOR,
        )
        output_label.move_to(center + DOWN * lexer_config["output_label_y_offset"])

        self.lexer_title = title
        self.buffer = buffer
        self.buffer_label = buffer_label
        self.buffer_value = buffer_value

        self.upper_rail = upper_rail
        self.lower_rail = lower_rail

        self.scanner = scanner
        self.status_text = status
        self.output_label = output_label

    def build_token_world(self) -> None:
        center = UP * self.config["camera"]["tokens_y"]
        token_config = self.config["token_stream"]

        title = StationTitle(
            "03",
            "TOKEN STREAM",
            "Structured input for the parser",
            OPERATOR_COLOR,
        )
        title.move_to(center + UP * token_config["title_y_offset"])

        before_label = Text(
            "characters",
            font="Menlo",
            font_size=token_config["before_label_font_size"],
            color=MUTED_COLOR,
        )
        before_label.move_to(center + UP * token_config["before_label_y_offset"])

        before_stream = Text(
            "i n t · r e s u l t · = · ...",
            font="Menlo",
            font_size=token_config["before_stream_font_size"],
            color=MUTED_COLOR,
        )
        before_stream.move_to(center + UP * token_config["before_stream_y_offset"])

        arrow = Arrow(
            center + UP * token_config["arrow_y_start"],
            center + UP * token_config["arrow_y_end"],
            color=ACCENT_COLOR,
            stroke_width=token_config["arrow_stroke_width"],
        )

        after_label = Text(
            "tokens",
            font="Menlo",
            font_size=token_config["after_label_font_size"],
            color=OPERATOR_COLOR,
        )
        after_label.move_to(center + UP * token_config["after_label_y_offset"])

        self.token_title = title
        self.before_label = before_label
        self.before_stream = before_stream
        self.token_arrow = arrow
        self.after_label = after_label

    def build_parser_world(self) -> None:
        center = UP * self.config["camera"]["parser_y"]
        parser_config = self.config["parser"]

        title = StationTitle(
            "04",
            "PARSER",
            "The next compilation stage",
            PUNCTUATION_COLOR,
        )
        title.move_to(center + UP * parser_config["title_y_offset"])

        question = Text(
            "How do tokens become\na syntax tree?",
            font="Menlo",
            font_size=parser_config["question_font_size"],
            color=TEXT_COLOR,
            line_spacing=parser_config["question_line_spacing"],
        )
        question.move_to(center + UP * parser_config["question_y_offset"])

        parser_arrow = Arrow(
            center + UP * parser_config["arrow_y_start"],
            center + UP * parser_config["arrow_y_end"],
            color=PUNCTUATION_COLOR,
            stroke_width=parser_config["arrow_stroke_width"],
        )

        ast_nodes, ast_edges = create_vertical_ast(
            center + DOWN * parser_config["ast_center_y_offset"],
            parser_config
        )

        final_caption = Text(
            "Tokens → Syntax Tree",
            font="Menlo",
            font_size=parser_config["final_caption_font_size"],
            color=PUNCTUATION_COLOR,
        )
        final_caption.move_to(center + DOWN * parser_config["final_caption_y_offset"])

        next_video = Text(
            "Next video: Parsing",
            font="Menlo",
            font_size=parser_config["next_video_font_size"],
            color=MUTED_COLOR,
        )
        next_video.next_to(
            final_caption,
            DOWN,
            buff=parser_config["next_video_buff"],
        )

        self.parser_title = title
        self.parser_question = question
        self.parser_arrow = parser_arrow
        self.ast_nodes = ast_nodes
        self.ast_edges = ast_edges
        self.final_caption = final_caption
        self.next_video = next_video

    def animate_intro(self) -> None:
        self.play(
            FadeIn(self.intro_title, shift=DOWN * 0.2),
            run_time=0.8,
        )

        self.play(
            Write(self.intro_line_1),
            run_time=1.2,
        )

        self.play(
            FadeIn(self.intro_line_2, shift=UP * 0.15),
            run_time=1.3,
        )

        self.play(
            Create(self.code_box),
            Write(self.code),
            run_time=2.0,
        )

        self.wait(0.8)

        self.play(
            FadeIn(self.compiler_label),
            GrowArrow(self.compiler_arrow),
            FadeIn(self.stream_label, shift=UP * 0.15),
            run_time=1.3,
        )

        self.wait(0.7)

    def animate_character_stream(self) -> None:
        cells = VGroup(
            *[
                CharacterCell(character)
                for character in self.source_code
            ]
        )

        cells.arrange(RIGHT, buff=CONFIG["character_cell"]["cell_buff"])
        cells.width = CONFIG["character_cell"]["stream_width"]
        cells.move_to(
            UP * self.config["camera"]["lexer_y"] + UP * 0.57
        )

        self.character_cells = cells
        self.token_spans = self.find_token_spans()

        self.play(
            self.camera.frame.animate.move_to( # noqa
                UP * self.config["camera"]["lexer_y"]
            ),
            run_time=self.config["camera"]["move_duration"],
            rate_func=smooth,
        )

        self.play(
            FadeIn(self.lexer_title, shift=DOWN * 0.2),
            Create(self.upper_rail),
            Create(self.lower_rail),
            run_time=1.1,
        )

        self.play(
            FadeIn(cells),
            FadeIn(self.scanner),
            FadeIn(self.buffer),
            FadeIn(self.buffer_label),
            FadeIn(self.buffer_value),
            FadeIn(self.status_text),
            FadeIn(self.output_label),
            run_time=1.2,
        )

    def animate_lexer(self) -> None:
        output_positions = self.create_lexer_output_positions()

        for token_index, spec in enumerate(self.token_specs):
            start, end = self.token_spans[token_index]

            detailed = token_index in {0, 1}
            show_boundary = token_index in {0, 1}

            card = self.scan_token(
                spec=spec,
                start=start,
                end=end,
                output_position=output_positions[token_index],
                detailed=detailed,
                show_boundary=show_boundary,
            )

            self.emitted_cards.append(card)

        self.play(
            self.replace_status(
                "character stream complete",
                ACCENT_COLOR,
            ),
            run_time=0.6,
        )

        self.wait(0.7)

    def scan_token(
            self,
            spec: TokenSpec,
            start: int,
            end: int,
            output_position: np.ndarray,
            detailed: bool,
            show_boundary: bool,
    ) -> TokenCard:
        if self.character_cells is None:
            raise RuntimeError("Character stream is not initialized.")

        cells = self.character_cells[start:end]
        accumulated = ""
        scan_config = self.config["scanning"]
        lexer_config = self.config["lexer_scene"]

        for cell in cells:
            accumulated += cell.character

            new_buffer = Text(
                accumulated,
                font="Menlo",
                font_size=lexer_config["buffer_value_font_size"],
                color=spec.color,
            )
            new_buffer.move_to(
                self.buffer.get_center() + DOWN * lexer_config["buffer_value_y_offset"]
            )

            target_x = cell.get_center()[0]

            scanner_target = self.scanner.copy()
            scanner_target.set_x(target_x)

            self.play(
                Transform(self.scanner, scanner_target),
                cell.highlight(spec.color),
                Transform(self.buffer_value, new_buffer),
                self.replace_status(
                    f"reading '{cell.character}'",
                    spec.color,
                ),
                run_time=scan_config["scan_duration_detailed"] if detailed
                else scan_config["scan_duration_simple"],
                rate_func=linear,
            )

        if show_boundary and end < len(self.character_cells):
            next_cell = self.character_cells[end]

            boundary = DashedLine(
                next_cell.get_top() + UP * 0.25,
                next_cell.get_bottom() + DOWN * 0.25,
                color=NUMBER_COLOR,
                dash_length=scan_config["boundary_dash_length"],
                stroke_width=scan_config["boundary_stroke_width"],
            )

            boundary_label = Text(
                "token boundary",
                font="Menlo",
                font_size=scan_config["boundary_label_font_size"],
                color=NUMBER_COLOR,
            )
            boundary_label.next_to(
                boundary,
                UP,
                buff=scan_config["boundary_label_buff"],
            )

            self.play(
                next_cell.highlight(NUMBER_COLOR),
                Create(boundary),
                FadeIn(boundary_label, shift=UP * 0.1),
                self.replace_status(
                    "next character does not fit",
                    NUMBER_COLOR,
                ),
                run_time=scan_config["boundary_duration"],
            )

            self.wait(0.25)

            self.play(
                FadeOut(boundary),
                FadeOut(boundary_label),
                next_cell.reset_style(),
                run_time=scan_config["boundary_fade_duration"],
            )

        card = TokenCard(
            spec.token_type,
            spec.lexeme,
            spec.color,
            width=CONFIG["token_card"]["default_width"],
            height=lexer_config["scanner_height"],
            font_size=lexer_config["scanner_font_size"],
        )
        card.move_to(self.buffer)

        source_group = VGroup(*cells)

        flash_offset_y = scan_config.get("flash_offset_y", 0)
        flash_position = self.buffer.get_center() + DOWN * abs(
            flash_offset_y) if flash_offset_y < 0 else self.buffer.get_center() + UP * flash_offset_y

        self.play(
            self.replace_status(
                "token complete",
                ACCENT_COLOR,
            ),
            Flash(
                flash_position,
                color=ACCENT_COLOR,
                flash_radius=scan_config["flash_radius"],
                line_length=scan_config["flash_line_length"],
            ),
            run_time=scan_config["token_complete_duration_detailed"] if detailed
            else scan_config["token_complete_duration_simple"],
        )

        self.play(
            TransformFromCopy(source_group, card),
            FadeOut(self.buffer_value),
            run_time=scan_config["transform_duration_detailed"] if detailed
            else scan_config["transform_duration_simple"],
        )

        empty_buffer = Text(
            "",
            font="Menlo",
            font_size=lexer_config["buffer_value_font_size"],
            color=TEXT_COLOR,
        )
        empty_buffer.move_to(
            self.buffer.get_center() + DOWN * lexer_config["buffer_value_y_offset"]
        )

        self.play(
            card.animate.move_to(output_position),
            FadeIn(empty_buffer),
            source_group.animate.set_opacity(CONFIG["character_cell"]["consumed_opacity"]),
            run_time=scan_config["move_duration_detailed"] if detailed
            else scan_config["move_duration_simple"],
        )

        self.buffer_value = empty_buffer

        return card

    def animate_token_stream(self) -> None:
        token_config = self.config["token_stream"]

        self.play(
            self.camera.frame.animate.move_to( # noqa
                UP * self.config["camera"]["tokens_y"]
            ),
            run_time=self.config["camera"]["move_duration"],
            rate_func=smooth,
        )

        self.play(
            FadeIn(self.token_title, shift=DOWN * 0.2),
            FadeIn(self.before_label),
            FadeIn(self.before_stream),
            GrowArrow(self.token_arrow),
            FadeIn(self.after_label),
            run_time=1.2,
        )

        final_cards = VGroup(
            *[
                TokenCard(
                    spec.token_type,
                    spec.lexeme,
                    spec.color,
                    width=CONFIG["token_card"]["default_width"],
                    height=token_config["final_height"],
                    font_size=token_config["final_font_size"],
                )
                for spec in self.token_specs
            ]
        )

        final_cards.arrange_in_grid(
            rows=token_config["final_grid_rows"],
            cols=token_config["final_grid_cols"],
            buff=(token_config["final_grid_buff_x"],
                  token_config["final_grid_buff_y"]),
        )
        final_cards.move_to(
            UP * self.config["camera"]["tokens_y"] + DOWN * token_config["final_grid_y_offset"]
        )

        animations = [
            TransformFromCopy(source, target)
            for source, target in zip(
                self.emitted_cards,
                final_cards,
            )
        ]

        self.play(
            LaggedStart(
                *animations,
                lag_ratio=token_config["lag_ratio"],
            ),
            run_time=token_config["token_stream_duration"],
        )

        summary = Text(
            "characters → tokens",
            font="Menlo",
            font_size=token_config["summary_font_size"],
            color=ACCENT_COLOR,
        )
        summary.next_to(
            final_cards,
            DOWN,
            buff=token_config["summary_buff"],
        )

        self.play(
            Write(summary),
            run_time=token_config["summary_duration"],
        )

        self.final_token_cards = final_cards
        self.token_summary = summary

        self.wait(0.6)

    def animate_symbol_table(self) -> None:
        center = UP * self.config["camera"]["tokens_y"]
        st_config = self.config["symbol_table"]

        table = RoundedRectangle(
            width=st_config["table_width"],
            height=st_config["table_height"],
            corner_radius=st_config["table_corner_radius"],
            stroke_color=IDENTIFIER_COLOR,
            stroke_width=st_config["table_stroke_width"],
            fill_color=IDENTIFIER_COLOR,
            fill_opacity=st_config["table_fill_opacity"],
        )
        table.move_to(center + DOWN * st_config["table_y_offset"])

        title = Text(
            "SYMBOL TABLE",
            font="Menlo",
            font_size=st_config["table_title_font_size"],
            color=IDENTIFIER_COLOR,
        )
        title.next_to(
            table.get_top(),
            DOWN,
            buff=st_config["table_title_buff"],
        )

        rows = VGroup(
            create_symbol_row("result", "identifier", st_config),
            create_symbol_row("max", "identifier", st_config),
            create_symbol_row("a", "identifier", st_config),
            create_symbol_row("b", "identifier", st_config),
        )

        rows.arrange_in_grid(
            rows=st_config["row_grid_rows"],
            cols=st_config["row_grid_cols"],
            buff=(st_config["row_grid_buff_x"],
                  st_config["row_grid_buff_y"]),
        )
        rows.next_to(
            title,
            DOWN,
            buff=st_config["row_title_buff"],
        )

        self.play(
            FadeIn(table),
            FadeIn(title),
            run_time=st_config["table_fade_duration"],
        )

        identifier_indices = st_config["identifier_indices"]

        for token_index, row in zip(identifier_indices, rows):
            token = self.final_token_cards[token_index]

            arrow = Arrow(
                token.get_bottom(),
                row.get_top(),
                buff=st_config["arrow_buff"],
                color=IDENTIFIER_COLOR,
                stroke_width=st_config["arrow_stroke_width"],
                max_tip_length_to_length_ratio=st_config["arrow_max_tip_length_ratio"],
            )

            self.play(
                GrowArrow(arrow),
                FadeIn(row, shift=DOWN * 0.1),
                run_time=st_config["symbol_animation_duration"],
            )

            self.play(
                FadeOut(arrow),
                run_time=st_config["symbol_fade_duration"],
            )

        self.wait(0.7)

    def animate_parser_preview(self) -> None:
        parser_config = self.config["parser"]

        self.play(
            self.camera.frame.animate.move_to( # noqa
                UP * self.config["camera"]["parser_y"]
            ),
            run_time=self.config["camera"]["move_duration"],
            rate_func=smooth,
        )

        self.play(
            FadeIn(self.parser_title, shift=DOWN * 0.2),
            Write(self.parser_question),
            GrowArrow(self.parser_arrow),
            run_time=1.4,
        )

        self.play(
            LaggedStart(
                *[
                    Create(edge)
                    for edge in self.ast_edges
                ],
                lag_ratio=parser_config["edge_lag_ratio"],
            ),
            run_time=parser_config["edge_duration"],
        )

        self.play(
            LaggedStart(
                *[
                    FadeIn(node, scale=0.8)
                    for node in self.ast_nodes
                ],
                lag_ratio=parser_config["node_lag_ratio"],
            ),
            run_time=parser_config["node_duration"],
        )

        if parser_config.get("hide_arrow_after", False):
            self.play(
                FadeOut(self.parser_arrow),
                run_time=parser_config.get("arrow_fade_duration", 0.5),
            )

        self.play(
            Write(self.final_caption),
            FadeIn(self.next_video),
            run_time=parser_config["final_duration"],
        )

        self.wait(2.0)

    def find_token_spans(self) -> list[tuple[int, int]]:
        spans: list[tuple[int, int]] = []
        search_start = 0

        for spec in self.token_specs:
            start = self.source_code.find(
                spec.lexeme,
                search_start,
            )

            if start == -1:
                raise ValueError(
                    f"Token {spec.lexeme!r} was not found."
                )

            end = start + len(spec.lexeme)
            spans.append((start, end))
            search_start = end

        return spans

    def create_lexer_output_positions(
            self,
    ) -> list[np.ndarray]:
        center = (UP * self.config["camera"]["lexer_y"] + DOWN
                  * self.config["lexer_scene"]["output_y_offset"])

        positions: list[np.ndarray] = []

        x_positions = self.config["lexer_scene"]["output_x_positions"]
        y_positions = self.config["lexer_scene"]["output_y_positions"]

        for y in y_positions:
            for x in x_positions:
                positions.append(
                    center + RIGHT * x + UP * y
                )

        return positions

    def replace_status(
            self,
            text: str,
            color: str, # noqa
    ) -> Animation:
        new_status = Text(
            text,
            font="Menlo",
            font_size=self.config["lexer_scene"]["status_font_size"],
            color=color,
        )
        new_status.move_to(self.status_text)

        return Transform(
            self.status_text,
            new_status,
        )
