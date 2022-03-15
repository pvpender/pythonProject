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

    def insert_row(self, mas):
        """
        Добавление строки в базу
        :return: None
        author Moiseev Nicolay
        """
        request = f"INSERT INTO {self.__name} {tuple(i for i in self.__columns)} VALUES {tuple(i for i in mas)}"
        self.__cursor.execute(request)
        self.__connection.commit()

    def del_row(self):
        pass

    def find_data(self):
        pass
