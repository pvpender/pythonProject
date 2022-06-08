from Interface import *
from tkinter import Tk
from application_functions import *
""" authors: Moiseev Nikolay and Addrey Kamakin """
if __name__ == "__main__":
    disease_base = Database("../Data/disease2.db", "info", ["country", "date", "disease", "dies"])
    world_base = Database("../Data/world.db", "info", ["date", "disease", "dies"])
    par = Parser()
    root = Tk()
    inf = par.get_info()
    ex = mainInterface(inf, disease_base, par)
    f = open("config.txt", "r")
    geom = f.read()
    f.close()
    root.geometry(geom)
    root.mainloop()


