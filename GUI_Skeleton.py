from tkinter.ttk import Frame, Button, Style
from tkinter import *
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


class Main(Frame):
    top = Tk()

    C = Canvas(top, bg="blue", height=700, width=700)

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.master.title("Project Astronomical-Yearly-Location-Apparatus")
        self.pack(fill=BOTH, expand=1)
        self.centerWindow()
        self.master.title("Buttons")
        self.style = Style()
        self.style.theme_use("default")
        frame = Frame(self, relief=RAISED, borderwidth=1)
        frame.pack(fill=BOTH, expand=True)

        self.pack(fill=BOTH, expand=True)

        nextButton = Button(self, text="Next", background = "green")
        nextButton.pack(side=RIGHT)

        backButton = Button(self, text="Back", background = "blue")
        backButton.pack(side=RIGHT)

        recordButton = Button(self, text="Record", background="red")
        recordButton.pack(side=RIGHT)

        self.master.title("Commence")

        menubar = Menu(self.master)
        self.master.config(menu=menubar)

        fileMenu = Menu(menubar)
        fileMenu.add_command(label="Side View", command=self.side_view)
        fileMenu.add_command(label="Bye Felicia", command=self.onExit)
        menubar.add_cascade(label="Commence", menu=fileMenu)

    def side_view(self):
        t = Toplevel(self)
        t.wm_title("Side View")
        l = Label(t, text="This is window")
        l.pack(side="top", fill="both", expand=True, padx=100, pady=100)

    def onExit(self):
        self.quit()

    def centerWindow(self):
        w = 700
        h = 700

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

        canvas = FigureCanvasTkAgg(fig, self)
        canvas.show()
        canvas.get_tk_widget().pack(side=BOTTOM, fill=BOTH, expand=True)

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
