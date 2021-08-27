from environs import Env
import requests


SAVED_WEEKLY_MENU_PATH = "week_menu.json"


def fetch_random_recipes(api_key, count=1):
    response = requests.get(
        "https://api.spoonacular.com/recipes/random",
        params={"number": count, "apiKey": api_key}
    )
    response.raise_for_status()
    return response.json()["recipes"]


def convert_solid_amount_to_grams(amount, unit):
    if unit == "g":
        return amount
    if "kilogram" in unit:
        return amount * 1000
    if unit == "ml":
        return amount
    if unit == "l":
        return amount * 1000
    if "Tbs" in unit or unit == "Tb":
        return amount * 15
    if "tsp" in unit:
        return amount * 10
    if "pinch" in unit:
        return amount * 3
    if "quart" in unit:
        return amount * 954
    if "dash" in unit.lower():
        return amount * 0.7
    if "serving" in unit:
        return amount * 150
    if "can" in unit:
        return amount * 330
    if "handful" in unit:
        return amount * 100
    #garlic
    if "clove" in unit:
        return amount * 3
    if "head" in unit:
        return amount * 30


def convert_liquid_amount_to_ml(amount, unit):
    if unit == "ml":
        return amount
    if unit == "g":
        return amount
    if unit == "l":
        return amount * 1000
    if "gallon" in unit:
        return amount * 3785
    if "Tbs" in unit or unit == "Tb":
        return amount * 15
    if "tsp" in unit:
        return amount * 5
    if "can" in unit:
        return amount * 330
    if "cup" in unit:
        return amount * 236
    if "serving" in unit:
        return amount * 200


def convert_amount_to_metric(consistency, amount, unit):
    if consistency == "liquid":
        return convert_liquid_amount_to_ml(amount, unit), "ml"
    if consistency == "solid":
        return convert_solid_amount_to_grams(amount, unit), "g"
    if consistency is None and unit in ("g", "ml"):
        return amount, unit
    return None, None


def sum_ingredient_amount(ingredients):
    ingredient_amounts = {}
    tmp = []
    for ingredient in ingredients:
        ingredient_name = ingredient["nameClean"]
        if not ingredient_name:
            ingredient_name = ingredient["name"]
        consistency = ingredient["consistency"]
        amount = ingredient["measures"]["metric"]["amount"]
        unit = ingredient["measures"]["metric"]["unitShort"]

        metric_amount, metric_unit = convert_amount_to_metric(
            consistency, amount, unit,
        )
        if metric_amount is not None and metric_unit is not None:
            amount, unit = metric_amount, metric_unit

        if unit in ["", "small", "medium", "large"]:
            unit = "pcs"

        if ingredient_name in ingredient_amounts:
            ingredient_amounts[ingredient_name]["amount"] += amount
            continue
        ingredient_amounts[ingredient_name] = {"amount": amount, "unit": unit}
    return ingredient_amounts


if __name__ == "__main__":
    env = Env()
    env.read_env()
    api_key = env.str("SPOONACULAR_TOKEN")

    recipes = fetch_random_recipes(api_key, 21)
    ingredients = [
        ingredient for recipe in recipes
        for ingredient in recipe["extendedIngredients"]
    ]
    ingredient_amounts = sum_ingredient_amount(ingredients)
