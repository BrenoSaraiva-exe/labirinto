import itertools as it

from manim import *

from main import navigate, print_map, Point


def get_graph():
    with open("maps/01.txt", "r") as f:
        m = [[int(c) for c in line if c != "\n"] for line in f.readlines()]
        vertices = [
            Point(x, y) for y, row in enumerate(m) for x, v in enumerate(row) if v == 0
        ]

        start, end = [
            Point(x, y) for y, row in enumerate(m) for x, v in enumerate(row) if v == 2
        ]

        vertices.append(start)
        vertices.append(end)

        indexed_vertices = dict(enumerate(vertices))
        edges = [
            (a[0], b[0])
            for a, b in it.combinations(indexed_vertices.items(), 2)
            if a[1].is_neighbor(b[1]) == 1
        ]

        return edges, indexed_vertices, m


class Intro(Scene):
    def construct(self):
        edges, vertices, matrix = get_graph()
        # matrix = [row[::-1] for row in matrix]
        g = Graph(vertices.keys(), edges)

        m = Matrix(matrix)
        m.scale(0.75)

        self.play(Write(m))
        self.wait(1)
        self.play(Unwrite(m))

        # Draw dots
        self.play(Create(g))
        self.play(
            g[k].animate.move_to([v.x - 4.5, v.y - 4.5, 0]) for k, v in vertices.items()
        )
        self.wait(1)

        # Highlight start and end
        self.play(
            [
                g[len(vertices) - 1].animate.set_color(RED),
                g[len(vertices) - 2].animate.set_color(RED),
            ]
        )

        self.wait(0.5)

        # Draw path
        path = navigate(
            matrix, vertices[len(vertices) - 2], vertices[len(vertices) - 1]
        )

        vertices_values = list(vertices.values())

        self.play(
            g[vertices_values.index(path[i])].animate.set_color(RED)
            for i in range(len(path) - 1)
        )

        self.wait(1.5)
