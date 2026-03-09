import requests
from bs4 import BeautifulSoup
import json

def get_recipe(url):

    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(response.text, "html.parser")
    scripts = soup.find_all("script", type="application/ld+json")
    
    recipe = None

    for script in scripts:
        try:
            data = json.loads(script.get_text())
        except:
            continue

        if data.get("@type") == "Recipe":
            recipe = data
            break

        if "@graph" in data:
            for item in data["@graph"]:
                if item.get("@type") == "Recipe":
                    recipe = item
                    break

        if recipe:
            break

    if recipe is None:
        return None

    recipe_data = {
        "name": recipe["name"],
        "ingredients": recipe["recipeIngredient"]
    }

    print(recipe_data["name"])
    print()

    for ingredient in recipe_data["ingredients"]:
        print(ingredient)

    return recipe_data

if __name__ == "__main__":
    url = "https://www.allrecipes.com/recipe/12349/raspberry-pie-iii/"
    get_recipe(url)