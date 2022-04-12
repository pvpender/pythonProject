import tkinter as tk
import numpy as np
import re
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from Work.Library.standard_functions import Database
import requests as req


class MainWindow:
    def __init__(self):
        pass


class NoCountryLink(Exception):
    def __init__(self):
        self.message = "No country link in dictionary"
        super().__init__(self.message)


class Parser:
    """
    Класс парсера данных
    """

    def __init__(self):
        self.__page = req.get(self.__url, headers=self.__headers)
        soup = BeautifulSoup(self.__page.text, "lxml")
        country_names = [tag.find("a").text for tag in soup.select("td:has(a)") if
                         tag.find("a")["href"].count("covid-19")]
        country_links = [tag.find("a")["href"] for tag in soup.select("td:has(a)") if
                         tag.find("a")["href"].count("covid-19")]
        for i in range(len(country_names)):
            self.__links.update({country_names[i]: country_links[i]})

    __url = "https://gogov.ru/covid-19/world"
    __page = req.Response
    __links = {}
    __headers = {
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/53.0.2785.116 Safari/537.36 OPR/40.0.2308.81',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'DNT': '1',
        'Accept-Encoding': 'gzip, deflate, lzma, sdch',
        'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.6,en;q=0.4'
    }

    @staticmethod
    def __none_testing(string: re.Match) -> str:
        """
        Функция проверки строку на пустоту
        :param string: объект класса re.Match
        :return: Саму строку или "0"
        author Moiseev Nicolay
        """
        if string is None:
            return "0"
        else:
            return string.group(0)

    def get_info(self) -> dict:
        """Функция получения чего-то
        :return: Словарь
        author Moiseev Nicolay
        """
        soup = BeautifulSoup(self.__page.text, "lxml")
        mas = list(map(str, soup.tbody.text.split("\n")))[2:]
        output_dict = {}
        for i in range(0, len(mas), 16):
            output_dict.update({mas[i]: [self.__none_testing(re.search(r"\d+", mas[i + 2])),
                                         self.__none_testing(re.search(r"\d+", mas[i + 7]))]})
        return output_dict

    def get_country_info(self, name: str, database: Database) -> list:
        """
        Функция получения подробной информации по стране
        :param name:
        :param database:
        :return:
        author Moiseev Nicolay
        """
        if name in self.__links:
            if not database.find_data([0, 1], [name, str(datetime.now() - timedelta(days=1))[8:10].replace("-", ".") + "." +
                                            str(datetime.now() - timedelta(days=1))[5:7].replace("-", ".") + "." +
                                            str(datetime.now() - timedelta(days=1))[2:4].replace("-", ".")]):
                page = req.get(self.__links[name], headers=self.__headers)
                soup = BeautifulSoup(page.text, "lxml")
                mas = soup.table.find_all("td")
                data = []
                data_base = []
                for i in range(0, len(mas), 4):
                    data.append([re.search(r"[0-9]+\.[0-9]+\.[0-9]+", str(mas[i])).group(0),
                                int(re.search(r"[\d+\s]+", str(mas[i+1])).group(0).replace(" ", "")),
                                int(re.search(r"[\d+\s]+", str(mas[i+2])).group(0).replace(" ", ""))])
                    data_base.append([name, re.search(r"[0-9]+\.[0-9]+\.[0-9]+", str(mas[i])).group(0),
                                int(re.search(r"[\d+\s]+", str(mas[i+1])).group(0).replace(" ", "")),
                                int(re.search(r"[\d+\s]+", str(mas[i+2])).group(0).replace(" ", ""))])
                database.insert_rows(data_base)
            else:
                r = database.find_data([0], [name])
                data_np = np.array(r)
                data = data_np[0:, 1:].tolist()
            return data
        else:
            raise NoCountryLink

    def get_info_new_disease(self) -> dict:
        """
        Функция получения количества новых заражений
        :return: Словарь вида {Страна : количество}
        author Moiseev Nicolay
        """
        soup = BeautifulSoup(self.__page.text, "lxml")
        mas = list(map(str, soup.tbody.text.split("\n")))[2:]
        output_dict = {}
        for i in range(0, len(mas), 16):
            output_dict.update({mas[i]: self.__none_testing(re.search(r"\d+", mas[i + 2]))})
        return output_dict

    def get_info_new_dies(self) -> dict:
        """
        Функция получения количества новых смертей
        :return: Словарь вида {Страна : количество}
        author Moiseev Nicolay
        """
        soup = BeautifulSoup(self.__page.text, "lxml")
        mas = list(map(str, soup.tbody.text.split("\n")))[2:]
        output_dict = {}
        for i in range(0, len(mas), 16):
            output_dict.update({mas[i]: self.__none_testing(re.search(r"\d+", mas[i + 7][1:]))})
        return output_dict
