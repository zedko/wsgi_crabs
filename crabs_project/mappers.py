import sqlite3
from crabs_project.models import User
from crabs_project.settings import DATABASE_CONNECT

connection_ = sqlite3.connect(DATABASE_CONNECT)


# Exceptions
class DbFindException(Exception):
    def __init__(self, message):
        super().__init__(f'Record not found {message}')


class DbCommitException(Exception):
    def __init__(self, message):
        super().__init__(f'Commit error {message}')


class DbUpdateException(Exception):
    def __init__(self, message):
        super().__init__(f'Update error {message}')


class DbDeleteException(Exception):
    def __init__(self, message):
        super().__init__(f'Delete error {message}')


# mappers
class UserMapper:
    def __init__(self, connection):
        self.connection = connection
        self.connection.row_factory = sqlite3.Row
        self.cursor = connection.cursor()
        self.table_name = "users"

    def get_all(self) -> list:
        """
        Fetching all users and creates model instances
        """
        sql = f'SELECT * FROM {self.table_name}'
        self.cursor.execute(sql)
        result = []
        for item in self.cursor.fetchall():
            id_, name, email, role = tuple(item)
            user = User.create_user(role, name, email)
            user.id = id_
            result.append(user)
        return result

    def find_by_id(self, user_id):
        """
        Finds and returns user by id or raises exception
        """
        sql = f"SELECT * FROM {self.table_name} WHERE id=?"
        self.cursor.execute(sql, (user_id,))
        result = self.cursor.fetchone()
        if not result:
            raise DbFindException(f'Cant find user with id {user_id}')
        user: User = User.create_user(result['role'], result['name'], result['email'])
        user.id = result['id']
        return user

    def insert(self, obj: User):
        """
        Inserts a new User object into database
        """
        sql = f"INSERT INTO {self.table_name} (name, email, role) VALUES (?, ?, ?)"
        val = (obj.name, obj.email, obj.role)
        self.cursor.execute(sql, val)
        try:
            self.connection.commit()
        except Exception as e:
            raise DbCommitException(e.args)

    def update(self, obj: User):
        """
            Updates database to User object state
        """
        sql = f"UPDATE {self.table_name} " \
              f"SET name = ?, email = ?, role = ? " \
              f"WHERE id = ?"
        val = (obj.name, obj.email, obj.role, obj.id)
        self.cursor.execute(sql, val)
        try:
            self.connection.commit()
        except Exception as e:
            raise DbUpdateException(e.args)

    def delete(self, obj: User):
        sql = f"DELETE FROM {self.table_name} WHERE id=?"
        val = (obj.id,)
        self.cursor.execute(sql, val)
        try:
            self.connection.commit()
        except Exception as e:
            raise DbDeleteException(e.args)


if __name__ == '__main__':

    mapper = UserMapper(connection_)

    # add user
    test_user = User.create_user('student', 'John', 'john@johnys.com')
    mapper.insert(test_user)

    # update user
    to_change: User = mapper.find_by_id('1')
    print(to_change.__dict__)
    to_change.name = "Bobby"
    mapper.update(to_change)

    # select *
    a = mapper.get_all()
    [print(_.__dict__) for _ in a]

    # delete user
    mapper.delete(a[1])
    a = mapper.get_all()
    [print(_.__dict__) for _ in a]

    print('done')
