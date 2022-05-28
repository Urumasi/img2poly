from PIL import Image
import numpy as np

from .shape import Shape


def read_data(data, w, x, y):
    h = len(data) // w
    if x < 0 or x >= w or y < 0 or y >= h:
        return False
    return data[x + y * w]


def rotate_right(direction):
    return -direction[1], direction[0]


def rotate_left(direction):
    return direction[1], -direction[0]


def trace(data, w, idx):
    x = idx % w
    y = idx // w
    point_list = [(x, y)]
    forward = (0, 1)  # Down
    while len(point_list) <= 1 or (x, y) != point_list[0]:
        right = rotate_right(forward)
        if read_data(data, w, x + right[0], y + right[1]):
            forward = right
            x += forward[0]
            y += forward[1]
            point_list.append((x, y))
            continue
        if read_data(data, w, x + forward[0], y + forward[1]):
            x += forward[0]
            y += forward[1]
            point_list.append((x, y))
            continue
        left = rotate_left(forward)
        if read_data(data, w, x + left[0], y + left[1]):
            forward = left
            x += forward[0]
            y += forward[1]
            point_list.append((x, y))
            continue
        back = rotate_left(left)
        if read_data(data, w, x + back[0], y + back[1]):
            forward = left
            point_list.append((x, y))
            continue
        break
    return point_list


def trace_image(image: Image, threshold=128):
    (width, height) = image.size
    image_threshold = image.convert('L').point(lambda val: 255 if val > threshold else 0, mode='1')
    # image_threshold.save('threshold.png')
    initial_data = ~np.array(image_threshold.getdata()).astype(bool)

    shapes = list()

    data_layer = initial_data
    while True:
        found_shape = False
        shapes.append(list())
        data = data_layer
        while True:
            found = False
            hits = np.where(data == True)[0]
            if len(hits):
                path = trace(data, width, hits[0])
                shape = Shape(path, width, height)
                shapes[-1].append(shape)
                data = data & ~shape.area
                found = True
            if not found:
                break
            found_shape = True
        if not found_shape:
            break
        for shape in shapes[-1]:
            data_layer = data_layer ^ shape.area


    image_paths = image_threshold.convert('RGB')
    for i, layer in enumerate(shapes):
        for j, shape in enumerate(layer):
            shape.save_as_image(f'shape{i}_{j}.png')
            for pixel in shape.path:
                image_paths.putpixel(pixel, (255, 0, 0))
    image_paths.save('paths.png')


    return shapes[:-1]

