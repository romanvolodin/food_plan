from environs import Env

from ingredient import sum_ingredient_amount
from recipe import fetch_random_recipes


SAVED_WEEKLY_MENU_PATH = "week_menu.json"


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
