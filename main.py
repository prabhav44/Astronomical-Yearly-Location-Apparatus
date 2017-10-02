import callhorizons


# define horizons function that outputs Ephem data for specified planet and target body
# pass orbiting body, julian day, and target body ID and get RA, DEC at specified instance

def horizon(orbit_body, julian_day, target_body_string):
    data = callhorizons.query(orbit_body, smallbody=False)
    data.set_discreteepochs([julian_day])
    data.get_ephemerides(target_body_string)
    return float(data['RA']), float(data['DEC'])

    # create loop that feeds in 48 hours of import callhorizons
from ctypes import *
import datetime


class JDHorizon:
    @staticmethod
    # configure so if values not given it uses current time - josh this is you
    def jd_alg(year, month, day, hour, minute, second):
        # make sure dll file is in same directory as main.py
        jd_alg_c = cdll.LoadLibrary('JDalg_final.dll')
        # loading dll file above
        # setting argtypes for C function
        jd_alg_c.JulianDay.argtypes = [c_int, c_int, c_int, c_int]
        # defining c function result as a python variable
        julian_day = jd_alg_c.JulianDay(year, month, day, hour)
        # adding hour minute second interval decimal places
        julian_day_n = julian_day + ((hour - 12) / 24) \
                       + (minute / 1440) \
                       + (second / 86400)
        return julian_day_n

    # leave alone temporarily, may configure as one time function on main class, kinda like WinUpdate
    @staticmethod
    def horizon_data(orbit_body, julian_day_n, target_body_string):
        data = callhorizons.query(orbit_body, smallbody=False)
        data.set_discreteepochs([julian_day_n])
        data.get_ephemerides(target_body_string)
        return float(data['RA']), float(data['DEC'])
Julian days to get Ephem data at each instance
    # store ephem data into list or SQLite DB
    # split 48 hours into intervals dependent on PC speed (future)
