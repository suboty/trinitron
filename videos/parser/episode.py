from dataclasses import dataclass

from _base_animation.common import *


def load_scene_config(
    config_path: str = Path("videos", "parser", "config.yaml"),
) -> dict:
    with open(config_path, "r", encoding="utf-8") as file:
        return yaml.safe_load(file)["parser"]


SCENE_CONFIG = load_scene_config()


@dataclass(frozen=True)
class TokenSpec:
    lexeme: str
    token_type: str
    color: str


class ParserAnimation(BaseAnimation):
    def __init__(
        self,
        camera_class: type[Camera] = MovingCamera,
        **kwargs: Any,
    ) -> None:
        super().__init__(camera_class, **kwargs)

        self.config = SCENE_CONFIG
        self.token_specs = [
            TokenSpec(
                lexeme=item["lexeme"],
                token_type=item["token_type"],
                color=self.get_token_color(item["token_type"]),
            )
            for item in self.config["tokens"]
        ]

        self.subtitle: Text | None = None
        self.explanation: Text | None = None

        self.token_cards: list[Mobject] = []
        self.cursor: Mobject | None = None
        self.status_text: Text | None = None

        self.rule_cards: list[VGroup] = []
        self.rules_group = VGroup()
        self.rules_anchor: np.ndarray | None = None # noqa

        self.ast_nodes: dict[str, VGroup] = {}
        self.ast_edges: dict[tuple[str, str], Line] = {}

    @staticmethod
    def get_token_color(token_type: str) -> str:
        return {
            "KEYWORD": KEYWORD_COLOR,
            "IDENTIFIER": IDENTIFIER_COLOR,
            "OPERATOR": OPERATOR_COLOR,
            "NUMBER": NUMBER_COLOR,
            "PAREN": PUNCTUATION_COLOR,
            "SEPARATOR": PUNCTUATION_COLOR,
            "TERMINATOR": PUNCTUATION_COLOR,
        }.get(token_type, TEXT_COLOR)

    def construct(self) -> None:
        camera = self.config["camera"]

        self.camera.background_color = BACKGROUND
        self.camera.frame.width = camera["frame_width"] # noqa
        self.camera.frame.move_to(self.station_center("tokens_y")) # noqa

        self.build_ast_objects()

        self.animate_token_station()
        self.move_to_station("rules_y")
        self.animate_rules_station()
        self.move_to_station("tree_y")
        self.animate_tree_station()
        self.move_to_station("final_y")
        self.animate_final_station()

        self.wait(self.config["timing"]["final_hold"])

    # Station 01. Stream of tokens

    def create_token_grid(
        self,
        center: np.ndarray,
        config: dict, # noqa
    ) -> VGroup:
        cards = VGroup()
        self.token_cards = []

        for token in self.token_specs:
            card = TokenCard(
                token.token_type,
                token.lexeme,
                token.color,
                width=config["card_width"],
                height=config["card_height"],
                font_size=config["card_font_size"],
            )
            cards.add(card)
            self.token_cards.append(card)

        cards.arrange_in_grid(
            rows=config["grid_rows"],
            cols=config["grid_cols"],
            buff=(config["grid_buff_x"], config["grid_buff_y"]),
        )
        cards.move_to(center + UP * config["grid_y"])
        return cards

    def animate_token_station(self) -> None:
        center = self.station_center("tokens_y")
        cfg = self.config["token_station"]
        timing = self.config["timing"]

        title = self.create_station_title("tokens", center)
        source = self.create_text(
            self.config["source_code"],
            center + UP * cfg["source_y"],
            cfg["source_font_size"],
        )
        source.scale_to_fit_width(cfg["source_max_width"])

        arrow = Arrow(
            center + UP * cfg["arrow_start_y"],
            center + UP * cfg["arrow_end_y"],
            color=ACCENT_COLOR,
            stroke_width=cfg["arrow_stroke_width"],
        )

        label = self.create_text(
            "TOKEN STREAM",
            center + UP * cfg["label_y"],
            cfg["label_font_size"],
            OPERATOR_COLOR,
        )

        token_grid = self.create_token_grid(center, cfg)

        self.play(FadeIn(title, shift=DOWN), run_time=timing["title_fade"])
        self.set_subtitle("tokens_input", center)
        self.play(FadeIn(source), run_time=timing["content_fade"])
        self.play(GrowArrow(arrow), FadeIn(label), run_time=timing["content_fade"])
        self.play(
            LaggedStart(
                *[FadeIn(card, shift=DOWN * 0.12) for card in token_grid],
                lag_ratio=cfg["token_lag_ratio"],
            ),
            run_time=timing["token_grid"],
        )
        self.set_explanation("tokens", center)
        self.wait(timing["normal_pause"])

    # Station 02. Recursive descent and active rules

    def create_compact_token_rows(
        self,
        center: np.ndarray,
        cfg: dict,
    ) -> VGroup:
        rows = VGroup()
        compact_cards: list[Mobject] = []

        for token in self.token_specs:
            card = TokenCard(
                token.token_type,
                token.lexeme,
                token.color,
                width=cfg["token_width"],
                height=cfg["token_height"],
                font_size=cfg["token_font_size"],
            )
            compact_cards.append(card)

        first_row = VGroup(*compact_cards[: cfg["first_row_count"]])
        second_row = VGroup(*compact_cards[cfg["first_row_count"] :])
        first_row.arrange(RIGHT, buff=cfg["token_buff_x"])
        second_row.arrange(RIGHT, buff=cfg["token_buff_x"])
        rows.add(first_row, second_row)
        rows.arrange(DOWN, buff=cfg["token_buff_y"])
        rows.move_to(center + UP * cfg["token_rows_y"])

        self.token_cards = compact_cards
        return rows

    def animate_rules_station(self) -> None:
        center = self.station_center("rules_y")
        cfg = self.config["rules_station"]
        timing = self.config["timing"]

        title = self.create_station_title("rules", center)
        token_rows = self.create_compact_token_rows(center, cfg)

        cursor = Triangle(
            color=self.token_specs[0].color,
            fill_color=self.token_specs[0].color,
            fill_opacity=1,
        )
        cursor.scale(cfg["cursor_size"])
        cursor.rotate(PI)
        cursor.next_to(self.token_cards[0], UP, buff=cfg["cursor_buff"])
        self.cursor = cursor

        rules_label = self.create_text(
            "ACTIVE RULES",
            center + UP * cfg["rules_label_y"],
            cfg["rules_label_font_size"],
            MUTED_COLOR,
        )

        self.rules_anchor = (
            center
            + RIGHT * cfg["rules_anchor_x"]
            + UP * cfg["rules_anchor_y"]
        )

        self.status_text = self.create_text(
            "start at the first token",
            center + UP * cfg["status_y"],
            cfg["status_font_size"],
            MUTED_COLOR,
        )

        self.play(FadeIn(title, shift=DOWN), run_time=timing["title_fade"])
        self.set_subtitle("rules_start", center)
        self.play(
            FadeIn(token_rows),
            FadeIn(cursor),
            FadeIn(rules_label),
            FadeIn(self.status_text),
            run_time=timing["content_fade"],
        )

        self.enter_rule("Declaration")
        self.scan(0, "read type")
        self.scan(1, "read variable name")
        self.scan(2, "read assignment")

        self.enter_rule("Expression")
        self.enter_rule("Call")
        self.scan(3, "read function name")
        self.scan(4, "open argument list")

        self.enter_rule("Arguments")
        self.enter_rule("Expression")
        self.scan(5, "read left operand")
        self.scan(6, "read operator")
        self.scan(7, "read right operand")

        self.set_subtitle("rules_nested", center)
        self.set_explanation("rules", center)
        self.wait(timing["normal_pause"])

        self.play(
            FadeOut(token_rows),
            FadeOut(cursor),
            FadeOut(rules_label),
            FadeOut(self.status_text),
            FadeOut(self.rules_group),
            run_time=timing["station_fade"],
        )
        self.rule_cards.clear()
        self.rules_group = VGroup()

    def scan(self, index: int, status: str) -> None:
        cfg = self.config["scanning"]
        token = self.token_specs[index]
        target = self.token_cards[index]

        new_cursor = self.cursor.copy()
        new_cursor.set_color(token.color)
        new_cursor.next_to(
            target,
            UP,
            buff=self.config["rules_station"]["cursor_buff"],
        )

        self.play(
            Transform(self.cursor, new_cursor),
            self.replace_status(status, token.color),
            run_time=cfg["move_duration"],
            rate_func=smooth,
        )
        self.play(
            Indicate(target, color=token.color, scale_factor=cfg["scale_factor"]),
            run_time=cfg["indicate_duration"],
        )
        self.wait(cfg["pause"])

    def create_rule_card(self, name: str) -> VGroup:
        cfg = self.config["rules_station"]

        text = self.create_text(
            name,
            ORIGIN,
            cfg["rule_font_size"],
            KEYWORD_COLOR,
        )
        box = RoundedRectangle(
            width=text.width + cfg["rule_padding_x"] * 2,
            height=cfg["rule_height"],
            corner_radius=cfg["rule_corner_radius"],
            stroke_color=KEYWORD_COLOR,
            stroke_width=cfg["rule_stroke_width"],
            fill_color=KEYWORD_COLOR,
            fill_opacity=cfg["rule_fill_opacity"],
        )
        text.move_to(box)
        return VGroup(box, text)

    def enter_rule(self, name: str) -> None:
        cfg = self.config["recursion"]
        card = self.create_rule_card(name)

        if self.rule_cards:
            self.play(
                self.rule_cards[-1].animate.set_opacity(cfg["inactive_opacity"]),
                run_time=cfg["enter_duration"] * 0.4,
            )

        self.rule_cards.append(card)
        self.rules_group.add(card)
        self.arrange_rule_cards()

        self.play(
            FadeIn(card, shift=RIGHT * 0.10),
            self.replace_status(f"enter {name}", KEYWORD_COLOR),
            run_time=cfg["enter_duration"],
        )

    def arrange_rule_cards(self) -> None:
        if not self.rule_cards or self.rules_anchor is None:
            return

        group = VGroup(*self.rule_cards)
        group.arrange(RIGHT, buff=self.config["rules_station"]["rule_buff"])
        group.move_to(self.rules_anchor, aligned_edge=LEFT)

    # Station 03. Returning subtrees

    def animate_tree_station(self) -> None:
        center = self.station_center("tree_y")
        cfg = self.config["tree_station"]
        timing = self.config["timing"]

        title = self.create_station_title("tree", center)
        rule_path = self.create_text(
            "Expression → Call → Arguments → Expression",
            center + UP * cfg["rule_path_y"],
            cfg["rule_path_font_size"],
            KEYWORD_COLOR,
        )
        rule_path.scale_to_fit_width(cfg["rule_path_max_width"])

        status = self.create_text(
            "return BinaryExpression",
            center + UP * cfg["status_y"],
            cfg["status_font_size"],
            OPERATOR_COLOR,
        )
        self.status_text = status

        self.play(FadeIn(title, shift=DOWN), run_time=timing["title_fade"])
        self.set_subtitle("tree_return", center)
        self.play(FadeIn(rule_path), FadeIn(status), run_time=timing["content_fade"])

        self.reveal_ast_part(
            node_names=["+", "a", "b"],
            edge_names=[("+", "a"), ("+", "b")],
        )

        self.play(
            self.replace_status("return NumberLiteral", NUMBER_COLOR),
            run_time=timing["status_change"],
        )
        self.reveal_ast_part(node_names=["42"], edge_names=[])

        self.play(
            self.replace_status("return CallExpression", IDENTIFIER_COLOR),
            run_time=timing["status_change"],
        )
        self.reveal_ast_part(
            node_names=["CALL", "max"],
            edge_names=[("CALL", "max"), ("CALL", "+"), ("CALL", "42")],
        )

        self.play(
            self.replace_status("return Assignment", OPERATOR_COLOR),
            run_time=timing["status_change"],
        )
        self.reveal_ast_part(
            node_names=["=", "result"],
            edge_names=[("=", "result"), ("=", "CALL")],
        )

        self.play(
            self.replace_status("return Declaration", KEYWORD_COLOR),
            run_time=timing["status_change"],
        )
        self.reveal_ast_part(
            node_names=["DECL", "int"],
            edge_names=[("DECL", "int"), ("DECL", "=")],
        )

        self.set_subtitle("tree_complete", center)
        self.set_explanation("tree", center)
        self.wait(timing["normal_pause"])

    def reveal_ast_part(
        self,
        node_names: list[str],
        edge_names: list[tuple[str, str]]
    ) -> None:
        cfg = self.config["tree_station"]
        animations: list[Animation] = []

        for edge_name in edge_names:
            animations.append(Create(self.ast_edges[edge_name]))

        for node_name in node_names:
            animations.append(FadeIn(self.ast_nodes[node_name], scale=0.82))

        self.play(
            LaggedStart(*animations, lag_ratio=cfg["reveal_lag_ratio"]),
            run_time=cfg["reveal_duration"],
        )

    # Station 04. A ready-made abstract syntax tree

    def animate_final_station(self) -> None:
        center = self.station_center("final_y")
        cfg = self.config["final_station"]
        timing = self.config["timing"]

        title = self.create_station_title("final", center)

        tree = VGroup(
            VGroup(*self.ast_edges.values()),
            VGroup(*self.ast_nodes.values()),
        )
        final_tree = tree.copy()
        final_tree.scale(cfg["tree_scale"])
        final_tree.move_to(center + UP * cfg["tree_y"])

        self.play(FadeIn(title, shift=DOWN), run_time=timing["title_fade"])
        self.set_subtitle("final", center)
        self.play(
            TransformFromCopy(tree, final_tree),
            run_time=cfg["tree_transform_duration"],
            rate_func=smooth,
        )
        self.set_explanation("final", center)
        self.wait(timing["normal_pause"])

    # AST building

    def build_ast_objects(self) -> None:
        """
            Creates a tree immediately, but only adds it to the scene in parts.
        """
        center = (
            self.station_center("tree_y")
            + RIGHT * self.config["layout"]["content_offset_x"]
            + UP * self.config["tree_station"]["ast_center_y"]
        )
        cfg = self.config["ast"]

        colors = {
            "DECL": KEYWORD_COLOR,
            "int": KEYWORD_COLOR,
            "=": OPERATOR_COLOR,
            "result": IDENTIFIER_COLOR,
            "CALL": IDENTIFIER_COLOR,
            "max": IDENTIFIER_COLOR,
            "+": OPERATOR_COLOR,
            "42": NUMBER_COLOR,
            "a": IDENTIFIER_COLOR,
            "b": IDENTIFIER_COLOR,
        }

        for name, coordinates in cfg["positions"].items():
            radius = cfg["node_radius_default"]
            font_size = cfg["font_size_default"]

            if name in {"int", "42", "a", "b"}:
                radius = cfg["node_radius_small"]
                font_size = cfg["font_size_small"]
            elif name == "result":
                radius = cfg["node_radius_result"]
                font_size = cfg["font_size_result"]
            elif name == "DECL":
                radius = cfg["node_radius_decl"]
                font_size = cfg["font_size_decl"]

            node = self.create_ast_node(name, colors[name], radius, font_size)
            node.move_to(
                center
                + RIGHT * coordinates[0]
                + UP * coordinates[1]
            )
            self.ast_nodes[name] = node

        for parent, child in cfg["edges"]:
            self.ast_edges[(parent, child)] = self.create_edge(
                self.ast_nodes[parent],
                self.ast_nodes[child],
            )

    def create_ast_node(
        self,
        label: str,
        color: str, # noqa
        radius: float,
        font_size: int,
    ) -> VGroup:
        cfg = self.config["ast"]
        circle = Circle(
            radius=radius,
            stroke_color=color,
            stroke_width=cfg["stroke_width"],
            fill_color=color,
            fill_opacity=cfg["fill_opacity"],
        )
        text = self.create_text(label, circle.get_center(), font_size, TEXT_COLOR)
        text.move_to(circle)
        return VGroup(circle, text)

    def create_edge(self, parent: Mobject, child: Mobject) -> Line:
        cfg = self.config["ast"]
        edge = Line(
            parent.get_center(),
            child.get_center(),
            color=BORDER_COLOR,
            stroke_width=cfg["edge_stroke_width"],
        )
        edge.set_length(max(edge.get_length() - cfg["edge_shorten"], 0.1))
        return edge

    def replace_status(
            self,
            text: str,
            color: str # noqa
    ) -> Animation:
        new_status = self.create_text(
            text,
            self.status_text.get_center(),
            self.config["rules_station"]["status_font_size"],
            color,
        )
        return Transform(self.status_text, new_status)
