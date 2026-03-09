import requests
from bs4 import BeautifulSoup
import json

def get_recipe(url):

    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})

    print("Status code:", response.status_code)
    print("Final URL:", response.url)
    print("HTML preview:", response.text[:500])

    soup = BeautifulSoup(response.text, "html.parser")
    scripts = soup.find_all("script", type="application/ld+json")

    print("JSON blocks found:", len(scripts))

    if response.status_code != 200:
        print(f"Request failed with status code: {response.status_code}")
        return None
    
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
    url = "https://www.foodnetwork.com/recipes/food-network-kitchen/chicken-fettuccine-alfredo-3364118"
    get_recipe(url)