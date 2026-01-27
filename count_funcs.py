import httpx
from config import API_TOKEN_WEATHER
import random


async def day_value_water(weight, activity_time, city):
    """Функция для расчёта дневной нормы воды"""
    user_water_value = float(weight) * 30 + 500 * (float(activity_time) // 30)
    temperature = await get_weather_async(city, API_TOKEN_WEATHER)
    try:
        if float(temperature) > 25:
            delta = float(temperature) - 25
            extra_water = 15 * (delta ** 2)  # нелинейный коэффициент
            user_water_value += extra_water
    except ValueError:
        pass
    return user_water_value


async def get_weather_async(city, api_key):
    """Асинхронная функция для получения текущей погоды в выбранном городе
    :param city: выбранный город
    :param api_key: API-ключ OpenWeatherMap"""

    url = f"http://api.openweathermap.org/data/2.5/weather"
    params = {"q": city, "appid": api_key, "units": "metric"}

    async with httpx.AsyncClient(timeout=2) as client:
        response = await client.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        return data['main']['temp']
    else:
        return f"Ошибка при запросе данных!\n\n{response.text}"


async def day_value_calorie(text, weight, height, age, activity_time, gender):
    """Функция для расчёта дневной нормы калорий """
    if text == 'да':
        # Разный расчёт для женщин и мужчин
        if gender == 'Женский':
            user_calorie_goal = 0.9 * (
                    10 * float(weight) + 6.25 * float(height) - 5 * float(age) + 400 * float(activity_time) / 60)
        else:
            user_calorie_goal = 10 * float(weight) + 6.25 * float(height) - 5 * float(age) + 500 * float(
                activity_time) / 60
    else:
        # Установка пользовательского значения
        user_calorie_goal = text
    return float(user_calorie_goal)


async def get_food_info(product_name: str):
    try:
        url = "https://world.openfoodfacts.org/cgi/search.pl"
        params = {
            "action": "process",
            "search_terms": product_name,
            "json": "true",
            "page_size": 1
        }

        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.get(url, params=params)

        data = response.json()
        products = data.get("products", [])

        if not products:
            return None

        product = products[0]

        return {
            "name": product.get("product_name", product_name),
            "calories_100g": product.get("nutriments", {}).get("energy-kcal_100g")}

    except httpx.ReadTimeout:
        return None

    except httpx.RequestError:
        return None


def get_food_recommendation(remaining_calories):
    """Функция для рекомендации низкокалорийных продуктов"""
    LOW_CAL_PRODUCTS = [
        # Салаты
        ("🥗 Овощной салат (огурец, помидор, зелень)", 18),
        ("🥬 Салат из капусты с морковью", 25),
        ("🥒 Салат из огурцов с йогуртом", 30),
        ("🍅 Салат «Греческий лайт» (без сыра)", 45),
        ("🥦 Салат из брокколи на пару", 35),
        ("🍠 Винегрет без масла", 55),
        ("🥬 Салат из пекинской капусты", 20),

        # Вторые блюда (лёгкие)
        ("🍗 Куриная грудка отварная", 110), ("🐟 Рыба на пару (хек, треска)", 95),
        ("🍳 Омлет из белков", 52), ("🥩 Индейка запечённая", 120),
        ("🍄 Тушёные грибы", 50), ("🥦 Овощи на пару (микс)", 40),
        ("🍲 Овощное рагу", 60),

        # Перекусы
        ("🍎 Яблоко", 52), ("🍐 Груша", 57),
        ("🍊 Апельсин", 47), ("🍓 Клубника", 32),
        ("🍌 Банан", 89), ("🥛 Йогурт 1-2%", 40),
        ("🧀 Творог 0–2%", 80), ("🥚 Варёное яйцо", 155),
        ("🥕 Морковь", 41), ("🥒 Огурец", 16)]

    suitable = [(name, kcal) for name, kcal in LOW_CAL_PRODUCTS
                if kcal <= remaining_calories]

    if not suitable:
        return None

    product = random.choice(suitable)
    return f"🥗 Хочешь перекусить?\n Попробуй {product[0]} — примерно {product[1]} ккал на 100 г."
