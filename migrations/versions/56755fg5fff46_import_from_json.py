"""empty message

Revision ID: 56755fg5fff46_import_from_json
Revises:
Create Date: 2020-11-25 22:46:00.000000

"""
import json

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table, column


# revision identifiers, used by Alembic.
revision = '56755fg5fff46_import_from_json'
down_revision = '2bf63ba82110'
branch_labels = None
depends_on = None


def upgrade():

    goals_table = table('goals',
                        column('id', sa.Integer()),
                        column('name_slug', sa.String()),
                        column('name', sa.String()),
                        column('name_symvol'))

    teachers_table = table('teachers',
                           column('id', sa.Integer()),
                           column('name', sa.String()),
                           column('about', sa.String()),
                           column('rating', sa.Float()),
                           column('picture', sa.String()),
                           column('price', sa.Integer()),
                           column('free', sa.String()))

    association_table = table('association',
                                 column('teacher_id'),
                                 column('goal_id'))

    with open("json_files/teachers.json") as f:
        teachers = json.load(f)
    with open("json_files/goals.json") as f:
        goals = json.load(f)

    goals_dict = []
    i = 0
    for goal, name in goals.items():
        goals_dict.append({"id": i, "name_slug": goal, "name": name[2:], "name_symvol": name[0]})
        i += 1
    op.bulk_insert(goals_table, goals_dict)

    teachers_dict = []
    association_table_dict = []
    for teacher in teachers:
        name = teacher["name"]
        about = teacher["about"]
        rating = float(teacher["rating"])
        picture = teacher["picture"]
        price = int(teacher["price"])
        free = json.dumps(teacher["free"])
        id = teacher["id"]
        teachers_dict.append({"id": id, "name": name, "about": about, "rating": rating, "picture": picture,
                              "price": price, "free": free})
        """"""
        for goal in teacher["goals"]:
            for goal_with_id in goals_dict:
                if goal == goal_with_id["name_slug"]:
                    association_table_dict.append({"goal_id": goal_with_id["id"], "teacher_id": id})
    op.bulk_insert(teachers_table, teachers_dict)
    op.bulk_insert(association_table, association_table_dict)


def downgrade():
    """
    Вариант А: Пересоздать таблицы (код взят из автоматически сгенерированной миграции)
    op.drop_table('goals')
    op.drop_table('association')
    op.drop_table('teachers')
    op.create_table('goals',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name_slug', sa.String(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('name_symvol', sa.String(length=1), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('teachers',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('name', sa.String(), nullable=False),
                    sa.Column('about', sa.String(), nullable=False),
                    sa.Column('rating', sa.Float(), nullable=False),
                    sa.Column('picture', sa.String(), nullable=False),
                    sa.Column('price', sa.Integer(), nullable=False),
                    sa.Column('free', sa.String(), nullable=False),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('association',
                    sa.Column('teacher_id', sa.Integer(), nullable=True),
                    sa.Column('goal_id', sa.Integer(), nullable=True),
                    sa.ForeignKeyConstraint(['goal_id'], ['goals.id'], ),
                    sa.ForeignKeyConstraint(['teacher_id'], ['teachers.id'], )
                    )"""

    """
    Вариант Б: очистить таблицы посредством SQL запросов
    SQLITE не имеет в своем составе команду TRUNCATE
    """
    op.execute("DELETE FROM `association`;")
    op.execute("REINDEX  `association`;")
    op.execute("DELETE FROM `teachers`;")
    op.execute("REINDEX  `teachers`;")
    op.execute("DELETE FROM `goals`;")
    op.execute("REINDEX  `goals`;")
    op.execute("VACUUM;")
