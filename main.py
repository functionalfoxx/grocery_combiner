from scraper import get_recipe
from ingredients import add_recipe, collect_ingredients, count_ingredients, display_grocery_list

all_recipes = []

while True:
    url = input("Enter recipe URL or type done when finished: ").strip()

    if url == "":
        print ("\nPlease enter a URL.\n")
        continue

    if url.lower() == "done":
        break

    recipe_data = get_recipe(url)

    if recipe_data is None:
        print("\nCould not extract recipe from this URL.\n")
        continue

    all_recipes = add_recipe(all_recipes, recipe_data)

if len(all_recipes) == 0:
    print("No recipes were added.")
else:
    all_ingredients = collect_ingredients(all_recipes)

    print("\nDEBUG INGREDIENT DATA\n")
    for item in all_ingredients:
        print(item)

    ingredient_counts = count_ingredients(all_ingredients)
    display_grocery_list(ingredient_counts)