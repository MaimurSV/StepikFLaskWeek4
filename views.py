import json
import random

from flask import render_template, request, abort

from app import app, days
from forms import *
from models import *


@app.route("/")
def index_view():
    teachers = Teacher.query.all()
    goals = Goal.query.all()
    random.shuffle(teachers)
    return render_template("index.html", goals=goals, teachers=teachers[:6])


@app.route("/all/", methods=["POST", "GET"])
def all_view():
    form = SortingForm()
    goals = Goal.query.all()
    teachers = None
    if request.method == "POST":
        if form.validate_on_submit():
            sort_type = form.sort.data
            if sort_type == "1":
                teachers = Teacher.query.all()
                random.shuffle(teachers)
            elif sort_type == "2":
                teachers = Teacher.query.order_by(Teacher.rating.desc()).all()
            elif sort_type == "3":
                teachers = Teacher.query.order_by(Teacher.price.desc()).all()
            elif sort_type == "4":
                teachers = Teacher.query.order_by(Teacher.price).all()
    # По умолчанию в случае невалидной формы или при первом открытии по GET запросу будем
    # отражать преподавателей в случайном порядке
    if teachers is None:
        teachers = Teacher.query.all()
        random.shuffle(teachers)
    return render_template("all.html", form=form, goals=goals, teachers=teachers)


@app.route("/goal/<goal>/")
def goal_view(goal):
    # Если придет неверная переменная goal цели обучения нас выкинет на 404
    goal_query = Goal.query.filter(Goal.name_slug == goal).first_or_404()
    teachers = Teacher.query.filter(Teacher.goals.any(Goal.name_slug == goal)).order_by(Teacher.rating.desc()).all()
    name_goal = goal_query.name
    name_goal_symbol = goal_query.name_symvol
    return render_template("goal.html", name_goal=name_goal, name_goal_symbol=name_goal_symbol, teachers=teachers)


@app.route("/profile/<int:teacher_id>/")
def profile_view(teacher_id):
    teacher = Teacher.query.get_or_404(teacher_id)
    free = json.loads(teacher.free)
    goals = Goal.query.filter(Goal.teachers.any(Teacher.id == teacher_id)).all()
    return render_template("profile.html", days=days, goals=goals, teacher=teacher, free=free)


@app.route("/request/", methods=["GET", "POST"])
def request_view():
    form = RequestForm()
    if request.method == "POST":
        if form.validate_on_submit():
            goal = form.goal.data
            goal_name = Goal.query.get(goal).name
            free = form.free.data
            name = form.name.data
            phone = form.phone.data
            request_to_save = Request(goal_id=goal, free=free, name=name, phone=phone)
            db.session.add(request_to_save)
            db.session.commit()
            return render_template("request_done.html", goal_name=goal_name, free=free, name=name, phone=phone)
    return render_template("request.html", form=form)


@app.route("/booking/<time>/<day>/<int:teacher_id>/", methods=["GET", "POST"])
def booking_view(time, day, teacher_id):
    # Приводим время, переданное в скрытом запросе обратно к виду XX:XX или X:XX
    # Возможно есть способ попроще, регулярные выражения точно бы помогли
    if len(time) == 3:
        time = time.replace("00", ":00")
    else:
        time = time[:2] + time[2:].replace("00", ":00")
    # Добываем имя преподавателя
    teacher = Teacher.query.get_or_404(teacher_id)
    teacher_name = teacher.name
    picture = teacher.picture
    free = json.loads(teacher.free)
    # Проверяем что в строке запроса нам пришли корректные день и время
    time_is_not_correct = True
    for day_k in days.keys():
        if time in free[day_k]:
            time_is_not_correct = False
    if time_is_not_correct or day not in days.keys():
        abort(404)
    form = BookingForm()
    if request.method == "POST":
        if form.validate_on_submit():
            name = form.name.data
            phone = form.phone.data
            booking_to_save = Booking(teacher_id=teacher_id, name=name, phone=phone, time=time, weekday=day)
            db.session.add(booking_to_save)
            db.session.commit()
            return render_template("booking_done.html", name=name, phone=phone,
                                   weekday=days[day], time=time)
    return render_template("booking.html", form=form, day=day, dayname=days[day], time=time, teacher_id=teacher_id,
                           teacher_name=teacher_name, picture=picture)
