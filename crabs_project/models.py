import pickle
from crabs_project.settings import LOGGER as log
from crabs_project.settings import ROOT_DIR
from typing import Optional
from mods.PrototypeMixin import PrototypeMixin
from os import path


# COURSES

class Course(PrototypeMixin):
    def __init__(self, title: str, desc: str = '', price: float = 0, image_url: str = 'images/breakfast-1.jpg'):
        self.title = title
        self.description = desc
        self.price = price
        self.img = image_url

    # def __repr__(self):
    #     return f'{self.title}'

    @staticmethod
    def create_course(course_type, *args, **kwargs):
        COURSES = {
            'kitchen': KitchenCourse,
            'online': OnlineCourse
        }
        return COURSES.get(course_type)(*args, **kwargs)


class KitchenCourse(Course):
    def __init__(self, *args, **kwargs):
        super(KitchenCourse, self).__init__(*args, **kwargs)
        self.location = ''

    def set_location(self, location: str):
        self.location = location


class OnlineCourse(Course):
    def __init__(self, *args, **kwargs):
        super(OnlineCourse, self).__init__(*args, **kwargs)
        self.url = ''

    def set_url(self, url: str):
        self.url = url


# PROFESSIONS
class Profession:
    def __init__(self, title: str, description: str = '', course_discount: float = 20):
        """
        Notice! This class is iterable. You can loop through courses added
        :param course_discount - represents a bulk % discount for each Course if you buy a Profession (20 = 20% discount)
        """
        self.title = title
        self.description = description
        self.courses_list = []
        self.__iterator_cursor = 0
        self._course_discount = course_discount

    def __repr__(self):
        return f'{self.title}, courses: {self.courses_list}'

    def __iter__(self):
        return self

    def __next__(self):
        while self.__iterator_cursor < len(self.courses_list):
            rv = self.courses_list[self.__iterator_cursor]
            self.__iterator_cursor += 1
            return rv
        else:
            raise StopIteration

    def add_course(self, course: Course):
        if course.title not in (item.title for item in self.courses_list):
            try:
                self.courses_list.append(course)
            except KeyError:
                log.warning(f"The course with id {course} do not exist")
        else:
            log.info(f'Tried to add course {course.title} duplicate to a profession {self.title}')

    def get_price(self):
        """
        Calculates price of Profession based on Courses included and basic_discount
        """
        price = sum(course.price for course in self.courses_list)
        price = price - (price * self._course_discount / 100)
        return round(price, 2)


# USERS
class User:
    def __init__(self, name, email):
        self.id: int
        self.name = name
        self.email = email
        self.role = None
        self.active: bool = False
        self.courses: set = set()

    @staticmethod
    def create_user(type_: str, *args, **kwargs):
        """
        Users Fabric. Provide 'type', 'name', 'email' -> get new subclass User
        """
        USERS = {
            'student': Student,
            'chef': Chef,
        }
        return USERS.get(type_)(*args, **kwargs)


class Student(User):
    def __init__(self, *args, **kwargs):
        super(Student, self).__init__(*args, **kwargs)
        self.role = 'student'

    def buy_course(self, course: Course):
        if course not in self.courses:
            self.courses.add(course)
            log.info(f"Course {course} successfully sold to {self.name}")
        else:
            log.info(f"Course {course} is already bought by student {self.name}")


class Chef(User):
    def __init__(self, *args, **kwargs):
        super(Chef, self).__init__(*args, **kwargs)
        self.role = 'chef'

    def authorize_for_course(self, course: Course):
        if course not in self.courses:
            self.courses.add(course)
            log.info(f"Course {course} successfully authorized to {self.name}")
        else:
            log.info(f"Course {course} is already authorized by chef {self.name}")


# Class that contains current app state
class AppData:
    def __init__(self):
        self._dump_file = path.join(ROOT_DIR, 'crabs_project', 'db', f'{self.__class__.__name__}.dump')
        self.courses = dict()
        self.professions = dict()
        self.users = dict()

        # self.load()

    def get_context_data(self, *args: str) -> dict:
        """
        provide a name of attributes as *args and get needed attribute;
        example: args = ('courses', 'professions').
        return would be {'courses': self.courses, 'professions': self.professions}
        """
        context = {}
        for arg in args:
            val = getattr(self, arg, None)
            if val:
                context[arg] = val
        return context

    def __repr__(self):
        string = f'{"=" * 20} \n' \
                 f'All courses: {self.courses} \n' \
                 f'All professions: {self.professions} \n' \
                 f'All users: {self.users} \n' \
                 f'{"=" * 20} \n'
        return string

    def add_course(self, type_: str, title: str, *args, **kwargs) -> Optional[Course]:
        if title not in self.courses.keys():
            course = (Course.create_course(type_, title, *args, **kwargs))
            self.courses[title] = course
            return course

    def get_course(self, title: str) -> Optional[Course]:
        return self.courses.get(title)

    def add_profession(self, title: str, *args, **kwargs) -> Optional[Profession]:
        if title not in self.professions.keys():
            profession = Profession(title, *args, **kwargs)
            self.professions[title] = profession
            return profession

    def get_profession(self, title: str) -> Optional[Profession]:
        return self.professions.get(title)

    def add_user(self, type_: str, name: str, email: str):
        if email not in self.users.keys():
            user = User.create_user(type_, name, email)
            self.users[email] = user
            return user

    def get_user(self, email: str) -> Optional[User]:
        return self.users.get(email)

    def get_active_user(self) -> Optional[User]:
        for user in self.users.values():
            if user.active:
                return user

    def set_active_user(self, user: User) -> User:
        for user_ in self.users.values():
            user_.active = False
        user.active = True
        return user

    def set_active_user_by_email(self, email: str) -> User:
        user = self.get_user(email)
        return self.set_active_user(user)

    def save(self):
        log.info(f'Trying to save to {self._dump_file}')
        with open(self._dump_file, 'wb') as f:
            try:
                pickle.dump(self, f)
                log.info(f'Save succeed')
            except PermissionError as e:
                log.warning(e)

    def load(self):
        log.info(f'Trying to load from {self._dump_file}')
        try:
            with open(self._dump_file, 'rb') as f:
                restored: AppData = pickle.load(f)
                self.__dict__ = restored.__dict__
                log.info(f'Load succeed')
        except FileNotFoundError:
            log.info(f'AppData.dump was not found. Creating empty data object')

    def set_test_data(self):
        course = self.add_course('kitchen', 'test course 1', price=95.5, desc="A simple kitchen course") or \
                 self.get_course('test course 1')
        course2 = self.add_course('kitchen', 'test course 2', price=15.7) or \
                 self.get_course('test course 2')
        course3 = self.add_course('online', 'online course 1', price=19) or \
                 self.get_course('online course 1')
        course4 = self.add_course('kitchen', 'test course 3', price=795.5, desc="A simple kitchen course") or \
                 self.get_course('test course 3')

        prof = self.add_profession('Povarenok') or self.get_profession('Povarenok')
        prof.add_course(course)
        prof.add_course(course2)

        prof2 = self.add_profession('Online coulinar') or self.get_profession('Online coulinar')
        prof2.add_course(course3)

        user = self.add_user("student", "Joe", "doe@mail.com") or app.get_user("doe@mail.com")
        user.active = True
        user.buy_course(course)
        user.buy_course(course2)


if __name__ == '__main__':
    app = AppData()
    # app.load()
    print(app)

    app.set_test_data()

    a = app.get_profession('Povarenok')
    for course_ in a:
        print(course_)

    app.save()
