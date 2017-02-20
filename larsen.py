from numpy import pi, sqrt, deg2rad, tan, cos, sin
import area
r0 = 40.0
D = 2.0 * r0
area = pi * r0 ** 2.0
H = 100.0  # Hub height
ia = 0.08  # Ambient turbulence intensity according to vanluvanee. 8% on average


def wake_radius(c1, ct, A, x):
    return ((35.0 / 2.0 / pi) ** (1.0 / 5.0)) * ((3.0 * c1 ** 2.0) ** (1.0 / 5.0)) * ((ct * A * x) ** (1.0 / 3.0))


def deff(u1, Ct):
    return D * sqrt((1.0 + sqrt(1.0 - Ct(u1))) / (2.0 * sqrt(1.0 - Ct(u1))))

rnb = max(1.08 * D, 1.08 * D + 21.7 * D * (ia - 0.05))
r95 = 0.5 * (rnb + min(H, rnb))


def x0(u2):
    return 9.5 * D / ((2.0 * r95 / deff(u2)) ** 3.0 - 1.0)


def c1(u3):
    return (deff(u3) / 2.0) ** (5.0 / 2.0) * (105.0 / 2.0 / pi) ** (- 1.0 / 2.0) * (Ct(u3) * A * x0(u3)) ** (
        - 5.0 / 6.0)  # Prandtl mixing length


def determine_if_in_wake_larsen(xt, yt, xw, yw, ct, alpha, r0, x0, A=area, c11=c1()):  # According to Larsen Model only
    # Eq. of centreline is Y = tan (d) (X - Xt) + Yt
    # Distance from point to line
    alpha = deg2rad(alpha + 180)
    distance_to_centre = abs(- tan(alpha) * xw + yw + tan(alpha) * xt - yt) / sqrt(1.0 + tan(alpha) ** 2.0)
    # print distance_to_centre
    # Coordinates of the intersection between closest path from turbine in wake to centreline.
    X_int = (xw + tan(alpha) * yw + tan(alpha) * (tan(alpha) * xt - yt)) / (tan(alpha) ** 2.0 + 1.0)
    Y_int = (- tan(alpha) * (- xw - tan(alpha) * yw) - tan(alpha) * xt + yt) / (tan(alpha) ** 2.0 + 1.0)
    # Distance from intersection point to turbine
    distance_to_turbine = sqrt((X_int - xt) ** 2.0+(Y_int - yt) ** 2.0)
    # Radius of wake at that distance
    radius = wake_radius(c1, ct, A, distance_to_turbine + x0)
    # print radius
    if (xw - xt) * cos(alpha) + (yw - yt) * sin(alpha) <= 0.0:
        if abs(radius) >= abs(distance_to_centre):
            if abs(radius) >= abs(distance_to_centre) + r0:
                fraction = 1.0
                value = True
                return fraction, value, distance_to_centre, distance_to_turbine
            elif abs(radius) < abs(distance_to_centre) + r0:
                fraction = area.AreaReal(r0, radius, distance_to_centre).area()
                value = True
                return fraction, value, distance_to_centre, distance_to_turbine
        elif abs(radius) < abs(distance_to_centre):
            if abs(radius) <= abs(distance_to_centre) - r0:
                fraction = 0.0
                value = False
                return fraction, value, distance_to_centre, distance_to_turbine
            elif abs(radius) > abs(distance_to_centre) - r0:
                fraction = area.AreaReal(r0, radius, distance_to_centre).area()
                value = True
                return fraction, value, distance_to_centre, distance_to_turbine
    else:
        return 0.0, False, distance_to_centre, distance_to_turbine
