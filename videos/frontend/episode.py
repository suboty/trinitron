from _base_animation.common import *


def load_scene_config(
    config_path: str = Path("videos", "frontend", "config.yaml"),
) -> dict:
    with open(config_path, "r", encoding="utf-8") as file:
        return yaml.safe_load(file)["frontend"]


SCENE_CONFIG = load_scene_config()


class FrontendAnimation(BaseAnimation):
    def __init__(
        self,
        camera_class: type[Camera] = MovingCamera,
        **kwargs: Any,
    ) -> None:
        super().__init__(camera_class, **kwargs)
        self.config = SCENE_CONFIG
        self.subtitle: Text | None = None
        self.explanation: Text | None = None

    def construct(self) -> None:
        camera = self.config["camera"]
        self.camera.background_color = BACKGROUND
        self.camera.frame.width = camera["frame_width"]  # noqa
        self.camera.frame.move_to(self.station_center("source_y"))  # noqa

        self.animate_source_station()
        self.move_to_station("stages_y")
        self.animate_stages_station()
        self.move_to_station("pipeline_y")
        self.animate_pipeline_station()
        self.move_to_station("boundary_y")
        self.animate_boundary_station()
        self.wait(self.config["timing"]["final_hold"])

    # Station 01. Source Code

    def animate_source_station(self) -> None:
        center = self.station_center("source_y")
        cfg = self.config["source_station"]
        timing = self.config["timing"]
        title = self.create_station_title("source", center)

        code_box = RoundedRectangle(
            width=cfg["code_box_width"],
            height=cfg["code_box_height"],
            corner_radius=cfg["code_box_corner_radius"],
            stroke_color=ACCENT_COLOR,
            stroke_width=cfg["code_box_stroke_width"],
            fill_color=ACCENT_COLOR,
            fill_opacity=cfg["code_box_fill_opacity"],
        ).move_to(center + UP * cfg["code_y"])
        code = self.create_text(
            "int result = max(a + b, 42);",
            code_box.get_center(),
            cfg["code_font_size"],
            TEXT_COLOR,
        )
        code.scale_to_fit_width(cfg["code_box_width"] * 0.9)

        question = self.create_text(
            "How does the compiler understand this?",
            center + UP * cfg["question_y"],
            cfg["question_font_size"],
            MUTED_COLOR,
        )

        labels = VGroup(
            self.create_badge(
                "LEXER", KEYWORD_COLOR, cfg["label_width"],
                cfg["label_height"], cfg["label_font_size"]
            ),
            self.create_badge(
                "PARSER", IDENTIFIER_COLOR, cfg["label_width"],
                cfg["label_height"], cfg["label_font_size"]
            ),
            self.create_badge(
                "SEMANTICS", ACCENT_COLOR, cfg["label_width"],
                cfg["label_height"], cfg["label_font_size"]
            ),
        )
        labels.arrange(RIGHT, buff=cfg["label_gap"])
        labels.move_to(center + UP * cfg["labels_y"])

        self.play(FadeIn(title, shift=DOWN), run_time=timing["title_fade"])
        self.set_subtitle("source", center)
        self.play(Create(code_box), FadeIn(code), run_time=timing["content_fade"])
        self.set_subtitle("source_question", center)
        self.play(
            FadeIn(question),
            LaggedStart(
                *[FadeIn(x, shift=UP * 0.08) for x in labels],
                lag_ratio=0.18
            ), run_time=1.2
        )
        self.set_explanation("source", center)
        self.wait(timing["normal_pause"])

    # Station 02. Three stages

    def animate_stages_station(self) -> None:
        center = self.station_center("stages_y")
        cfg = self.config["stages_station"]
        timing = self.config["timing"]
        title = self.create_station_title("stages", center)

        specs = [
            ("LEXICAL ANALYSIS", "characters  →  tokens", KEYWORD_COLOR, "lexer"),
            ("SYNTAX ANALYSIS", "tokens  →  AST", IDENTIFIER_COLOR, "parser"),
            ("SEMANTIC ANALYSIS", "AST  →  checked AST", ACCENT_COLOR, "semantic"),
        ]
        cards = VGroup(*[self.create_stage_card(a, b, c, cfg) for a, b, c, _ in specs])
        cards.arrange(DOWN, buff=cfg["stage_gap"])
        cards.move_to(center + UP * 0.75)

        arrows = VGroup()
        for upper, lower in zip(cards[:-1], cards[1:]):
            arrows.add(Arrow(
                upper.get_bottom(),
                lower.get_top(),
                buff=0.08,
                color=BORDER_COLOR,
                stroke_width=cfg["arrow_stroke_width"],
                max_tip_length_to_length_ratio=0.22,
            ))

        self.play(FadeIn(title, shift=DOWN), run_time=timing["title_fade"])
        for index, (_, _, color, subtitle_key) in enumerate(specs): # noqa
            self.set_subtitle(subtitle_key, center)
            self.play(
                FadeIn(cards[index], shift=RIGHT * 0.12),
                run_time=timing["content_fade"]
            )
            self.play(Indicate(cards[index], color=color), run_time=cfg["highlight_duration"])
            if index < len(arrows):
                self.play(GrowArrow(arrows[index]), run_time=0.6)
        self.set_explanation("stages", center)
        self.wait(timing["normal_pause"])

    def create_stage_card(
            self,
            name: str,
            transformation: str,
            color: str, # noqa
            cfg: dict
    ) -> VGroup:
        box = RoundedRectangle(
            width=cfg["stage_width"],
            height=cfg["stage_height"],
            corner_radius=cfg["stage_corner_radius"],
            stroke_color=color,
            stroke_width=cfg["stage_stroke_width"],
            fill_color=color,
            fill_opacity=cfg["stage_fill_opacity"],
        )
        name_text = self.create_text(name, ORIGIN, cfg["name_font_size"], color)
        transformation_text = self.create_text(
            transformation, ORIGIN,
            cfg["transformation_font_size"], TEXT_COLOR
        )
        content = VGroup(name_text, transformation_text).arrange(DOWN, buff=0.12)
        content.move_to(box)
        return VGroup(box, content)

    # Station 03. Frontend architecture

    def animate_pipeline_station(self) -> None:
        center = self.station_center("pipeline_y")
        cfg = self.config["pipeline_station"]
        timing = self.config["timing"]
        title = self.create_station_title("pipeline", center)

        source = self.create_pipeline_box(
            "SOURCE", MUTED_COLOR, cfg["source_width"],
            cfg["source_height"], cfg
        )
        source.move_to(
            center + RIGHT * cfg["source_x"] + UP * cfg["source_y"]
        )

        lexer = self.create_pipeline_box(
            "LEXER", KEYWORD_COLOR,
            cfg["stage_width"], cfg["stage_height"], cfg
        )
        parser = self.create_pipeline_box(
            "PARSER", IDENTIFIER_COLOR,
            cfg["stage_width"], cfg["stage_height"], cfg
        )
        semantic = self.create_pipeline_box(
            "SEMANTIC", ACCENT_COLOR,
            cfg["stage_width"], cfg["stage_height"], cfg
        )
        lexer.move_to(
            center + RIGHT * cfg["lexer_x"] + UP * cfg["stage_y"]
        )
        parser.move_to(
            center + RIGHT * cfg["parser_x"] + UP * cfg["stage_y"]
        )
        semantic.move_to(
            center + RIGHT * cfg["semantic_x"] + UP * cfg["stage_y"]
        )

        boxes = [source, lexer, parser, semantic]
        arrows = VGroup(*[
            Arrow(
                a.get_right(), b.get_left(),
                buff=0.09, color=BORDER_COLOR, stroke_width=cfg["arrow_stroke_width"]
            )
            for a, b in zip(boxes[:-1], boxes[1:])
        ])

        artifacts = VGroup(
            self.create_text(
                "characters", center + RIGHT * -2.8 + UP * cfg["output_y"],
                cfg["artifact_font_size"], MUTED_COLOR
            ),
            self.create_text(
                "tokens", center + RIGHT * -1.1 + UP * cfg["output_y"],
                cfg["artifact_font_size"], KEYWORD_COLOR
            ),
            self.create_text(
                "AST", center + RIGHT * 0.5 + UP * cfg["output_y"],
                cfg["artifact_font_size"], IDENTIFIER_COLOR
            ),
            self.create_text(
                "checked AST", center + RIGHT * 2 + UP * cfg["output_y"],
                cfg["artifact_font_size"], ACCENT_COLOR
            ),
        )

        frontend_frame = RoundedRectangle(
            width=cfg["frontend_box_width"],
            height=cfg["frontend_box_height"],
            corner_radius=cfg["box_corner_radius"],
            stroke_color=ACCENT_COLOR,
            stroke_width=cfg["box_stroke_width"],
        ).move_to(center + RIGHT * 0.45 + UP * cfg["frontend_box_y"])
        frontend_label = self.create_text(
            "COMPILER FRONTEND",
            center + RIGHT * 0.45 + UP * cfg["frontend_label_y"],
            cfg["frontend_label_font_size"],
            ACCENT_COLOR,
        )

        self.play(FadeIn(title, shift=DOWN), run_time=timing["title_fade"])
        self.set_subtitle("pipeline", center)
        self.play(FadeIn(source), run_time=0.5)
        for index, stage in enumerate([lexer, parser, semantic]):
            self.play(
                GrowArrow(arrows[index]),
                FadeIn(stage, shift=RIGHT * 0.08),
                run_time=0.8
            )
        self.play(
            LaggedStart(
                *[FadeIn(x, shift=UP * 0.06) for x in artifacts],
                lag_ratio=0.14
            ),
            run_time=1
        )
        self.play(Create(frontend_frame), FadeIn(frontend_label), run_time=0.75)
        self.set_explanation("pipeline", center)
        self.wait(timing["normal_pause"])

    def create_pipeline_box(
            self,
            text: str,
            color: str, # noqa
            width: float,
            height: float,
            cfg: dict
    ) -> VGroup:
        box = RoundedRectangle(
            width=width,
            height=height,
            corner_radius=cfg["box_corner_radius"],
            stroke_color=color,
            stroke_width=cfg["box_stroke_width"],
            fill_color=color,
            fill_opacity=cfg["box_fill_opacity"],
        )
        label = self.create_text(text, box.get_center(), cfg["box_font_size"], color)
        label.scale_to_fit_width(width * 0.82)
        return VGroup(box, label)

    # Station 04. Frontend and Backend

    def animate_boundary_station(self) -> None:
        center = self.station_center("boundary_y")
        cfg = self.config["boundary_station"]
        timing = self.config["timing"]
        title = self.create_station_title("boundary", center)

        frontend = self.create_phase_block(
            "FRONTEND",
            ["tokens", "AST", "symbols", "types"],
            ACCENT_COLOR,
            cfg,
        ).move_to(center + RIGHT * cfg["frontend_x"] + UP * cfg["block_y"])

        backend = self.create_phase_block(
            "BACKEND",
            ["optimization", "instructions", "registers", "machine code"],
            MUTED_COLOR,
            cfg,
        ).move_to(center + RIGHT * cfg["backend_x"] + UP * cfg["block_y"])
        backend.set_opacity(0.42)

        separator = DashedLine(
            center + RIGHT * cfg["separator_x"] + UP * (cfg["separator_height"] / 2 + 0.15),
            center + RIGHT * cfg["separator_x"] + DOWN * (cfg["separator_height"] / 2 - 0.15),
            color=BORDER_COLOR,
            stroke_width=cfg["separator_stroke_width"],
        )

        arrow = Arrow(
            frontend.get_bottom() + DOWN * 0.12,
            center + UP * cfg["ir_y"] + UP * cfg["ir_height"] / 2,
            color=ACCENT_COLOR,
            stroke_width=cfg["arrow_stroke_width"],
        )
        ir = self.create_badge(
            "INTERMEDIATE REPRESENTATION", ACCENT_COLOR,
            cfg["ir_width"], cfg["ir_height"], cfg["ir_font_size"]
        )
        ir.move_to(center + UP * cfg["ir_y"])

        self.play(FadeIn(title, shift=DOWN), run_time=timing["title_fade"])
        self.set_subtitle("boundary", center)
        self.play(FadeIn(frontend), Create(separator), FadeIn(backend), run_time=1)
        self.play(Indicate(frontend, color=ACCENT_COLOR), run_time=0.7)
        self.play(GrowArrow(arrow), FadeIn(ir, scale=0.86), run_time=0.8)
        self.set_subtitle("teaser", center)
        self.set_explanation("boundary", center)
        self.wait(timing["normal_pause"])

    def create_phase_block(
            self,
            title: str,
            lines: list[str],
            color: str, # noqa
            cfg: dict
    ) -> VGroup:
        box = RoundedRectangle(
            width=cfg["block_width"],
            height=cfg["block_height"],
            corner_radius=cfg["block_corner_radius"],
            stroke_color=color,
            stroke_width=cfg["block_stroke_width"],
            fill_color=color,
            fill_opacity=cfg["block_fill_opacity"],
        )
        heading = self.create_text(title, ORIGIN, cfg["block_title_font_size"], color)
        items = VGroup(*[
            self.create_text(f"• {line}", ORIGIN, cfg["block_line_font_size"], TEXT_COLOR)
            for line in lines
        ])
        items.arrange(DOWN, buff=0.12, aligned_edge=LEFT)
        content = VGroup(heading, items).arrange(DOWN, buff=0.25)
        content.move_to(box)
        return VGroup(box, content)

    def create_badge(
            self,
            text: str,
            color: str, # noqa
            width: float,
            height: float,
            font_size: int
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
        return VGroup(box, label)
