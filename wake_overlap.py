from math import sqrt


def wake_overlap(array_deficits):
    #  This is one model, root sum square of individual wind speed deficits.
    total_deficit = sqrt(sum([deficit ** 2.0 for deficit in range(len(array_deficits))]))
    return total_deficit

if __name__ == '__main__':
    deficits = [0.3, 0.4, 0.5, 0.6]
    print wake_overlap(deficits)
