def order(layout_array, wind_direction):
    ordered_layout = [[[1, 2], 2], [[4, 7], 0], [[3, 7], 1]] # return list of coordinates and original index of turbines, but ordered with respect to incoming wind.
    return ordered_layout

if __name__ == '__main__':
    layout = [[4, 6], [3, 8], [7, 4]]
    angle = 54
    print order(layout, angle)
