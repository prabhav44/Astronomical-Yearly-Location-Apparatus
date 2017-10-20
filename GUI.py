from tkinter import Tk, BOTH, RIGHT, RAISED, Menu
from tkinter.ttk import Frame, Button, Style


class Main(Frame):
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

        nextButton = Button(self, text="Next")
        nextButton.pack(side=RIGHT)

        backButton = Button(self, text="Back")
        backButton.pack(side=RIGHT)

        recordButton = Button(self, text="Record")
        recordButton.pack(side=RIGHT)

        self.master.title("Commence")

        menubar = Menu(self.master)
        self.master.config(menu=menubar)

        fileMenu = Menu(menubar)
        fileMenu.add_command(label="Top View", command=self.initUI)
        fileMenu.add_command(label="Bye Felicia", command=self.onExit)
        menubar.add_cascade(label="Commence", menu=fileMenu)


    def onExit(self):
        self.quit()

    def centerWindow(self):
        w = 750
        h = 500

        sw = self.master.winfo_screenwidth()
        sh = self.master.winfo_screenheight()

        x = (sw - w) / 2
        y = (sh - h) / 2
        self.master.geometry('%dx%d+%d+%d' % (w, h, x, y))


def main():
    root = Tk()
    ex = Main()
    root.mainloop()


if __name__ == '__main__':
    main()