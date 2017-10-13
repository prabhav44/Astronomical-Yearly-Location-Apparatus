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

        @jit
        def ra_i(real_ra):
            ra = [None] * 525601
            j = 0
            for i in real_ra:
                ra[j] = i
                j += 10
            return ra

        ra =  ra_i(real_ra)

        def ra_inter(ra):
            while type(None) in ra:
                brad_alg(ra)
            return ra

