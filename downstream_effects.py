import jensen
from larsen import c1, x0, determine_if_in_wake_larsen
import larsen

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


def JensenEffects(coordinates_upstream, thrust_coefficient, coordinates_downstream, angle):
    angle3 = angle + 180.0
    # coordinates downstream will be an array with coordinates and original index.
    partial_deficits = []

    for i in range(len(coordinates_downstream)):
        determ = jensen.determine_if_in_wake(coordinates_upstream[0], coordinates_upstream[1],
                                             coordinates_downstream[i][0], coordinates_downstream[i][1],
                                             angle3)

        if determ[0] != 0.0:
            partial_deficits.append(determ[0] * jensen.wake_deficit(thrust_coefficient, determ[1]))
        else:
            partial_deficits.append(0.0)
    # deficits = [0.4, 0.38, 0.68, 0.94, 0.01]  # Array with size of number of downstream turbines


def LarsenEffects(coordinates_upstream, thrust_coefficient, coordinates_downstream, angle):
    angle3 = angle + 180.0
    partial_deficits = []

    for i in range(len(coordinates_downstream)):
        proportion, flag, perpendicular_distance, parallel_distance = larsen.determine_if_in_wake_larsen(
            coordinates_upstream[0],
            coordinates_upstream[1],
            coordinates_downstream[i][0],
            coordinates_downstream[i][1],
            c1(U[distance[turbine][1]]),
            Ct(U[distance[turbine][1]]), angle3,
            r0, x0(U[distance[turbine][1]]))
        if parallel_distance[distance[i][1]] > 0.0:
            if proportion[distance[i][1]] != 0.0:
                deficit_matrix[distance[i][1]][distance[turbine][1]] = proportion[
                                                                           distance[i][
                                                                               1]] * larsen.wake_deficit(
                    U[distance[turbine][1]], Ct(U[distance[turbine][1]]), A,
                    parallel_distance[distance[i][1]] + x0(U[distance[turbine][1]]),
                    perpendicular_distance[distance[i][1]], c1(U[distance[turbine][1]]))
            else:
                deficit_matrix[distance[i][1]][distance[turbine][1]] = 0.0
        else:
            deficit_matrix[distance[i][1]][distance[turbine][1]] = 0.0

    return partial_deficits


if __name__ == '__main__':
    upstream = [0.0, 0.0]
    ct_upstream = 0.79
    downstream_turbines = [[560.0, 0.0], [1120., 0.0]]#, [1680., 0.0], [2240., 0.0], [2800., 0.0], [3360., 0.0], [3920., 0.0], [4480., 0.0]]
    # lay1 = PartialDeficit(upstream, ct_upstream, downstream_turbines)
    print JensenEffects(upstream, ct_upstream, downstream_turbines, 180.0)
