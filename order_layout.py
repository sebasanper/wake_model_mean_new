from numpy import radians, tan, cos, sqrt


def distance_to_front(x, y, theta):
    theta = radians(theta)
    return abs(x + tan(theta) * y - 10000000000.0 / cos(theta)) / sqrt(1.0 + tan(theta) ** 2.0)


def order(layout_array, wind_direction):
    distances = []
    i = 0
    for turbine in layout_array:
        distances.append([distance_to_front(turbine[0], turbine[1], wind_direction), i])
        i += 1
    distances.sort()
    ordered_indices = [item[1] for item in distances]
    ordered_layout = [[layout_array[i], i] for i in ordered_indices]

    return ordered_layout

if __name__ == '__main__':
    layout = [[5, 0], [3, 0], [7, 1], [2.5, 0]]
    angle = 90.0
    print order(layout, angle)
