import datetime
import time

from Work.Library.standard_functions import *
from Interface import *
from tkinter import Tk
from application_functions import *
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from Work.Scripts.Saving import *

if __name__ == "__main__":
    disease_base = Database("../Data/disease1.db", "info", ["country", "date", "disease", "dies"])
    world_base = Database("../Data/world.db", "info", ["date", "disease", "dies"])
    par = Parser()
    print()
    print(par.get_info())
    print(par.get_country_info("Россия", disease_base))
    print(par.get_country_info("Германия", disease_base))
    s = Saver()
    print(par.get_country_info("Россия", disease_base))

    """def sr(mas, a):
        x = []
        print(len(mas))
        for i in range(len(mas) - 2, -1, -1):
            x.append(int(mas[i][a]) - int(mas[i+1][a]))
        print(len(x))
        mas_y = pd.date_range(start="2020-03-03", end="2022-05-24").to_pydatetime().tolist()
        plt.plot(mas_y, x)
        plt.show()


    sr(par.get_country_info("Россия", disease_base), 2)"""
    '''print(Sorter.sorting(1, disease_base.find_data([0], ["Германия"])))
    mas_y = pd.date_range(start="2020-02-01", end="2022-04-16").to_pydatetime().tolist()
    rmas = np.array(par.get_country_info("Россия", disease_base))
    time.sleep(2)
    umas = np.array(par.get_country_info("США", disease_base))
    time.sleep(2)
    fmas = np.array(par.get_country_info("Франция", disease_base))
    time.sleep(2)
    pmas = np.array(par.get_country_info("Китай", disease_base))
    r = int(rmas[0, 1])
    u = int(umas[0, 1])
    f = int(fmas[0, 1])
    p = int(pmas[0, 1])
    print(r, u, f, p)
    n = ["США", "Франция", "Россия", "Китай"]
    plt.bar(n, [u, f, r, p])
    # plt.scatter(x=y_1, y = y)
    # plt.bar(mas_y, y[::-1])
    plt.title("Всего заражений к текущему моменту")

    plt.show()

    root = Tk()
    inf=par.get_info()
    ex = ListInterface(inf)
    f = open("config.txt", "r")
    geom = f.read(7)
    f.close()
    root.geometry(geom)
    root.mainloop()
   '''



