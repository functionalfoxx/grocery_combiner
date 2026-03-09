import requests
from bs4 import BeautifulSoup
import json

def get_recipe(url):

    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})

    soup = BeautifulSoup(response.text, "html.parser")

    scripts = soup.find_all("script", type="application/ld+json")

    if response.status_code in (403,404):
        print(f"Request failed with status code: {response.status_code}")
        return None
    
    recipe = None

    for script in scripts:

        try:
            data = json.loads(script.get_text())
        except:
            continue

        if isinstance(data, list):
            for item in data:
                if not isinstance(item, dict):
                    continue

                type_value = item.get("@type")

                if type_value == "Recipe" or (
                    isinstance(type_value, list) and "Recipe" in type_value
                ):
                    recipe = item
                    break

            if recipe:
                break

            continue
        
        type_value = data.get("@type")

        if type_value == "Recipe" or (
            isinstance(type_value, list) and "Recipe" in type_value
        ):
            recipe = data
            break

        if "@graph" in data:
            for item in data["@graph"]:
                type_value = item.get("@type")

                if type_value == "Recipe" or (
                    isinstance(type_value, list) and "Recipe" in type_value
                ):
                    recipe = item
                    break

        if recipe:
            break

    if recipe is None:
        ingredient_tags = soup.find_all(attrs={"itemprop": "recipeIngredient"})

        if ingredient_tags:
            ingredients = [tag.get_text(strip=True) for tag in ingredient_tags]

            title_tag = soup.find("title")
            name = title_tag.get_text(strip=True) if title_tag else "Unknown recipe"

            recipe_data = {
                "name": name,
                "ingredients": ingredients
            }

            print(recipe_data["name"])
            print()

            for ingredient in recipe_data["ingredients"]:
                print(ingredient)

            return recipe_data

        return None

    recipe_data = {
        "name": recipe.get("name", "Unknown recipe"),
        "ingredients": recipe.get("recipeIngredient")
    }

    print(recipe_data["name"])
    print()

    if recipe_data["ingredients"]:
        for ingredient in recipe_data["ingredients"]:
            print(ingredient)
    else:
        print("No ingredients found in recipe schema.")

    return recipe_data

if __name__ == "__main__":
    url = "https://smittenkitchen.com/2022/01/spanakopita/"
    if not url.startswith("http://") and not url.startswith("https://"):
        print("Invalid URL")
    else:
        get_recipe(url)