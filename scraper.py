import requests
from bs4 import BeautifulSoup
import json

url = "https://www.culinaryhill.com/blueberry-muffins/"

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

print(recipe.keys())
print(recipe["name"])
print()

for ingredient in recipe["recipeIngredient"]:
    print(ingredient)