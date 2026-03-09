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
    print('"Recipe"' in response.text)
    print('"recipeIngredient"' in response.text)
    print('"@type": "Recipe"' in response.text)
    print('"@type":"Recipe"' in response.text)

    if response.status_code != 200:
        print(f"Request failed with status code: {response.status_code}")
        return None
    
    recipe = None

    for script in scripts:
        print("SCRIPT START:")
        print(script.get_text()[:300])
        print()

        try:
            data = json.loads(script.get_text())
        except:
            print("JSON parse failed")
            continue

        if isinstance(data, list):
            for item in data:
                if isinstance(item, dict) and item.get("@type") == "Recipe":
                    recipe = item
                    break

            if recipe:
                break

            continue
        
        print("top level @type:", data.get("@type"))

        if data.get("@type") == "Recipe":
            recipe = data
            break

        if "@graph" in data:
            for item in data["@graph"]:
                print("graph item @type:", item.get("@type"))
                if item.get("@type") == "Recipe":
                    recipe = item
                    break

        if recipe:
            break

    if recipe is None:
        return None
    
    print(recipe.keys())

    recipe_data = {
        "name": recipe.get("name"),
        "ingredients": recipe.get("recipeIngredient")
    }

    print(recipe_data["name"])
    print()

    if recipe_data["ingredients"] is None:
        print("No ingredients found in recipe schema.")
    else:
        for ingredient in recipe_data["ingredients"]:
            print(ingredient)

    return recipe_data

if __name__ == "__main__":
    url = "https://www.kraftheinz.com/jell-o/recipes/551923-chocolate-pudding-pie-recipe"
    if not url.startswith("http://") and not url.startswith("https://"):
        print("Invalid URL")
    else:
        get_recipe(url)