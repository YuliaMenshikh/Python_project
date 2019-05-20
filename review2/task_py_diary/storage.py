import re
from datetime import date

from .decorators import with_connection


SQL_INSERT_GOAL = '''
    INSERT INTO diary (
        goal_name, goal_text, date_for_complete
    ) VALUES (
        ?, ?, ?
    )
'''

SQL_UPDATE = '''
    UPDATE diary SET {}=? WHERE id=?
'''


SQL_UPDATE_NAME = SQL_UPDATE.format('goal_name')
SQL_UPDATE_TEXT = SQL_UPDATE.format('goal_text')
SQL_UPDATE_DATE = SQL_UPDATE.format('date_for_complete')
SQL_UPDATE_STATUS = SQL_UPDATE.format('goal_status')


SQL_SELECT_ALL = '''
    SELECT
        id, goal_name, goal_text, date_for_complete, goal_status
    FROM
        diary
'''

SQL_SELECT_GOAL_BY_ID = SQL_SELECT_ALL + ' WHERE id=?'
SQL_SELECT_GOAL_BY_TIME = SQL_SELECT_ALL + ' WHERE date_for_complete=?'


@with_connection()
def initialize(conn, creation_schema):
    """Инициализирует базу данных"""
    with open(creation_schema) as f:
        conn.executescript(f.read())


@with_connection()
def add_goal(conn, goal_name, goal_text, goal_date):
    if not goal_name:
        raise RuntimeError('Имя задачи не может быть пустым.')

    if not goal_date:
        raise RuntimeError('Дата выполнения задачи не может быть пустой.')

    conn.execute(SQL_INSERT_GOAL, (goal_name, goal_text, goal_date))


@with_connection()
def redact_goal(conn, id, code):
    find_goal_by_id(id)

    code_rel = {'1' : SQL_UPDATE_NAME, '2' : SQL_UPDATE_TEXT, '3' : SQL_UPDATE_DATE}

    if code == '3':
        new = date(input('Дату вводить в формате ГГГГ-ММ-ДД'))
    else:
        new = input('Введите новую информацию: ')

    conn.execute(code_rel.get(code), (new, id))


@with_connection()
def find_all(conn):
    """Возвращает все задачи"""
    return conn.execute(SQL_SELECT_ALL).fetchall()


@with_connection()
def find_goal_by_id(conn, id):
    """Возвращает задачу по ID"""
    goal = conn.execute(SQL_SELECT_GOAL_BY_ID, (id,)).fetchone()
    if not goal:
        raise RuntimeError('Нет такой задачи')
    return goal


@with_connection()
def find_goals_by_date(conn, dt):
    """Возвращает задачи по опредлённой дате"""

    if not bool(re.match(r"\d{4}-[0-1]\d-[0-3]\d", dt)):
        print(dt)
        raise RuntimeError('Неверный формат даты')

    return conn.execute(SQL_SELECT_GOAL_BY_TIME, (dt,)).fetchall()


@with_connection()
def update_status(conn, id, flag):
    find_goal_by_id(id)
    msg = "Выполнено" if flag else "Не выполнено"
    conn.execute(SQL_UPDATE_STATUS, (msg, id))
