import math
import random
from collections import deque
from typing import List, Tuple, Callable
from dataclasses import dataclass

from .entities import GraphData, NodeData


@dataclass
class InitSchemaTypes:
    random = 'random'
    zeros = 'zeros'


@dataclass
class Directions:
    LR = 'lr'
    TB = 'tb'


class KamadaKawaiAlgorithm:
    def __init__(
            self,
            graph: GraphData,
            width_range: Tuple[float, float],
            height_range: Tuple[float, float],
            epsilon: float = 0.001,
            max_iterations: int = 1000,
            init_schema: InitSchemaTypes = InitSchemaTypes.zeros,
            direction: Directions = Directions.LR,
    ):
        self.graph = graph
        self.min_width, self.max_width = width_range
        self.min_height, self.max_height = height_range
        self.epsilon = epsilon
        self.max_iterations = max_iterations
        self.iter_count = 0

        self.d = self.all_pairs_shortest_path()
        self.diam = max(max(row) for row in self.d)

        self.l = []
        self.k = []
        self.get_distance_and_spring_strength()

        match init_schema:
            case 'random':
                for node in self.graph.nodes:
                    node.pos_x = random.uniform(self.min_width, self.max_width)
                    node.pos_y = random.uniform(self.min_height, self.max_height)
            case 'zeros':
                for node in self.graph.nodes:
                    node.pos_x = random.uniform(-0.1, 0.1)
                    node.pos_y = random.uniform(-0.1, 0.1)

        if direction == 'tb':
            self.rotate_positions_90_degrees_right()

    def rotate_positions_90_degrees_right(self):
        center_x = (self.min_width + self.max_width) / 2
        center_y = (self.min_height + self.max_height) / 2

        for node in self.graph.nodes:
            rel_x = node.pos_x - center_x
            rel_y = node.pos_y - center_y
            new_rel_x = rel_y
            new_rel_y = -rel_x
            node.pos_x = center_x + new_rel_x
            node.pos_y = center_y + new_rel_y

    def all_pairs_shortest_path(self) -> List[List[float]]:
        n = len(self.graph.nodes)
        dist = [[math.inf for _ in range(n)] for _ in range(n)]

        adj_list = [[] for _ in range(n)]
        for start_idx, end_idx in self.graph.edges:
            adj_list[start_idx].append(end_idx)
            adj_list[end_idx].append(start_idx)

        for start in range(n):
            queue = deque([start])
            dist[start][start] = 0

            while queue:
                v = queue.popleft()
                for neighbor in adj_list[v]:
                    if dist[start][neighbor] == math.inf:
                        dist[start][neighbor] = dist[start][v] + 1
                        queue.append(neighbor)

        return dist

    def get_distance_and_spring_strength(self):
        l0 = math.sqrt((self.max_width - self.min_width) * (self.max_height - self.min_height)) / 2
        n = len(self.graph.nodes)

        self.l = [[0] * n for _ in range(n)]
        self.k = [[0] * n for _ in range(n)]

        for i in range(n):
            for j in range(n):
                if i != j:
                    l_ij = l0 * self.d[i][j] / self.diam
                    self.l[i][j] = l_ij # noqa
                    self.k[i][j] = 1.0 / (l_ij * l_ij) # noqa

    def calculate_displacement_energy(self, i: int, new_x: float, new_y: float) -> float:
        E = 0.0
        for j, node in enumerate(self.graph.nodes):
            if i == j:
                continue

            dx = new_x - node.pos_x
            dy = new_y - node.pos_y
            dist = math.sqrt(dx * dx + dy * dy)

            delta = dist - self.l[i][j]
            E += 0.5 * self.k[i][j] * delta * delta

        return E

    @staticmethod
    def golden_ratio(
            start_index: int,
            start_node: NodeData,
            direction: Tuple[float, float],
            energy_func: Callable,
    ) -> float:
        phi = (1 + math.sqrt(5)) / 2
        a = 0.0
        b = 1.0
        tolerance = 0.001

        x1 = b - (b - a) / phi
        x2 = a + (b - a) / phi

        while (b - a) > tolerance:
            f1 = energy_func(
                start_index,
                start_node.pos_x - x1 * direction[0],
                start_node.pos_y - x1 * direction[1]
            )
            f2 = energy_func(
                start_index,
                start_node.pos_x - x2 * direction[0],
                start_node.pos_y - x2 * direction[1]
            )

            if f1 < f2:
                b = x2
                x2 = x1
                x1 = b - (b - a) / phi
            else:
                a = x1
                x1 = x2
                x2 = a + (b - a) / phi

        return (a + b) / 2

    def step(self) -> int:
        self.iter_count += 1

        max_grad = 0.0
        target = -1
        target_grad_x = 0.0
        target_grad_y = 0.0

        for i, i_node in enumerate(self.graph.nodes):
            grad_x = 0.0
            grad_y = 0.0

            for j, j_node in enumerate(self.graph.nodes):
                if i == j:
                    continue

                dx = i_node.pos_x - j_node.pos_x
                dy = i_node.pos_y - j_node.pos_y
                dist = math.sqrt(dx * dx + dy * dy)

                if dist < 0.001:
                    dist = 0.001

                force = self.k[i][j] * (dist - self.l[i][j]) / dist
                grad_x += force * dx
                grad_y += force * dy

            grad_norm = math.sqrt(grad_x * grad_x + grad_y * grad_y)

            if grad_norm > max_grad:
                max_grad = grad_norm
                target = i
                target_grad_x = grad_x
                target_grad_y = grad_y

        if max_grad < self.epsilon:
            return -1

        lambda_opt = self.golden_ratio(
            start_index=target,
            start_node=self.graph.nodes[target],
            direction=(target_grad_x, target_grad_y),
            energy_func=self.calculate_displacement_energy
        )

        self.graph.nodes[target].pos_x -= lambda_opt * target_grad_x
        self.graph.nodes[target].pos_y -= lambda_opt * target_grad_y

        return target

    def run(self) -> List[NodeData]:
        for _ in range(self.max_iterations):
            moved = self.step()
            if moved == -1:
                break

        return self.graph.nodes

    def __call__(self) -> int:
        return self.step()


@dataclass
class ReingoldTilfordAlgorithm:
    def __init__(
            self,
            graph: GraphData,
            width_range: Tuple[float, float],
            height_range: Tuple[float, float],
            horizontal_spacing: float = 1.0,
            vertical_spacing: float = 1.0,
            direction: Directions = Directions.TB,
    ):
        self.graph = graph
        self.min_width, self.max_width = width_range
        self.min_height, self.max_height = height_range
        self.horizontal_spacing = horizontal_spacing
        self.vertical_spacing = vertical_spacing
        self.direction = direction

        self._normalize_factor = 1.0

        self.root = self._find_root()
        if self.root is None:
            raise ValueError(
                "Graph must have exactly one root node (node with parent=None)"
            )

        self._init_temp_fields()

    def _find_root(self) -> NodeData | None:
        roots = [node for node in self.graph.nodes if node.parent is None]
        if len(roots) == 0:
            all_children = set()
            for node in self.graph.nodes:
                all_children.update(node.children)
            for node in self.graph.nodes:
                if node not in all_children:
                    return node
            return None
        return roots[0] if roots else None

    def _init_temp_fields(self):
        for node in self.graph.nodes:
            node.mod = 0.0
            node.thread = None
            node.ancestor = node

    @staticmethod
    def get_left_sibling(node: NodeData) -> NodeData | None:
        if node.parent is None:
            return None
        siblings = node.parent.children
        try:
            index = siblings.index(node)
        except ValueError:
            return None
        if index > 0:
            return siblings[index - 1]
        return None

    @staticmethod
    def get_first_child(node: NodeData) -> NodeData | None:
        return node.children[0] if node.children else None

    @staticmethod
    def get_last_child(node: NodeData) -> NodeData | None:
        return node.children[-1] if node.children else None

    def first_walk(self, node: NodeData, depth: int) -> None:
        node.pos_y = depth * self.vertical_spacing

        if not node.children:
            if node.parent is not None:
                left_sibling = self.get_left_sibling(node)
                if left_sibling is not None:
                    node.pos_x = left_sibling.pos_x + self.horizontal_spacing
            else:
                node.pos_x = 0.0
        else:
            for child in node.children:
                self.first_walk(child, depth + 1)

            first_child = self.get_first_child(node)
            last_child = self.get_last_child(node)
            if first_child is not None and last_child is not None:
                mid = (first_child.pos_x + last_child.pos_x) / 2.0
            else:
                mid = 0.0

            left_sibling = self.get_left_sibling(node)
            if left_sibling is not None:
                node.pos_x = left_sibling.pos_x + self.horizontal_spacing
                node.mod = node.pos_x - mid
            else:
                node.pos_x = mid

    def second_walk(self, node: NodeData, cum_mod: float) -> None:
        node.pos_x = node.pos_x + cum_mod
        for child in node.children:
            self.second_walk(child, cum_mod + (node.mod or 0.0))

    def normalize_coordinates(self) -> None:
        if not self.graph.nodes:
            return

        min_x = min(node.pos_x for node in self.graph.nodes)
        max_x = max(node.pos_x for node in self.graph.nodes)
        min_y = min(node.pos_y for node in self.graph.nodes)
        max_y = max(node.pos_y for node in self.graph.nodes)

        x_range = max_x - min_x
        y_range = max_y - min_y
        target_x_range = self.max_width - self.min_width
        target_y_range = self.max_height - self.min_height

        for node in self.graph.nodes:
            norm_x = (node.pos_x - min_x) / x_range if x_range > 0 else 0.5
            norm_y = (node.pos_y - min_y) / y_range if y_range > 0 else 0.5

            node.pos_x = self.min_width + norm_x * target_x_range
            node.pos_y = self.min_height + norm_y * target_y_range

    def apply_direction(self) -> None:
        if self.direction == 'tb':
            min_y = min(node.pos_y for node in self.graph.nodes)
            max_y = max(node.pos_y for node in self.graph.nodes)
            for node in self.graph.nodes:
                node.pos_y = max_y + min_y - node.pos_y

        elif self.direction == 'lr':
            center_x = sum(node.pos_x for node in self.graph.nodes) / len(self.graph.nodes)
            center_y = sum(node.pos_y for node in self.graph.nodes) / len(self.graph.nodes)
            for node in self.graph.nodes:
                rel_x = node.pos_x - center_x
                rel_y = node.pos_y - center_y
                new_rel_x = rel_y
                new_rel_y = -rel_x
                node.pos_x = center_x + new_rel_x
                node.pos_y = center_y + new_rel_y
            min_y = min(node.pos_y for node in self.graph.nodes)
            max_y = max(node.pos_y for node in self.graph.nodes)
            for node in self.graph.nodes:
                node.pos_y = max_y + min_y - node.pos_y

    def run(self) -> List[NodeData]:
        if self.root is None:
            raise ValueError(
                "No root node found in the graph"
            )

        self._init_temp_fields()

        self.first_walk(self.root, 0)
        self.second_walk(self.root, 0.0)

        self.normalize_coordinates()

        self.apply_direction()

        return self.graph.nodes

    def __call__(self) -> List[NodeData]:
        return self.run()

    def step(self) -> int:
        self.run()
        return -1
