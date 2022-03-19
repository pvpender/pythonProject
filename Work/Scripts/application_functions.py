import tkinter as tk
from bs4 import BeautifulSoup
import requests as req


class MainWindow:
    def __init__(self):
        pass


class Parser:
    """
    Класс парсера данных
    """

    def __init__(self):
        self.__page = req.get(self.__url, headers=self.__headers)

    __url = "https://gogov.ru/covid-19/world"
    __page = req.Response
    __headers = {
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36 OPR/40.0.2308.81',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'DNT': '1',
        'Accept-Encoding': 'gzip, deflate, lzma, sdch',
        'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.6,en;q=0.4'
    }

    @staticmethod
    def __none_testing(string: str):
        """
        Функция проверки строку на пустоту
        :param string: Строка
        :return: Саму строку или "0"
        author Moiseev Nicolay
        """
        if string == "":
            return "0"
        else:
            return string

    def get_info(self) -> dict:
        """Функция получения чего-то
        :return: Словарь
        author Moiseev Nicolay
        """
        soup = BeautifulSoup(self.__page.text, "lxml")
        mas = list(map(str, soup.tbody.text.split("\n")))[2:]
        output_dict = {}
        for i in range(0, len(mas), 16):
            output_dict.update({mas[i]: [self.__none_testing(mas[i + 2][1:]), self.__none_testing(mas[i + 7][1:])]})
        return output_dict

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
            output_dict.update({mas[i]: self.__none_testing(mas[i + 2][1:])})
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
            output_dict.update({mas[i]: self.__none_testing(mas[i + 7][1:])})
        return output_dict
