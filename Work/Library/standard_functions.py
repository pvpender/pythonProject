import sqlite3


class Database:
    """
    Класс в котором реализуется работа с БД
    """
    __connection = sqlite3.Connection
    __name = ""
    __cursor = sqlite3.Cursor
    __columns = []

    def __init__(self, path: str, table_name: str, columns: list):
        """
        Инициализация базы данных
        :param path(Str): Путь к файлу с базой данных
        :param table_name(Str): Имя таблицы в базе
        :param columns(List of Str): Список столбцов
        :return None
        author Moiseev Nicolay
        """
        self.__connection = sqlite3.connect(path)
        self.__cursor = self.__connection.cursor()
        self.__name = table_name
        self.__columns = columns
        self.create_table()

    def create_table(self):
        """
        Создание базы, если её не существует
        :return: None
        author Moiseev Nicolay
        """
        request = f"CREATE TABLE IF NOT EXISTS {self.__name} {tuple(i for i in self.__columns)}"
        self.__cursor.execute(request)

    def insert_row(self, mas: list):
        """
        Добавление строки в базу
        :param mas (List)
        :return: None
        author Moiseev Nicolay
        """
        request = f"INSERT INTO {self.__name} {tuple(i for i in self.__columns)} VALUES {tuple(i for i in mas)}"
        self.__cursor.execute(request)
        self.__connection.commit()

    def insert_rows(self, mas: list):
        """
        Добавление строки в базу
        :param mas (List)
        :return: None
        author Moiseev Nicolay
        """
        request = f"INSERT INTO {self.__name} {tuple(j for j in self.__columns)} VALUES "
        for i in range(len(mas) - 1):
            request += f"{tuple(j for j in mas[i])}, "
        request += f"{tuple(mas[len(mas)-1])}"
        self.__cursor.execute(request)
        self.__connection.commit()

    def del_row(self, table_rows: list, mas: list):
        """
        Удаление строки из базы
        :param table_rows: Массив номеров столбцов которые проверяются
        :param mas: Массив значений по которым рсуществляется проверка
        :return: None
        author Moiseev Nicolay
        """
        request = f"DELETE FROM {self.__name} WHERE "
        for i in range(len(table_rows) - 1):
            request += f"{self.__columns[table_rows[i]]} = {mas[i]} AND"
        request += f" {self.__columns[table_rows[len(table_rows) - 1]]} = '{mas[len(mas) - 1]}'"
        self.__cursor.execute(request)
        self.__connection.commit()

    def find_data(self, table_rows: list = None, mas: list = None) -> list:
        """
        Поиск строк в базе
        :param table_rows:
        :param mas:
        :return: Список столбцов с их значениями
        author Moiseev Nicolay
        """
        if (table_rows is None) & (mas is None):
            request = f"SELECT * FROM {self.__name}"
        else:
            request = f"SELECT * FROM {self.__name} WHERE "
            for i in range(len(table_rows) - 1):
                request += f"{self.__columns[table_rows[i]]} = '{mas[i]}' AND"
            request += f" {self.__columns[table_rows[len(table_rows) - 1]]} = '{mas[len(mas) - 1]}'"
        self.__cursor.execute(request)
        data = self.__cursor.fetchall()
        return data
