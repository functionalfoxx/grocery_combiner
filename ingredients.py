from fractions import Fraction
import re

leading_descriptors = {
    "beaten",
    "boiling",
    "boneless",
    "chilled",
    "chopped",
    "cold",
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
    "skin-on",
    "skin on",
    "skinless",
    "sliced",
    "small",
    "softened",
    "steamed",
    "stemmed",
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
    normalized = normalized.replace("‐", "-")
    normalized = normalized.replace("-", "-")
    normalized = normalized.replace("‒", "-")
    normalized = normalized.replace("–", "-")
    normalized = normalized.replace("—", "-")
    normalized = normalized.replace("−", "-")
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

def remove_leading_of(text):
    if text.startswith("of "):
        return text[3:]
    return text

def remove_toppings_prefix(text):
    if text.startswith("toppings: "):
        return text.replace("toppings: ", "", 1)
    return text

def remove_trailing_prep_words(text):
    trailing_words = {
        "thinly",
        "sliced",
    }

    words = text.split()

    while len(words) > 0 and words[-1] in trailing_words:
        words.pop()

    return " ".join(words)

def remove_leading_container_words(text):
    leading_words = {
        "one",
        "two",
    }

    words = text.split()

    while len(words) > 0 and words[0] in leading_words:
        words.pop(0)

    return " ".join(words)

def remove_leading_packaging_phrases(text):
    patterns = [
        r'^\d+(?:\.\d+)?(?:-\d+/\d+)?\s*-\s*ounce\s+(?:can|cans|container|containers|package|packages|pack|packs|jar|jars|box|boxes|bag|bags)\s+',
        r'^\d+(?:\.\d+)?(?:-\d+/\d+)?\s*-\s*oz\.?\s+(?:can|cans|container|containers|package|packages|pack|packs|jar|jars|box|boxes|bag|bags)\s+',
        r'^\d+(?:\.\d+)?(?:-\d+/\d+)?[- ]?ounce\s+(?:can|cans|container|containers|package|packages|pack|packs|jar|jars|box|boxes|bag|bags)\s+',
        r'^\d+(?:\.\d+)?(?:-\d+/\d+)?[- ]?oz\.?\s+(?:can|cans|container|containers|package|packages|pack|packs|jar|jars|box|boxes|bag|bags)\s+',
        r'^(?:can|cans|container|containers|package|packages|pack|packs|jar|jars|box|boxes|bag|bags)\s+',
    ]

    cleaned = text

    for pattern in patterns:
        cleaned = re.sub(pattern, '', cleaned).strip()

    return cleaned

print(remove_leading_packaging_phrases("28-ounce can fire roasted crushed tomatoes"))
print(remove_leading_packaging_phrases("14-ounce cans beans"))

def remove_duplicate_adjacent_words(text):
    words = text.split()

    if not words:
        return text

    cleaned_words = [words[0]]

    for word in words[1:]:
        if word != cleaned_words[-1]:
            cleaned_words.append(word)

    return " ".join(cleaned_words)

def remove_leading_packaging_words(text):
    words = text.split()

    packaging_words = {
        "bag", "bags",
        "box", "boxes",
        "can", "cans",
        "container", "containers",
        "jar", "jars",
        "package", "packages",
        "pack", "packs",
        "packet", "packets",
        "pouch", "pouches",
        "ounce", "ounces",
        "oz",
        "oz.",
        "lb",
        "lb.",
        "lbs",
        "lbs.",
        "pound",
        "pounds"
    }

    while words:
        first = words[0].lower().strip(".,")
        normalized_first = first.replace("–", "-").replace("—", "-")

        if re.match(r"^\d+(?:\.\d+)?(?:-\d+/\d+)?(?:-(?:ounce|ounces|oz|lb|lbs|pound|pounds))$", normalized_first):
            words.pop(0)
            continue

        if re.match(r"^\d+(?:\.\d+)?$", normalized_first):
            words.pop(0)
            continue

        if normalized_first in packaging_words:
            words.pop(0)
            continue

        break

    return " ".join(words)

def is_bad_ingredient(text):
    bad_standalones = {
        "skin-on",
        "skin off",
        "skin-on bone-in",
        "bone-in",
        "boneless",
        "boneless skinless",
        "ground",
        "fresh",
        "frozen"
    }

    return text.strip() in bad_standalones

def extract_quantity(ingredient):
    words = ingredient.split()

    if len(words) == 0:
        return None

    written_numbers = {
        "one": 1.0,
        "two": 2.0,
        "three": 3.0,
        "four": 4.0,
        "five": 5.0,
        "six": 6.0,
        "seven": 7.0,
        "eight": 8.0,
        "nine": 9.0,
        "ten": 10.0
    }

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

    first_word = words[0].lower().strip(",.")
    first_word = first_word.replace("–", "-").replace("—", "-")

    if len(words) > 2 and first_word in written_numbers:
        second_word = words[1].lower().strip(",.")
        third_word = words[2].lower().strip(",.")
        second_word = second_word.replace("–", "-").replace("—", "-")

        ounce_match = re.match(r"^(\d+(?:\.\d+)?)-ounce$", second_word)
        oz_match = re.match(r"^(\d+(?:\.\d+)?)-oz$", second_word)

        if ounce_match and third_word in {"can", "cans"}:
            package_size = float(ounce_match.group(1))
            return written_numbers[first_word] * package_size

        if oz_match and third_word in {"can", "cans"}:
            package_size = float(oz_match.group(1))
            return written_numbers[first_word] * package_size

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
        pass

    if first_word in written_numbers:
        return written_numbers[first_word]

    return None
    
def remove_leading_quantity(ingredient):
    pattern = r'^\s*(?:(?:plus\s+)?\d+(?:\.\d+)?\s+[¼½¾⅐⅑⅒⅓⅔⅕⅖⅗⅘⅙⅚⅛⅜⅝⅞]\s+|(?:plus\s+)?\d+[¼½¾⅐⅑⅒⅓⅔⅕⅖⅗⅘⅙⅚⅛⅜⅝⅞]\s+|(?:plus\s+)?\d+(?:\.\d+)?\s+and\s+\d+/\d+\s+|(?:plus\s+)?\d+(?:\.\d+)?\s+and\s+[¼½¾⅐⅑⅒⅓⅔⅕⅖⅗⅘⅙⅚⅛⅜⅝⅞]\s+|(?:plus\s+)?\d+(?:\.\d+)?\s+\d+/\d+\s+|(?:plus\s+)?\d+(?:\.\d+)?-\d+/\d+\s+|(?:plus\s+)?\d+/\d+\s+|(?:plus\s+)?[¼½¾⅐⅑⅒⅓⅔⅕⅖⅗⅘⅙⅚⅛⅜⅝⅞]\s+|(?:plus\s+)?\d+(?:\.\d+)?-[a-z]+\.?\s+|(?:plus\s+)?\d+(?:\.\d+)?[a-z]+\.?\s+|(?:plus\s+)?\.\d+\s+|(?:plus\s+)?\d+(?:\.\d+)?\s+)'
    return re.sub(pattern, '', ingredient).strip()

def remove_leading_plus_quantity_phrase(text):
    pattern = r'^\s*plus\s+(?:\d+(?:\.\d+)?\s+[¼½¾⅐⅑⅒⅓⅔⅕⅖⅗⅘⅙⅚⅛⅜⅝⅞]|\d+[¼½¾⅐⅑⅒⅓⅔⅕⅖⅗⅘⅙⅚⅛⅜⅝⅞]|\d+(?:\.\d+)?\s+and\s+\d+/\d+|\d+(?:\.\d+)?\s+and\s+[¼½¾⅐⅑⅒⅓⅔⅕⅖⅗⅘⅙⅚⅛⅜⅝⅞]|\d+(?:\.\d+)?\s+\d+/\d+|\d+(?:\.\d+)?-\d+/\d+|\d+/\d+|[¼½¾⅐⅑⅒⅓⅔⅕⅖⅗⅘⅙⅚⅛⅜⅝⅞]|\d+(?:\.\d+)?)\s+(?:[a-zA-Z]+)\s+'
    return re.sub(pattern, '', text).strip()

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

    written_numbers = {
        "one", "two", "three", "four", "five",
        "six", "seven", "eight", "nine", "ten"
    }

    unicode_fractions = {
        "¼", "½", "¾", "⅓", "⅔", "⅛", "⅜", "⅝", "⅞"
    }

    first_word = words[0].lower().strip(",.")
    first_word = first_word.replace("–", "-").replace("—", "-")

    attached_match = re.match(r"^(\d+(?:\.\d+)?|\.\d+)([a-z]+)\.?$", first_word)
    if attached_match:
        unit_word = singularize_unit(attached_match.group(2))
        return unit_map.get(unit_word)

    if len(words) > 2 and first_word in written_numbers:
        second_word = words[1].lower().strip(",.")
        third_word = words[2].lower().strip(",.")
        second_word = second_word.replace("–", "-").replace("—", "-")

        if re.match(r"^\d+(?:\.\d+)?-ounce$", second_word) and third_word in {"can", "cans"}:
            return "oz"

        if re.match(r"^\d+(?:\.\d+)?-oz$", second_word) and third_word in {"can", "cans"}:
            return "oz"

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

        if first_word in written_numbers:
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
            normalized = normalize_ingredient(ingredient)
            quantity = extract_quantity(normalized)
            no_parentheses = remove_parentheses(normalized)
            no_brackets = remove_brackets(no_parentheses)
            normalized_ranges = normalize_quantity_ranges(no_brackets)
            cleaned = remove_filler_words(normalized_ranges)
            no_amount = remove_leading_quantity(cleaned)
            unit = extract_unit(cleaned)
            no_unit = remove_leading_unit(no_amount)
            no_unit = remove_leading_plus_quantity_phrase(no_unit)
            no_unit = remove_leading_container_words(no_unit)
            no_packaging = remove_leading_packaging_words(no_unit)
            no_packaging = remove_leading_packaging_phrases(no_packaging)
            final_ingredient = normalize_spaces(no_packaging)
            final_ingredient = remove_comma_descriptors(final_ingredient)
            final_ingredient = remove_leading_descriptors(final_ingredient)
            final_ingredient = remove_duplicate_adjacent_words(final_ingredient)
            final_ingredient = remove_leading_of(final_ingredient)
            final_ingredient = remove_toppings_prefix(final_ingredient)
            final_ingredient = remove_trailing_prep_words(final_ingredient)
            final_ingredient = remove_trailing_punctuation(final_ingredient)

            quantity, unit, final_ingredient = normalize_garlic_cloves(
                quantity, unit, final_ingredient
            )

            if final_ingredient != "" and not is_bad_ingredient(final_ingredient):
                all_ingredients.append((quantity, unit, final_ingredient))

    return all_ingredients

def get_ingredient_name(ingredient):
    return ingredient.strip()

def normalize_garlic_cloves(quantity, unit, ingredient):
    if ingredient == "garlic cloves":
        return quantity, "clove", "garlic"
    if ingredient == "clove garlic":
        return quantity, "clove", "garlic"
    if ingredient == "garlic clove":
        return quantity, "clove", "garlic"
    return quantity, unit, ingredient

def singularize_ingredient(name):
    if " and " in name:
        return name

    no_change = {
        "baby potatoes",
        "bay leaves",
        "beans",
        "black beans",
        "breadcrumbs",
        "chickpeas",
        "chips",
        "chocolate chips",
        "crushed tomatoes",
        "diced tomatoes",
        "fire roasted crushed tomatoes",
        "fire roasted diced tomatoes",
        "fire roasted tomatoes",
        "garbanzo beans",
        "graham cracker crumbs",
        "green peas",
        "greens",
        "hash browns",
        "kidney beans",
        "milk chocolate chips",
        "mixed greens",
        "oats",
        "peanut butter chips",
        "peas",
        "pinto beans",
        "potatoes",
        "rolled oats",
        "semisweet chocolate chips",
        "snap peas",
        "tomatoes",
        "white beans",
        "yukon gold potatoes",
    }

    if name in no_change:
        return name

    if name.endswith("ies"):
        return name[:-3] + "y"

    if name.endswith("oes"):
        return name[:-2]

    if name.endswith("ves"):
        if name.endswith("cloves"):
            return name[:-1]
        return name

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

        if key in ingredient_counts:
            if quantity is not None:
                ingredient_counts[key] += quantity
        else:
            ingredient_counts[key] = quantity

    return ingredient_counts

def display_grocery_list(ingredient_counts):
    print("\nGROCERY LIST\n")

    for (ingredient, unit) in sorted(ingredient_counts, key=lambda item: ((item[0] or ""), (item[1] or ""))):
        quantity = ingredient_counts[(ingredient, unit)]

        if quantity is None:
            if unit is None:
                print(ingredient)
            else:
                print(unit, ingredient)
        else:
            quantity = round(quantity, 2)
            if unit is None:
                print(quantity, ingredient)
            else:
                print(quantity, unit, ingredient)

    print()