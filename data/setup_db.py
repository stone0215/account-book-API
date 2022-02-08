import sqlite3

# import csv

# Read data
# with open('./members.csv', 'r', encoding='UTF-8', newline='') as f:
#     csv_reader = csv.DictReader(f)
#     members = [
#         (row['名字'], row['團體'])
#         for row in csv_reader
#     ]

# Create SQLite database


def create_db(app):
    with open(app.config["DB_SCHEEMA"], encoding="utf8") as db_scheema:
        create_db_sql = db_scheema.read()
    with open(app.config["INIT_DATA"], encoding="utf8") as init_data:
        init_data_sql = init_data.read()

    db = sqlite3.connect(app.config["DB_NAME"])  # , check_same_thread=False)
    with db:
        db.executescript(create_db_sql)
        db.commit()
        db.executescript(init_data_sql)

    db.commit()


# db.executemany(
#     'INSERT INTO  members (name, group_name) VALUES (?, ?)',
#     members
# )
