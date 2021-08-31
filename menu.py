import calendar
import json
from datetime import date, datetime, timedelta

from ingredient import add_ingredient_prices
from recipe import (
    fetch_recipe,
    fetch_recipe_price_breakdown,
    fetch_week_recipes,
)


def read_json_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json_file(filepath, data):
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f)


def get_date(delta=0):
    return date.today() + timedelta(days=delta)


def get_week_day_name(date):
    return calendar.day_name[date.weekday()]


def parse_date(iso_date):
    return datetime.fromisoformat(iso_date)


def create_week_menu(api_key):
    menu = fetch_week_recipes(api_key)
    week_menu = {}
    for date_offset, (_, day_menu) in enumerate(menu.items(), start=1):
        date = get_date(date_offset).isoformat()
        week_menu[date] = []
        for recipe in day_menu["meals"]:
            id = recipe["id"]
            recipe = fetch_recipe(api_key, id)
            ingredient_prices = fetch_recipe_price_breakdown(api_key, id)
            priced_recipe = add_ingredient_prices(recipe, ingredient_prices)
        week_menu[date].append(priced_recipe)
    return week_menu
