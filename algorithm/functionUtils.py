import math

a_coeff, b_coeff, c_coeff = 20, 0.2, 2 * math.pi


def ackleyFunction(x):
    N = len(x)
    sum1 = 0
    sum2 = 0

    for i in range(N):
        sum1 += x[i] ** 2
        sum2 += math.cos(x[i] * c_coeff)

    term1 = -a_coeff * math.exp(-b_coeff * math.sqrt(1 / N * sum1))
    term2 = -math.exp(1 / N * sum2)

    result = term1 + term2 + a_coeff + math.e

    return result
