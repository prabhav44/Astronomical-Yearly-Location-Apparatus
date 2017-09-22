#So we have successful extraction of ephemeris data from JPL
import callhorizons
import numpy as np
import datetime

IoMoon = callhorizons.query(501, smallbody=False)

IoMoon.set_discreteepochs([2458010])

IoMoon.get_ephemerides('500@599')

print(IoMoon['RA'], IoMoon['DEC'])
