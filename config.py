import os


# Для указания пути к файлу БД воспользумся путем до текущего модуля
# - Текущая папка
current_path = os.path.dirname(os.path.realpath(__file__))
# - Путь к файлу БД в данной папке
db_path = "sqlite:///" + current_path + "\\base.db"


class Config:
    DEBUG = True
    SECRET_KEY = "uZM3KBTnEFXZfCFmzGdgLeYQwRjMD6INp4C0JiO1VHy9LXYsdv"
    SQLALCHEMY_DATABASE_URI = db_path
    SQLALCHEMY_TRACK_MODIFICATIONS = False


# Словарь, хранящий имена дней недели
days = {"mon": "Понедельник", "tue": "Вторник", "wed": "Среда", "thu": "Четверг", "fri": "Пятница",
        "sat": "Суббота", "sun": "Воскресенье"}
