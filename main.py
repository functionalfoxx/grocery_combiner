from scraper import get_recipe
from ingredients import add_recipe, collect_ingredients

all_recipes = []

url = input("Enter recipe URL: ").strip()

recipe_data = get_recipe(url)
all_recipes = add_recipe(all_recipes, recipe_data)
all_ingredients = collect_ingredients(all_recipes)

if recipe_data is None:
    print("Could not extract recipe from this URL.")