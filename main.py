from JD_backend import JDHorizonData
import sqlite3

GD_FIRST = '2017-05-24 01:00'
GD_LAST = '2018-05-24 01:00'

# only run if year later and they say yes they want to use new data
# I watch twilight every night - Jaden Smith
# How can mirrors be real if our eyes aren't real - Jaden Smith

def db_gen(GD_FIRST, GD_LAST):
    gd_list = JDHorizonData.db_gen_gd(GD_FIRST)
    ra, dec = JDHorizonData.db_gen_ra_dec(GD_FIRST, GD_LAST)
    y = JDHorizonData.y_alg(ra, dec)
    x = JDHorizonData.x_alg(ra, y,  dec)
    z = JDHorizonData.z_alg(dec)

    db_args = []
    for i in range(0, len(ra), 1):
        db_args.append([gd_list[i], ra[i], dec[i], x[i], y[i], z[i]])

    # in future have db location definable
    # also have db generation be an option, notify if past update period but do not auto generate
    conn = sqlite3.connect('orbit_data.db')
    c = conn.cursor()
    c.execute('''DROP TABLE IF EXISTS orbit''')
    c.execute('''CREATE TABLE orbit (gd TEXT, ra REAL, dec REAL, x REAL, y REAL, z REAL)''')
    c.executemany('''INSERT INTO orbit VALUES (?, ?, ?, ?, ?, ?)''', db_args)
    conn.commit()
    conn.close()
