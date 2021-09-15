# type: ignore
from flask import Flask
from typing import Callable


class Widget:
    __app: Flask

    def __init__(self, app: Flask):
        self.__app = app

    def widget(self, name: str):
        def inner(func: Callable[..., str]):
            __app.add_template_global(func, name)
        return inner
