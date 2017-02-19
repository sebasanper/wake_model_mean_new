def effects_downstream(coordinates_0, ct_0, coordinates_downstream):
    # coordinates downstream will be an array with coordinates and original index.
    coordinates_only = [coordinates_downstream[i][0] for i in range(len(coordinates_downstream))]
    deficits = [0.4, 0.38, 0.68, 0.94, 0.01]  # Array with size of number of downstream turbines
    return deficits

if __name__ == '__main__':
    x_upstream = 5.1
    y_upstream = 9.6
    ct_upstream = 0.64
    downstream_turbines = [[3, 4], [7, 2], [4, 8]]
    print effects_downstream([x_upstream, y_upstream], ct_upstream, downstream_turbines)
