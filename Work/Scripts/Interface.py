from tkinter import Tk, Listbox, StringVar, BOTH, END
from tkinter.ttk import Frame, Label
""" author Kamakin Andrey """
class ListInterface(Frame):
    def __init__(self, info: dict):
        super().__init__()
        self.inf=info
        self.initUI()

    def WhenPoint(self, val):
        sender = val.widget
        index = sender.curselection()
        num = sender.get(index)

        self.var.set("Заражений за сегодня: "+str(self.inf.get(num)[0])+"; Смертей за сегодня: "+str(self.inf.get(num)[1]))

    def initUI(self):
        self.master.title("Информация по странам")
        self.pack(fill=BOTH, expand=1)
        names=self.inf.keys()
        lb = Listbox(self)
        for i in names:
            lb.insert(END, i)
        lb.bind("<<ListboxSelect>>", self.WhenPoint)
        lb.pack(pady=15)
        self.var = StringVar()
        self.label = Label(self, text=0, textvariable=self.var)
        self.label.pack()

def main():
    root = Tk()
    f=open("config.txt","r")
    geom=f.read(7)
    root.geometry(geom)
    root.mainloop()


if __name__ == '__main__':
    main()
