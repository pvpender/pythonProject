from application_functions import *
from Work.Scripts.Saving import *
from tkinter.ttk import Frame, Label, Button, Entry
from tkinter import filedialog as fd
from tkinter import *
from tkinter import messagebox
import tkinter as tk
import tkinter.ttk as ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg,
    NavigationToolbar2Tk
)


class TablesWindow(tk.Tk):
    def __init__(self, names, par: Parser, database: Database, saver: Saver):
        super().__init__()
        self.mas = []
        self.names = names
        self.par = par
        self.saver = saver
        self.database = database
        self.vsb = tk.Scrollbar(self, orient="vertical")
        self.text = tk.Text(self, width=15, height=700, yscrollcommand=self.vsb.set)
        self.vsb.config(command=self.text.yview)
        self.vsb.pack(side="right", fill="y")
        self.text.pack(side="left", fill="y", expand=True, anchor="w")
        self.lb = Label(self, text="Выберите страны и столбцы по которым нужно создать таблицу", font=("Arial", 20))
        self.lb.pack(side=TOP)
        self.btn = Button(self, text="Создать таблицу", width=30, command=lambda: self.create_table())
        self.btn.pack(side=RIGHT)
        self.cb_d = ttk.Checkbutton(self, width=25, takefocus=False, variable='', text="Заражения")
        self.cb_d.pack(side="left")
        self.cb_di = ttk.Checkbutton(self, width=25, takefocus=False, variable='', text="Смерти")
        self.cb_di.pack(side="left")
        j = 0
        for i in names:
            cb = ttk.Checkbutton(self, width=25, takefocus=False, variable='', text=i)
            self.mas.append(cb)
            self.text.window_create("end", window=cb)
            self.text.insert("end", "\n")
            j += 1

    @staticmethod
    def show(names, par: Parser, database: Database, saver: Saver):
        ex = TablesWindow(names, par, database, saver)
        ex.geometry("1400x720")
        ex.mainloop()

    def create_table(self):
        mas_lists = []
        list_names = []
        list_columns = []
        if self.cb_d.state():
            list_columns.append("disease")
        if self.cb_di.state():
            list_columns.append("dies")
        for i in range(len(self.mas)):
            columns = [0, ]
            if self.mas[i].state() and self.mas[i].state()[0] == 'selected':
                if self.cb_d.state():
                    columns.append(1)
                if self.cb_di.state():
                    columns.append(2)
                try:
                    r = self.par.get_country_info(list(self.names)[i], self.database)
                except NoCountryLink:
                    continue
                data_np = np.array(r)
                data = data_np[0:, np.r_[columns]].tolist()
                mas_lists.append(data)
                list_names.append(list(self.names)[i])
        try:
            self.saver.unite_data(list_columns, mas_lists, list_names)
            messagebox.showinfo("Готово", "Файл сохранён", parent=self)
        except ValueError:
            messagebox.showerror("Ошибка", "Вы не выбрали ни одной станы!", parent=self)


class Graphics(tk.Tk):
    def __init__(self, country: str, typef: str, disease_base: Database, par: Parser, saver: Saver):
        super().__init__()
        self.title('Статистика по стране')
        self.country = country
        self.type = typef
        self.disease_base = disease_base
        self.par = par
        self.saver = saver
        flag = TRUE
        info = list
        stats = list
        try:
            info = par.get_country_info(str(country), disease_base)
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
            gr.set_title(typef + ' по стране ' + country)
            gr.set_ylabel('')
            canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
            btn = Button(self, text="Обновить данные", font=("Arial", 20), width=30, height=1,
                         command=lambda: Graphics.insert(self, disease_base, country))
            btn.pack(side=RIGHT)
            info.reverse()
            btn2 = Button(self, text="Сохранить текстовый отчёт", font=("Arial", 20), width=30, height=1,
                          command=lambda: saver.save_country_data(country, info))
            btn2.pack(side=LEFT)
        else:
            if country is None:
                label = Label(self, text="Вы не выбрали страну!", font=("Courier", 30))
                label.pack(pady=300)
            else:
                label = Label(self, text=f"Отсутствует информация по стране {country}! \n Хотите добавить данные "
                                         f"вручную?", font=("Courier", 30))
                label.pack()
                btn = Button(self, text="Добавить", font=("Arial", 20), width=30, height=1,
                             command=lambda: Graphics.insert(self, disease_base, country))
                btn.pack()

    def insert(self, database: Database, country: str):
        filepath = fd.askopenfilename(parent=self, filetypes=[("CSV file", "*.csv")])
        try:
            mas = pd.read_csv(filepath)
        except FileNotFoundError:
            return None
        mas = mas.values.tolist()
        if Graphics.check(mas):
            database.del_row([0], [country])
            for i in range(len(mas)):
                mas[i][0] = country
            database.insert_rows(mas)
            self.destroy()
            Graphics.show(country, self.type, database, self.par, self.saver)
        else:
            messagebox.showerror("Ошибка", "Неправильное строение файла!", parent=self)
            return None

    @staticmethod
    def check(mas: list):
        try:
            if (len(mas[0]) != 4) or not (datetime.strptime(mas[0][1], "%d.%m.%y")):
                return False
            else:
                return True
        except TypeError:
            return False

    @staticmethod
    def show(country, typef, disease_base, par, saver):
        gr = Graphics(country, typef, disease_base, par, saver)
        gr.geometry('1400x720')
        gr.mainloop()


class MainInterface(Frame):

    countryNameText = StringVar
    permText = StringVar
    names = list
    lb = Listbox
    var = StringVar
    label = Label
    countryNameLb = Label

    def __init__(self, info: dict, disease_base: Database, par: Parser, saver: Saver):
        super().__init__()
        self.country = None
        self.disease_base = disease_base
        self.par = par
        self.inf = info
        self.init_ui()
        self.saver = saver
        saver.save_world_data(info)

    def when_point(self, val):
        sender = val.widget
        index = sender.curselection()
        try:
            num = sender.get(index)
            self.var.set(f"Заражений за сегодня: {str(self.inf.get(num)[0])}; Смертей за сегодня: "
                         f"{str(self.inf.get(num)[1])}")
            self.countryNameText.set(num)
            self.country = num
        except TclError:
            self.confirm()

    def confirm(self):
        try:
            index = self.lb.get(0, "end").index(self.permText.get())
            print(self.permText.get())
            self.lb.select_set(index)
            self.country = str(self.permText.get())
            self.countryNameText.set(self.permText.get())
            self.var.set(f"Заражений за сегодня: {str(self.inf.get(self.permText.get())[0])}; Смертей за сегодня: "
                         f"{str(self.inf.get(self.permText.get())[1])}")
        except ValueError:
            self.countryNameText.set('Страна не найдена')
            self.var.set("Заражений за сегодня: -- ; Смертей за сегодня: -- ")

    def init_ui(self):
        self.master.title("Информация по странам")
        self.countryNameText = StringVar()
        self.countryNameText.set("Выберите страну")
        self.permText = StringVar()
        self.pack(fill=BOTH, expand=1)
        frame1 = Frame(self)
        frame1.pack(fill=X, side=LEFT)
        name_frame = Frame(self)
        name_frame.pack(fill=X, side=LEFT)
        frame2 = Frame(self)
        under_name = Frame(name_frame)
        under_name.pack(fill=X, side=LEFT)
        frame2.pack(fill=X, side=LEFT)
        self.names = self.inf.keys()
        self.lb = Listbox(frame1, height=20, width=30)
        for i in self.names:
            self.lb.insert(END, i)
            self.lb.bind("<<ListboxSelect>>", self.when_point)
        self.var = StringVar()
        self.label = Label(name_frame, text=0, textvariable=self.var)
        self.countryNameLb = Label(name_frame, text=0, textvariable=self.countryNameText, font=("Arial", 25), width=20)
        txt = Entry(frame1, width=36, textvariable=self.permText)
        btn = Button(frame2, text="График смертей", width=30)
        btn.bind('<Button-1>', lambda a: Graphics.show(self.country, "dies", self.disease_base, self.par, self.saver))
        btn2 = Button(frame2, text="График заражений", width=30)
        btn2.bind('<Button-1>', lambda a: Graphics.show(self.country, "disease", self.disease_base, self.par,
                                                        self.saver))
        btn3 = Button(frame2, text="График прироста смертей", width=30)
        btn3.bind('<Button-1>', lambda a: Graphics.show(self.country, "moredies", self.disease_base, self.par,
                                                        self.saver))
        btn4 = Button(frame2, text="График прироста заражений", width=30)
        btn4.bind('<Button-1>', lambda a: Graphics.show(self.country, "morediseases", self.disease_base, self.par,
                                                        self.saver))
        btn5 = Button(frame1, text="Подтвердить", width=30)
        btn5.bind('<Button-1>', lambda a: self.confirm())
        btn6 = Button(frame1, text="Создание таблиц", width=30)
        btn6.bind('<Button-1>', lambda a: TablesWindow.show(self.names, self.par, self.disease_base, self.saver))

        txt.pack(padx=15)
        btn5.pack(padx=15)
        self.lb.pack(padx=15, pady=15)
        btn.pack(padx=15, pady=15)
        btn2.pack(padx=15, pady=15)
        btn3.pack(padx=15, pady=15)
        btn4.pack(padx=15, pady=15)
        btn6.pack(padx=15, pady=15)
        self.countryNameLb.pack(padx=80, pady=10)
        self.label.pack(padx=80, pady=10)
