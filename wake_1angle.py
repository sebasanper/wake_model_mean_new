from order_layout import order
from thrust_coefficient import thrust_coefficient
from downstream_effects import effects_downstream
from wake_overlap import wake_overlap


def wake_one_angle(original_layout, freestream_wind_speed, wind_angle):
    ordered_layout = order(original_layout, wind_angle)
    ct = []
    wind_speeds_array = [freestream_wind_speed]
    deficit_matrix = [[0.0] for _ in range(len(ordered_layout))]
    total_deficit = []
    for i in range(len(ordered_layout)):
        total_deficit.append(wake_overlap(deficit_matrix[i]))
        wind_speeds_array.append(freestream_wind_speed * (1.0 - total_deficit[i]))
        ct.append(thrust_coefficient(wind_speeds_array[i]))
        deficit_matrix[i] = [0.0 for _ in range(i + 1)]
        for j in range(i + 1, len(ordered_layout)):
            deficit_matrix[i].append(effects_downstream(ordered_layout[i][0], ct[i], [item[0] for item in ordered_layout]))

    return wind_speeds_array

if __name__ == '__main__':
    layout = [[4, 5], [6, 6], [0, 4]]
    U_inf = 8.5
    angle = 64.0
    print wake_one_angle(layout, U_inf, angle)
