# Codename: Astronomical-Yearly-Location-Apparatus
# TechDebt:
# TODO: Check for database update
# TODO: Enter date function
# I think the ab tag would allow it to simply append to the last entry

from scipy.optimize import curve_fit
from tkinter.ttk import Frame, Button, Style
from tkinter import *
import sqlite3
import matplotlib as plt
from math import sin, cos
from mpl_toolkits.mplot3d import Axes3D
plt.use("TkAgg")
import matplotlib.pyplot as pltw
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import pickle
import datetime
from backend import backAlgs
from scipy.optimize import curve_fit
from db_gen import db_gen

# connect to DB and get all our data
conn = sqlite3.connect('orbit_data.db')
c = conn.cursor()

# DB check for first entry
c.execute('''SELECT gd[0] FROM io_orbit''')
check_entry = c.fetchall()
check_entry = list(check_entry[0])[0]
print(check_entry)

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
# convert tuple to list
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

curday = gd_list.index(str(datetime.date.today())+' 01:00:00')
with open('i_pickle', 'wb') as initi:
    pickle.dump(curday, initi)

# initial value of sine func file
with open('io_pickle', 'wb') as io_init:
    pickle.dump([[str(datetime.date.today())+' 01:00:00', 0, 0]], io_init)

with open('eur_pickle', 'wb') as eur_init:
    pickle.dump([[str(datetime.date.today())+' 01:00:00', 0, 0]], eur_init)


class Main(Tk):

    def __init__(self):
        super(Main, self).__init__()
        self.title("Jupiter and Its Moons")
        self.centerWindow()
        self.resizable(width=False, height=False)
        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        t = (sw - 700) / 2
        j = (sh - 743) / 2
        self.geometry('%dx%d+%d+%d' % (700, 770, t, j))

        self.menubar = Menu(self)
        self.fileMenu = Menu(self.menubar, tearoff=0)
        self.fileMenu.add_command(label='Io Sine Graph', command=lambda: self.io_sine_view())
        self.fileMenu.add_command(label='Europa Sine Graph', command=lambda: self.eur_sine_view())

        self.menubar.add_cascade(label="Initiate", menu=self.fileMenu, state=DISABLED)

        self.menubar.add_cascade(label='Exit', command=self.onExit)
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
        cur_day_dt = datetime.datetime.strptime(str(gd_list[curday]), '%Y-%m-%d %H:%M:%S')
        jd.set('Julian Day: '+str(backAlgs.jd_alg(cur_day_dt.year, cur_day_dt.month, cur_day_dt.day, cur_day_dt.hour, cur_day_dt.minute, cur_day_dt.second)))
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
                pickle.dump((prev+var), fi)

            def graph():
                # open variable on each run of wrapper
                with open('i_pickle', 'rb') as fii:
                    i = pickle.load(fii)

                cur_day_dt = datetime.datetime.strptime(str(gd_list[i]), '%Y-%m-%d %H:%M:%S')
                jd.set('Julian Day: ' + str(backAlgs.jd_alg(cur_day_dt.year, cur_day_dt.month, cur_day_dt.day, cur_day_dt.hour,
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
            self.menubar.entryconfigure('Initiate', state=NORMAL)
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

            # RA of Eur
            rec_curs.execute('''SELECT ra FROM eur_orbit''')
            eur_ra_raw = rec_curs.fetchall()
            eur_ra_raw = [l[0] for l in eur_ra_raw]
            # Dec of Eur
            rec_curs.execute('''SELECT dec FROM eur_orbit''')
            eur_dec_raw = rec_curs.fetchall()
            eur_dec_raw = [w[0] for w in eur_dec_raw]
            rec_conn.close()

            # index variable goes for all data variables
            with open('i_pickle', 'rb') as rec_read:
                # this is the current index variable at time that record button is pressed for every moon
                rec_i = pickle.load(rec_read)

            # io relevant data dump
            io_dump = [gd_list[rec_i], io_ra_raw[rec_i], io_dec_raw[rec_i]]
            with open('io_pickle', 'rb') as io_prev:
                prev_io = pickle.load(io_prev)
            comp_dump_io = prev_io + io_dump
            with open('io_pickle', 'wb') as io_next:
                pickle.dump(comp_dump_io, io_next)

            # europa dump
            eur_dump = [gd_list[rec_i], eur_ra_raw[rec_i], eur_dec_raw[rec_i]]
            with open('eur_pickle', 'rb') as eur_prev:
                prev_eur = pickle.load(eur_prev)
            comp_dump_eur = prev_eur + eur_dump
            with open('eur_pickle', 'wb') as eur_next:
                pickle.dump(comp_dump_eur, eur_next)

        self.nextbutton = Button(self, text='Next', command=lambda: wrapper())
        self.nextbutton.grid(row=1, column=0, sticky=SE)

        self.rec = Button(self, text='Record', command=lambda: record())
        self.rec.grid(row=1, column=0, sticky=SE, padx=35)

    def io_sine_view(self):
        with open('io_pickle', 'rb') as io_ev:
            io_raw = pickle.load(io_ev)
            del io_raw[0]
        # storing dates as JD's
        graph_jds = []
        for cu in range(0, len(io_raw), 3):
            gds_dt = datetime.datetime.strptime(io_raw[cu], '%Y-%m-%d %H:%M:%S')
            graph_jds.append(backAlgs.jd_alg(gds_dt.year, gds_dt.month, gds_dt.day, gds_dt.hour,
                                             gds_dt.minute, gds_dt.second))
        graph_io_ra = []
        for buffs in range(1, len(io_raw), 3):
            graph_io_ra.append(io_raw[buffs])

        graph_io_dec = []
        for suck in range(2, len(io_raw), 3):
            graph_io_dec.append(io_raw[suck])

        io_graph_y = []
        io_graph_a = []
        for brad in range(0, len(graph_jds), 1):
            io_graph_a.append(.002819 * (np.cos(graph_io_dec[brad])))
            io_graph_y.append(io_graph_a[brad]*np.sin(3.548152371*graph_jds[brad]))

        io_t = Toplevel()
        io_t.wm_title('Io sin Plot')
        plt.rcParams['toolbar'] = 'None'
        io_sin_fig = pltw.figure()
        io_sin_fig.add_subplot(111)

        pltw.scatter(graph_io_ra, io_graph_y)
        pltw.ylabel('Distance from Jupiter (AU)')
        pltw.xticks([])

        io_sincanvas = FigureCanvasTkAgg(io_sin_fig, io_t)
        io_sincanvas.show()
        io_sincanvas.get_tk_widget().grid(row=0, column=0)

        def sine_curve():
            def func(x, A):
                return A*np.sin(3.548152371*x)
            popt, pcov = curve_fit(func, np.array(graph_jds, dtype='float'), io_graph_y)
            io_sin_fig = pltw.figure()
            io_sin_fig.add_subplot(111)

            pltw.scatter(graph_io_ra, io_graph_y)
            pltw.scatter(np.array(graph_io_ra, dtype='float64'), func(np.array(graph_jds, dtype='float'), *popt))
            pltw.ylabel('Distance from Jupiter (AU)')
            pltw.xticks([])
            amp_gen = func(np.array(graph_jds, dtype='float'), *popt)/np.sin(3.548152371*np.array(graph_jds, dtype='float'))
            amp.set('Amplitude: '+str(amp_gen[0]))
            io_sincanvas = FigureCanvasTkAgg(io_sin_fig, io_t)
            io_sincanvas.show()
            io_sincanvas.get_tk_widget().grid(row=0, column=0)
            io_sincanvas.draw()

        amp = StringVar()
        amp.set('Amplitude: ')
        IOfitButton = Button(io_t, text='Fit Sin Curve', command=lambda: sine_curve())
        IOfitButton.grid(row=1, column=0, sticky=SE)
        Io_amp = Label(io_t, textvariable=amp)
        Io_amp.grid(row=1, column=0, sticky=SW)
        Io_per = Label(io_t, text='Period: 152853.5232')
        Io_per.grid(row=2, column=0, sticky=SW)


    def eur_sine_view(self):
        with open('eur_pickle', 'rb') as eur_ev:
            eur_raw = pickle.load(eur_ev)
            del eur_raw[0]
        # storing dates as JD's
        graph_jds = []
        for cu in range(0, len(eur_raw), 3):
            gds_dt = datetime.datetime.strptime(eur_raw[cu], '%Y-%m-%d %H:%M:%S')
            graph_jds.append(backAlgs.jd_alg(gds_dt.year, gds_dt.month, gds_dt.day, gds_dt.hour,
                                             gds_dt.minute, gds_dt.second))
        graph_eur_ra = []
        for buffs in range(1, len(eur_raw), 3):
            graph_eur_ra.append(eur_raw[buffs])

        graph_eur_dec = []
        for suck in range(2, len(eur_raw), 3):
            graph_eur_dec.append(eur_raw[suck])

        eur_graph_y = []
        eur_graph_a = []
        for brad in range(0, len(graph_jds), 1):
            eur_graph_a.append(.004485 * (np.cos(graph_eur_dec[brad])))
            eur_graph_y.append(eur_graph_a[brad]*np.sin(3.548152371*graph_jds[brad]))

        eur_t = Toplevel()
        eur_t.wm_title('Europa sin Plot')
        plt.rcParams['toolbar'] = 'None'
        eur_sin_fig = pltw.figure()
        eur_sin_fig.add_subplot(111)

        pltw.scatter(graph_eur_ra, eur_graph_y)
        pltw.ylabel('Distance from Jupiter (AU)')
        pltw.xticks([])

        eur_sincanvas = FigureCanvasTkAgg(eur_sin_fig, eur_t)
        eur_sincanvas.show()
        eur_sincanvas.get_tk_widget().grid(row=0, column=0)

        def sine_curve():
            def func(x, A):
                return A*np.sin(3.548152371*x)
            popt, pcov = curve_fit(func, np.array(graph_jds, dtype='float'), eur_graph_y)
            io_sin_fig = pltw.figure()
            io_sin_fig.add_subplot(111)

            pltw.scatter(graph_eur_ra, eur_graph_y)
            pltw.scatter(np.array(graph_eur_ra, dtype='float64'), func(np.array(graph_jds, dtype='float'), *popt))
            pltw.ylabel('Distance from Jupiter (AU)')
            pltw.xticks([])
            amp_gen = func(np.array(graph_jds, dtype='float'), *popt)/np.sin(3.548152371*np.array(graph_jds, dtype='float'))
            amp.set('Amplitude: '+str(amp_gen[0]))
            eur_sincanvas = FigureCanvasTkAgg(eur_sin_fig, eur_t)
            eur_sincanvas.show()
            eur_sincanvas.get_tk_widget().grid(row=0, column=0)
            eur_sincanvas.draw()

        amp = StringVar()
        amp.set('Amplitude: ')
        eurfitButton = Button(eur_t, text='Fit Sin Curve', command=lambda: sine_curve())
        eurfitButton.grid(row=1, column=0, sticky=SE)
        eur_amp = Label(eur_t, textvariable=amp)
        eur_amp.grid(row=1, column=0, sticky=SW)
        eur_per = Label(eur_t, text='Period: 306822.0384')
        eur_per.grid(row=2, column=0, sticky=SW)


def main():
    ex = Main()
    ex.iconbitmap('icon.ico')
    ex.mainloop()


if __name__ == '__main__':
    main()
