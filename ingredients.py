def add_recipe(all_recipes, recipe_data):
    if recipe_data is not None:
        all_recipes.append(recipe_data)
    return all_recipes

def normalize_ingredient(ingredient):
    normalized = ingredient.strip().lower()
    return normalized

def collect_ingredients(all_recipes):
    all_ingredients = []

    for recipe in all_recipes:
        ingredients = recipe["ingredients"]

            for ingredient in ingredients:
                normalized = normalize_ingredient(ingredient)
                all_ingredients.append(normalized)

    return all_ingredients

def display_ingredients(all_ingredients):
    for ingredient in all_ingredients:
        print("-", ingredient)
        print()