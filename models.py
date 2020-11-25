from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()


asocciation_table = db.Table('association', db.Column('teacher_id', db.Integer, db.ForeignKey('teachers.id')),
                             db.Column('goal_id', db.Integer, db.ForeignKey('goals.id')))


class Booking(db.Model):
    __tablename__ = "bookings"
    id = db.Column(db.Integer, primary_key=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.id'), nullable=False)
    teachers = db.relationship('Teacher', back_populates='bookings')
    name = db.Column(db.String, nullable=False)
    phone = db.Column(db.String, nullable=False)
    weekday = db.Column(db.String, nullable=False)
    time = db.Column(db.String, nullable=False)


class Goal(db.Model):
    __tablename__ = "goals"
    id = db.Column(db.Integer, primary_key=True)
    name_slug = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)
    name_symvol = db.Column(db.String(1), nullable=False)
    teachers = db.relationship(
        "Teacher", secondary=asocciation_table, back_populates="goals"
    )


class Request(db.Model):
    __tablename__ = "requests"
    id = db.Column(db.Integer, primary_key=True)
    goal_id = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String, nullable=False)
    phone = db.Column(db.String, nullable=False)
    free = db.Column(db.String, nullable=False)


class Teacher(db.Model):
    __tablename__ = "teachers"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    about = db.Column(db.String, nullable=False)
    rating = db.Column(db.Float, nullable=False)
    picture = db.Column(db.String, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    free = db.Column(db.String, nullable=False)
    goals = db.relationship(
        "Goal", secondary=asocciation_table, back_populates="teachers"
    )
    bookings = db.relationship('Booking', back_populates='teachers')
