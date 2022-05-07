import time

from Work.Library.standard_functions import *
from Interface import *
from tkinter import Tk
from application_functions import *
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
if __name__ == "__main__":
    disease_base = Database("../Data/disease1.db", "info", ["country", "date", "disease", "dies"])
    world_base = Database("../Data/world.db", "info", ["date", "disease", "dies"])
    par = Parser()
    print(par.get_info())
    print(par.get_country_info("Россия", disease_base))
    print(par.get_country_info("Германия", disease_base))
    #disease_base.del_row([0, 1], ["Германия", "16-04-22"])

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

    plt.show()'''

    print(Sorter.sorting(1, disease_base.find_data([0], ["Германия"])))
    print(par.get_world_info(world_base))
    root = Tk()
    inf=par.get_info()
    ex = ListInterface(inf)
    f = open("config.txt", "r")
    geom = f.read(7)
    f.close()
    root.geometry(geom)
    root.mainloop()

