from order_layout import order
from thrust_coefficient import thrust_coefficient
from downstream_effects import JensenEffects as Jensen, LarsenEffects as Larsen, Ainslie1DEffects as Ainslie1D, Ainslie2DEffects as Ainslie2D
from wake_overlap import wake_overlap
from time import time

class Wake1Angle:
    def __init__(self, model):
        # print "Model parameter must be Jensen, Larsen, Ainslie1D or Ainslie2D without quotation marks.\n"
        self.WakeModel = model

    def wake_one_angle(self, original_layout, freestream_wind_speed, wind_angle, ambient_turbulence):
        ordered_layout = order(original_layout, wind_angle)
        ct = []
        wind_speeds_array = [freestream_wind_speed]
        deficit_matrix = [[] for _ in range(len(ordered_layout))]
        total_deficit = [0.0]
        for i in range(len(ordered_layout)):
            # start = time()
            if i == 0:
                pass
            else:
                total_deficit.append(wake_overlap([deficit_matrix[j][i] for j in range(i)]))
                wind_speeds_array.append(freestream_wind_speed * (1.0 - total_deficit[i]))
            ct.append(thrust_coefficient(wind_speeds_array[i]))
            deficit_matrix[i] = [0.0 for _ in range(i + 1)]
            deficit_matrix[i] += self.WakeModel(ordered_layout[i][0], ct[i], [item[0] for item in ordered_layout[i + 1:]], wind_angle, freestream_wind_speed, ambient_turbulence)
            # print time() - start, wind_angle, i
        # print deficit_matrix
        wind_speeds_array_original = [x for (y, x) in sorted(zip([item[1] for item in ordered_layout], wind_speeds_array), key=lambda pair: pair[0])]
        return wind_speeds_array_original

if __name__ == '__main__':

    layout = [[500.0, 0.0], [1000.0, 0.0], [1500.0, 0.0], [2000.0, 0.0], [2500.0, 0.0], [3000.0, 0.0]]
    U_inf = 11.0
    angle = 180.0
    I0 = 0.08
    model1 = Wake1Angle(Jensen)
    model2 = Wake1Angle(Larsen)
    model3 = Wake1Angle(Ainslie1D)
    model4 = Wake1Angle(Ainslie2D)
    print model1.wake_one_angle(layout, U_inf, angle, I0)
    print model2.wake_one_angle(layout, U_inf, angle, I0)
    print model3.wake_one_angle(layout, U_inf, angle, I0)
    print model4.wake_one_angle(layout, U_inf, angle, I0)
