from flask_wtf import FlaskForm
from wtforms import StringField, RadioField, SelectField
from wtforms import validators
from sqlalchemy import exc

from models import Goal


class RequestForm(FlaskForm):
    goals_list = []
    goals = []
    # Чтобы корректно сработала миграция с нуля сделаем обход ошибки sqlalchemy.exc.OperationalError
    try:
        goals = Goal.query.all()
    except exc.OperationalError:
        goals = []
    for goal in goals:
        goals_list.append((goal.id, goal.name))
    goal = RadioField("Какая цель занятий?", choices=goals_list,
                      validators=[validators.InputRequired("Выберите цель занятий!")])
    free = RadioField("Сколько времени есть?", choices=[("1-2 часа в неделю", "1-2 часа в неделю"),
                                                        ("3-5 часов в неделю", "3-5 часов в неделю"),
                                                        ("5-7 часов в неделю", "5-7 часов в неделю"),
                                                        ("7-10 часов в неделю", "7-10 часов в неделю")],
                      validators=[validators.InputRequired("Выберите свободное время!")])
    name = StringField("Вас зовут", validators=[validators.InputRequired("Введите своё имя!"),
                                                validators.length(min=3,
                                                                  message="Имя не может быть меньше 3 символов!")])
    phone = StringField("Ваш телефон", validators=[validators.InputRequired("Введите свой номер!"),
                                                   validators.regexp(
                                                       r"^((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$",
                                                       message="Вы ввели некорректный номер телефона!")])


class BookingForm(FlaskForm):
    name = StringField("Вас зовут", validators=[validators.InputRequired("Введите своё имя!"),
                                                validators.length(min=3,
                                                                  message="Имя не может быть меньше 3 символов!")])
    phone = StringField("Ваш телефон", validators=[validators.InputRequired("Введите свой номер!"),
                                                   validators.regexp(
                                                             r"^((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$",
                                                             message="Вы ввели некорректный номер телефона!")])


class SortingForm(FlaskForm):
    sort = SelectField("Сколько времени есть?", choices=[(1, "В случайном порядке"),
                                                         (2, "Сначала лучшие по рейтингу"),
                                                         (3, "Сначала дорогие"),
                                                         (4, "Сначала недорогие")])
