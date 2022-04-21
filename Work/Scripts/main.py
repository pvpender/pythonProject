from Work.Library.standard_functions import *
from Interface import *
from tkinter import Tk
from application_functions import *

if __name__ == "__main__":
    disease_base = Database("../Data/disease1.db", "info", ["country", "date", "disease", "dies"])
    world_base = Database("../Data/world.db", "info", ["date", "disease", "dies"])
    par = Parser()
    print(par.get_info())
    print(par.get_country_info("Великобритания", disease_base))
    print(par.get_country_info("Германия", disease_base))
    #disease_base.del_row([0, 1], ["Германия", "16-04-22"])
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
