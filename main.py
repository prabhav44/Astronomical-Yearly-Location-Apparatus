import callhorizons
from datetime import datetime
from dateutil.relativedelta import relativedelta
from math import floor
from numba.decorators import generated_jit, jit


class JDHorizonData:
    @staticmethod
    @jit
    def jd_alg(year, month, day, hour, minute, second):
        ysincebc = year + 4800 - floor((14 - month) / 12)
        msincebc = month + 12 * floor((14 - month) / 12) - 3

        jdn = day + floor((153 * msincebc + 2) / 5) + (365 * ysincebc) + floor(ysincebc / 4) - floor(
            ysincebc / 100) + floor(ysincebc / 400) - 32045

        if 0 <= hour < 12:
            jdn += 1

        jdn = jdn + ((hour - 12) / 24) \
              + (minute / 1440) \
              + (second / 86400)

        return jdn

    @staticmethod
    def horizon_data(orbit_body, target_body, start_d, end_d, step):
        data = callhorizons.query(orbit_body, smallbody=False)
        data.set_epochrange(start_d, end_d, step)
        data.get_ephemerides(target_body)
        return data['RA'], data['DEC']

    gd_first = '2017-05-24 01:00'
    gd_last = '2018-05-24 01:00'

    @staticmethod
    def db_gen_gd(gd_first):
        # separating function for performance
        # cannot multicore datetime process
        def time_add(time, minute_counter):
            new_time = time + relativedelta(minutes=minute_counter)
            return new_time
        # done so easy to change starting date
        gd_list = []
        first = datetime.strptime(gd_first, '%Y-%m-%d %H:%M')
        # generating primary gd_list which is divied into 10 min increments to feed into horizons
        for i in range(0, 525601, 1):
            new = time_add(first, i)
            gd_list.append(str(new))
        return gd_list

    # this algorithm should only be as slow as data pull
    @staticmethod
    def db_gen_ra_dec(gd_first, gd_last):
        # actual not interpolated data use this to get alg for interpolating data, run this parallel with gd_gen
        real_ra, real_dec = JDHorizonData.horizon_data(501, '500@599', gd_first, gd_last, '10 m')

        # these will run sequentially together concurrently with dec interpolation
        @jit
        def ra_i(real_ra):
            ra = [None] * 525601
            j = 0
            for i in real_ra:
                ra[j] = i
                j += 10
            return ra

        ra = ra_i(real_ra)

        @jit
        def brad_alg(ra):
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

        ra = brad_alg(ra)

