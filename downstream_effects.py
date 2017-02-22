import jensen
import larsen
import ainslie1d
import ainslie2d
from ainslie_common import crosswind_distance, determine_front
from time import time
# class PartialDeficit:
#     def __init__(self, coordinates_upstream, thrust_coefficient, coordinates_downstream):
#         self.coordinates_0 = coordinates_upstream
#         self.ct_0 = thrust_coefficient
#         self.coordinates_downstream = coordinates_downstream
# 
#     def JensenEffects(self, angle):
#         angle3 = angle + 180.0
#         # coordinates downstream will be an array with coordinates and original index.
#         partial_deficits = []
# 
#         for i in range(len(self.coordinates_downstream)):
# 
#             determ = jensen.determine_if_in_wake(self.coordinates_0[0], self.coordinates_0[1], self.coordinates_downstream[i][0], self.coordinates_downstream[i][1], angle3)
# 
#             if determ[0] != 0.0:
#                 partial_deficits.append(determ[0] * jensen.wake_deficit(self.ct_0, determ[1]))
#             else:
#                 partial_deficits.append(0.0)
#         # deficits = [0.4, 0.38, 0.68, 0.94, 0.01]  # Array with size of number of downstream turbines
#         return partial_deficits


def JensenEffects(coordinates_upstream, thrust_coefficient, coordinates_downstream, angle, wind_speed_upstream, ambient_turbulence_intensity):
    angle3 = angle + 180.0
    # coordinates downstream will be an array with coordinates and original index.
    partial_deficits = []

    for i in range(len(coordinates_downstream)):
        determ = jensen.determine_if_in_wake(coordinates_upstream[0], coordinates_upstream[1],
                                             coordinates_downstream[i][0], coordinates_downstream[i][1],
                                             angle3)
        # print determ[1], "determ1"
        # print determ[0], "determ0"

        if determ[0] != 0.0:
            # print jensen.wake_deficit(thrust_coefficient, determ[1])
            partial_deficits.append(determ[0] * jensen.wake_deficit(thrust_coefficient, determ[1]))
        else:
            partial_deficits.append(0.0)

    return partial_deficits


def LarsenEffects(coordinates_upstream, thrust_coefficient, coordinates_downstream, angle, wind_speed_upstream, ambient_turbulence_intensity):
    angle3 = angle + 180.0
    partial_deficits = []

    for i in range(len(coordinates_downstream)):
        proportion, flag, perpendicular_distance, parallel_distance = larsen.determine_if_in_wake_larsen(coordinates_upstream[0], coordinates_upstream[1], coordinates_downstream[i][0], coordinates_downstream[i][1], thrust_coefficient, angle3, ambient_turbulence_intensity)
        if parallel_distance > 0.0:
            if proportion != 0.0:
                partial_deficits.append(proportion * larsen.wake_deficit(wind_speed_upstream, thrust_coefficient, parallel_distance + larsen.x0(thrust_coefficient, ambient_turbulence_intensity), perpendicular_distance, ambient_turbulence_intensity))
            else:
                partial_deficits.append(0.0)
        else:
            partial_deficits.append(0.0)

    return partial_deficits


def Ainslie1DEffects(coordinates_upstream, thrust_coefficient, coordinates_downstream, angle, wind_speed_upstream, ambient_turbulence_intensity):
    angle3 = angle + 180.0
    partial_deficits = []
    normalised_upstream = [coordinates_upstream[i] / 80.0 for i in range(2)]
    normalised_downstream = [[coordinates_downstream[j][i] / 80.0 for i in range(2)] for j in range(len(coordinates_downstream))]

    for i in range(len(normalised_downstream)):

        parallel_distance = determine_front(angle3, normalised_upstream[0], normalised_upstream[1], normalised_downstream[i][0], normalised_downstream[i][1])
        perpendicular_distance = crosswind_distance(angle3, normalised_upstream[0], normalised_upstream[1], normalised_downstream[i][0], normalised_downstream[i][1])
        if perpendicular_distance <= 1.7 and parallel_distance > 0.0:  # 1.7 gives same results as a bigger distance, many times faster.
            partial_deficits.append(ainslie1d.ainslie(thrust_coefficient, wind_speed_upstream, parallel_distance, perpendicular_distance, ambient_turbulence_intensity))
        else:
            partial_deficits.append(0.0)

    return partial_deficits

# from time import time
def Ainslie2DEffects(coordinates_upstream, thrust_coefficient, coordinates_downstream, angle, wind_speed_upstream, ambient_turbulence_intensity):
    angle3 = angle + 180.0
    partial_deficits = []
    normalised_upstream = [coordinates_upstream[i] / 80.0 for i in range(2)]
    normalised_downstream = [[coordinates_downstream[j][i] / 80.0 for i in range(2)] for j in range(len(coordinates_downstream))]
    # start = time()
    for i in range(len(normalised_downstream)):
        parallel_distance = determine_front(angle3, normalised_upstream[0], normalised_upstream[1], normalised_downstream[i][0], normalised_downstream[i][1])
        perpendicular_distance = crosswind_distance(angle3, normalised_upstream[0], normalised_upstream[1], normalised_downstream[i][0], normalised_downstream[i][1])
        if perpendicular_distance <= 2.0 and parallel_distance > 0.0:
            partial_deficits.append(ainslie2d.ainslie_full(thrust_coefficient, wind_speed_upstream, parallel_distance, perpendicular_distance, ambient_turbulence_intensity))
        else:
            partial_deficits.append(0.0)

    return partial_deficits


if __name__ == '__main__':
    upstream = [423974.0, 6151447.0]
    ct_upstream = 0.79
    downstream_turbines = [[423974.0, 6151447.0], [424033.0, 6150889.0], [424092.0, 6150332.0], [424151.0, 6149774.0], [424210.0, 6149216.0], [424268.0, 6148658.0], [424327.0, 6148101.0], [424386.0, 6147543.0], [424534.0, 6151447.0], [424593.0, 6150889.0], [424652.0, 6150332.0], [424711.0, 6149774.0], [424770.0, 6149216.0], [424829.0, 6148658.0], [424888.0, 6148101.0], [424947.0, 6147543.0], [425094.0, 6151447.0], [425153.0, 6150889.0], [425212.0, 6150332.0], [425271.0, 6149774.0], [425330.0, 6149216.0], [425389.0, 6148658.0], [425448.0, 6148101.0], [425507.0, 6147543.0], [425654.0, 6151447.0], [425713.0, 6150889.0], [425772.0, 6150332.0], [425831.0, 6149774.0], [425890.0, 6149216.0], [425950.0, 6148659.0], [426009.0, 6148101.0], [426068.0, 6147543.0], [426214.0, 6151447.0], [426273.0, 6150889.0], [426332.0, 6150332.0], [426392.0, 6149774.0], [426451.0, 6149216.0], [426510.0, 6148659.0], [426569.0, 6148101.0], [426628.0, 6147543.0], [426774.0, 6151447.0], [426833.0, 6150889.0], [426892.0, 6150332.0], [426952.0, 6149774.0], [427011.0, 6149216.0], [427070.0, 6148659.0], [427129.0, 6148101.0], [427189.0, 6147543.0], [427334.0, 6151447.0], [427393.0, 6150889.0], [427453.0, 6150332.0], [427512.0, 6149774.0], [427571.0, 6149216.0], [427631.0, 6148659.0], [427690.0, 6148101.0], [427749.0, 6147543.0], [427894.0, 6151447.0], [427953.0, 6150889.0], [428013.0, 6150332.0], [428072.0, 6149774.0], [428132.0, 6149216.0], [428191.0, 6148659.0], [428250.0, 6148101.0], [428310.0, 6147543.0], [428454.0, 6151447.0], [428513.0, 6150889.0], [428573.0, 6150332.0], [428632.0, 6149774.0], [428692.0, 6149216.0], [428751.0, 6148659.0], [428811.0, 6148101.0], [428870.0, 6147543.0], [429014.0, 6151447.0], [429074.0, 6150889.0], [429133.0, 6150332.0], [429193.0, 6149774.0], [429252.0, 6149216.0], [429312.0, 6148659.0], [429371.0, 6148101.0], [429431.0, 6147543.0]]
    # lay1 = PartialDeficit(upstream, ct_upstream, downstream_turbines)
    # print JensenEffects(upstream, ct_upstream, downstream_turbines, 180.0, 8.5, 0.08)
    # #
    # print LarsenEffects(upstream, ct_upstream, downstream_turbines, 180.0, 8.5, 0.08)
    #
    # print Ainslie1DEffects(upstream, ct_upstream, downstream_turbines, 180.0, 8.5, 0.08)
    #
    print Ainslie2DEffects(upstream, ct_upstream, downstream_turbines, 210.0, 8.5, 0.08)

