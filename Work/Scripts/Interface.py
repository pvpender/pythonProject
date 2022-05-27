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

import matplotlib.pyplot as plt

""" author Addrey Kamakin """
class Graphics(tk.Tk):
    def __init__(self, coutry: str, typef: str, disease_base, par):
        super().__init__()
        self.title('Статистика по стране')
        self.country = coutry
        self.type = typef
        self.disease_base = disease_base
        self.par = par
        flag = TRUE
        try:
            info = par.get_country_info(str(coutry), disease_base)
        except NoCountryLink:
            flag = FALSE
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
                stats = []
                for i in range(1, len(prestats) - 1):
                    stats.append(prestats[i] - prestats[i - 1])
                typef = "Прирост заражений"
            elif typef == "moredies":
                dates.pop(0)
                dates.pop()
                prestats = [int(item[2]) for item in info]
                stats = []
                for i in range(1, len(prestats) - 1):
                    stats.append(prestats[i] - prestats[i - 1])
                typef = "Прирост смертей"
            if len(stats) > len(dates):
                del stats[len(stats) - (len(stats) - len(dates)):len(stats)]
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
    def show(country, typef, disease_base, par):
        gr = Graphics(country, typef, disease_base, par)
        gr.geometry('1200x720')
        gr.mainloop()


class mainInterface(Frame):
    def __init__(self, info: dict, disease_base, par):
        super().__init__()
        self.country = None
        self.disease_base = disease_base
        self.par = par
        self.inf = info
        self.initUI()

    def WhenPoint(self, val):
        sender = val.widget
        index = sender.curselection()
        try:
            num = sender.get(index)
            self.var.set("Заражений за сегодня: " + str(self.inf.get(num)[0]) + "; Смертей за сегодня: " + str(self.inf.get(num)[1]))
            self.countryNameText.set(num)
            self.country = num
        except TclError:
            self.confirm()

    def confirm(self):
        try:
            index = self.lb.get(0, "end").index(self.permText.get())
            self.lb.select_set(index)
            self.country = str(self.permText.get())
            self.countryNameText.set(self.permText.get())
            self.var.set("Заражений за сегодня: " + str(self.inf.get(self.permText.get())[0]) + "; Смертей за сегодня: " + str(
                self.inf.get(self.permText.get())[1]))

        except ValueError:
            self.countryNameText.set('Страна не найдена')
            self.var.set(
                "Заражений за сегодня: -- ; Смертей за сегодня: -- " )

    def initUI(self):
        self.master.title("Информация по странам")
        self.countryNameText = StringVar()
        self.countryNameText.set("Выберите страну")
        self.permText=StringVar()
        self.pack(fill=BOTH, expand=1)
        frame1 = Frame(self)
        frame1.pack(fill=X, side=LEFT)
        nameFrame = Frame(self)
        nameFrame.pack(fill=X, side=LEFT)
        frame2 = Frame(self)
        underName = Frame(nameFrame)
        underName.pack(fill=X, side=LEFT)
        frame2.pack(fill=X, side=LEFT)

        self.names = self.inf.keys()
        self.lb = Listbox(frame1, height=20)
        for i in self.names:
            self.lb.insert(END, i)
            self.lb.bind("<<ListboxSelect>>", self.WhenPoint)
        self.var = StringVar()
        self.label = Label(nameFrame, text=0, textvariable=self.var)
        self.countryNameLb = Label(nameFrame, text=0, textvariable=self.countryNameText, font=("Arial", 25), width=20)
        txt = Entry(frame1, width=36, textvariable=self.permText)
        btn = Button(frame2, text="График смертей", width=30)
        btn.bind('<Button-1>', lambda a: Graphics.show(self.country, "dies", self.disease_base, self.par))
        btn2 = Button(frame2, text="График заражений", width=30)
        btn2.bind('<Button-1>', lambda a: Graphics.show(self.country, "disease", self.disease_base, self.par))
        btn3 = Button(frame2, text="График прироста смертей", width=30)
        btn3.bind('<Button-1>', lambda a: Graphics.show(self.country, "moredies", self.disease_base, self.par))
        btn4 = Button(frame2, text="График прироста заражений", width=30)
        btn4.bind('<Button-1>', lambda a: Graphics.show(self.country, "morediseases", self.disease_base, self.par))
        btn5 = Button(frame1, text="Подтвердить", width=30)
        btn5.bind('<Button-1>', lambda a: self.confirm())

        txt.pack(padx=15)
        btn5.pack(padx=15)
        self.lb.pack(padx=15, pady=15)
        btn.pack(padx=15, pady=15)
        btn2.pack(padx=15, pady=15)
        btn3.pack(padx=15, pady=15)
        btn4.pack(padx=15, pady=15)
        self.countryNameLb.pack(padx=80, pady=10)
        self.label.pack(padx=80, pady=10)
