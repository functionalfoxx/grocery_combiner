from scraper import get_recipe

url = input("Enter recipe URL: ").strip()

recipe_data = get_recipe(url)

if recipe_data is None:
    print("Could not extract recipe from this URL.")