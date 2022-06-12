class NoCountryLink(Exception):
    """
    Класс ошибки
    """

    def __init__(self):
        self.message = "No country link in dictionary"
        super().__init__(self.message)


class TooMoreRequests(Exception):
    """
    Класс ошибки
    """

    def __init__(self):
        self.message = "Too much requests please try again later"
        super().__init__(self.message)
