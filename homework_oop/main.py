from functools import total_ordering


def avg_grade_homework(students: list, course_name: str):
    temp_sum = 0
    temp_avg = 0
    for student in students:
        if not isinstance(student, Student):
            return 'Ошибка'
    else:
        for student in students:
            if course_name in student.grades:
                temp_sum += sum(student.grades.get(course_name))
                temp_avg += len(student.grades.get(course_name))
        return temp_sum / temp_avg


def avg_grade_lector(lectors: list, course_name: str):
    temp_sum = 0
    temp_avg = 0
    for lector in lectors:
        if not isinstance(lector, Lecturer):
            return 'Ошибка'
    else:
        for lector in lectors:
            if course_name in lector.grades:
                temp_sum += sum(lector.grades.get(course_name))
                temp_avg += len(lector.grades.get(course_name))
        return temp_sum / temp_avg

# мне кажется функцию создать правилньей чем метод, но по-похорему нужно создать ещё один класс стоящий над Mentor
# где будут объеденены какие-то похожие действия пользователей
def avg_rating(self):
    if hasattr(self, 'grades') and len(self.grades) > 0:
        temp_sum = 0
        temp_count = 0
        for value in self.grades.values():
            temp_sum += sum(value)
            temp_count += len(value)
        return temp_sum / temp_count
    else:
        return 'ошибка'


class Mentor:
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.courses_attached = []

    def __str__(self):
        res = f'Имя: {self.name}\nФамилия: {self.surname}'
        return res


@total_ordering
class Lecturer(Mentor):  # Лекторы
    def __init__(self, name, surname):
        super().__init__(name, surname)
        self.grades = {}

    def __str__(self):
        res = f'{super().__str__()}\nСредняя оценка за лекции: {avg_rating(self)}'
        return res

    def __eq__(self, other):
        if isinstance(self, Lecturer) and isinstance(other, Lecturer):
            return avg_rating(self) == avg_rating(other)
        else:
            return 'Вы сравниваете разные объекты'

    def __lt__(self, other):
        if isinstance(self, Lecturer) and isinstance(other, Lecturer):
            return avg_rating(self) < avg_rating(other)
        else:
            return 'Вы сравниваете разные объекты'


class Reviewer(Mentor):  # Эксперты, проверяющие домашние задания
    def rate_hw(self, student, course, grade):
        if isinstance(student,
                      Student) and course in self.courses_attached and course in student.courses_in_progress and 10 >= grade >= 0:
            if course in student.grades:
                student.grades[course] += [grade]
            else:
                student.grades[course] = [grade]
        else:
            return 'Ошибка'

    def __str__(self):
        res = super().__str__()
        return res


@total_ordering
class Student:
    def __init__(self, name, surname, gender):
        self.name = name
        self.surname = surname
        self.gender = gender
        self.finished_courses = []
        self.courses_in_progress = []
        self.grades = {}

    def rate_lector(self, lector, course, grade):
        if isinstance(lector,
                      Lecturer) and course in self.courses_in_progress and course in lector.courses_attached and 10 >= grade >= 0:
            if course in lector.grades:
                lector.grades[course] += [grade]
            else:
                lector.grades[course] = [grade]
        else:
            return 'Ошибка'

    def __str__(self):
        # скорее всего неправильно с точки зрения ООП вызывать от Student метод __str__ класса Mentor, по идее нужен ещё один класс стоящий над ними обоими в котором
        # были бы общие черты вообще всех пользователей и там бы выводились имена и фамилил, но в рамках этой программы просто покажем, что так можно
        res = f'{Mentor.__str__(self)}\nСредняя оценка за домашние задания: {avg_rating(self)}\nКурсы в процессе изучения: {self.courses_in_progress}\nЗавершённые курсы: {self.finished_courses}'
        return res

    def __eq__(self, other):
        if isinstance(self, Student) and isinstance(other, Student):
            return avg_rating(self) == avg_rating(other)
        else:
            return 'Вы сравниваете разные объекты'

    def __lt__(self, other):
        if isinstance(self, Student) and isinstance(other, Student):
            return avg_rating(self) < avg_rating(other)
        else:
            return 'Вы сравниваете разные объекты'


mentor1 = Mentor('mentor', 'one')
mentor2 = Mentor('mentor', 'two')

print(mentor1)
print()
print(mentor2)

lecturer1 = Lecturer('lecturer', 'one')
lecturer2 = Lecturer('lecturer', 'two')
lecturer1.courses_attached += ['Python']
lecturer2.courses_attached += ['Java', 'Python']

reviewer1 = Reviewer('reviewer', 'one')
reviewer2 = Reviewer('reviewer', 'two')
reviewer1.courses_attached += ['Python']
reviewer2.courses_attached += ['Java', 'Python']

student1 = Student('student', 'one', 'man')
student2 = Student('student', 'two', 'woman')
student1.courses_in_progress += ['Python']
student2.courses_in_progress += ['Java', 'Python']

student1.rate_lector(lecturer1, 'Python', 10)
student1.rate_lector(lecturer1, 'Python', 2)
student2.rate_lector(lecturer1, 'Java', 9)  # оценка не добавится так как лектор1 не ведёт курсы Java
student2.rate_lector(lecturer1, 'Python', 0)

student2.rate_lector(lecturer2, 'Java', 9)
student2.rate_lector(lecturer2, 'Python', 9)

print(lecturer1, end='\n\n')
print(lecturer2, end='\n\n')
print(lecturer1 > lecturer2, lecturer2 > lecturer1, lecturer1 == lecturer2, end='\n\n')

reviewer1.rate_hw(student1, 'Python', 10)
reviewer1.rate_hw(student1, 'Python', 9)
reviewer1.rate_hw(student1, 'Python', 9)

reviewer2.rate_hw(student2, 'Java', 9)
reviewer2.rate_hw(student2, 'Python', 1)

print(student1, end='\n\n')
print(student2, end='\n\n')
print(student1 > student2, student2 > student1, student1 == student2, end='\n\n')

# print(student1.grades, student2.grades)
# print(avg_grade_homework([student1, student2], 'Python'))

# print(lecturer1.grades, lecturer2.grades)
# print(avg_grade_lector([lecturer1, lecturer2], 'Java'))
