import requests


def fetch_random_recipes(api_key, count=1):
    response = requests.get(
        "https://api.spoonacular.com/recipes/random",
        params={"number": count, "apiKey": api_key}
    )
    response.raise_for_status()
    return response.json()["recipes"]


def fetch_week_recipes(api_key):
    response = requests.get(
        "https://api.spoonacular.com/mealplanner/generate",
        params={"timeFrame": "week", "apiKey": api_key}
    )
    response.raise_for_status()
    return response.json()["week"]


def fetch_recipe(api_key, recipe_id, include_nutrition=False):
    response = requests.get(
        f"https://api.spoonacular.com/recipes/{recipe_id}/information",
        params={"includeNutrition": include_nutrition, "apiKey": api_key}
    )
    response.raise_for_status()
    return response.json()


def fetch_recipe_price_breakdown(api_key, recipe_id):
    response = requests.get(
        f"https://api.spoonacular.com/recipes/{recipe_id}/priceBreakdownWidget.json",
        params={"apiKey": api_key}
    )
    response.raise_for_status()
    return response.json()["ingredients"]
