"""Database models."""
from extensions import db
from sqlalchemy import BigInteger, Column, ForeignKey, Numeric, String, func
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship


class LevelsCourses(db.Model):
    __tablename__ = "levels_courses"
    level_id = Column(ForeignKey("level.id"), primary_key=True)
    course_id = Column(ForeignKey("course.id"), primary_key=True)

    level = relationship("Level", back_populates="courses")
    course = relationship("Course", back_populates="levels")


class Level(db.Model):
    __tablename__ = "level"

    id = Column(BigInteger, primary_key=True)
    name = Column(String(120), nullable=True)
    courses = relationship("LevelsCourses", back_populates="level")


###### Intermediate StudentsCourses ######
class StudentsCourses(db.Model):
    __tablename__ = "students_courses"
    student_id = Column(ForeignKey("student.id"), primary_key=True)
    course_id = Column(ForeignKey("course.id"), primary_key=True)
    grade_id = Column(ForeignKey("grade.id"), primary_key=True)

    student = relationship("Student", back_populates="courses")
    course = relationship("Course", back_populates="students")
    grade = relationship("Grade", back_populates="students_courses")


class StudentsClasses(db.Model):
    __tablename__ = "students_classes"
    student_id = Column(ForeignKey("student.id"), primary_key=True)
    class_id = Column(ForeignKey("class.id"), primary_key=True)

    student = relationship("Student", back_populates="classes")
    class_ = relationship("Class", back_populates="students")


class Student(db.Model):
    __tablename__ = "student"

    id = Column(BigInteger, primary_key=True)
    firstname = Column(String(120), nullable=True)
    middlename = Column(String(120), nullable=True)
    lastname = Column(String(120), nullable=True)

    courses = relationship("StudentsCourses", back_populates="student")
    classes = relationship("StudentsClasses", back_populates="student")

    @hybrid_property
    def fullname(self):
        if self.middle:
            return " ".join([self.firstname, self.middlename, self.lastname])
        return " ".join([self.firstname, self.lastname])

    @fullname.expression
    def fullname(cls):
        middle = func.coalesce(cls.middlename, None)
        return func.trim("both", func.concat_ws(" ", cls.firstname, func.coalesce(middle, ""), cls.lastname))


class Course(db.Model):
    __tablename__ = "course"
    id = Column(BigInteger, primary_key=True, unique=True)
    name = Column(String(128))

    levels = relationship("LevelsCourses", back_populates="course")
    classes = relationship("CoursesClasses", back_populates="course")
    students = relationship("StudentsCourses", back_populates="course")


###### End StudentsCourses ######


class Grade(db.Model):
    __tablename__ = "grade"
    id = Column(BigInteger, primary_key=True)
    target = Column(Numeric(19, 2), nullable=True)
    target_aspirational = Column(Numeric(19, 2), nullable=True)
    working = Column(Numeric(19, 2), nullable=True)
    prelim = Column(Numeric(19, 2), nullable=True)
    baseline_assessment = Column(Numeric(19, 2), nullable=True)
    prediction_sqa = Column(Numeric(19, 2), nullable=True)
    students_courses = relationship(
        "StudentsCourses", primaryjoin="and_(Grade.id==StudentsCourses.grade_id)", back_populates="grade"
    )


class CoursesClasses(db.Model):
    __tablename__ = "courses_classes"
    course_id = Column(ForeignKey("course.id"), primary_key=True)
    class_id = Column(ForeignKey("class.id"), primary_key=True)

    course = relationship("Course", back_populates="classes")
    class_ = relationship("Class", back_populates="courses")


class Class(db.Model):
    __tablename__ = "class"
    id = Column(BigInteger, primary_key=True)
    name = Column(String(128), nullable=True)
    courses = relationship("CoursesClasses", back_populates="class_")
    students = relationship("StudentsClasses", back_populates="class_")
