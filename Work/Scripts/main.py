from Work.Library.standard_functions import *
from application_functions import *

if __name__ == "__main__":
    first_base = Database("../Data/test.db", "test", ["a", "b", "c"])
    disease_base = Database("../Data/disease.db", "info", ["country", "date", "disease", "dies"])
    par = Parser()
    print(par.get_info())
    print(par.get_country_info("Великобритания", disease_base))
    print(par.get_country_info("Германия", disease_base))
    #disease_base.del_row([0, 1], ["Германия", "12-04-22"])
    print(disease_base.find_data([0], ["Германия"]))
