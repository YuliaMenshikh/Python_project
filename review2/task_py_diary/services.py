from collections import namedtuple, OrderedDict
import pkg_resources
from configparser import ConfigParser
import os
import sqlite3
import shutil

from appdirs import AppDirs


app_dirs = AppDirs(__package__)

for path in (app_dirs.user_config_dir, app_dirs.user_data_dir):
    if not os.path.exists(path):
        os.makedirs(path, 0o755)


def make_config(*config_files):
    """
    Читает конфигурационный файл и возвращает объект ConfigParser.
    """
    config = ConfigParser()
    config.read(config_files)
    return config


def make_default_config():
    """Читает конфигурационный файл по умолчанию"""
    filename = os.path.join(
        app_dirs.user_config_dir, 'config.ini'
    )

    if not os.path.exists(filename):
        default = pkg_resources.resource_filename(
            __name__, 'resources/config.ini'
        )
        shutil.copyfile(default, filename)

    return make_config(filename)


config = make_default_config()


def dict_factory(cursor, row):
    d = {}
    for column, data in zip(cursor.description, row):
        d[column[0]] = data
    return d


def make_connection(name='db'):
    """
    Возвращает объект-подключение к БД SQLite
    """
    db_name = os.path.join(
        app_dirs.user_data_dir,
        config.get(name, 'db_name')
    )

    conn = sqlite3.connect(db_name)
    conn.row_factory = dict_factory
    return conn


def make_menu():
    """
    Создает меню и возвращает кортеж из двух элементов:
    1. декоратор
    2. обработчик ввода команды
    """

    Action = namedtuple('Action', ('func', 'title'))
    actions = OrderedDict()

    def action(cmd, title=None):
        def decorator(func):
            nonlocal title

            if title is None:
                title = str(func.__doc__).strip().splitlines().pop(0)

            actions[str(cmd)] = Action(func, title)

            return func
        return decorator


    def action_default():
        print('Не известная команда')

    action_default = Action(action_default, '')

    def handler(cmd_name):
        action = actions.get(cmd_name, action_default)
        action.func()

    @action('m', 'Показать меню')
    def show_menu():
        for cmd, action in sorted(actions.items()):
            print('{}. {}'.format(cmd, action.title))

    return action, handler
