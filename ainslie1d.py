from numpy import exp
from ainslie_common import b, E
D = 80.0


def ainslie(ct, u0, distance_parallel, distance_perpendicular, I0):
    # centreline = open('centreline.dat', 'w')
    # velocity = open('velocity.dat', 'w')
    h = 0.01
    L = distance_parallel
    n = int(L / h) + 1
    Uc1 = [0.0 for _ in range(n)]
    d1 = [0.0 for _ in range(n)]
    Ct = ct  # Thrust coefficient
    U0 = u0
    # dr = 0.1
    Y = distance_perpendicular
    # m = int(Y / dr)

    Dmi = Ct - 0.05 - (16.0 * Ct - 0.5) * I0 / 10.0

    Uc1[0] = U0 * (1.0 - Dmi)  # Boundary condition at x = 2.0
    d1[0] = Dmi
    for i in range(1, n):  # For all positions in the wake centreline direction. Recursive. Whole grid
        Uc1[i] = Uc1[i - 1] + (h * 16.0 * E(i * h, Uc1[i - 1], d1[i - 1], U0, I0, Ct) * (Uc1[i - 1] ** 3.0 - U0 * Uc1[i - 1] ** 2.0 - Uc1[i - 1] * U0 ** 2.0 + U0 ** 3.0) / (Uc1[i - 1] * Ct * U0 ** 2.0))
        d1[i] = 1.0 - Uc1[i] / U0
    # Code to calculate wake deficit at a specific point instead of the whole grid. Namely, the rotor's centrepoint.
    answer = d1[-1] * exp(- 3.56 * (Y / b(d1[-1], ct)) ** 2.0) * (1.0 + 7.12 * (0.07 * distance_parallel / b(d1[-1], ct))) ** (- 0.5)
    return answer

    # Code to calculate average wake deficit in all area of the rotor ###############

    # Define function to integrate.

    # p. 77 Adapting and calibration of existing wake models to meet the conditions inside offshore wind farms. For integrand squared momentum deficit.
    # def G(r, theta):
    #     z = sqrt(Y ** 2.0 + r ** 2.0 + 2.0 * Y * r * cos(theta))
    #     gauss = U0 * (1.0 - d1[n - 1] * exp(- 3.56 * (z / b(d1[n - 1])) ** 2.0))
    #     return r * (U0 - gauss) ** 2.0
    #
    # A = pi * 0.5 ** 2.0  ## Unitary diameter in this program.
    # U = U0 - sqrt((1.0 / A) * simpson_integrate2D(G, 0.0, 0.5, 5, 0.0, 2.0 * pi, 10))

    # return 1.0 - U / U0

if __name__ == '__main__':
    print ainslie(0.79, 8.5, 7.0, 0.0, 0.08)