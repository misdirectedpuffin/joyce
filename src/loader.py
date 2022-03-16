import csv
from itertools import groupby

from extensions import db
from models.model import (
    Class,
    Course,
    CoursesClasses,
    Grade,
    Level,
    LevelsCourses,
    Student,
    StudentsClasses,
    StudentsCourses,
)


class Name:
    def __init__(self, instr: str) -> None:
        self.instr = instr
        parts = self.instr.split(" ")
        if len(parts) <= 1:
            raise ValueError("Invalid name")
        fname, middle, lname = parts[0], parts[1:-1], parts[-1]
        self.first = fname
        self.last = lname
        if any(middle):
            bits = [m.strip() for m in middle]
            self.middle = " ".join(bits)
        else:
            self.middle = None

    def fullname(self):
        if self.middle:
            fullname = " ".join([self.first, self.middle, self.last])
        else:
            fullname = " ".join([self.first, self.last])
        return fullname


class Row:

    def __init__(self, item):
        self.item = item

    @property
    def fullname(self):
        middle = self.item.get("middlename")
        if not middle:
            fullname = " ".join([self.item['forename'], self.item['surname']])
        else:
            fullname = " ".join([self.item['forename'], middle, self.item['surname']])
        if fullname is None:
            return ""
        return fullname

    @property
    def level(self):
        level = self.item.get("level", "")
        if level is None:
            return ""
        return level

    @property
    def code(self):
        code = self.item.get("code", "")
        if code is None:
            return ""
        return code

    @property
    def course_name(self):
        course_name = self.item.get("course_name", "")
        if course_name is None:
            return ""
        return course_name

    @property
    def forename(self):
        forename = self.item.get("forename", "")
        if forename is None:
            return ""
        return forename

    @property
    def middlename(self):
        middlename = self.item.get("middlename", "")
        if middlename is None:
            return ""
        return middlename

    @property
    def surname(self):
        surname = self.item.get("surname", "")
        if surname is None:
            return ""
        return surname

    @property
    def class_(self):
        class_ = self.item.get("class_", "")
        if class_ is None:
            return ""
        return class_

    @property
    def period(self):
        period = self.item.get("period", "")
        if period is None:
            return ""
        return period

    @property
    def target_aspirational(self):
        target_aspirational = self.item.get("target_aspirational", "")
        if target_aspirational is None:
            return ""
        return target_aspirational

    @property
    def target(self):
        target = self.item.get("target", "")
        if target is None:
            return ""
        return target

    @property
    def working(self):
        working = self.item.get("working", "")
        if working is None:
            return ""
        return working

    @property
    def effort(self):
        effort = self.item.get("effort", "")
        if effort is None:
            return ""
        return effort

    @property
    def behaviour(self):
        behaviour = self.item.get("behaviour", "")
        if behaviour is None:
            return ""
        return behaviour

    @property
    def homework(self):
        homework = self.item.get("homework", "")
        if homework is None:
            return ""
        return homework

    @property
    def prelim(self):
        prelim = self.item.get("prelim", "")
        if prelim is None:
            return ""
        return prelim

    @property
    def baseline_assessment(self):
        baseline_assessment = self.item.get("baseline_assessment", "")
        if baseline_assessment is None:
            return ""
        return baseline_assessment

    @property
    def prediction_sqa(self):
        prediction_sqa = self.item.get("prediction_sqa", "")
        if prediction_sqa is None:
            return ""
        return prediction_sqa


def main(fname):
    yield from load_rows(fname)

def load_rows(fname):
    with open(fname, mode='r') as f:
        headers = [
          "level",
          "code",
          "course_name",
          "class_",
          "surname",
          "forename",
          "middlename",
          "period",
          "target_aspirational",
          "working",
          "target",
          "effort",
          "behaviour",
          "homework",
          "prelim",
          "baseline_assessment",
          "prediction_sqa",
        ]
        rows = csv.DictReader(f, fieldnames=headers)
        for ix, r in enumerate(rows, 1):
            for k, v in r.items():
                r[k.strip()] = v.strip()

                if not v:
                    r[k] = None
                if r[k] == 'target_aspirational':
                    print(f"{ix}: {r}")
            yield Row(r)

by_student = lambda r: r.fullname

def by_level(r):
    return r.level

by_class_ = lambda r: r.class_
by_course = lambda r: r.course_name
by_courses_classes = lambda r: (r.course_name, r.class_)
by_levels_courses = lambda r: (r.level, r.course_name)
by_students_courses = lambda r: (r.fullname, r.course_name)
by_students_classes = lambda r: (r.class_, r.fullname)


def create_levels(rows):
    for level_name, llist in groupby(sorted(rows, key=by_level), key=by_level):
        level = Level(name=level_name)
        db.session.add(level)
    db.session.commit()
    print("Create Levels")

def create_courses(rows):
    for course_name, clist in groupby(sorted(rows, key=by_course), key=by_course):
        course = Course(name=course_name)
        db.session.add(course)
    db.session.commit()
    print("Create Courses")

def create_classes(rows):
    for class_name, clist in groupby(sorted(rows, key=by_class_), key=by_class_):
        class_ = Class(name=class_name)
        db.session.add(class_)
    db.session.commit()
    print("Create Classes")

def create_students(rows):
    for fullname, slist in groupby(sorted(rows, key=by_student), key=by_student):
        name = Name(fullname)
        student = Student(firstname=name.first, middlename=name.middle, lastname=name.last)
        db.session.add(student)
    db.session.commit()
    print("Create Students")

def create_students_courses(rows):
    """Create students courses with grades."""
    for (fullname, course_name), slist in groupby(sorted(rows, key=by_students_courses), key=by_students_courses):
        grades = list(slist)
        name = Name(fullname)

        student = db.session.query(Student).filter(
            Student.firstname == name.first,
            Student.middlename == name.middle,
            Student.lastname == name.last
        ).first()
        course = db.session.query(Course).filter(Course.name == course_name).first()

        students_courses = db.session.query(StudentsCourses).filter(
            StudentsCourses.student_id == student.id,
            StudentsCourses.course_id == course.id
        ).first()

        if not students_courses:
            for g in grades:
                grade = Grade(
                    target=g.target or None,
                    target_aspirational=g.target_aspirational or None,
                    working=g.working or None,
                    prelim=g.prelim or None,
                    baseline_assessment=g.baseline_assessment or None,
                    prediction_sqa=g.prediction_sqa or None,
                )
            students_courses = StudentsCourses(student=student, grade=grade, course=course)
            db.session.add(students_courses)
        else:
            print("Student course found. Oh Noes!!!")
        print(f"Student Id: {student.id}, Course Id: {course.id} {fullname}")
    db.session.commit()
    print("Commit students_courses")

def create_students_classes(rows):
    for (class_name, fullname), slist in groupby(sorted(rows, key=by_students_classes), key=by_students_classes):
        name = Name(fullname)
        slist = list(slist)
        student = db.session.query(Student).filter(
            Student.firstname == name.first,
            Student.middlename == name.middle,
            Student.lastname == name.last
        ).first()
        class_ = db.session.query(Class).filter(Class.name == class_name).first()

        students_classes = db.session.query(StudentsClasses).filter(
            StudentsClasses.student_id == student.id,
            StudentsClasses.class_id == class_.id
        ).all()
        if not students_classes:
            students_classes = StudentsClasses(student=student, class_=class_)
            db.session.add(students_classes)
        else:
            for sc in students_classes:
                class_.students.append(sc)
            db.session.add(class_)
        print(f"Student Id: {student.id}, Class Id: {class_.id} {fullname}")

    db.session.commit()
    print("Commit students_classes")


def create_courses_classes(rows):
    for (course_name, class_name), slist in groupby(sorted(rows, key=by_courses_classes), key=by_courses_classes):
        slist = list(slist)
        course = db.session.query(Course).filter(
            Course.name == course_name,
        ).first()
        class_ = db.session.query(Class).filter(Class.name == class_name).first()

        courses_classes = db.session.query(CoursesClasses).filter(
            CoursesClasses.course_id == course.id,
            CoursesClasses.class_id == class_.id
        ).all()
        if not courses_classes:
            courses_classes = CoursesClasses(course=course, class_=class_)
            db.session.add(courses_classes)
        else:
            for sc in courses_classes:
                course.classes.append(sc)
            db.session.add(course)
        print(f"Course Id: {course.id}, Class Id: {class_.id}")

    db.session.commit()
    print("Commit courses_classes")


def create_levels_courses(rows):
    for (level_name, course_name), slist in groupby(sorted(rows, key=by_levels_courses), key=by_levels_courses):
        slist = list(slist)
        course = db.session.query(Course).filter(
            Course.name == course_name,
        ).first()
        level = db.session.query(Level).filter(Level.name == level_name).first()

        levels_courses = db.session.query(LevelsCourses).filter(
            LevelsCourses.level_id == level.id,
            LevelsCourses.course_id == course.id
        ).all()
        if not levels_courses:
            levels_courses = LevelsCourses(level=level, course=course)
            db.session.add(levels_courses)
        else:
            for lc in levels_courses:
                level.courses.append(lc)
            db.session.add(course)
        print(f"Level Id: {level.id}, Course Id: {course.id}")

    db.session.commit()
    print("Commit courses_classes")


def write(rows):
    rows = list(rows)
    create_levels(rows)
    create_courses(rows)
    create_classes(rows)
    create_students(rows)
    create_levels_courses(rows)
    create_students_courses(rows)
    create_students_classes(rows)
    create_courses_classes(rows)

def merge_object(obj):
    try:
        db.session.merge(obj)
        # print("Add")
    except Exception:
        db.session.rollback()
        print("Rollback")
    else:
        db.session.commit()
        print("Commit")

if __name__ == '__main__':
    rows = load_rows("test.csv")
    write(rows)
