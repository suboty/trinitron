from dataclasses import dataclass
from typing import Any

from common import *


def load_scene_config(
    config_path: str = Path("videos", "semantic", "config.yaml"),
) -> dict:
    with open(config_path, "r", encoding="utf-8") as file:
        return yaml.safe_load(file)["semantic"]


SCENE_CONFIG = load_scene_config()


@dataclass(frozen=True)
class SymbolSpec:
    name: str
    kind: str
    data_type: str
    scope: str


class SemanticAnimation(MovingCameraScene):
    def __init__(
        self,
        camera_class: type[Camera] = MovingCamera,
        **kwargs: Any,
    ) -> None:
        super().__init__(camera_class, **kwargs)

        self.config = SCENE_CONFIG
        self.subtitle: Text | None = None
        self.explanation: Text | None = None
        self.status_text: Text | None = None

        self.symbols = [
            SymbolSpec(
                name=item["name"],
                kind=item["kind"],
                data_type=item["data_type"],
                scope=item["scope"],
            )
            for item in self.config["symbols"]
        ]

        self.ast_nodes: dict[str, VGroup] = {}
        self.ast_edges: dict[tuple[str, str], Line] = {}
        self.input_tree: VGroup | None = None

    def construct(self) -> None:
        camera = self.config["camera"]

        self.camera.background_color = BACKGROUND
        self.camera.frame.width = camera["frame_width"]  # noqa
        self.camera.frame.move_to(self.station_center("ast_y"))  # noqa

        self.build_input_ast()

        self.animate_ast_station()
        self.move_to_station("symbols_y")
        self.animate_symbol_table_station()
        self.move_to_station("types_y")
        self.animate_type_check_station()
        self.move_to_station("final_y")
        self.animate_final_station()

        self.wait(self.config["timing"]["final_hold"])

    # General geometry of the four zones

    def station_center(self, camera_key: str) -> np.ndarray:
        """
            The center of the station is vertical.
            Each station is lower than the previous one.
        """
        return UP * self.config["camera"][camera_key]

    def zone_center(
            self,
            station_center: np.ndarray,
            top_key: str,
            bottom_key: str,
    ) -> np.ndarray:
        """
            Returns the center of a specific zone relative to the station center.
        """
        layout = self.config["layout"]

        center_x = (layout["content_left"] + layout["content_right"]) / 2
        center_x += layout["content_offset_x"]

        center_y = (layout[top_key] + layout[bottom_key]) / 2

        return station_center + RIGHT * center_x + UP * center_y

    def create_station_title(
            self,
            station_key: str,
            center: np.ndarray,
    ) -> StationTitle:
        station = self.config["stations"][station_key]

        title = StationTitle(
            station["number"],
            station["name"],
            station["description"],
            station["color"],
        )

        title.move_to(
            self.zone_center(
                center,
                "title_top",
                "title_bottom",
            )
            + RIGHT * self.config["layout"]["title_offset_x"]
        )

        return title

    def create_text(
            self,
            text: str,
            center: np.ndarray,
            font_size: int,
            color: str = TEXT_COLOR,  # noqa
            line_spacing: float | None = None,
    ) -> Text:
        kwargs: dict[str, Any] = {
            "text": text,
            "font": self.config["typography"]["font"],
            "font_size": font_size,
            "color": color,
        }

        if line_spacing is not None:
            kwargs["line_spacing"] = line_spacing

        return Text(**kwargs).move_to(center)

    def set_explanation(self, key: str, center: np.ndarray) -> None:
        """
            Shows a short thought only inside the Text Area.
        """
        cfg = self.config["text_area"]
        new_text = self.create_text(
            cfg["lines"][key],
            self.zone_center(center, "text_top", "text_bottom"),
            cfg["font_size"],
            MUTED_COLOR,
            cfg["line_spacing"],
        )
        new_text.scale_to_fit_width(cfg["max_width"])

        if self.explanation is None:
            self.explanation = new_text
            self.play(FadeIn(new_text), run_time=self.config["timing"]["text_change"])
            return

        self.play(
            ReplacementTransform(self.explanation, new_text),
            run_time=self.config["timing"]["text_change"],
        )
        self.explanation = new_text

    def set_subtitle(self, key: str, center: np.ndarray) -> None:
        """
            Shows the replica only inside the Subtitle Area.
        """
        cfg = self.config["subtitles"]
        new_text = self.create_text(
            cfg["lines"][key],
            self.zone_center(center, "subtitles_top", "subtitles_bottom"),
            cfg["font_size"],
            TEXT_COLOR,
            cfg["line_spacing"],
        )
        new_text.scale_to_fit_width(cfg["max_width"])

        if self.subtitle is None:
            self.subtitle = new_text
            self.play(FadeIn(new_text), run_time=self.config["timing"]["subtitle_change"])
            return

        self.play(
            ReplacementTransform(self.subtitle, new_text),
            run_time=self.config["timing"]["subtitle_change"],
        )
        self.subtitle = new_text

    def clear_station_text(self) -> None:
        animations: list[Animation] = []

        if self.subtitle is not None:
            animations.append(FadeOut(self.subtitle))
            self.subtitle = None

        if self.explanation is not None:
            animations.append(FadeOut(self.explanation))
            self.explanation = None

        if animations:
            self.play(*animations, run_time=self.config["timing"]["station_fade"])

    def move_to_station(self, camera_key: str) -> None:
        self.clear_station_text()
        self.play(
            self.camera.frame.animate.move_to(self.station_center(camera_key)),  # noqa
            run_time=self.config["camera"]["move_duration"],
            rate_func=smooth,
        )
    # Station 01. The finished AST is sent for semantic analysis

    def animate_ast_station(self) -> None:
        center = self.station_center("ast_y")
        cfg = self.config["ast_station"]
        timing = self.config["timing"]

        title = self.create_station_title("ast", center)

        parser_label = self.create_text(
            "PARSER OUTPUT",
            center + UP * cfg["parser_label_y"],
            cfg["parser_label_font_size"],
            MUTED_COLOR,
        )

        analyzer_box = RoundedRectangle(
            width=cfg["analyzer_width"],
            height=cfg["analyzer_height"],
            corner_radius=cfg["analyzer_corner_radius"],
            stroke_color=ACCENT_COLOR,
            stroke_width=cfg["analyzer_stroke_width"],
            fill_color=ACCENT_COLOR,
            fill_opacity=cfg["analyzer_fill_opacity"],
        )
        analyzer_box.move_to(center + UP * cfg["analyzer_y"])

        analyzer_text = self.create_text(
            "SEMANTIC ANALYZER",
            analyzer_box.get_center(),
            cfg["analyzer_font_size"],
            ACCENT_COLOR,
        )

        arrow = Arrow(
            center + UP * cfg["arrow_start_y"],
            center + UP * cfg["arrow_end_y"],
            color=ACCENT_COLOR,
            stroke_width=cfg["arrow_stroke_width"],
        )

        self.play(FadeIn(title, shift=DOWN), run_time=timing["title_fade"])
        self.set_subtitle("ast_input", center)
        self.play(
            FadeIn(parser_label),
            FadeIn(self.input_tree, scale=0.92),
            run_time=timing["content_fade"],
        )

        self.set_subtitle("meaning_question", center)
        self.play(
            GrowArrow(arrow),
            Create(analyzer_box),
            FadeIn(analyzer_text),
            run_time=timing["content_fade"],
        )

        self.set_explanation("ast", center)
        self.wait(timing["normal_pause"])

    # Station 02. Symbol table and name resolution

    def animate_symbol_table_station(self) -> None:
        center = self.station_center("symbols_y")
        cfg = self.config["symbol_station"]
        timing = self.config["timing"]

        title = self.create_station_title("symbols", center)
        tree = self.create_tree_copy(
            center
            + RIGHT * cfg["tree_x"]
            + UP * cfg["tree_y"],
            cfg["tree_scale"],
        )

        table, rows = self.create_symbol_table(
            center
            + RIGHT * cfg["table_x"]
            + UP * cfg["table_y"]
        )

        traversal = self.create_text(
            "AST WALK",
            center + RIGHT * cfg["traversal_x"] + UP * cfg["traversal_y"],
            cfg["traversal_font_size"],
            MUTED_COLOR,
        )

        self.status_text = self.create_text(
            "visit Declaration",
            center + UP * cfg["status_y"],
            cfg["status_font_size"],
            KEYWORD_COLOR,
        )

        self.play(FadeIn(title, shift=DOWN), run_time=timing["title_fade"])
        self.set_subtitle("symbol_start", center)
        self.play(
            FadeIn(tree),
            FadeIn(traversal),
            FadeIn(self.status_text),
            run_time=timing["content_fade"],
        )
        self.play(
            Create(table[0]),
            FadeIn(table[1]),
            FadeIn(table[2]),
            run_time=timing["content_fade"]
        )

        declaration_node = self.find_node_in_tree(tree, "DECL")
        result_node = self.find_node_in_tree(tree, "result")
        self.play(
            Indicate(declaration_node, color=KEYWORD_COLOR),
            Indicate(result_node, color=IDENTIFIER_COLOR),
            self.replace_status("declare result : int", IDENTIFIER_COLOR),
            run_time=cfg["step_duration"],
        )
        self.play(
            FadeIn(rows["result"], shift=RIGHT * 0.12),
            run_time=cfg["row_duration"],
        )

        self.set_subtitle("symbol_lookup", center)

        lookup_steps = [
            ("max", "resolve max", "max"),
            ("a", "resolve a", "a"),
            ("b", "resolve b", "b"),
        ]
        for node_name, status, row_name in lookup_steps:
            node = self.find_node_in_tree(tree, node_name)
            self.play(
                Indicate(node, color=IDENTIFIER_COLOR),
                self.replace_status(status, IDENTIFIER_COLOR),
                run_time=cfg["step_duration"],
            )
            self.play(
                FadeIn(rows[row_name], shift=RIGHT * 0.12),
                run_time=cfg["row_duration"],
            )
            self.play(
                Indicate(rows[row_name], color=IDENTIFIER_COLOR),
                run_time=cfg["indicate_duration"],
            )

        resolved = self.create_badge(
            "SYMBOLS RESOLVED",
            IDENTIFIER_COLOR,
            cfg["resolved_badge_width"],
            cfg["resolved_badge_height"],
            cfg["resolved_badge_font_size"],
        )
        resolved.move_to(center + UP * cfg["resolved_badge_y"])
        self.play(
            FadeIn(resolved, scale=0.85),
            run_time=timing["content_fade"]
        )

        self.set_explanation("symbols", center)
        self.wait(timing["normal_pause"])

    def create_symbol_table(
            self,
            center: np.ndarray,
    ) -> tuple[VGroup, dict[str, VGroup]]:
        cfg = self.config["symbol_table"]

        background = RoundedRectangle(
            width=cfg["width"],
            height=cfg["height"],
            corner_radius=cfg["corner_radius"],
            stroke_color=IDENTIFIER_COLOR,
            stroke_width=cfg["stroke_width"],
            fill_color=IDENTIFIER_COLOR,
            fill_opacity=cfg["fill_opacity"],
        )
        background.move_to(center)
        background.set_z_index(0)

        title = self.create_text(
            "SYMBOL TABLE",
            center + UP * cfg["title_y_offset"],
            cfg["title_font_size"],
            IDENTIFIER_COLOR,
        )
        title.set_z_index(3)

        header = self.create_symbol_row(
            "NAME",
            "KIND",
            "TYPE",
            "SCOPE",
            cfg,
            is_header=True,
        )
        header.move_to(
            center + UP * cfg["header_y_offset"]
        )
        header.set_z_index(3)

        rows: dict[str, VGroup] = {}
        previous_row: Mobject = header

        for symbol in self.symbols:
            row = self.create_symbol_row(
                symbol.name,
                symbol.kind,
                symbol.data_type,
                symbol.scope,
                cfg,
            )

            row.next_to(
                previous_row,
                DOWN,
                buff=cfg["row_gap"],
            )
            row.set_x(center[0]) # noqa
            row.set_z_index(3)

            rows[symbol.name] = row
            previous_row = row

        table_base = VGroup(
            background,
            title,
            header,
        )

        return table_base, rows

    def create_symbol_row(
        self,
        name: str,
        kind: str,
        data_type: str,
        scope: str,
        cfg: dict,
        is_header: bool = False,
    ) -> VGroup:
        color = TEXT_COLOR
        font_size = cfg["header_font_size"] if is_header else cfg["row_font_size"]

        columns = VGroup(
            self.create_text(name, ORIGIN, font_size, color),
            self.create_text(kind, ORIGIN, font_size, color),
            self.create_text(data_type, ORIGIN, font_size, color),
            self.create_text(scope, ORIGIN, font_size, color),
        )

        for column, width in zip(columns, cfg["column_widths"]):
            column.set_width(min(column.width, width * 0.90))
            holder = Rectangle(width=width, height=cfg["row_height"])
            holder.set_stroke(opacity=0)
            column.move_to(holder)
            holder.add(column)

        columns.arrange(RIGHT, buff=0.2)

        row_background = RoundedRectangle(
            width=sum(cfg["column_widths"]),
            height=cfg["row_height"],
            corner_radius=cfg["row_corner_radius"],
            stroke_color=IDENTIFIER_COLOR,
            stroke_width=cfg["row_stroke_width"],
            fill_color=IDENTIFIER_COLOR,
            fill_opacity=(
                cfg["header_fill_opacity"] if is_header else cfg["row_fill_opacity"]
            ),
        )
        columns.move_to(row_background)
        return VGroup(row_background, columns)

    # Station 03. Bottom-up type checking

    def animate_type_check_station(self) -> None:
        center = self.station_center("types_y")
        cfg = self.config["type_station"]
        timing = self.config["timing"]

        title = self.create_station_title("types", center)
        tree = self.create_tree_copy(
            center + RIGHT * cfg["tree_x"] + UP * cfg["tree_y"],
            cfg["tree_scale"],
        )

        self.status_text = self.create_text(
            "infer leaf types",
            center + UP * cfg["status_y"],
            cfg["status_font_size"],
            MUTED_COLOR,
        )

        self.play(FadeIn(title, shift=DOWN), run_time=timing["title_fade"])
        self.set_subtitle("types_start", center)
        self.play(FadeIn(tree), FadeIn(self.status_text), run_time=timing["content_fade"])

        type_badges: dict[str, VGroup] = {}

        leaf_types = [
            ("a", "int", IDENTIFIER_COLOR),
            ("b", "int", IDENTIFIER_COLOR),
            ("42", "int", NUMBER_COLOR),
        ]
        for node_name, data_type, color in leaf_types:
            node = self.find_node_in_tree(tree, node_name)
            badge = self.create_type_badge(data_type, color)
            badge.next_to(node, DOWN, buff=cfg["badge_buff"])
            if node_name == "42":
                badge.next_to(node, RIGHT, buff=cfg["badge_buff_42"])
            type_badges[node_name] = badge
            self.play(
                Indicate(node, color=color),
                FadeIn(badge, shift=UP * 0.08),
                run_time=cfg["type_step_duration"],
            )

        plus_node = self.find_node_in_tree(tree, "+")
        plus_badge = self.create_type_badge("int", OPERATOR_COLOR)
        plus_badge.next_to(plus_node, RIGHT, buff=cfg["operator_badge_buff"])
        rule = self.create_rule_panel(
            "+ : (int, int) → int",
            OPERATOR_COLOR,
            cfg,
        )
        rule.move_to(center + RIGHT * cfg["rule_x"] + UP * cfg["rule_y"])

        self.play(
            self.replace_status("check a + b", OPERATOR_COLOR),
            FadeIn(rule),
            Indicate(plus_node, color=OPERATOR_COLOR),
            run_time=cfg["type_step_duration"],
        )
        self.play(FadeIn(plus_badge, shift=LEFT * 0.08), run_time=cfg["type_step_duration"])

        self.set_subtitle("call_check", center)

        call_node = self.find_node_in_tree(tree, "CALL")
        call_badge = self.create_type_badge("int", IDENTIFIER_COLOR)
        call_badge.next_to(call_node, RIGHT, buff=cfg["operator_badge_buff"])
        call_rule = self.create_rule_panel(
            "max : (int, int) → int",
            IDENTIFIER_COLOR,
            cfg,
        )
        call_rule.move_to(rule)

        self.play(
            ReplacementTransform(rule, call_rule),
            self.replace_status("verify max arguments", IDENTIFIER_COLOR),
            Indicate(call_node, color=IDENTIFIER_COLOR),
            run_time=cfg["type_step_duration"],
        )
        self.play(FadeIn(call_badge, shift=LEFT * 0.08), run_time=cfg["type_step_duration"])

        assignment_node = self.find_node_in_tree(tree, "=")
        assignment_badge = self.create_badge(
            "ASSIGNMENT OK",
            KEYWORD_COLOR,
            cfg["assignment_badge_width"],
            cfg["assignment_badge_height"],
            cfg["assignment_badge_font_size"],
        )
        assignment_badge.move_to(center + UP * cfg["assignment_badge_y"])

        self.play(
            self.replace_status("int result = int", KEYWORD_COLOR),
            Indicate(assignment_node, color=KEYWORD_COLOR),
            FadeIn(assignment_badge, scale=0.85),
            run_time=cfg["type_step_duration"],
        )

        self.set_explanation("types", center)
        self.wait(timing["normal_pause"])

    def create_type_badge(self, text: str, color: str) -> VGroup:  # noqa
        cfg = self.config["type_badge"]
        return self.create_badge(
            text,
            color,
            cfg["width"],
            cfg["height"],
            cfg["font_size"],
        )

    def create_rule_panel(
        self,
        text: str,
        color: str,  # noqa
        cfg: dict,
    ) -> VGroup:
        label = self.create_text(text, ORIGIN, cfg["rule_font_size"], color)
        box = RoundedRectangle(
            width=cfg["rule_width"],
            height=cfg["rule_height"],
            corner_radius=cfg["rule_corner_radius"],
            stroke_color=color,
            stroke_width=cfg["rule_stroke_width"],
            fill_color=color,
            fill_opacity=cfg["rule_fill_opacity"],
        )
        label.scale_to_fit_width(cfg["rule_width"] * 0.88)
        label.move_to(box)
        return VGroup(box, label)

    # Station 04. Semantically correct program

    def animate_final_station(self) -> None:
        center = self.station_center("final_y")
        cfg = self.config["final_station"]
        timing = self.config["timing"]

        title = self.create_station_title("final", center)
        tree = self.create_tree_copy(
            center + RIGHT * cfg["tree_x"] + UP * cfg["tree_y"],
            cfg["tree_scale"],
        )

        checks = VGroup()
        for item in cfg["checks"]:
            check = self.create_check_row(item, cfg)
            checks.add(check)
        checks.arrange(DOWN, buff=cfg["check_gap"], aligned_edge=LEFT)
        checks.move_to(
            center + RIGHT * cfg["checks_x"] + UP * cfg["checks_y"],
            aligned_edge=LEFT,
        )

        ready = self.create_badge(
            cfg["ready_text"],
            ACCENT_COLOR,
            cfg["ready_width"],
            cfg["ready_height"],
            cfg["ready_font_size"],
        )
        ready.move_to(center + UP * cfg["ready_y"])

        self.play(FadeIn(title, shift=DOWN), run_time=timing["title_fade"])
        self.set_subtitle("final", center)
        self.play(FadeIn(tree, scale=0.94), run_time=cfg["tree_fade"])
        self.play(
            LaggedStart(
                *[FadeIn(check, shift=RIGHT * 0.10) for check in checks],
                lag_ratio=cfg["check_lag_ratio"],
            ),
            run_time=cfg["checks_duration"],
        )
        self.play(FadeIn(ready, scale=0.82), run_time=timing["content_fade"])

        self.set_explanation("final", center)
        self.wait(timing["normal_pause"])

    def create_check_row(self, text: str, cfg: dict) -> VGroup:
        check = self.create_text("✓", ORIGIN, cfg["check_mark_font_size"], ACCENT_COLOR)
        label = self.create_text(text, ORIGIN, cfg["check_font_size"], TEXT_COLOR)
        row = VGroup(check, label)
        row.arrange(RIGHT, buff=cfg["check_text_buff"])
        return row

    # AST and common visual elements

    def build_input_ast(self) -> None:
        cfg = self.config["ast"]
        station_cfg = self.config["ast_station"]
        center = (
            self.station_center("ast_y")
            + RIGHT * station_cfg["tree_x"]
            + UP * station_cfg["tree_y"]
        )

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
                center + RIGHT * coordinates[0] + UP * coordinates[1]
            )
            self.ast_nodes[name] = node

        for parent, child in cfg["edges"]:
            self.ast_edges[(parent, child)] = self.create_edge(
                self.ast_nodes[parent],
                self.ast_nodes[child],
            )

        tree = VGroup(
            VGroup(*self.ast_edges.values()),
            VGroup(*self.ast_nodes.values()),
        )
        tree.scale(station_cfg["tree_scale"])
        tree.move_to(center)
        self.input_tree = tree

    def create_tree_copy(
        self,
        center: np.ndarray,
        scale: float,
    ) -> VGroup:
        if self.input_tree is None:
            raise RuntimeError("AST has not been built yet.")

        tree = self.input_tree.copy()
        tree.scale(scale / self.config["ast_station"]["tree_scale"])
        tree.move_to(center)
        return tree

    def find_node_in_tree(self, tree: VGroup, name: str) -> Mobject:
        node_names = list(self.config["ast"]["positions"].keys())
        index = node_names.index(name)
        return tree[1][index]

    def create_ast_node(
        self,
        label: str,
        color: str,  # noqa
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

    def create_badge(
        self,
        text: str,
        color: str,  # noqa
        width: float,
        height: float,
        font_size: int,
    ) -> VGroup:
        box = RoundedRectangle(
            width=width,
            height=height,
            corner_radius=self.config["style"]["badge_corner_radius"],
            stroke_color=color,
            stroke_width=self.config["style"]["badge_stroke_width"],
            fill_color=color,
            fill_opacity=self.config["style"]["badge_fill_opacity"],
        )
        label = self.create_text(text, box.get_center(), font_size, color)
        label.scale_to_fit_width(width * 0.88)
        label.move_to(box)
        return VGroup(box, label)

    def replace_status(
        self,
        text: str,
        color: str,  # noqa
    ) -> Animation:
        if self.status_text is None:
            raise RuntimeError("Status text has not been created yet.")

        new_status = self.create_text(
            text,
            self.status_text.get_center(),
            self.config["symbol_station"]["status_font_size"],
            color,
        )
        return Transform(self.status_text, new_status)
