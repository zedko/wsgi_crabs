import pickle
from crabs_project.settings import LOGGER as log
from typing import Optional
from mods.PrototypeMixin import PrototypeMixin


# COURSES

class Course(PrototypeMixin):
    def __init__(self, title: str, desc: str = '', price: float = 0, image_url: str = '/static/images/breakfast-1.jpg'):
        self.title = title
        self.desc = desc
        self.price = price
        self.img = image_url

    def __repr__(self):
        return f'{self.title}'

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
        :param course_discount - represents a bulk % discount for each Course if you buy a Profession (20 = 20% discount)
        """
        self.title = title
        self.description = description
        self.courses_list = []
        self._course_discount = course_discount

    def __repr__(self):
        return f'{self.title}, courses: {self.courses_list}'

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
        self.name = name
        self.email = email

    @staticmethod
    def create_user(type_: str, *args, **kwargs):
        USERS = {
            'student': Student,
            'chef': Chef,
        }
        return USERS.get(type_)(*args, **kwargs)


class Student(User):
    def __init__(self, *args, **kwargs):
        super(Student, self).__init__(*args, **kwargs)
        self._bought_courses = set()

    def buy_course(self, course: Course):
        if course not in self._bought_courses:
            self._bought_courses.add(course)
            log.info(f"Course {course} successfully sold to {self.name}")
        else:
            log.info(f"Course {course} is already bought by student {self.name}")


class Chef(User):
    def __init__(self, *args, **kwargs):
        super(Chef, self).__init__(*args, **kwargs)
        self._authorized_courses = dict()

    def authorize_for_course(self, course: Course):
        if course.title not in self._authorized_courses.keys():
            self._authorized_courses[course.title] = course


# Class that contains current app state
class AppData:
    def __init__(self):
        try:
            self.load()
        except FileNotFoundError:
            self.courses = dict()
            self.professions = dict()
            self.users = dict()

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

    def save(self):
        with open(f'db/{self.__class__.__name__}.dump', 'wb') as f:
            pickle.dump(self, f)

    def load(self):
        with open(f'db/{self.__class__.__name__}.dump', 'rb') as f:
            restored: AppData = pickle.load(f)
            self.courses = restored.courses
            self.professions = restored.professions
            self.users = restored.users


if __name__ == '__main__':
    app = AppData()
    print(app)
    app.add_course('kitchen', 'SvetaFirst')
    app.add_course('kitchen', 'Gecond', price=50)
    course = app.add_course('online', 'third') or app.get_course('third')
    course2 = course.copy()

    prof = app.add_profession("Chefcooker") or app.get_profession("Chefcooker")
    prof.add_course(course)
    prof.add_course(course2)

    user = app.add_user("student", "Joe", "doe@mail.com") or app.get_user("doe@mail.com")
    user.buy_course(course)
    user.buy_course(course2)

    app.save()
