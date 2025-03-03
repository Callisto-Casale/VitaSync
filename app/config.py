import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    PIHOLE_PASSWORD = os.getenv("PIHOLE_PASSWORD")
    PIHOLE_URL = os.getenv("PIHOLE_URL")

    OPEN_WEATHER_KEY = os.getenv("OPEN_WEATHER_KEY")

    AUTH_RELOAD_TOKEN = os.getenv("AUTH_RELOAD_TOKEN")


class Databases:
    MEALS = "app/database/meals.db"
    INGREDIENTS = "app/database/ingredients.db"
