import tkinter as tk
import matplotlib.pyplot as plt

class Main(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("Project-Astronomical-Yearly-Location-Aparatus")
        self.centerWindow()

        self.menubar = tk.Menu(self)
        self.fileMenu = tk.Menu(self.menubar,tearoff=0)
        self.fileMenu.add_command(label="Side View", command = self.side_view)
        self.fileMenu.add_command(label="Bye Felicia", command = self.onExit)

        self.menubar.add_cascade(label="Commence", menu=self.fileMenu)
        self.config(menu=self.menubar)

    def side_view(self):
        t = tk.Toplevel(self)
        t.wm_title("Side View")
        l = tk.Label(t, text="This is window")
        l.pack(side="top",fill="both",expand=True,padx=100,pady=100)

    def onExit(self):
        self.destroy()

    def centerWindow(self):
        w = 700
        h = 700
        self.button1 = tk.Button(self, text="Next")
        self.button2 = tk.Button(self, text="Record")
        self.button3 = tk.Button(self, text="Back")
        self.button1.grid(row=1,column=1)
        self.button2.grid(row=1,column=2)
        self.button3.grid(row=1,column=3)

        self.resizable(width=False, height=False)
        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        x = (sw - w) / 2
        y = (sh - h) / 2
        self.geometry('%dx%d+%d+%d' % (w, h, x, y))

main = Main()
main.mainloop()