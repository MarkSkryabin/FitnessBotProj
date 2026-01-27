import aiosqlite
from datetime import date
from count_funcs import day_value_water

DB_PATH = 'fitness_database.db'


async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                telegram_id INTEGER PRIMARY KEY,
                weight REAL,
                height REAL,
                age INTEGER,
                gender TEXT,
                activity_time INTEGER,
                city TEXT,
                calorie_goal REAL,
                water_goal REAL,
                logged_water REAL,
                logged_calories REAL,
                burned_calories REAL,
                last_update TEXT
            );
        """)
        await db.commit()


async def save_user_profile(
    telegram_id: int,
    weight: float,
    height: float,
    age: int,
    gender: str,
    activity_time: int,
    city: str,
    calorie_goal: float,
    water_goal: float,
    logged_water: float,
    logged_calories: float,
    burned_calories: float,
    last_update: str
):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            INSERT INTO users (
                telegram_id, weight, height, age,
                gender, activity_time, city, calorie_goal, water_goal,
                logged_water, logged_calories, burned_calories, last_update
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(telegram_id) DO UPDATE SET
                weight = excluded.weight,
                height = excluded.height,
                age = excluded.age,
                gender = excluded.gender,
                activity_time = excluded.activity_time,
                city = excluded.city,
                calorie_goal = excluded.calorie_goal,
                water_goal = excluded.water_goal,
                logged_water = excluded.logged_water,
                logged_calories = excluded.logged_calories,
                burned_calories = excluded.burned_calories,
                last_update = excluded.last_update
        """, (
            telegram_id,
            weight,
            height,
            age,
            gender,
            activity_time,
            city,
            calorie_goal,
            water_goal,
            logged_water,
            logged_calories,
            burned_calories,
            last_update
        ))
        await db.commit()


async def get_user_profile(telegram_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute("""
            SELECT weight, height, age, gender,
                   activity_time, city, calorie_goal, water_goal,
                   logged_water, logged_calories, burned_calories, last_update
            FROM users WHERE telegram_id = ?
        """, (telegram_id,))
        row = await cursor.fetchone()
        await cursor.close()
        return row


async def new_day(telegram_id: int):
    """Функция для сброса целей на новый день"""
    today = date.today().isoformat()

    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute("""
            SELECT last_update, weight, activity_time, city
            FROM users WHERE telegram_id = ?
        """, (telegram_id,))
        row = await cursor.fetchone()
        await cursor.close()

        if not row:
            return

        last_update, weight, activity_time, city = row

        # Если день новый — сбрасываем
        if last_update != today:
            new_water_goal = day_value_water(weight, activity_time, city)

            await db.execute("""
                UPDATE users SET
                    logged_water = 0,
                    logged_calories = 0,
                    burned_calories = 0,
                    water_goal = ?,
                    last_update = ?
                WHERE telegram_id = ?
            """, (new_water_goal, today, telegram_id))

            await db.commit()


async def last_update_day():
    """Функция для проверки дня"""
    return date.today().isoformat()
