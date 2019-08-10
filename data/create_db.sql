CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY ASC AUTOINCREMENT,
    user_name TEXT NOT NULL,
    user_password TEXT NOT NULL,
    user_nickname TEXT,
    user_email TEXT NOT NULL
);