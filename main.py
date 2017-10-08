import callhorizons
from ctypes import *
from datetime import *
from dateutil.relativedelta import relativedelta


class JDHorizonData:
    @staticmethod
    def jd_alg(year, month, day, hour, minute, second):
        # make sure dll file is in same directory as main.py

        jd_alg_c = cdll.LoadLibrary('JDalg_final.dll')
        # loading dll file above
        # setting argtypes for C function
        jd_alg_c.JulianDay.argtypes = [c_int, c_int, c_int, c_int]
        # defining c function result as a python variable
        julian_day = jd_alg_c.JulianDay(year, month, day, hour)
        # adding hour minute second interval decimal places because of C floating point errors
        julian_day_n = julian_day + ((hour - 12) / 24) \
                                  + (minute / 1440) \
                                  + (second / 86400)
        return julian_day_n

    @staticmethod
    def horizon_data(orbit_body, target_body, start_d, end_d, step):
        data = callhorizons.query(orbit_body, smallbody=False)
        data.set_epochrange(start_d, end_d, step)
        data.get_ephemerides(target_body)
        return data['RA'], data['DEC']

    # run when may 24th + defined year is true, defined year changes everytime it's run
    @staticmethod
    def db_gen():
        # global first bound variable in UTC, in future have year updated when it downloads new .db file at this date
        # year later
        gd_first = '2017-05-24 03:00'
        gd_list = [datetime.strptime(gd_first, '%Y-%m-%d %H:%M')]

        # adding a years worth of minutes to time variable then converting to str so we can feed to callhorizons
        for i in range(1, 525602, 1):
            gd_list.append(str(datetime.strptime(gd_first, '%Y-%m-%d %H:%M') + relativedelta(minutes=i)))

        # since first variable is untouched when adding timedelta to time variables and converting them to strings
        gd_list[0] = str(gd_list[0])

        # master list is gd_list which will be fed into sqlite insert command

        # chunks of data to feed horizons since it only supports 90024 lines a time
        gd_hz_chnk1 = gd_list[0:87600]
        gd_hz_chnk2 = gd_list[87600:175200]
        gd_hz_chnk3 = gd_list[175200:262800]
        gd_hz_chnk4 = gd_list[262800:350400]
        gd_hz_chnk5 = gd_list[350400:438000]
        gd_hz_chnk6 = gd_list[438000:-1]

        # this class and function however is essentially the core of our backend which can be housed on a central server
        # see how this will be time intensive though? because it relies on network speed not processor
        # in progress implement radians call to JPL, function finished just need to integrate within master
        
        # below lines are temporary ugly lines of code, will optimize 10/9/2017, need to concatenate all RA, DEC data
        # into single list to be fed into DB
        # don't judge fuckers
        RA_chnk1, DEC_chnk1 = JDHorizonData.horizon_data(501, '500@599', gd_hz_chnk1[0], gd_hz_chnk1[-1], '1m')
        RA_chnk2, DEC_chnk2 = JDHorizonData.horizon_data(501, '500@599', gd_hz_chnk2[0], gd_hz_chnk2[-1], '1m')
        RA_chnk3, DEC_chnk3 = JDHorizonData.horizon_data(501, '500@599', gd_hz_chnk3[0], gd_hz_chnk3[-1], '1m')
        RA_chnk4, DEC_chnk4 = JDHorizonData.horizon_data(501, '500@599', gd_hz_chnk4[0], gd_hz_chnk4[-1], '1m')
        RA_chnk5, DEC_chnk5 = JDHorizonData.horizon_data(501, '500@599', gd_hz_chnk5[0], gd_hz_chnk5[-1], '1m')
        RA_chnk6, DEC_chnk6 = JDHorizonData.horizon_data(501, '500@599', gd_hz_chnk6[0], gd_hz_chnk6[-1], '1m')
