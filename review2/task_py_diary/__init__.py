import datetime
import os
import pkg_resources
import re
import sys
import textwrap


from terminaltables import AsciiTable


from . import storage
from .services import make_menu


main_menu, main_menu_handler = make_menu()


@main_menu(1)
def action_add():
    """Добавить задачу"""
    goal_name = input('\nВведите название задачи: ')
    goal_text = input('\nВведите информацию о задаче: ')
    goal_date = input('\nВведите дату выполнения задачи в формате ГГГГ-ММ-ДД: ')
    if not bool(re.match(r"\d{4}-[01]\d-[0-3]\d", goal_date)):
        raise RuntimeError('Неверный формат даты')
    #goal_date = datetime.date(*[int(i) for i in goal_date.split('-')])
    storage.add_goal(goal_name, goal_text, goal_date)
    print('Задча успешно добавлена!')


@main_menu(2)
def acion_redact_goal():
    """Изменить задчу"""
    id = int(input('Введите id задачи: '))
    print(textwrap.dedent('''
    \nОтредактировать:
    1. Название задачи
    2. Описание задачи
    3. Дату выполнения задачи
    '''))
    code = input('Введите команду: ')
    storage.redact_goal(id, code)
    print('Задача успешно изменена!')


@main_menu(3)
def acion_complete():
    """Завершить задачу"""
    id = input('Введите id задачи: ')
    storage.update_status(id, 1)
    print('Задача успешно завершена!')


@main_menu(4)
def acion_uncomplete():
    """Начать задачу сначала """
    id = input('Введите id задачи: ')
    storage.update_status(id, 0)
    if input('Задача начата повторно, изменить время выполнения? Д/н: ') in ('Д', ''):
        storage.redact_goal(id, '3')
        print('Дата успешно изменена!')


@main_menu(5)#сделать ещё один поиск
def action_find_all():
    """Вывести задачи"""

    print(textwrap.dedent('''
    \nВывести:
    1. Все задачи
    2. Задачи на опредлённое число
    3. Задачи на сегодня
    '''))
    code = input('Введите команду: ')

    if code == '2':
        dt = input('Введите дату выполнения задачи в формате ГГГГ-ММ-ДД: ')

    code_rel = {'1' : storage.find_all(),
                '2' : storage.find_goals_by_date(dt),
                '3' : storage.find_goals_by_date(str(datetime.date.today()))}
    goals = code_rel.get(code)
    data = [
        ['ID', 'Имя', 'Описание', 'Дата завершения', 'Статус'],
    ]

    for goal in goals:
        data.append([
            goal['id'],
            goal['goal_name'],
            goal['goal_text'],
            goal['date_for_complete'],
            goal['goal_status']
        ])


    table = AsciiTable(data)
    print(table.table)


@main_menu('e')
def action_exit():
    """Выйти"""
    sys.exit(0)


def main():
    creation_schema = pkg_resources.resource_filename(
        __name__,
        'resources/schema.sql'
    )

    storage.initialize(creation_schema)

    main_menu_handler('m')

    while 1:
        cmd = input('\nВведите команду: ')
        main_menu_handler(cmd)
