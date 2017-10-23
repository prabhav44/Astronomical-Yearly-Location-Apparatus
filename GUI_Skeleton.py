from tkinter.ttk import Frame, Button, Style
from tkinter import *


class Main(Frame):
    top = Tk()

    C = Canvas(top, bg="blue", height=700, width=450)
    filename = PhotoImage(file="C:\\Users\\Owner\\Pictures\\Saved Pictures\\Jupiter.png")
    background_label = Label(top, image=filename)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)

    C.pack()
    top.mainloop

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

        recordButton = Button(self, text="Record", background = "red")
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
        w = 1036
        h = 720

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