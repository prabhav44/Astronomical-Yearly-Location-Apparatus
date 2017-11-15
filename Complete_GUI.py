from tkinter.ttk import Frame, Button, Style
import tkinter as tk
import sqlite3
import matplotlib as plt
from mpl_toolkits.mplot3d import Axes3D
plt.use("TkAgg")
import matplotlib.pyplot as pltw
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np


# connect to DB
conn = sqlite3.connect('orbit_data.db')
c = conn.cursor()

# select x values and save to x list
c.execute('''SELECT x FROM orbit''')
x = c.fetchall()
# remove tuples from list
X = [i[0] for i in x]

# same thing as above
c.execute('''SELECT y FROM orbit''')
y = c.fetchall()
Y = [j[0] for j in y]

c.execute('''SELECT z FROM orbit''')
z = c.fetchall()
Z = [k[0] for k in z]

# close connection
conn.close()

X = x[2880:5760]
Y = y[2880:5760]
Z = z[2880:5760]


class Main(tk.Tk):
    def __init__(self):
        tk.Tk.__init(self)
        self.title("Project Astronomical-Yearly-Location-Apparatus")
        self.centerWindow()

        self.menubar = tk.Menu(self)
        self.fileMenu = tk.Menu(self.menubar, tearoff=0)
        self.fileMenu.add_command(label="Side View", command=self.side_view)
        self.fileMenu.add_command(label="Bye Felicia", command=self.onExit)

        self.menubar.add_cascade(label="Commence", menu=self.fileMenu)
        self.config(menu=self.menubar)

    def side_view(self):
        t = tk.Toplevel(self)
        t.wm_title("Side View")
        l = tk.Label(t, text="This is window")
        l.pack(side="top", fill="both", expand=True, padx=100, pady=100)

    def onExit(self):
        self.quit()

    def centerWindow(self):
        w = 700
        h = 700
        self.button1 = tk.Button(self, text="Back")
        self.button2 = tk.Button(self, text="Record")
        self.button3 = tk.Button(self, text="Next")
        self.button1.grid(row=1, column=1)
        self.button2.grid(row=1, column=2)
        self.button3.grid(row=1, column=3)
        # matplotlib graph

        plt.rcParams['toolbar'] = 'None'
        fig = pltw.figure(figsize=(7, 7), dpi=100)
        ax = fig.add_subplot(111, projection='3d')
        for angle in range(0, 360):
            ax.view_init(90, angle)

        for c, m, zlow, zhigh in [('r', 'o', -3000, -3000), ('b', '^', -3000, -3000)]:
            xs = X
            ys = Y
            zs = Z
            ax.scatter(xs, ys, zs, c=c, marker=m)

        pltw.plot([0], [0], marker='o', markersize=60, color="orange")
        ax.set_facecolor('grey')
        pltw.axis('on')

        """canvas = FigureCanvasTkAgg(fig, self)
        canvas.show()
        canvas.get_tk_widget().pack(side=BOTTOM, fill=BOTH, expand=True)"""

        self.master.resizable(width=False, height=False)
        sw = self.master.winfo_screenwidth()
        sh = self.master.winfo_screenheight()
        x = (sw - w) / 2
        y = (sh - h) / 2
        self.master.geometry('%dx%d+%d+%d' % (w, h, x, y))


def main():
    ex = Main()
    ex.mainloop()


if __name__ == '__main__':
    main()
