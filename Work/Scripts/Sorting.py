from datetime import datetime


class Sorter:
    """
    Клас сортировщика
    """

    @staticmethod
    def sorting(table: int, data: list):
        """
        Сортировка количества заболеваний/смертей по дате
        :param table: Номер столбца в котором находятся даты
        :param data: Массив данных
        :return: Отсортированный массив данных
        author Moiseev Nicolay
        """
        return sorted(data, key=lambda x: datetime.strptime(x[table], "%d.%m.%y"), reverse=True)

    @staticmethod
    def old_sorting(table: int, data: list):
        """
        Сортировка количества заболеваний/смертей по дате
        :param table: Номер столбца в котором находятся даты
        :param data: Массив данных
        :return: Отсортированный массив данных
        author Moiseev Nicolay
        """
        time = datetime.now()
        p = (time - datetime.strptime(data[0][table], "%d.%m.%y")).days
        i = p
        while (i != 0) & (i > 0):
            if (time - datetime.strptime(data[len(data) - abs(i)][table], "%d.%m.%y")).days < p:
                new_data = data[len(data) - i:] + data[:len(data) - i]
                break
            i -= 1
        else:
            new_data = data
        return new_data
