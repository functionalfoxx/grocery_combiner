from scraper import get_recipe
from ingredients import add_recipe, collect_ingredients, count_ingredients, display_grocery_list

all_recipes = []

while True:
    user_input = input("Enter recipe URL, paste multiple URLs separated by commas, or type done when finished: ").strip()

    if user_input == "":
        print("\nPlease enter a URL.\n")
        continue

    if user_input.lower() == "done":
        break

    raw_urls = user_input.replace(",", "\n").splitlines()
    urls = [url.strip() for url in raw_urls if url.strip()]

    for url in urls:
        recipe_data = get_recipe(url)

        if recipe_data is None:
            print(f"\nCould not extract recipe from this URL:\n{url}\n")
            continue

        all_recipes = add_recipe(all_recipes, recipe_data)

if len(all_recipes) == 0:
    print("No recipes were added.")
else:
    all_ingredients = collect_ingredients(all_recipes)

    print("\nDEBUG INGREDIENT DATA\n")

    for quantity, unit, ingredient in all_ingredients:
        print("quantity:", quantity, "| unit:", unit, "| ingredient:", ingredient)

    ingredient_counts = count_ingredients(all_ingredients)
    display_grocery_list(ingredient_counts)