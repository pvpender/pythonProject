from Work.Library.standard_functions import *
from application_functions import *

if __name__ == "__main__":
    first_base = Database("../Data/test.db", "test", ["a", "b", "c"])
    disease_base = Database("../Data/disease.db", "info", ["country", "date", "disease", "dies"])
    par = Parser()
    print(par.get_info())
    print(par.get_country_info("Великобритания", disease_base))
