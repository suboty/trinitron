import math
import random
from collections import deque
from typing import List, Tuple, Callable

from .entities import GraphData, NodeData


class KamadaKawaiAlgorithm:
    def __init__(
            self,
            graph: GraphData,
            width_range: Tuple[float, float],
            height_range: Tuple[float, float],
            epsilon: float = 0.001,
            max_iterations: int = 1000,
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

        for node in self.graph.nodes:
            node.pos_x = random.uniform(self.min_width, self.max_width)
            node.pos_y = random.uniform(self.min_height, self.max_height)

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
