class NoCountryLink(Exception):
    """
    Класс ошибки
    """

    def __init__(self):
        self.message = "No country link in dictionary"
        super().__init__(self.message)
