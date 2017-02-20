from math import sqrt


def wake_overlap(array_deficits):
    #  This is one model, root sum square of individual wind speed deficits.
    total_deficit = sqrt(sum([deficit ** 2.0 for deficit in array_deficits]))
    return total_deficit

if __name__ == '__main__':
    deficits = [3, 4]
    print wake_overlap(deficits)
