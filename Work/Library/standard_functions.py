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
        request = f"CREATE TABLE IF NOT EXISTS {self.__name}("
        for i in self.__columns:
            request += f"{i},"
        request = request[0:-1] + ")"
        self.__cursor.execute(request)

    def insert_row(self):
        pass

    def del_row(self):
        pass

    def find_data(self):
        pass
