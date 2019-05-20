CREATE TABLE IF NOT EXISTS diary (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    goal_name TEXT NOT NULL,
    goal_text TEXT NOT NULL DEFAULT "",
    date_for_complete DATE NOT NULL,
    goal_status TEXT NOT NULL DEFAULT "Не выполнено"
)
