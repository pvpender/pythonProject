from Work.Library.standard_functions import *
from application_functions import *

if __name__ == "__main__":
    first_base = Database("../Data/test.db", "test", ["a", "b", "c"])
    par = Parser()
    print(par.get_info())