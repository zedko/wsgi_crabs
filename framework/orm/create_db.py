import sqlite3
from os import path, walk
from framework.wsgi import App

# db_path = path.join(App.settings.DATABASE_CONNECTION)
# print(path.exists(db_path))
# print(db_path)

# path for test only.
db_path = path.abspath(path.join('../', '../',))


migrations_path = path.join(db_path, 'migrations')


# apply migrations
def get_migrations_file_names(folder=migrations_path) -> list:
    """
    collects migration filenames from a folder
    :folder provide a path to folder with migrations
    :return list of full filenames (path+name)
    """
    dir_path, _, file_names = next(walk(folder))
    print(dir_path, file_names)
    migrations_file_names = [path.join(dir_path, file_name) for file_name in file_names]
    return migrations_file_names


def apply_migrations(cursor, migrations_list: list):
    """
    Executes migrations SQL commands
    """
    for migration in migrations_list:
        with open(migration, 'r') as f:
            sql_statement = f.read()
        cursor.executescript(sql_statement)


if __name__ == '__main__':
    db_name = 'db.sqlite'
    connection = sqlite3.connect(path.join(db_path, db_name))
    cursor_ = connection.cursor()
    apply_migrations(cursor_, get_migrations_file_names())
    connection.close()
