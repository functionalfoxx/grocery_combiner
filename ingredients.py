from fractions import Fraction
import re

leading_descriptors = {
    "beaten",
    "boneless",
    "chilled",
    "chopped",
    "cooled",
    "crushed",
    "defrosted",
    "deveined",
    "diced",
    "drained",
    "fresh",
    "frozen",
    "grated",
    "ground",
    "halved",
    "juiced",
    "julienned",
    "large",
    "levelled",
    "leveled",
    "melted",
    "minced",
    "optional",
    "packed",
    "peeled",
    "pitted",
    "quartered",
    "rinsed",
    "room-temperature",
    "room temperature",
    "sauteed",
    "sautéed",
    "shredded",
    "skinless",
    "sliced",
    "small",
    "softened",
    "thinly",
    "toasted",
    "trimmed",
    "warmed",
    "zested"
}

def add_recipe(all_recipes, recipe_data):
    if recipe_data is not None:
        all_recipes.append(recipe_data)
    return all_recipes

def normalize_ingredient(ingredient):
    normalized = ingredient.strip().lower()
    normalized = normalized.replace("&nbsp;", " ")
    return normalized

def normalize_spaces(text):
    words = text.split()
    return " ".join(words)

def remove_trailing_punctuation(text):
    return text.rstrip(",.* ")

def remove_comma_descriptors(text):
    parts = [part.strip() for part in text.split(",")]

    if len(parts) == 1:
        return text

    first_part_words = parts[0].split()

    if len(first_part_words) > 0 and all(word in leading_descriptors for word in first_part_words):
        return " ".join(parts[:2]).strip()

    return parts[0]

def remove_leading_descriptors(text):
    words = text.split()

    if len(words) == 0:
        return text

    while len(words) > 0 and words[0] in leading_descriptors:
        words.pop(0)

    return " ".join(words)

def extract_quantity(ingredient):
    words = ingredient.split()

    if len(words) == 0:
        return None

    first_word = words[0].lower().strip(",")

    unicode_fractions = {
        "¼": "1/4",
        "½": "1/2",
        "¾": "3/4",
        "⅓": "1/3",
        "⅔": "2/3",
        "⅛": "1/8",
        "⅜": "3/8",
        "⅝": "5/8",
        "⅞": "7/8"
    }

    attached_match = re.match(r"^(\d+(?:\.\d+)?)([a-z]+)$", first_word)
    if attached_match:
        return float(attached_match.group(1))

    hyphen_unit_match = re.match(r"^(\d+(?:\.\d+)?)-[a-z]+$", first_word)
    if hyphen_unit_match:
        return float(hyphen_unit_match.group(1))

    if "-" in first_word and "/" in first_word:
        parts = first_word.split("-")
        if len(parts) == 2:
            try:
                whole = float(parts[0])
                fraction = float(Fraction(parts[1]))
                return round(whole + fraction, 2)
            except ValueError:
                pass

    if len(words) > 1 and "/" in words[1]:
        try:
            whole = float(words[0])
            fraction = float(Fraction(words[1]))
            return round(whole + fraction, 2)
        except ValueError:
            pass

    if len(words) > 1 and words[1] in unicode_fractions:
        try:
            whole = float(words[0])
            fraction = float(Fraction(unicode_fractions[words[1]]))
            return round(whole + fraction, 2)
        except ValueError:
            pass

    if first_word in unicode_fractions:
        return round(float(Fraction(unicode_fractions[first_word])), 2)

    if "/" in first_word:
        return round(float(Fraction(first_word)), 2)

    try:
        return float(first_word)
    except ValueError:
        return None
    
def remove_leading_quantity(ingredient):
    pattern = r'^\s*(?:\d+(?:\.\d+)?-[a-z]+\.?|\d+(?:\.\d+)?[a-z]+\.?|\.\d+|\d+(?:\.\d+)?\s*[¼½¾⅐⅑⅒⅓⅔⅕⅖⅗⅘⅙⅚⅛⅜⅝⅞]|\d+(?:\.\d+)?(?:\s+\d+/\d+|-\d+/\d+|/\d+)?|[¼½¾⅐⅑⅒⅓⅔⅕⅖⅗⅘⅙⅚⅛⅜⅝⅞])\s*'
    return re.sub(pattern, '', ingredient).strip()

def singularize_unit(word):
    if word.endswith("ches"):
        return word[:-2]
    if word.endswith("xes"):
        return word[:-2]
    if word.endswith("ses"):
        return word[:-2]
    if word.endswith("s") and not word.endswith("ss"):
        return word[:-1]
    return word

unit_map = {
        "bag": "bag",
        "bottle": "bottle",
        "box": "box",
        "bulb": "bulb",
        "bunch": "bunch",
        "c": "cup",
        "can": "can",
        "carton": "carton",
        "clove": "clove",
        "container": "container",
        "cup": "cup",
        "dash": "dash",
        "drizzle": "drizzle",
        "drop": "drop",
        "ear": "ear",
        "g": "g",
        "gram": "g",
        "head": "head",
        "jar": "jar",
        "kg": "kg",
        "kilogram": "kg",
        "l": "l",
        "lb": "lb",
        "liter": "l",
        "litre": "l",
        "loaf": "loaf",
        "ml": "ml",
        "milliliter": "ml",
        "millilitre": "ml",
        "ounce": "oz",
        "oz": "oz",
        "pack": "pack",
        "package": "package",
        "packet": "packet",
        "piece": "piece",
        "pinch": "pinch",
        "pkg": "package",
        "pouch": "pouch",
        "pound": "lb",
        "rib": "rib",
        "sheet": "sheet",
        "slice": "slice",
        "splash": "splash",
        "sprig": "sprig",
        "stalk": "stalk",
        "stick": "stick",
        "tablespoon": "tbsp",
        "tbsp": "tbsp",
        "teaspoon": "tsp",
        "tsp": "tsp",
        "tub": "tub",
        "tube": "tube",
        "wedge": "wedge",
    }

def extract_unit(ingredient):
    words = ingredient.split()

    if not words:
        return None

    first_word = words[0].lower().strip(",")
    attached_match = re.match(r"^(\d+(?:\.\d+)?|\.\d+)([a-z]+)\.?$", first_word)

    if attached_match:
        unit_word = singularize_unit(attached_match.group(2))
        return unit_map.get(unit_word)

    unicode_fractions = {
        "¼", "½", "¾", "⅓", "⅔", "⅛", "⅜", "⅝", "⅞"
    }

    if len(words) > 2:
        second_word = words[1].lower().strip(",.")
        third_word = words[2].lower().strip(",.")
        third_word = singularize_unit(third_word)

        if first_word.replace(".", "", 1).isdigit():
            if "/" in second_word or second_word in unicode_fractions:
                return unit_map.get(third_word)

    if len(words) > 1:
        second_word = words[1].lower().strip(",.")
        second_word = singularize_unit(second_word)

        if first_word.replace(".", "", 1).isdigit():
            return unit_map.get(second_word)

        if "/" in first_word:
            return unit_map.get(second_word)

        if first_word in unicode_fractions:
            return unit_map.get(second_word)

    first_word = singularize_unit(first_word)
    return unit_map.get(first_word)

def remove_leading_unit(ingredient):
    words = ingredient.split()

    if not words:
        return ingredient

    first_word = words[0].lower().strip(".,")
    first_word = singularize_unit(first_word)

    if first_word in unit_map:
        return " ".join(words[1:])

    return ingredient

def remove_filler_words(ingredient):
    filler_phrases = [
        "about",
        "approximately",
        "as desired",
        "as needed",
        "at room temperature",
        "divided",
        "extra for garnish",
        "extra for serving",
        "extra for topping",
        "for garnish",
        "for serving",
        "for topping",
        "if desired",
        "more to taste",
        "or frozen",
        "or more",
        "or more to taste",
        "plus a little extra",
        "plus a little extra for frying",
        "plus more",
        "plus more for serving",
        "plus more to taste",
        "such as",
        "to brush",
        "to coat",
        "to drizzle",
        "to dust",
        "to finish",
        "to garnish",
        "to grease",
        "to line",
        "to serve",
        "to sprinkle",
        "to taste",
        "to top"
    ]

    cleaned = ingredient

    for phrase in filler_phrases:
        cleaned = cleaned.replace(phrase, "")

    words = cleaned.split()
    filler_words = [
        "about",
        "approximately",
        "divided",
        "extra",
        "garnish",
        "optional",
        "roughly",
        "such",
    ]

    cleaned_words = []

    for word in words:
        if word not in filler_words:
            cleaned_words.append(word)

    return " ".join(cleaned_words)

def remove_parentheses(ingredient):
    result = ""
    skip = False

    for char in ingredient:
        if char == "(":
            skip = True
        elif char == ")":
            skip = False
        elif not skip:
            result += char

    return result.strip()

def remove_brackets(ingredient):
    result = ""
    skip = False

    for char in ingredient:
        if char == "[":
            skip = True
        elif char == "]":
            skip = False
        elif not skip:
            result += char

    return result.strip()

def normalize_quantity_ranges(ingredient):
    pattern = r'^\s*(\d+(?:\.\d+)?|\d+/\d+|[¼½¾⅓⅔⅛⅜⅝⅞])\s*(?:to|-|–|—)\s*(\d+(?:\.\d+)?|\d+/\d+|[¼½¾⅓⅔⅛⅜⅝⅞])\s+'
    return re.sub(pattern, r'\1 ', ingredient).strip()

def remove_repeated_leading_word(text):
    words = text.split()

    if len(words) >= 2 and words[0] == words[1]:
        return " ".join(words[1:])

    return text

def collect_ingredients(all_recipes):
    all_ingredients = []

    for recipe in all_recipes:
        ingredients = recipe["ingredients"]

        for ingredient in ingredients:
            quantity = extract_quantity(ingredient)
            normalized = normalize_ingredient(ingredient)
            no_parentheses = remove_parentheses(normalized)
            no_brackets = remove_brackets(no_parentheses)
            normalized_ranges = normalize_quantity_ranges(no_brackets)
            cleaned = remove_filler_words(normalized_ranges)
            no_amount = remove_leading_quantity(cleaned)
            unit = extract_unit(cleaned)
            no_unit = remove_leading_unit(no_amount)
            final_ingredient = normalize_spaces(no_unit)
            final_ingredient = remove_repeated_leading_word(final_ingredient)
            final_ingredient = remove_comma_descriptors(final_ingredient)
            final_ingredient = remove_leading_descriptors(final_ingredient)
            final_ingredient = remove_trailing_punctuation(final_ingredient)

            if final_ingredient != "":
                all_ingredients.append((quantity, unit, final_ingredient))

    return all_ingredients

def get_ingredient_name(ingredient):
    return ingredient.strip()

def singularize_ingredient(name):
    if " and " in name:
        return name

    if name.endswith("ies"):
        return name[:-3] + "y"
    
    if name.endswith("oes"):
        return name[:-2]
    
    if name.endswith("ves"):
        return name[:-3] + "f"

    if name.endswith("s") and not name.endswith("ss"):
        return name[:-1]

    return name

def count_ingredients(all_ingredients):
    ingredient_counts = {}

    for item in all_ingredients:
        quantity, unit, ingredient = item
        name = get_ingredient_name(ingredient)
        name = singularize_ingredient(name)
        key = (name, unit)

        if quantity is None:
            quantity = 1

        if key in ingredient_counts:
            ingredient_counts[key] += quantity
            
        else:
            ingredient_counts[key] = quantity

    return ingredient_counts

def display_grocery_list(ingredient_counts):
    print("\nGROCERY LIST\n")

    for (ingredient, unit) in sorted(ingredient_counts, key=lambda item: ((item[0] or ""), (item[1] or ""))):
        quantity = round(ingredient_counts[(ingredient, unit)], 2)

        if unit is None:
            print(quantity, ingredient)
        else:
            print(quantity, unit, ingredient)

    print()