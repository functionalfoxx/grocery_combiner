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

def get_ingredient_name(ingredient):
    words = ingredient.split()

    if len(words) == 0:
        return ""

    return words[-1]

def singularize_ingredient(name):
    if name.endswith("s"):
        return name [:-1]
    return name

def count_ingredients(all_ingredients):
    ingredient_counts = {}

    for ingredient in all_ingredients:
        name = get_ingredient_name(ingredient)
        name = singularize_ingredient(name)

        if name in ingredient_counts:
            ingredient_counts[name] += 1
        else:
            ingredient_counts[name] = 1
    
    return ingredient_counts

def display_grocery_list(ingredient_counts):
    print ("\nGROCERY LIST\n")

    for ingredient in sorted(ingredient_counts):
        count = ingredient_counts[ingredient]
        print(count, "-", ingredient)

    print()