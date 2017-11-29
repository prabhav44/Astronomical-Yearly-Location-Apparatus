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

with open('pickle', 'wb') as initi:
    pickle.dump(0, initi)

# connect to DB
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

# same thing as above
c.execute('''SELECT y FROM eur_orbit''')
Y_eur = c.fetchall()
Y_eur = [j[0] for j in Y_eur]

c.execute('''SELECT z FROM eur_orbit''')
Z_eur = c.fetchall()
Z_eur = [k[0] for k in Z_eur]
# close connection
conn.close()


class Main(Tk):

    def __init__(self):
        super(Main, self).__init__()
        self.title("Project Astronomical-Yearly-Location-Apparatus")
        self.centerWindow()
        self.resizable(width=False, height=False)
        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        t = (sw - 700) / 2
        j = (sh - 743) / 2
        self.geometry('%dx%d+%d+%d' % (700, 750, t, j))

        self.menubar = Menu(self)
        self.fileMenu = Menu(self.menubar, tearoff=0)
        self.fileMenu.add_command(label="Bye Felicia", command=self.onExit)

        self.menubar.add_cascade(label="Commence", menu=self.fileMenu)
        self.config(menu=self.menubar)

        incrementList = ('1 minute', '2 minutes', '6 minutes', '255 minutes', '24 hours')
        self.v = StringVar()
        self.v.set(incrementList[0])
        self.om = OptionMenu(self, self.v, *incrementList)
        self.om.grid(row=1, column=0, sticky=SW)


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
        ax.scatter(X_io[0], Y_io[0], Z_io[0], c='y', marker='o')
        ax.scatter(X_eur[0], Y_eur[0], Z_eur[0], c='b', marker='o')
        pltw.plot([0], [0], marker='o', markersize=60, color="orange")
        ax.set_facecolor('grey')
        pltw.ylim(-.0035, .0035)
        pltw.xlim(-.0035, .0035)
        pltw.axis('on')
        canvas = FigureCanvasTkAgg(fig, self)
        fig.tight_layout()
        canvas.show()
        canvas.get_tk_widget().grid(row=0, column=0)



        def wrapper(var):
            # this will save variable across runs
            with open('pickle', 'rb') as fiii:
                prev = pickle.load(fiii)
            with open('pickle', 'wb') as fi:
                pickle.dump((prev+var), fi)
            def graph():
                # open variable on each run of wrapper
                with open('pickle', 'rb') as fii:
                    i = pickle.load(fii)
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

        self.nextbutton = Button(self, text='Next', command=lambda: wrapper(5))
        self.nextbutton.grid(row=1, column=0, sticky=SE)


def main():
    ex = Main()
    ex.iconbitmap('icon.ico')
    ex.mainloop()


if __name__ == '__main__':
    main()
