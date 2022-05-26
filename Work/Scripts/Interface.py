import time
from application_functions import *
from Work.Scripts.Saving import *
from tkinter.ttk import Frame, Label, Button, Entry
from tkinter import *
import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg,
    NavigationToolbar2Tk
)

""" author Kamakin Andrey """
import matplotlib.pyplot as plt


class Graphics(tk.Tk):
    def __init__(self, coutry: str, typef: str):
        super().__init__()
        self.title('Статистика по стране')
        self.country = coutry
        self.type = typef
        disease_base = Database("../Data/disease1.db", "info", ["country", "date", "disease", "dies"])
        par = Parser()
        flag=TRUE
        try:
            info = par.get_country_info(str(coutry), disease_base)
        except NoCountryLink:
            flag=FALSE
        if flag:
            info.reverse()
            dates1 = [item[0] for item in info]
            dates = pd.date_range(start=datetime.strptime(dates1[0], "%d.%m.%y"),
                                  end=datetime.strptime(dates1[len(dates1) - 1],
                                                        "%d.%m.%y")).to_pydatetime().tolist()
            if typef == "disease":
                stats = [int(item[1]) for item in info]
                typef = 'Количество заболевших'
            elif typef == "dies":
                stats = [int(item[2]) for item in info]
                typef = 'Количество умерших'
            elif typef == "morediseases":
                dates.pop(0)
                dates.pop()
                prestats = [int(item[1]) for item in info]
                stats=[]
                for i in range(1, len(prestats)-1):
                    stats.append(prestats[i]-prestats[i-1])
                typef="Прирост заражений"
            elif typef=="moredies":
                dates.pop(0)
                dates.pop()
                prestats = [int(item[2]) for item in info]
                stats=[]
                for i in range(1, len(prestats)-1):
                    stats.append(prestats[i]-prestats[i-1])
                typef="Прирост смертей"
            figure = Figure(figsize=(6, 4), dpi=100)
            canvas = FigureCanvasTkAgg(figure, self)
            NavigationToolbar2Tk(canvas, self)
            gr = figure.add_subplot()
            gr.plot(dates, stats)
            gr.set_title(typef + ' по стране ' + coutry)
            gr.set_ylabel('')
            canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        else:
            label = Label(self, text="Отсутствует информация по стране " + coutry)
            label.pack()
    @staticmethod
    def show(country, typef):
        gr = Graphics(country, typef)
        gr.geometry('1200x720')
        gr.mainloop()


class ListInterface(Frame):
    def __init__(self, info: dict):
        super().__init__()
        self.inf = info
        self.initUI()

    def WhenPoint(self, val):
        sender = val.widget
        index = sender.curselection()
        num = sender.get(index)
        self.var.set(
            "Заражений за сегодня: " + str(self.inf.get(num)[0]) + "; Смертей за сегодня: " + str(self.inf.get(num)[1]))
        self.country=num

    def initUI(self):
        self.master.title("Информация по странам")
        self.country = "Италия"
        self.names = self.inf.keys()
        self.pack(fill=BOTH, expand=1)
        lb = Listbox(self, height=16)
        txt = Entry(self, width=30)
        btn = Button(self, text="График смертей")
        btn.bind('<Button-1>',lambda a: App.show(self.country, "dies"))
        btn2 = Button(self, text="График заражений")
        btn2.bind('<Button-1>',lambda a: App.show(self.country, "disease"))
        for i in self.names:
            lb.insert(END, i)
        lb.bind("<<ListboxSelect>>", self.WhenPoint)
        self.var = StringVar()
        self.label = Label(self, text=0, textvariable=self.var)
        lb.pack(side=LEFT)
        self.label.pack(padx=80)
        txt.pack(padx=80)
        btn.pack(padx=80)
        btn2.pack(padx=80)


def main():
    root = Tk()
    f = open("config.txt", "r")
    geom = f.read(7)
    root.geometry(geom)
    root.mainloop()


if __name__ == '__main__':
    main()
