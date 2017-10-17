# gotta say, goddamn I'm good - Prabhav

from numba.decorators import jit


@jit
def ra_inter_alg(ra):
    # analyze every block of 10
    for i in range(10, len(ra), 10):
        # in every block of 10 analyze every single one
        for j in range(i - 10, i + 1, 1):
            if j == i:
                if ra[j] >= ra[j - 10]:
                    ra[j - 5] = ((ra[j] - ra[j - 10]) / 2) + ra[j - 10]
                    # now define values before halfway point
                    ra[j - 8] = ((ra[j - 5] - ra[j - 10]) / 2) + ra[j - 10]
                    ra[j - 9] = ((ra[j - 8] - ra[j - 10]) / 2) + ra[j - 10]
                    ra[j - 7] = ((ra[j - 5] - ra[j - 8]) / 2) + ra[j - 8]
                    ra[j - 6] = ((ra[j - 5] - ra[j - 7]) / 2) + ra[j - 7]

                    # now define values after halfway point
                    ra[j - 3] = ((ra[j] - ra[j - 5]) / 2) + ra[j - 5]
                    ra[j - 4] = ((ra[j - 3] - ra[j - 5]) / 2) + ra[j - 5]
                    ra[j - 2] = ((ra[j] - ra[j - 3]) / 2) + ra[j - 3]
                    ra[j - 1] = ((ra[j] - ra[j - 2]) / 2) + ra[j - 2]

                elif ra[j] <= ra[j - 10]:
                    # in future going to have to split these intervals into smaller sub ones to account for even numbers
                    # defining before halfway point
                    ra[j - 5] = ((360 - ra[j - 10]) / 2) + ra[j - 10]
                    ra[j - 8] = ((ra[j - 5] - ra[j - 10]) / 2) + ra[j - 10]
                    ra[j - 9] = ((ra[j - 8] - ra[j - 10]) / 2) + ra[j - 10]
                    ra[j - 7] = ((ra[j - 5] - ra[j - 8]) / 2) + ra[j - 8]
                    ra[j - 6] = ((ra[j - 5] - ra[j - 7]) / 2) + ra[j - 7]

                    # now for after halfway point
                    ra[j - 4] = (ra[j] / 2)
                    ra[j - 2] = ((ra[j] - ra[j - 4]) / 2) + ra[j - 4]
                    ra[j - 3] = ((ra[j - 2] - ra[j - 4]) / 2) + ra[j - 4]
                    ra[j - 1] = ((ra[j] - ra[j - 2]) / 2) + ra[j - 2]
    return ra

@jit
def dec_inter_alg(dec):
    # analyze every block of 10
    for i in range(10, len(dec), 10):
        # in every block of 10 analyze every single one
        for j in range(i - 10, i + 1, 1):
            if j == i:
                if dec[j] and dec[j - 10] >= 0:
                    dec[j - 5] = ((dec[j] - dec[j - 10]) / 2) + dec[j - 10]
                    dec[j - 8] = ((dec[j - 5] - dec[j - 10]) / 2) + dec[j - 10]
                    dec[j - 9] = ((dec[j - 8] - dec[j - 10]) / 2) + dec[j - 10]
                    dec[j - 7] = ((dec[j - 5] - dec[j - 8]) / 2) + dec[j - 8]
                    dec[j - 6] = ((dec[j - 5] - dec[j - 7]) / 2) + dec[j - 7]

                    # now define values after halfway point
                    dec[j - 3] = ((dec[j] - dec[j - 5]) / 2) + dec[j - 5]
                    dec[j - 4] = ((dec[j - 3] - dec[j - 5]) / 2) + dec[j - 5]
                    dec[j - 2] = ((dec[j] - dec[j - 3]) / 2) + dec[j - 3]
                    dec[j - 1] = ((dec[j] - dec[j - 2]) / 2) + dec[j - 2]

                if dec[j] and dec[j - 10] < 0:
                    dec[j - 5] = -((fabs(dec[j]) - fabs(dec[j - 10])) / 2) + dec[j - 10]
                    dec[j - 8] = -((fabs(dec[j - 5]) - fabs(dec[j - 10])) / 2) + dec[j - 10]
                    dec[j - 9] = -((fabs(dec[j - 8]) - fabs(dec[j - 10])) / 2) + dec[j - 10]
                    dec[j - 7] = -((fabs(dec[j - 5]) - fabs(dec[j - 8])) / 2) + dec[j - 8]
                    dec[j - 6] = -((fabs(dec[j - 5]) - fabs(dec[j - 7])) / 2) + dec[j - 7]

                    # now define values after halfway point
                    dec[j - 3] = -((fabs(dec[j]) - fabs(dec[j - 5])) / 2) + dec[j - 5]
                    dec[j - 4] = -((fabs(dec[j - 3]) - fabs(dec[j - 5])) / 2) + dec[j - 5]
                    dec[j - 2] = -((fabs(dec[j]) - fabs(dec[j - 3])) / 2) + dec[j - 3]
                    dec[j - 1] = -((fabs(dec[j]) - fabs(dec[j - 2])) / 2) + dec[j - 2]
    return dec
