import copy


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
    # garlic
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


def add_ingredient_prices(recipe, ingredient_prices):
    priced_recipe = copy.deepcopy(recipe)
    for ingredient in priced_recipe["extendedIngredients"]:
        ingredient["price"] = 0
        for priced_ingredient in ingredient_prices:
            if ingredient["name"] == priced_ingredient["name"]:
                ingredient["price"] = priced_ingredient["price"]
    return priced_recipe


def print_shopping_list(menu):
    ingredients = []
    for _, meals in menu.items():
        for recipe in meals:
            for ingredient in recipe["extendedIngredients"]:
                ingredients.append(ingredient)
    ingredient_amounts = sum_ingredient_amount(ingredients)
    # TODO: add prices
