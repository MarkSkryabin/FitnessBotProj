from aiogram.fsm.state import State, StatesGroup


class Form(StatesGroup):
    weight = State()
    height = State()
    age = State()
    activity_time = State()
    city = State()
    calorie_goal = State()
    water_goal = State()
    gender = State()
    add_food = State()
