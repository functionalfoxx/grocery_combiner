import requests
from bs4 import BeautifulSoup
import json

def get_recipe(url):

    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(response.text, "html.parser")
    scripts = soup.find_all("script", type="application/ld+json")
    json_text = scripts[0].get_text()
    data = json.loads(json_text)

    recipe = None
    for item in data["@graph"]:
        if item.get("@type") == "Recipe":
            recipe = item
            break

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
    url = "https://www.culinaryhill.com/blueberry-muffins/"
    get_recipe(url)