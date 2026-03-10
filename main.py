from scraper import get_recipe
from ingredients import add_recipe, collect_ingredients, display_ingredients

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
        print("Could not extract recipe from this URL.")
        continue

    all_recipes = add_recipe(all_recipes, recipe_data)

if len(all_recipes) == 0:
    print("No recipes were added.")
else:
    all_ingredients = collect_ingredients(all_recipes)
    display_ingredients(all_ingredients)

if recipe_data is None:
    print("\nCould not extract recipe from this URL.\n")