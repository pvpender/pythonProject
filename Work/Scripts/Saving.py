import pandas as pd
import numpy as np


class Saver:
    """
    Класс сохранителя отчётов
    """
    __world_text_path = "../Output/world.csv"
    __countries_text_path = "../Output/"

    def __init__(self):
        pass

    def save_world_data(self, data: dict):
        """
        Сохранение таблицы заражений и смертей по миру
        :param data: словарь с данными о заражениях и смертях по миру
        :return: pd.DataFrame
        author Moiseev Nicolay
        """
        df = pd.DataFrame(data)
        df = df.set_axis(["disease", "dies"], axis="index")
        df.to_csv(self.__world_text_path)
        return df

    def save_country_data(self, country_name: str, data: list):
        """
        Сохранение таблицы заражений и смертей для отдельной страны
        :param country_name: Название страны для которой даётся статистика
        :param data: Список списков вида [[Дата, Заражения, Смерти], ...]
        :return: pd.DataFrame
        """
        df = pd.DataFrame(data)
        df = df.set_axis(["Date", "Disease", "Dies"], axis="columns")
        df.to_csv(self.__countries_text_path + country_name + ".csv")
        return df

    def unite_data(self, list_columns: list, list_data: list, list_names: list):
        """
        Сохранение объединённой таблицы заражений и смертей
        :param list_columns:
        :param list_data: Список списков вида [[[Дата, Заражения, Смерти], ...], [[Дата, Заражения, Смерти], ...] ...]
        :param list_names: Список названий стран для которых даётся статистика
        :return: pd.DataFrame
        """
        mas = []
        for i in list_data:
            df = pd.DataFrame(i)
            df = df.set_axis(["Date"] + list_columns, axis="columns")
            mas.append(df)
        df = pd.concat(mas, keys=list_names, names=["Country"])
        df.to_csv(self.__countries_text_path + f"unite_{[i for i in list_columns]}_{[i for i in list_names]}.csv")
        return df

    def mean_unite_data(self, dataframe: pd.DataFrame):
        """
        Сохранение сводной таблицы данных
        :param dataframe: Объединённая таблица pd.DataFrame с данными
        :return: pd.DataFrame
        """
        dataframe = dataframe.astype({"Disease": "int64", "Dies": "int64"})
        df = pd.pivot_table(dataframe, values=["Disease", "Dies"],
                            index="Date", aggfunc={"Disease": np.mean, "Dies": np.mean})
        df.to_csv(self.__countries_text_path + "mean_unite.csv")
        return df
