import json
from app import db
from models import Teacher, Goal

"""
"""
with open("teachers.json") as f:
    teachers = json.load(f)

with open("goals.json") as f:
    goals = json.load(f)


for goal, name in goals.items():
    goal_add = Goal(name_slug=goal, name=name[2:], name_symvol=name[0])
    db.session.add(goal_add)


for teacher in teachers:
    name = teacher["name"]
    about = teacher["about"]
    rating = float(teacher["rating"])
    picture = teacher["picture"]
    price = int(teacher["price"])
    free = json.dumps(teacher["free"])
    teacher_add = Teacher(name=name, about=about, rating=rating, picture=picture, price=price, free=free)
    for goal in teacher["goals"]:
        goal_teacher = db.session.query(Goal).filter(Goal.name_slug == goal)
        teacher_add.goals.extend(goal_teacher)
    db.session.add(teacher_add)

db.session.commit()
