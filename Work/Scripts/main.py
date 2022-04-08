from Work.Library.standard_functions import *
from application_functions import *

if __name__ == "__main__":
    first_base = Database("../Data/test.db", "test", ["a", "b", "c"])
    second_base = Database("../Data/test.db", "test1", ["date", "desease", "dies"])
    par = Parser()
    print(par.get_info())
    print(par.get_country_info("Великобритания", second_base))
    print(second_base.find_data())
