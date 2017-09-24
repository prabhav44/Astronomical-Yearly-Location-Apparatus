import callhorizons


# define horizons function that outputs Ephem data for specified planet and target body
# pass orbiting body, julian day, and target body ID and get RA, DEC at specified instance

def horizon(orbit_body, julian_day, target_body_string):
    data = callhorizons.query(orbit_body, smallbody=False)
    data.set_discreteepochs([julian_day])
    data.get_ephemerides(target_body_string)
    return float(data['RA']), float(data['DEC'])

    # create loop that feeds in 48 hours of Julian days to get Ephem data at each instance
    # store ephem data into list or SQLite DB
    # split 48 hours into intervals dependent on PC speed (future)
