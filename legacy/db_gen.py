from backend import backAlgs
from multiprocessing import Process
import sqlite3

GD_FIRST = '2017-05-24 01:00'
GD_LAST = '2018-05-24 01:00'

# only run if year later and they say yes they want to use new data

gd_list = backAlgs.db_gen_gd(GD_FIRST)


def db_gen_io():
    ra, dec = backAlgs.db_gen_ra_dec(501, GD_FIRST, GD_LAST)
    y = backAlgs.y_alg(.002819, ra, dec)
    x = backAlgs.x_alg(.002819, ra, y, dec)
    z = backAlgs.z_alg(.002819, dec)

    db_args = []
    for i in range(0, len(ra), 1):
        db_args.append([gd_list[i], ra[i], dec[i], x[i], y[i], z[i]])

    # in future have db location definable
    # also have db generation be an option, notify if past update period but do not auto generate
    conn = sqlite3.connect('orbit_data.db')
    c = conn.cursor()
    c.execute('''DROP TABLE IF EXISTS io_orbit''')
    c.execute('''CREATE TABLE io_orbit (gd TEXT, ra REAL, dec REAL, x REAL, y REAL, z REAL)''')
    c.executemany('''INSERT INTO io_orbit VALUES (?, ?, ?, ?, ?, ?)''', db_args)
    conn.commit()
    conn.close()


def db_gen_eur():
    ra, dec = backAlgs.db_gen_ra_dec(502, GD_FIRST, GD_LAST)
    y = backAlgs.y_alg(.004485, ra, dec)
    x = backAlgs.x_alg(.004485, ra, y, dec)
    z = backAlgs.z_alg(.004485, dec)

    db_args = []
    for i in range(0, len(ra), 1):
        db_args.append([gd_list[i], ra[i], dec[i], x[i], y[i], z[i]])

    conn = sqlite3.connect('orbit_data.db')
    c = conn.cursor()
    c.execute('''DROP TABLE IF EXISTS eur_orbit''')
    c.execute('''CREATE TABLE eur_orbit (gd TEXT, ra REAL, dec REAL, x REAL, y REAL, z REAL)''')
    c.executemany('''INSERT INTO eur_orbit VALUES (?, ?, ?, ?, ?, ?)''', db_args)
    conn.commit()
    conn.close()


def db_gen():
    import_p1 = Process(target=db_gen_io())
    import_p2 = Process(target=db_gen_eur())
    import_p1.start()
    import_p2.start()


if __name__ == '__main__':
    p1 = Process(target=db_gen_io())
    p1.start()
    p2 = Process(target=db_gen_eur())
    p2.start()
