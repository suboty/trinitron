from typing import List, Tuple

from manim import *

from .base import ObjectBase
from .entities import FigureTypesForText, GraphData, NodeData
from .algorithms import KamadaKawaiAlgorithm
from .text import (
    TextInSomething,
    TextInCircle,
    TextInEllipse,
    TextInBox
)


class GraphNode(ObjectBase):
    def __init__(
            self,
            label: str,
            label_font_size: int = 24,
            label_color: ManimColor | str = BLACK, # noqa
            figure_color: ManimColor | str = BLUE, # noqa
            node_radius: float = 0.5,
            shape: FigureTypesForText = FigureTypesForText.circle,
    ):
        super().__init__()

        self.label = label
        self.label_font_size = label_font_size
        self.label_color = (
            label_color if isinstance(label_color, ManimColor) else ManimColor(label_color)
        )
        self.figure_color = (
            figure_color if isinstance(figure_color, ManimColor) else ManimColor(figure_color)
        )
        self.node_radius = node_radius
        self.shape = shape

        self.node: TextInSomething | None = None
        self.position = ORIGIN

    def create(self) -> 'GraphNode':
        if self.shape == FigureTypesForText.circle:
            self.node = TextInCircle(
                text=self.label,
                text_font_size=self.label_font_size,
                text_color=self.label_color,
                figure_color=self.figure_color,
                circle_radius=self.node_radius,
            ).create()
        elif self.shape == FigureTypesForText.ellipse:
            self.node = TextInEllipse(
                text=self.label,
                text_font_size=self.label_font_size,
                text_color=self.label_color,
                figure_color=self.figure_color,
                ellipse_width=self.node_radius * 2,
                ellipse_height=self.node_radius * 1.2,
            ).create()
        else:
            self.node = TextInBox(
                text=self.label,
                text_font_size=self.label_font_size,
                text_color=self.label_color,
                figure_color=self.figure_color,
                box_width=self.node_radius * 2,
                box_height=self.node_radius * 1.2,
            ).create()
        self.add(self.node)
        return self

    def set_position(self, x: float, y: float) -> 'GraphNode':
        self.position = np.array([x, y, 0])
        self.node.shift(self.position)
        return self

    def get_center(self) -> np.ndarray:
        return self.node.get_center()


class Graph(ObjectBase):
    DEFAULT_NODE_RADIUS = 0.5
    DEFAULT_EDGE_COLOR = WHITE
    DEFAULT_EDGE_STROKE_WIDTH = 3
    LEFT_LIMIT = -4.0
    RIGHT_LIMIT = 4.0
    TOP_LIMIT = 1.5
    BOTTOM_LIMIT = -2.0
    DEFAULT_FILL_OPACITY = 0.9

    def __init__(
            self,
            nodes: List[str],
            edges: List[Tuple[int, int]],
            node_color: ManimColor | str = BLUE, # noqa
            node_radius: float = DEFAULT_NODE_RADIUS,
            edge_color: ManimColor | str = DEFAULT_EDGE_COLOR, # noqa
            edge_stroke_width: int = DEFAULT_EDGE_STROKE_WIDTH,
            shape: FigureTypesForText = FigureTypesForText.circle,
            epsilon: float = 0.001,
            max_iterations: int = 1000,
    ):
        super().__init__()

        self._all_objects = None
        self.nodes_labels = nodes
        self.edges = edges
        self.node_color = (
            node_color if isinstance(node_color, ManimColor) else ManimColor(node_color)
        )
        self.node_radius = node_radius
        self.edge_color = (
            edge_color if isinstance(edge_color, ManimColor) else ManimColor(edge_color)
        )
        self.edge_stroke_width = edge_stroke_width
        self.shape = shape
        self.epsilon = epsilon
        self.max_iterations = max_iterations

        self.graph_nodes: List[GraphNode] = []
        self.edge_lines: List[Line] = []

    def _calculate_positions(self) -> List[Tuple[float, float]]:
        node_data = [NodeData(name=label) for label in self.nodes_labels]
        graph_data = GraphData(nodes=node_data, edges=self.edges)

        width_range = (self.LEFT_LIMIT, self.RIGHT_LIMIT)
        height_range = (self.BOTTOM_LIMIT, self.TOP_LIMIT)

        kk = KamadaKawaiAlgorithm(
            graph=graph_data,
            width_range=width_range,
            height_range=height_range,
            epsilon=self.epsilon,
            max_iterations=self.max_iterations,
        )

        result = kk.run()

        return [(node.pos_x, node.pos_y) for node in result]

    def create(self) -> 'Graph':
        positions = self._calculate_positions()

        self.graph_nodes = []
        self.edge_lines = []
        self._all_objects = []

        for edge in self.edges:
            if len(edge) >= 2:
                start_idx, end_idx = edge[0], edge[1]
                if start_idx < len(self.nodes_labels) and end_idx < len(self.nodes_labels):
                    start_pos = positions[start_idx]
                    end_pos = positions[end_idx]

                    line = Line(
                        np.array([start_pos[0], start_pos[1], 0]),
                        np.array([end_pos[0], end_pos[1], 0]),
                        color=self.edge_color,
                        stroke_width=self.edge_stroke_width,
                    )
                    self.edge_lines.append(line)
                    self._all_objects.append(line)
                    self.add(line)

        for i, label in enumerate(self.nodes_labels):
            node = GraphNode(
                label=label,
                label_font_size=24,
                label_color=BLACK,
                figure_color=self.node_color,
                node_radius=self.node_radius,
                shape=self.shape,
            ).create()

            x, y = positions[i]
            node.set_position(x, y)
            self.graph_nodes.append(node)
            self._all_objects.append(node)
            self.add(node)

        return self

    def get_node(self, index: int) -> GraphNode | None:
        if 0 <= index < len(self.graph_nodes):
            return self.graph_nodes[index]
        return None

    def get_edge(self, index: int) -> Line | None:
        if 0 <= index < len(self.edge_lines):
            return self.edge_lines[index]
        return None

    def highlight_node(
            self,
            index: int,
            color: ManimColor, # noqa
            scene: Scene
    ) -> None:
        node = self.get_node(index)
        if node:
            scene.play(node.node.animate.set_color(color))

    def highlight_edge(
            self,
            index: int,
            color: ManimColor,
            scene: Scene
    ) -> None:
        edge = self.get_edge(index)
        if edge:
            scene.play(edge.animate.set_color(color))

    def animate_in(
            self,
            scene: Scene,
            run_time: float = ObjectBase.DEFAULT_DURATION,
            **kwargs,
    ) -> None:
        if not self._all_objects:
            self.create()

        for obj in self._all_objects:
            if hasattr(obj, 'set_fill'):
                obj.set_fill(opacity=0)
                obj.set_stroke(opacity=0)
            elif hasattr(obj, 'set_opacity'):
                obj.set_opacity(0)

        scene.add(self)

        edge_animations = []
        for obj in self.edge_lines:
            if hasattr(obj, 'set_stroke'):
                edge_animations.append(
                    obj.animate.set_stroke(opacity=1)
                )
            elif hasattr(obj, 'set_opacity'):
                edge_animations.append(
                    obj.animate.set_opacity(1)
                )

        node_animations = []
        for obj in self.graph_nodes:
            if hasattr(obj, 'set_fill'):
                node_animations.append(
                    obj.animate
                    .set_fill(opacity=self.DEFAULT_FILL_OPACITY)
                    .set_stroke(opacity=1)
                )
            elif hasattr(obj, 'set_opacity'):
                node_animations.append(
                    obj.animate.set_opacity(1)
                )

        all_animations = edge_animations + node_animations

        if all_animations:
            scene.play(
                AnimationGroup(
                    *all_animations,
                    lag_ratio=kwargs.get('lag_ratio', self.DEFAULT_LAG_RATIO),
                ),
                run_time=run_time,
            )

    def animate_out(
            self,
            scene: Scene,
            run_time: float = 1,
            **kwargs,
    ) -> None:
        if not self._all_objects:
            return

        node_animations = []
        for obj in self.graph_nodes:
            if hasattr(obj, 'set_fill'):
                node_animations.append(
                    obj.animate
                    .set_fill(opacity=0)
                    .set_stroke(opacity=0)
                )
            elif hasattr(obj, 'set_opacity'):
                node_animations.append(
                    obj.animate.set_opacity(0)
                )

        edge_animations = []
        for obj in self.edge_lines:
            if hasattr(obj, 'set_stroke'):
                edge_animations.append(
                    obj.animate.set_stroke(opacity=0)
                )
            elif hasattr(obj, 'set_opacity'):
                edge_animations.append(
                    obj.animate.set_opacity(0)
                )

        all_animations = node_animations + edge_animations

        if all_animations:
            scene.play(
                AnimationGroup(
                    *all_animations,
                    lag_ratio=kwargs.get('lag_ratio', self.DEFAULT_LAG_RATIO),
                ),
                run_time=run_time,
            )

        scene.remove(self)
