from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from states import Form
from db import save_user_profile, get_user_profile, new_day, last_update_day
from count_funcs import *
from aiogram import F


router = Router()


# Обработчик команды /start
@router.message(Command("start"))
async def cmd_start(message: Message):
    await new_day(message.from_user.id)  # Проверка нового дня
    await message.reply("Привет! 🙂 Я твой персональный фитнес-помощник!\n\n"
                        "Готов помочь тебе:\n"
                        "✅ Следить за тренировками\n"
                        "✅ Отслеживать твой баланс и воды и калорий\n"
                        "✅ Рекомендовать полезные продукты\n\n"
                        "Нажми /help, чтобы увидеть все мои возможности!")


# Обработчик команды /help
@router.message(Command("help"))
async def cmd_help(message: Message):
    await new_day(message.from_user.id)  # Проверка нового дня
    await message.reply(
        "Вот что я умею:\n\n"
        "▶ /start — начало работы\n"
        "▶ /set_profile — настройка профиля\n"
        "▶ /profile — просмотр профиля\n"
        "▶ /log_water <мл> — учёт воды\n"
        "▶ /log_food <продукт> — учёт калорий\n"
        "▶ /log_workout <тип> <мин> — учёт активности\n"
        "▶ /check_progress — твой прогресс\n\n"
        "Выбери команду и мы начнём путь к твоей цели! 🙂"
    )


@router.message(Command("set_profile"))
async def start_profile(message: Message, state: FSMContext):
    await new_day(message.from_user.id)  # Проверка нового дня
    await message.reply("⚖️ Введи свой вес в килограммах.\n  Пример: 72.5")
    await state.set_state(Form.weight)


@router.message(Form.weight)
async def get_weight(message: Message, state: FSMContext):
    # Проверка сообщения
    try:
        float(message.text)
        if not 20 <= float(message.text) <= 200:
            await message.reply("❌ Введи число от 20 до 200.")
            await state.set_state(Form.weight)
            return
    except ValueError:
        await message.reply("❌ Я не смог распознать значение.\n  "
                            "Пожалуйста, введи число ещё раз 🙂")
        await state.set_state(Form.weight)
        return
    await state.update_data(weight=message.text)
    await message.reply("📏 Введи свой рост в сантиметрах.\n  Пример: 175")
    await state.set_state(Form.height)


@router.message(Form.height)
async def get_height(message: Message, state: FSMContext):
    # Проверка сообщения
    try:
        float(message.text)
        if not 50 <= float(message.text) <= 230:
            await message.reply("❌ Введи число от 50 до 230.")
            await state.set_state(Form.height)
            return
    except ValueError:
        await message.reply("❌ Я не смог распознать значение.\n  "
                            "Пожалуйста, введи число ещё раз 🙂")
        await state.set_state(Form.height)
        return
    await state.update_data(height=message.text)
    await message.reply(f"🚻 Укажи свой пол:\n  Варианты: Мужской и Женский")
    await state.set_state(Form.gender)


@router.message(Form.gender)
async def get_gender(message: Message, state: FSMContext):
    # Проверка сообщения
    if message.text != 'Мужской' and message.text != 'Женский':
        await message.reply("❌ Я не смог распознать значение.\n  "
                            "Пожалуйста, введи пол ещё раз 🙂")
        await state.set_state(Form.gender)
        return
    await state.update_data(gender=message.text)
    await message.reply(f"🎂 Сколько тебе лет?\n  Пример: 21")
    await state.set_state(Form.age)


@router.message(Form.age)
async def get_age(message: Message, state: FSMContext):
    # Проверка сообщения
    try:
        float(message.text)
        if not 10 <= float(message.text) <= 130:
            await message.reply("❌ Введи число от 10 до 130.")
            await state.set_state(Form.age)
            return
    except ValueError:
        await message.reply("❌ Я не смог распознать значение.\n  "
                            "Пожалуйста, введи число ещё раз 🙂")
        await state.set_state(Form.age)
        return
    await state.update_data(age=message.text)
    await message.reply(f"🏃 Сколько минут физической активности у тебя в день?\n  Пример: 60")
    await state.set_state(Form.activity_time)


@router.message(Form.activity_time)
async def get_activity_time(message: Message, state: FSMContext):
    # Проверка сообщения
    try:
        float(message.text)
        if not 0 <= float(message.text) <= 1440:
            await message.reply("❌ Введи число от 0 до 1440.")
            await state.set_state(Form.activity_time)
            return
    except ValueError:
        await message.reply("❌ Я не смог распознать значение.\n  "
                            "Пожалуйста, введи число ещё раз 🙂")
        await state.set_state(Form.activity_time)
        return
    await state.update_data(activity_time=message.text)
    await message.reply(f"🌍 В каком городе ты сейчас находишься?\n  Пример: Москва")
    await state.set_state(Form.city)


@router.message(Form.city)
async def get_city(message: Message, state: FSMContext):
    await state.update_data(city=message.text)
    await message.reply(
        "Давай настроим твою дневную норму калорий 😊\n\n"
        "Ты можешь:\n"
        "👉 Написать «да», и я рассчитаю норму автоматически.\n"
        "👉 Или отправить число, если знаешь свою норму.\n\n"
        "Например: 1800")
    await state.set_state(Form.calorie_goal)


@router.message(Form.calorie_goal)
async def get_calorie_goal(message: Message, state: FSMContext):
    # Проверка сообщения
    if message.text != 'да' and message.text != 'Да' and message.text != 'ДА':
        try:
            float(message.text)
        except ValueError:
            await message.reply("❌ Я не смог распознать значение.\n  "
                                "Пожалуйста, введи число ещё раз 🙂")
            await state.set_state(Form.calorie_goal)
            return
    data = await state.get_data()
    weight = data.get("weight")
    height = data.get("height")
    age = data.get("age")
    activity_time = data.get("activity_time")
    gender = data.get("gender")
    city = data.get("city")

    # Расчёт нормы калорий
    user_calorie_goal = await day_value_calorie(message.text, weight, height,
                                                age, activity_time, gender)

    await state.update_data(calorie_goal=user_calorie_goal)
    data = await state.get_data()
    calorie_goal = data.get("calorie_goal")

    # Расчёт дневной нормы воды
    water_goal = await day_value_water(weight, activity_time, city)

    await message.reply(
        "*Твой профиль*\n\n"
        f"⚖️ Вес: *{weight}* кг\n"
        f"📏 Рост: *{height}* см\n"
        f"🎂 Возраст: *{age}* лет\n"
        f"🚻 Пол: *{gender}*\n"
        f"🏃 Активность: *{activity_time}* мин/день\n"
        f"🌍 Город: *{city}*\n\n"
        "🔥 *Дневные нормы*\n"
        f"🍽 Калории: *{round(calorie_goal):,}* ккал\n"
        f"💧 Вода: *{round(water_goal):,}* мл", parse_mode="Markdown")

    profile = await get_user_profile(message.from_user.id)

    if not profile:
        logged_water, logged_calories, burned_calories = 0, 0, 0
        last_update = await last_update_day()
    else:
        (weight1, height1, age1, gender1, activity_time1, city1, calorie_goal1,
         water_goal1, logged_water, logged_calories, burned_calories,
         last_update) = profile  # Переменные с 1 перезаписываются

    await save_user_profile(
        telegram_id=message.from_user.id, weight=float(weight),
        height=float(height), age=int(age),
        gender=gender, activity_time=int(activity_time),
        city=city, calorie_goal=float(calorie_goal),
        water_goal=float(water_goal), logged_water=logged_water,
        logged_calories=logged_calories, burned_calories=burned_calories,
        last_update=last_update)

    await state.clear()


# Функции логирования
@router.message(Command('log_water'))
async def logging_water(message: Message):
    await new_day(message.from_user.id)  # Проверка нового дня
    # Проверка сообщения
    args = message.text.split(maxsplit=1)
    try:
        water = float(args[1])
    except IndexError:
        await message.reply("❌ Укажи количество воды в миллилитрах.\n\nПример: /log_water 200")
        return
    try:
        if water <= 0:
            await message.reply("❌ Введи корректное количество выпитой воды.\n\n"
                                "Пример: /log_water 200")
            return
    except ValueError:
        await message.reply("❌ Я не смог распознать значение.\n  "
                            "Пожалуйста, введи команду ещё раз 🙂\n\n"
                            "Пример: /log_water 200")
    # Получение данных из БД
    profile = await get_user_profile(message.from_user.id)

    if not profile:
        await message.reply("Профиль не найден 😔\nВведи /set_profile")
        return

    (weight, height, age, gender, activity_time, city, calorie_goal,
     water_goal, logged_water, logged_calories, burned_calories,
     last_update) = profile

    logged_water += water  # выпитая вода
    remaining_water = water_goal - logged_water  # осталось выпить воды до достижения цели

    today = await last_update_day()

    await save_user_profile(
        telegram_id=message.from_user.id, weight=float(weight),
        height=float(height), age=int(age),
        gender=gender, activity_time=int(activity_time),
        city=city, calorie_goal=float(calorie_goal),
        water_goal=float(water_goal), logged_water=logged_water,
        logged_calories=logged_calories, burned_calories=burned_calories,
        last_update=today)

    if remaining_water <= 0:
        await message.reply(
            f"💧 Выпито сейчас - {water} мл.\n"
            f"   Всего сегодня: {logged_water} мл.\n\n"
            f"📊 Цель достигнута! Поздравляю!")
    else:
        await message.reply(
            f"💧 Выпито сейчас - {water} мл.\n"
            f"   Всего сегодня: {logged_water} мл.\n\n"
            f"📊 Осталось до цели: {remaining_water} мл.\n")


@router.message(Command('log_food'))
async def logging_food(message: Message, state: FSMContext):
    await new_day(message.from_user.id)  # Проверка нового дня
    # Проверка сообщения
    args = message.text.split(maxsplit=1)
    try:
        food = args[1]
    except IndexError:
        await message.reply("❌ Укажи название продукта.\n\nПример: /log_food индейка")
        return
    res = await get_food_info(food)
    if not res:
        await message.reply("❌ Не удалось найти продукт. Попробуй другое название.")
        return
    if res['name'] and res['calories_100g']:
        await message.reply(f"{res['name'].replace('&quot;', ' ')} — {res['calories_100g']} ккал на 100 г. Сколько "
                            f"грамм вы съели?")
        await state.update_data(add_food=res['calories_100g'])
        await state.set_state(Form.add_food)
    else:
        await message.reply(f"❌ К сожалению, данных о продукте нет в базе данных.")


@router.message(Form.add_food)
async def adding_food(message: Message, state: FSMContext):
    # Проверка сообщения
    try:
        food_grams = float(message.text)
    except ValueError:
        await message.reply("❌ Я не смог распознать значение.\n  "
                            "Пожалуйста, введи число грамм ещё раз 🙂")
        await state.set_state(Form.add_food)
        return

    data = await state.get_data()
    calories_by_gram = float(data.get("add_food")) / 100
    calories = calories_by_gram * food_grams

    # Получение данных из БД
    profile = await get_user_profile(message.from_user.id)

    if not profile:
        await message.reply("Профиль не найден 😔\nВведи /set_profile")
        return

    (weight, height, age, gender, activity_time, city, calorie_goal,
     water_goal, logged_water, logged_calories, burned_calories,
     last_update) = profile

    logged_calories += calories  # съеденные калории

    today = await last_update_day()

    await save_user_profile(
        telegram_id=message.from_user.id, weight=float(weight),
        height=float(height), age=int(age),
        gender=gender, activity_time=int(activity_time),
        city=city, calorie_goal=float(calorie_goal),
        water_goal=float(water_goal), logged_water=float(logged_water),
        logged_calories=float(logged_calories), burned_calories=float(burned_calories),
        last_update=today)

    await message.reply(f"Записано - {int(calories)} ккал.")
    await state.clear()


def progress_bar(current, goal, length=10):
    """Функция для вывода прогресс-бара"""
    if goal <= 0:
        return "—"
    percent = min(current / goal, 1)
    filled = int(length * percent)
    empty = length - filled
    bar = "🟩" * filled + "⬜" * empty
    return f"{bar} {int(percent * 100)}%"


@router.message(Command('check_progress'))
async def check_progress(message: Message):
    await new_day(message.from_user.id)  # Проверка нового дня
    # Получение данных из БД
    profile = await get_user_profile(message.from_user.id)

    if not profile:
        await message.reply("Профиль не найден 😔\nВведи /set_profile")
        return

    (weight, height, age, gender, activity_time, city, calorie_goal,
     water_goal, logged_water, logged_calories, burned_calories, last_update) = profile

    remaining_water = water_goal - logged_water  # осталось выпить воды до достижения цели
    remaining_calories = calorie_goal - logged_calories  # осталось съесть до выполнения цели

    water_bar = progress_bar(logged_water, water_goal)  # визуализация прогресса
    calorie_bar = progress_bar(logged_calories, calorie_goal)

    water_block = (f"💧 <b>Вода</b>\n"
                   f"{water_bar}\n"
                   f"• Выпито: <b>{logged_water}</b> мл из <b>{water_goal}</b> мл\n")

    if remaining_water <= 0:
        water_block += "✅ Цель по воде выполнена!\n"
    else:
        water_block += f"⏳ Осталось: <b>{remaining_water}</b> мл\n"

    calorie_block = (f"\n🔥 <b>Калории</b>\n"
                     f"{calorie_bar}\n"
                     f"• Потреблено: <b>{int(logged_calories)}</b> ккал\n"
                     f"• Сожжено: <b>{int(burned_calories)}</b> ккал\n"
                     f"• Баланс: <b>{int(logged_calories - burned_calories)}</b> ккал\n")

    if remaining_calories <= 0:
        calorie_block += "✅ Лимит калорий на сегодня достигнут!\n"
    else:
        calorie_block += f"🎯 Цель: <b>{round(calorie_goal, 1)}</b> ккал\n"
        recommendation = get_food_recommendation(remaining_calories)  # Рекомендации
        if recommendation:
            calorie_block += recommendation

    await message.reply(
        "📊 <b>Твой прогресс на сегодня</b>\n\n"
        + water_block
        + calorie_block,
        parse_mode="HTML")


@router.message(Command('log_workout'))
async def logging_workout(message: Message):
    await new_day(message.from_user.id)  # Проверка нового дня
    WORKOUTS = {"бег": 10, "ходьба": 5,
                "велосипед": 8, "плавание": 11,
                "силовая": 9, "йога": 4}   # Типы тренировок
    args = message.text.split(maxsplit=2)  # Проверка сообщения
    if len(args) < 3:
        await message.reply(
            "❌ Используй формат:\n"
            "/log_workout <тип> <время в минутах>\n\n"
            "Пример: /log_workout бег 40"
        )
        return

    workout_type = args[1].lower()
    duration_raw = args[2]

    if workout_type not in WORKOUTS:
        await message.reply(
            "❌ Неизвестный тип тренировки.\n"
            f"Доступные: {', '.join(WORKOUTS.keys())}"
        )
        return

    try:
        duration = float(duration_raw)
        if duration <= 0:
            raise ValueError
    except ValueError:
        await message.reply("❌ Время тренировки должно быть положительным числом (в минутах).")
        return

    calories_per_min = WORKOUTS[workout_type]  # Калории
    dop_burned_calories = round(calories_per_min * duration, 1)

    extra_water = int((duration // 30) * 200)  # Дополнительная вода

    profile = await get_user_profile(message.from_user.id)
    if not profile:
        await message.reply("⚠️ Сначала настрой профиль командой /set_profile.")
        return

    (weight, height, age, gender, activity_time, city, calorie_goal,
     water_goal, logged_water, logged_calories, burned_calories,
     last_update) = profile

    burned_calories += dop_burned_calories
    water_goal += extra_water

    today = await last_update_day()

    await save_user_profile(
        telegram_id=message.from_user.id, weight=float(weight),
        height=float(height), age=int(age),
        gender=gender, activity_time=int(activity_time),
        city=city, calorie_goal=float(calorie_goal),
        water_goal=float(water_goal), logged_water=float(logged_water),
        logged_calories=float(logged_calories), burned_calories=float(burned_calories),
        last_update=today)

    await message.reply("🏋️ Тренировка записана!\n\n"
                        f"Тип: <b>{workout_type.capitalize()}</b>\n"
                        f"Время: <b>{duration}</b> мин\n"
                        f"🔥 Сожжено: <b>{dop_burned_calories}</b> ккал\n"
                        f"💧 Дополнительно выпей <b>{extra_water}</b> мл воды",
                        parse_mode="HTML")


@router.message(Command("profile"))
async def show_profile(message: Message):
    await new_day(message.from_user.id)  # Проверка нового дня
    profile = await get_user_profile(message.from_user.id)

    if not profile:
        await message.reply("Профиль не найден 😔\nВведи /set_profile")
        return

    (weight, height, age, gender, activity_time, city, calorie_goal,
     water_goal, logged_water, logged_calories, burned_calories,
     last_update) = profile

    await message.reply(
        "Твой профиль\n\n"
        f"⚖️ Вес: {weight} кг\n"
        f"📏 Рост: {height} см\n"
        f"🎂 Возраст: {age} лет\n"
        f"🚻 Пол: {gender}\n"
        f"🏃 Активность: {activity_time} мин/день\n"
        f"🌍 Город: {city}\n\n"
        "🔥 Дневные нормы\n"
        f"🍽 Калории: {round(calorie_goal):,} ккал\n"
        f"💧 Вода: {round(water_goal):,} мл\n"
        f"\n"
        f"✏️ Хочешь изменить данные? Напиши /set_profile")


@router.message(F.text)
async def unknown_message(message: Message):
    await new_day(message.from_user.id)  # Проверка нового дня
    await message.reply(
        "Вот что я умею:\n\n"
        "▶ /start — начало работы\n"
        "▶ /set_profile — настройка профиля\n"
        "▶ /profile — просмотр профиля\n"
        "▶ /log_water <мл> — учёт воды\n"
        "▶ /log_food <продукт> — учёт калорий\n"
        "▶ /log_workout <тип> <мин> — учёт активности\n"
        "▶ /check_progress — прогресс\n\n"
        "Напиши команду или нажми /help 📖"
    )


# Функция для подключения обработчиков
def setup_handlers(dp):
    dp.include_router(router)
