from App import App


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

    def angle_direction(self, vector):
        return sign(self.x * vector.y - self.y * vector.x)

    def tup(self):
        return self.x, self.y

    @staticmethod
    def from_tup(tup):
        return FlatVector(tup[0], tup[1])


def sign(x):
    if x > 0:
        return 1.
    elif x < 0:
        return -1.
    elif x == 0:
        return 0.
    else:
        return x


def find_non_convex_vertex(vectors):
    for i in range(0, len(vectors)):
        a = vectors[i] - vectors[i - 1]
        b = vectors[(i + 1) % len(vectors)] - vectors[i]
        if a.angle_direction(b) < 0:
            return i


def cross_segments(v11, v12, v21, v22):
    cut1 = v12 - v11
    cut2 = v22 - v21

    dir1 = cut1.angle_direction(v21 - v11)
    dir2 = cut1.angle_direction(v22 - v11)

    if dir1 == dir2:
        return False

    dir1 = cut2.angle_direction(v11 - v21)
    dir2 = cut2.angle_direction(v12 - v21)

    if dir1 == dir2:
        return False

    return True


def find_intersection(vectors, first, second):
    n = len(vectors)
    index = (second + 1) % n
    while (index + 1) % n != first:
        result = cross_segments(vectors[first], vectors[second], vectors[index], vectors[(index + 1) % n])
        if result:
            return index, (index + 1) % n
        index = (index + 1) % n

    index = (second - 1 + n) % n
    while (index - 1 + n) % n != first:
        result = cross_segments(vectors[first], vectors[second], vectors[index], vectors[(index - 1 + n) % n])
        if result:
            return index, (index - 1 + n) % n
        index = (index - 1 + n) % n


def break_into_convex_polygons(vectors):
    non_convex_vertex = find_non_convex_vertex(vectors)

    if not non_convex_vertex:
        return [vectors]

    n = len(vectors)
    for direction in [-1, 1]:
        opposite_vertex = (non_convex_vertex + n // 2) % n
        while (opposite_vertex + direction + n) % n != non_convex_vertex:
            a = vectors[non_convex_vertex] - vectors[non_convex_vertex - 1]
            b = vectors[opposite_vertex] - vectors[non_convex_vertex]
            c = vectors[(non_convex_vertex + 1) % n] - vectors[non_convex_vertex]

            result = find_intersection(vectors, non_convex_vertex, opposite_vertex)
            if (a.angle_direction(b) > 0 or c.angle_direction(b) > 0) and not result:
                first_polygon = vectors[min(non_convex_vertex, opposite_vertex):
                                        max(non_convex_vertex, opposite_vertex) + 1]
                second_polygon = vectors[:min(non_convex_vertex, opposite_vertex) + 1] + \
                                 vectors[max(non_convex_vertex, opposite_vertex):]
                return break_into_convex_polygons(first_polygon) + break_into_convex_polygons(second_polygon)
            opposite_vertex = (opposite_vertex + direction + n) % n


def triangulate_convex_polygon(vectors):
    main_vertex = vectors[0]
    previous_vertex = vectors[1]
    for vertex in vectors[2:]:
        yield [main_vertex, previous_vertex, vertex]
        previous_vertex = vertex


def polygons_to_segments(polygons):
    segments = set()
    for polygon in polygons:
        for i in range(len(polygon)):
            first_vertex = polygon[i]
            second_vertex = polygon[(i + 1) % len(polygon)]
            if (first_vertex, second_vertex) in segments or (second_vertex, first_vertex) in segments:
                continue
            segments.add((first_vertex, second_vertex))
    return segments


def main():
    width, height = 640, 640
    points = [(100, 100), (300, 150), (400, 300), (600, 400), (500, 450), (300, 420), (150, 350), (400, 350)]

    app = App((width, height))

    result = break_into_convex_polygons([FlatVector.from_tup(point) for point in points])

    triangles = []
    for i in [[vector.tup() for vector in polygon] for polygon in result]:
        triangles += [triangle for triangle in triangulate_convex_polygon(i)]

    for segment in polygons_to_segments(triangles):
        app.draw_line(segment[0], segment[1])

    app.draw_polygon(points, color=(255, 0, 0))

    app.update_image()
    app.save('img.png')
    app.mainloop()


if __name__ == '__main__':
    main()
