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
