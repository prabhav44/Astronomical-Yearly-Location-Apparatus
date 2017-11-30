# Codename: Astronomical-Yearly-Location-Apparatus
# TechDebt:
# TODO: Check for database update
# TODO: Enter date func
# TODO: Lower memory usage by setting max amounts of graphs open in background, no idea how to do this yet
# Urgent:
# TODO: define in sine graph window if pickle file is 0 then show warning

from tkinter.ttk import Frame, Button, Style
from tkinter import *
import sqlite3
import matplotlib as plt
from mpl_toolkits.mplot3d import Axes3D

plt.use("TkAgg")
import matplotlib.pyplot as pltw
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import pickle
import datetime
from backend import backAlgs

# connect to DB and get all our data
conn = sqlite3.connect('orbit_data.db')
c = conn.cursor()

# select x values and save to x list
c.execute('''SELECT x FROM io_orbit''')
X_io = c.fetchall()
# remove tuples from list
X_io = [i[0] for i in X_io]

# same thing as above
c.execute('''SELECT y FROM io_orbit''')
Y_io = c.fetchall()
Y_io = [j[0] for j in Y_io]

c.execute('''SELECT z FROM io_orbit''')
Z_io = c.fetchall()
Z_io = [k[0] for k in Z_io]

c.execute('''SELECT x FROM eur_orbit''')
X_eur = c.fetchall()
# remove tuples from list
X_eur = [i[0] for i in X_eur]

c.execute('''SELECT y FROM eur_orbit''')
Y_eur = c.fetchall()
Y_eur = [j[0] for j in Y_eur]

c.execute('''SELECT z FROM eur_orbit''')
Z_eur = c.fetchall()
Z_eur = [k[0] for k in Z_eur]

c.execute('''SELECT gd FROM io_orbit''')
gd_list = c.fetchall()
gd_list = [to[0] for to in gd_list]
# close connection
conn.close()

curday = gd_list.index(str(datetime.date.today()) + ' 01:00:00')
with open('i_pickle', 'wb') as initi:
    pickle.dump(curday, initi)

# initial value of sine func file
with open('io_pickle', 'wb') as io_init:
    pickle.dump([[str(datetime.date.today()) + ' 01:00:00', 0, 0]], io_init)


# with open('eur_pickle', 'wb') as eur_init:
#    pickle.dump([[str(datetime.date.today())+' 01:00:00', 0, 0]], eur_init)

class Main(Tk):

    def __init__(self):
        super(Main, self).__init__()
        self.title("Jupiter and it's moons")
        self.centerWindow()
        self.resizable(width=False, height=False)
        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        t = (sw - 700) / 2
        j = (sh - 743) / 2
        self.geometry('%dx%d+%d+%d' % (700, 770, t, j))

        # Rob changed the fun buttons to something serious.... not fun -_-

        # Rob stop changing the fun names dick

        self.menubar = Menu(self)
        self.fileMenu = Menu(self.menubar, tearoff=0)
        self.fileMenu.add_command(label='Io Sine Graph', command=lambda: self.sine_view())
        self.fileMenu.add_command(Label='Europa Sine Graph', command=lambda: self.sine_view())
        self.fileMenu.add_separator()
        self.fileMenu.add_command(label="Exit", command=self.onExit)

        self.menubar.add_cascade(label="Commence", menu=self.fileMenu)
        self.config(menu=self.menubar)

    def onExit(self):
        self.quit()
        self.destroy()

    def centerWindow(self):
        # matplotlib graph
        plt.rcParams['toolbar'] = 'None'
        fig = pltw.figure(figsize=(7, 7))
        ax = fig.add_subplot(111, projection='3d')
        # maybe useful for future
        for angle in range(0, 360):
            ax.view_init(90, angle)

        # initial graph
        ax.scatter(X_io[curday], Y_io[curday], Z_io[curday], c='y', marker='o')
        ax.scatter(X_eur[curday], Y_eur[curday], Z_eur[curday], c='b', marker='o')
        pltw.plot([0], [0], marker='o', markersize=60, color="orange")
        ax.set_facecolor('grey')
        pltw.ylim(-.0035, .0035)
        pltw.xlim(-.0035, .0035)
        pltw.axis('off')
        canvas = FigureCanvasTkAgg(fig, self)
        fig.tight_layout()
        canvas.show()
        canvas.get_tk_widget().grid(row=0, column=0)

        # initial JD label
        jd = StringVar(self)
        cur_day_dt = datetime.datetime.strptime(gd_list[curday], '%Y-%m-%d %H:%M:%S')
        jd.set('Julian Day: ' + str(
            backAlgs.jd_alg(cur_day_dt.year, cur_day_dt.month, cur_day_dt.day, cur_day_dt.hour, cur_day_dt.minute,
                            cur_day_dt.second)))
        jdate_lab = Label(self, textvariable=jd)
        jdate_lab.grid(row=2, column=0, sticky=SE)

        # gregorian day label
        gd = StringVar(self)
        gd.set(gd_list[curday] + ' UTC')
        gdate_lab = Label(self, textvariable=gd)
        gdate_lab.grid(row=2, column=0, sticky=SW)

        # static step size label
        ind_lab = Label(self, text='Step Size:')
        ind_lab.grid(row=1, column=0, sticky=SW)

        # initial drop down menu
        raw_i = StringVar(self)
        raw_i.set('')
        ind_ops = OptionMenu(self, raw_i, '1 minute', '2 minutes', '6 minutes', '20 minutes', '255 minutes', '24 hours')
        ind_ops.grid(row=1, column=0, sticky=SW, padx=53)

        # pretty much my own version of an on call loop since python doesn't have one
        def wrapper():
            # this will save variable across runs
            ops = {'': 0, '1 minute': 1, '2 minutes': 2, '6 minutes': 6, '20 minutes': 20, '255 minutes': 255,
                   '24 hours': 1440}
            var = ops[raw_i.get()]

            with open('i_pickle', 'rb') as fiii:
                prev = pickle.load(fiii)
            with open('i_pickle', 'wb') as fi:
                pickle.dump((prev + var), fi)

            def graph():
                # open variable on each run of wrapper
                with open('i_pickle', 'rb') as fii:
                    i = pickle.load(fii)

                cur_day_dt = datetime.datetime.strptime(gd_list[i], '%Y-%m-%d %H:%M:%S')
                jd.set('Julian Day: ' + str(
                    backAlgs.jd_alg(cur_day_dt.year, cur_day_dt.month, cur_day_dt.day, cur_day_dt.hour,
                                    cur_day_dt.minute, cur_day_dt.second)))
                gd.set(gd_list[i] + ' UTC')
                plt.rcParams['toolbar'] = 'None'
                fig = pltw.figure(figsize=(7, 7))
                ax = fig.add_subplot(111, projection='3d')
                # maybe useful for future
                for angle in range(0, 360):
                    ax.view_init(90, angle)
                ax.clear()
                ax.scatter(X_io[i], Y_io[i], Z_io[i], c='y', marker='o')
                ax.scatter(X_eur[i], Y_eur[i], Z_eur[i], c='b', marker='o')
                pltw.plot([0], [0], marker='o', markersize=60, color="orange")
                ax.set_facecolor('grey')
                pltw.ylim(-.0035, .0035)
                pltw.xlim(-.0035, .0035)
                pltw.axis('off')
                canvas = FigureCanvasTkAgg(fig, self)
                fig.tight_layout()
                canvas.show()
                canvas.get_tk_widget().grid(row=0, column=0)

            graph()

        def record():
            # extract ra, dec for both moons from DB
            rec_conn = sqlite3.connect('orbit_data.db')
            rec_curs = rec_conn.cursor()
            # right acension of Io
            rec_curs.execute('''SELECT ra FROM io_orbit''')
            io_ra_raw = rec_curs.fetchall()
            io_ra_raw = [u[0] for u in io_ra_raw]
            # Dec of Io
            rec_curs.execute('''SELECT dec FROM io_orbit''')
            io_dec_raw = rec_curs.fetchall()
            io_dec_raw = [p[0] for p in io_dec_raw]

            with open('i_pickle', 'rb') as rec_read:
                # this is the current index variable at time that record button is pressed for every moon
                rec_i = pickle.load(rec_read)
            # what data do I need to plot the sine wave? so the gd's are gonna be the x-axis
            # RA is x value for sin
            # a is calculated from dec

            i_dump = [gd_list[rec_i], io_ra_raw[rec_i], io_dec_raw[rec_i]]

            with open('io_pickle', 'rb') as io_prev:
                prev = pickle.load(io_prev)

            comp_dump = prev + i_dump

            with open('io_pickle', 'wb') as io_next:
                pickle.dump(comp_dump, io_next)
            # so each moons pickle file will have a string with previous value as well as new value written to it

        self.nextbutton = Button(self, text='Next', command=lambda: wrapper())
        self.nextbutton.grid(row=1, column=0, sticky=SE)

        self.rec = Button(self, text='Record', command=lambda: record())
        self.rec.grid(row=1, column=0, sticky=SE, padx=35)

    def sine_view(self):
        t = Toplevel()
        plt.rcParams['toolbar'] = 'None'
        sin_fig = pltw.figure(figsize=(7, 7))
        sin_fig.add_subplot(111)

        # test data
        freqs = np.arange(2, 20, 3)
        sin_x = np.arange(0.0, 1.0, 0.001)
        sin_y = np.sin(2 * np.pi * freqs[0] * sin_x)
        pltw.plot(sin_x, sin_y, lw=2)

        sincanvas = FigureCanvasTkAgg(sin_fig, t)
        sincanvas.show()
        sincanvas.get_tk_widget().grid(row=0, column=0)


def main():
    ex = Main()
    ex.iconbitmap('icon.ico')
    ex.mainloop()


if __name__ == '__main__':
    main()
