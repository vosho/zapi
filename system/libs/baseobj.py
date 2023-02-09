class BaseObj:
    def __init__(self, dct):
        self.__dict__.update(dct)

    def __getattr__(self, item):
        if item in self.__dict__:
            return self.__dict__[item]