from app import db

class Student(db.Model):
    __tablename__ = "student"
    student_ID = db.Column(db.String(50),primary_key=True,unique=True)
    name = db.Column(db.String(20))
    password = db.Column(db.String(20))
    teacher_ID = db.Column(db.String(50), db.ForeignKey('Class.teacher_ID'))
    class_ID = db.Column(db.String(50), db.ForeignKey('Class.class_ID'))

class Teacher(db.Model):
    __tablename__ = "Teacher"
    teacher_ID = db.Column(db.String(50),primary_key=True,unique=True)
    school_ID = db.Column(db.String(20),db.ForeignKey('School.school_ID'))
    password = db.Column(db.String(20))
    course_ID = db.Column(db.String(50), db.ForeignKey('Course.course_ID'))

class platform_Manager(db.Model):
    __tablename__ = "platform_Manager"
    pm_ID = db.Column(db.String(50),primary_key=True,unique=True)
    password = db.Column(db.String(20))

class School(db.Model):
    __tablename__ = "School"
    school_ID = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(50))

class Course(db.Model):
    __tablename__ = "Course"
    course_ID = db.Column(db.String(50), primary_key=True)
    course_Name = db.Column(db.String(50))
    Exps = db.relationship("Experiment",backref = "Course",secondary = "Exp_Course")

class Class(db.Model):
    __tablename__ = "Class"
    class_ID = db.Column(db.Integer,  primary_key=True)
    teacher_ID = db.Column(db.String(50), db.ForeignKey('Teacher.teacher_ID'), primary_key=True)
    course_ID = db.Column(db.String(50), db.ForeignKey('Teacher.course_ID'))

class Experiment(db.Model):
    __tablename__ = "Experiment"
    exp_ID = db.Column(db.Integer,primary_key=True,unique=True,autoincrement=True)
    exp_Name = db.Column(db.String(50))
    timeLimit = db.Column(db.String(250))

class Comment(db.Model):
    __tablename__ = "Comment"
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    comment = db.Column(db.String(200))
    student_ID = db.Column(db.String(50), db.ForeignKey('ai_platform.student_ID'))
    exp_ID = db.Column(db.String(50), db.ForeignKey('Experiment.exp_ID'))

Exp_Course = db.Table("Exp_Course",db.Column("course_ID",db.String(50),db.ForeignKey("Course.course_ID"),primary_key=True),
                                   db.Column("exp_ID",db.String(50),db.ForeignKey("Experiment.exp_ID"),primary_key=True))