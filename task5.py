import math
from App import App


class Vector:

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y, self.z + other.z)

    def __str__(self):
        return "X {} Y {} Z {}".format(self.x, self.y, self.z)

    def to_flat_xz(self):
        return FlatVector(self.x, self.z)

    def tup(self):
        return self.x, self.y, self.z

    def rotate_x(self, angle, y, z):
        return Vector(self.x,
                      (self.y - y) * math.cos(angle) - (self.z - z) * math.sin(angle) + y,
                      (self.y - y) * math.sin(angle) + (self.z - z) * math.cos(angle) + z)

    @staticmethod
    def from_tup(tup):
        return Vector(tup[0], tup[1], tup[2])


class FlatVector:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return FlatVector(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return FlatVector(self.x - other.x, self.y - other.y)

    def __str__(self):
        return "X {} Y {}".format(self.x, self.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def tup(self):
        return self.x, self.y

    @staticmethod
    def from_tup(tup):
        return FlatVector(tup[0], tup[1])


class Polyhedron:

    def __init__(self, points, polygons, colors):
        self.vertices = [Vector.from_tup(point) for point in points]
        self.polygons = polygons
        self.colors = colors

    def polyhedron_slice(self, y):
        for polygon_index in range(len(self.polygons)):
            interval = polygon_slice(self.vertices, self.polygons[polygon_index], y)
            if interval:
                yield Segment(interval[0], interval[1], polygon_index, self)

    def rotate_x(self, angle, y, z):
        points = [point.rotate_x(angle, y, z).tup() for point in self.vertices]
        return Polyhedron(points, self.polygons, self.colors)


class Segment:

    def __init__(self, left, right, polygon_index, polyhedron):
        self.polygon_index = polygon_index
        self.left = left
        self.right = right
        self.polyhedron = polyhedron

    def Same(self, other):
        return self.polyhedron == other.polyhedron and self.polygon_index == other.polygon_index

    def __str__(self):
        return "left {} right {}".format(self.left, self.right)


def cross(vertices, polygon, y):
    for i in range(-1, len(polygon) - 1):
        if vertices[polygon[i]].y < y <= vertices[polygon[i + 1]].y or \
                vertices[polygon[i]].y >= y > vertices[polygon[i + 1]].y:
            yield i + 1


def cross_with_line(v1, v2, y):
    a = (v1.x - v2.x) / (v1.y - v2.y)
    b = (v2.x * v1.y - v1.x * v2.y) / (v1.y - v2.y)
    x = a * y + b
    a = (v1.z - v2.z) / (v1.y - v2.y)
    b = (v2.z * v1.y - v1.z * v2.y) / (v1.y - v2.y)
    z = a * y + b
    return Vector(x, y, z)


def polygon_slice(vertices, polygon, y):
    x_max_point = None
    x_min_point = None

    for vertex in cross(vertices, polygon, y):
        vertex1 = vertices[polygon[vertex]]
        vertex2 = vertices[polygon[vertex - 1]]
        intersection_point = cross_with_line(vertex1, vertex2, y)

        if not x_max_point or intersection_point.x > x_max_point.x:
            x_max_point = intersection_point
        if not x_min_point or intersection_point.x < x_min_point.x:
            x_min_point = intersection_point

    if x_min_point and x_max_point:
        return x_min_point.to_flat_xz(), x_max_point.to_flat_xz()


def polyhedrons_to_borders(polyhedrons, y):
    for polyhedron in polyhedrons:
        for segment in polyhedron.polyhedron_slice(y):
            yield segment


def find_belonging(segments, x):
    min_y = math.inf
    current_segment = None
    for segment in segments:
        left = segment.left
        right = segment.right
        if not(left.x <= x <= right.x):
            continue
        if left.x - right.x == 0:
            continue
        a = (left.y - right.y) / (left.x - right.x)
        b = (right.y * left.x - left.y * right.x) / (left.x - right.x)
        y = a * x + b
        if y < min_y:
            current_segment = segment
            min_y = y

    return current_segment


def intersect(first, second):

    x1_1, z1_1 = first.left.x, first.left.y
    x1_2, z1_2 = first.right.x, first.right.y
    x2_1, z2_1 = second.left.x, second.left.y
    x2_2, z2_2 = second.right.x, second.right.y

    def point(x, y):
        if min(x1_1, x1_2) <= x <= max(x1_1, x1_2):
            return x, y

    A1 = z1_1 - z1_2
    B1 = x1_2 - x1_1
    C1 = x1_1 * z1_2 - x1_2 * z1_1
    A2 = z2_1 - z2_2
    B2 = x2_2 - x2_1
    C2 = x2_1 * z2_2 - x2_2 * z2_1

    if B1 * A2 - B2 * A1 and A1:
        z = (C2 * A1 - C1 * A2) / (B1 * A2 - B2 * A1)
        x = (-C1 - B1 * z) / A1
        return point(x, z)
    elif B1 * A2 - B2 * A1 and A2:
        z = (C2 * A1 - C1 * A2) / (B1 * A2 - B2 * A1)
        x = (-C2 - B2 * z) / A2
        return point(x, z)


def find_all_intersections(segments):
    intersections = []
    n = len(segments)
    for i in range(n):
        for j in range(i + 1, n):
            result = intersect(segments[i], segments[j])
            if result and not (result in intersections):
                intersections.append(result)
    return [FlatVector(int(border[0]), int(border[1])) for border in intersections]


def segments_to_borders(segments):
    borders = []
    for segment in segments:
        border = segment.left.tup()
        if not(border in borders):
            borders.append(border)
        border = segment.right.tup()
        if not(border in borders):
            borders.append(border)
    return [FlatVector(int(border[0]), int(border[1])) for border in borders]


def main():
    width, height = 800, 600
    app = App((width, height))

    tetrahedron = Polyhedron(
        [(300, 100, 200), (200, 300, 100), (350, 250, 150), (400, 200, 300)],
        [[0, 1, 2], [0, 1, 3], [0, 2, 3], [1, 2, 3]],
        [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0)]
    )
    pyramid = Polyhedron(
        [(400, 100, 200), (300, 300, 200), (450, 250, 150), (550, 150, 300), (300, 200, 300)],
        [[0, 1, 2], [0, 1, 4], [0, 2, 3], [1, 2, 3, 4], [0, 3, 4]],
        [(255, 0, 255), (0, 255, 255), (0, 0, 0), (255, 255, 0), (255, 125, 125)]
    )
    polygon = Polyhedron(
        [(400, 100, 200), (300, 300, 200), (450, 250, 150), (200, 200, 300)],
        [[0, 2, 1, 3]],
        [(255, 0, 0)]
    )

    pyramid = pyramid.rotate_x(-math.pi / 3.5, 100, 200)

    polyhedrons = [pyramid]

    for y in range(height):
        segments = [segment for segment in polyhedrons_to_borders(polyhedrons, y)]

        intersections = find_all_intersections(segments)

        borders = segments_to_borders(segments)

        all_borders = intersections + borders
        all_borders = sorted(all_borders, key=lambda border: border.x)

        for i in range(len(all_borders) - 1):
            left = all_borders[i]
            right = all_borders[i + 1]
            if left.x == right.x:
                continue
            result = find_belonging(segments, (left.x + right.x) / 2)
            if result:
                app.draw_line((left.x, y), (right.x, y), color=result.polyhedron.colors[result.polygon_index])

    app.update_image()

    app.save('img.png')
    app.mainloop()


if __name__ == '__main__':
    main()
