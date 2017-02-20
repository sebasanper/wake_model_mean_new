from order_layout import order
from thrust_coefficient import thrust_coefficient
from downstream_effects import JensenEffects as Jensen
from wake_overlap import wake_overlap


class Wake1Angle:
    def __init__(self, model):
        print "Model parameter must be Jensen, Larsen, Ainslie1D or Ainslie2D without quotation marks.\n"
        self.WakeModel = model

    def wake_one_angle(self, original_layout, freestream_wind_speed, wind_angle):
        ordered_layout = order(original_layout, wind_angle)
        ct = []
        wind_speeds_array = [freestream_wind_speed]
        deficit_matrix = [[] for _ in range(len(ordered_layout))]
        total_deficit = [0.0]
        for i in range(len(ordered_layout)):
            if i == 0:
                pass
            else:
                total_deficit.append(wake_overlap([deficit_matrix[j][i] for j in range(i)]))
                wind_speeds_array.append(freestream_wind_speed * (1.0 - total_deficit[i]))
            ct.append(thrust_coefficient(wind_speeds_array[i]))
            # print ordered_layout[i][0], ct[i], [item[0] for item in ordered_layout[i + 1:]], wind_angle
            deficit_matrix[i] = [0.0 for _ in range(i + 1)]
            deficit_matrix[i] += self.WakeModel(ordered_layout[i][0], ct[i], [item[0] for item in ordered_layout[i + 1:]], wind_angle)
            # print
            # print deficit_matrix[i], i
        # print original_layout
        # print ordered_layout
        # print [item[1] for item in ordered_layout]
        # print wind_speeds_array
        wind_speeds_array_original = [x for (y, x) in sorted(zip([item[1] for item in ordered_layout], wind_speeds_array), key=lambda pair: pair[0])]

        return wind_speeds_array_original

if __name__ == '__main__':
    layout = [[0.0, 0.0], [560.0, 0.0], [1120., 0.0], [1680., 0.0], [2240., 0.0], [2800., 0.0], [3360., 0.0], [3920., 0.0], [4480., 0.0]]
    U_inf = 8.5
    angle = 180.0
    model1 = Wake1Angle(Jensen)
    print model1.wake_one_angle(layout, U_inf, angle)
