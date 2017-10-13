def brad_alg(ra):
    # analyze every block of 10
    for i in range(10, len(ra), 10):
        # in every block of 10 analyze every single one
        for j in range(i-10, i+1, 1):
            # if j is equal to the upper bound
            if j == i:
                # if upper bound in RA is greater then run alg
                if ra[j] > ra[j-i]:
                    # middle bound between upper and lower bound
                    ra[j-5] = ((ra[j] - ra[j-i]) / 2) + ra[j-i]
                    # now define values before halfway point
                    ra[j-8] = ((ra[j-5] - ra[j-i]) / 2) + ra[j-i]
                    ra[j-9] = ((ra[j-8] - ra[j-i]) / 2) + ra[j-i]
                    ra[j-7] = ((ra[j-5] - ra[j-8]) / 2) + ra[j-8]
                    ra[j-6] = ((ra[j-5] - ra[j-7]) / 2) + ra[j-7]

                    # now define values after halfway point
    return ra
                # else if lower bound is greater then alternate
                #elif ra[j] < ra[j-i]:
                    # execute alt alg
