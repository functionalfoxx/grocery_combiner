def add_recipe(all_recipes, recipe_data):
    if recipe_data is not None:
        all_recipes.append(recipe_data)
    return all_recipes

def collect_ingredients(all_recipes):
    all_ingredients = []

    for recipe in all_recipes:
        ingredients = recipe["ingredients"]
        all_ingredients.extend(ingredients)

    return all_ingredients

def display_ingredients(all_ingredients):
    for ingredient in all_ingredients:
        print("-", ingredient)
        print()