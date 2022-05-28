from PIL import Image
import numpy as np


class Shape:
    def __init__(self, path, width, height):
        # Size of the whole image
        self.width = width
        self.height = height
        self.path = path
        self.area = np.full(width * height, False)
        self.fill_shape()
        self.cached_area = 0
        self.cache_valid = False

    def fill_shape(self):
        # Add border to final shape
        for pos in self.path:
            self.area[pos[0] + pos[1] * self.width] = True

        # Expand border inside the shape into the BFS open set
        queue = set()
        for i in range(len(self.path)):
            p0 = self.path[i]
            if self.path.count(p0) > 1:
                continue  # This would expand outside the shape (fix spikes and 1 pixel wide lines)
            p1 = self.path[(i + 1) % len(self.path)]
            dx = p1[0] - p0[0]
            dy = p1[1] - p0[1]
            inside = (p0[0] + dy, p0[1] - dx)
            queue.add(inside)

        # BFS fill in shape (slow!)
        while len(queue):
            pos = queue.pop()
            if self.area[pos[0] + pos[1] * self.width]:
                continue
            self.area[pos[0] + pos[1] * self.width] = True
            if pos[0] > 0 and not self.area[(pos[0] - 1) + pos[1] * self.width]:
                queue.add((pos[0] - 1, pos[1]))
            if pos[0] < (self.width - 1) and not self.area[(pos[0] + 1) + pos[1] * self.width]:
                queue.add((pos[0] + 1, pos[1]))
            if pos[1] > 0 and not self.area[pos[0] + (pos[1] - 1) * self.width]:
                queue.add((pos[0], pos[1] - 1))
            if pos[1] < (self.height - 1) and not self.area[pos[0] + (pos[1] + 1) * self.width]:
                queue.add((pos[0], pos[1] + 1))

    def save_area_as_image(self, filepath):
        data = self.area.astype(int).reshape((self.height, self.width)) * 255
        img = Image.fromarray(np.uint8(data))
        img.save(filepath)

    def calculate_path_area(self):
        if self.cache_valid:
            return self.cached_area

        self.cached_area = 0
        self.cache_valid = True
        return self.cached_area

    def simplify_path(self, smooth_diagonals=True):
        pass

    def path_verts(self):
        return len(self.path)

    def decimate_path(self, max_verts):
        pass

    def save_path_as_image(self, filepath):
        pass
