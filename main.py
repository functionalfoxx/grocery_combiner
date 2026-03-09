from scraper import get_recipe

url = input("Enter recipe URL: ").strip()

recipe_data = get_recipe(url)