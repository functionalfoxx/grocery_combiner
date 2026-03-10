from fractions import Fraction
import re

INVALID_STANDALONE_INGREDIENTS = {
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

LEADING_CONTAINER_WORDS = {
    "one",
    "two",
    "three",
    "four",
    "five",
    "six",
    "seven",
    "eight",
    "nine",
    "ten",
    "eleven",
    "twelve",
}

LEADING_DESCRIPTORS = {
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

PACKAGING_WORDS = {
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

UNICODE_FRACTIONS = {
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

WRITTEN_FRACTION_PREFIXES = {
    "half of an ": "1/2 ",
    "half of a ": "1/2 ",
    "half an ": "1/2 ",
    "half a ": "1/2 ",
    "a half ": "1/2 ",
    "quarter of an ": "1/4 ",
    "quarter of a ": "1/4 ",
    "a quarter of an ": "1/4 ",
    "a quarter of a ": "1/4 ",
    "quarter an ": "1/4 ",
    "quarter a ": "1/4 ",
}

WRITTEN_NUMBERS = {
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

def add_recipe(all_recipes, recipe_data):
    if recipe_data is not None:
        all_recipes.append(recipe_data)
    return all_recipes

def normalize_text(text):
    normalized = text.strip().lower()

    for dash in ["‐", "‒", "–", "—", "−"]:
        normalized = normalized.replace(dash, "-")

    normalized = normalized.replace("&nbsp;", " ")

    return " ".join(normalized.split())

def normalize_written_fractions(text):
    for old, new in WRITTEN_FRACTION_PREFIXES.items():
        if text.startswith(old):
            return text.replace(old, new, 1)
    return text

def clean_ingredient_phrase(text):
    parts = [part.strip() for part in text.split(",")]

    if len(parts) == 1:
        cleaned = text
    else:
        first_part_words = parts[0].split()

        if first_part_words and all(word in LEADING_DESCRIPTORS for word in first_part_words):
            cleaned = " ".join(parts[:2]).strip()
        else:
            cleaned = parts[0]

    words = cleaned.split()

    while words and words[0] in LEADING_DESCRIPTORS:
        words.pop(0)

    if words and words[0] == "of":
        words.pop(0)

    cleaned = " ".join(words)

    if cleaned.startswith("toppings: "):
        cleaned = cleaned.replace("toppings: ", "", 1)

    trailing_words = {"thinly", "sliced"}
    words = cleaned.split()

    while words and words[-1] in trailing_words:
        words.pop()

    cleaned = " ".join(words)

    return cleaned.rstrip(",.* ")

def remove_leading_container_words(text):
    words = text.split()

    while words and words[0] in LEADING_CONTAINER_WORDS:
        words.pop(0)

    return " ".join(words)

def remove_leading_packaging_phrases(text):
    patterns = [
        r'^\d+(?:\.\d+)?(?:-\d+/\d+)?\s*-\s*ounce\s+(?:can|cans|container|containers|package|packages|pack|packs|jar|jars|box|boxes|bag|bags)\s+',
        r'^\d+(?:\.\d+)?(?:-\d+/\d+)?\s*-\s*oz\.?\s+(?:can|cans|container|containers|package|packages|pack|packs|jar|jars|box|boxes|bag|bags)\s+',
        r'^\d+(?:\.\d+)?(?:-\d+/\d+)?[- ]?ounce\s+(?:can|cans|container|containers|package|packages|pack|packs|jar|jars|box|boxes|bag|bags)\s+',
        r'^\d+(?:\.\d+)?(?:-\d+/\d+)?[- ]?oz\.?\s+(?:can|cans|container|containers|package|packages|pack|packs|jar|jars|box|boxes|bag|bags)\s+',
        r'^\d+(?:\.\d+)?(?:-\d+/\d+)?\s*-\s*gram\s+(?:can|cans|container|containers|package|packages|pack|packs|jar|jars|box|boxes|bag|bags)\s+',
        r'^\d+(?:\.\d+)?(?:-\d+/\d+)?[- ]?gram\s+(?:can|cans|container|containers|package|packages|pack|packs|jar|jars|box|boxes|bag|bags)\s+',
        r'^(?:can|cans|container|containers|package|packages|pack|packs|jar|jars|box|boxes|bag|bags)\s+',
    ]

    cleaned = text

    for pattern in patterns:
        cleaned = re.sub(pattern, '', cleaned).strip()

    return cleaned

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

    while words:
        first = words[0].lower().strip(".,")
        normalized_first = first.replace("–", "-").replace("—", "-")

        if re.match(r"^\d+(?:\.\d+)?(?:-\d+/\d+)?(?:-(?:ounce|ounces|oz|lb|lbs|pound|pounds))$", normalized_first):
            words.pop(0)
            continue

        if re.match(r"^\d+(?:\.\d+)?$", normalized_first):
            words.pop(0)
            continue

        if normalized_first in PACKAGING_WORDS:
            words.pop(0)
            continue

        break

    return " ".join(words)

def is_invalid_standalone_ingredient(text):
    return text.strip() in INVALID_STANDALONE_INGREDIENTS

def extract_quantity(ingredient):
    words = ingredient.split()

    if len(words) == 0:
        return None

    first_word = words[0].lower().strip(",")
    first_word = first_word.replace("–", "-").replace("—", "-")

    if len(words) > 2 and first_word in WRITTEN_NUMBERS:
        second_word = words[1].lower().strip(",.")
        third_word = words[2].lower().strip(",.")
        second_word = second_word.replace("–", "-").replace("—", "-")

        ounce_match = re.match(r"^(\d+(?:\.\d+)?)-ounce$", second_word)
        oz_match = re.match(r"^(\d+(?:\.\d+)?)-oz$", second_word)

        if ounce_match and third_word in {"can", "cans"}:
            package_size = float(ounce_match.group(1))
            return WRITTEN_NUMBERS[first_word] * package_size

        if oz_match and third_word in {"can", "cans"}:
            package_size = float(oz_match.group(1))
            return WRITTEN_NUMBERS[first_word] * package_size

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

    if len(words) > 1 and words[1] in UNICODE_FRACTIONS:
        try:
            whole = float(words[0])
            fraction = float(Fraction(UNICODE_FRACTIONS[words[1]]))
            return round(whole + fraction, 2)
        except ValueError:
            pass

    if first_word in UNICODE_FRACTIONS:
        return round(float(Fraction(UNICODE_FRACTIONS[first_word])), 2)

    if "/" in first_word:
        return round(float(Fraction(first_word)), 2)

    try:
        return float(first_word)
    except ValueError:
        pass

    if first_word in WRITTEN_NUMBERS:
        return WRITTEN_NUMBERS[first_word]

    return None

def remove_leading_written_number(text):
    words = text.split()

    if not words:
        return text

    if words[0] in WRITTEN_NUMBERS:
        return " ".join(words[1:])

    return text

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

    first_word = words[0].lower().strip(",")
    first_word = first_word.replace("–", "-").replace("—", "-")

    attached_match = re.match(r"^(\d+(?:\.\d+)?|\.\d+)([a-z]+)\.?$", first_word)
    if attached_match:
        unit_word = singularize_unit(attached_match.group(2))
        return unit_map.get(unit_word)

    if len(words) > 2 and first_word in WRITTEN_NUMBERS:
        second_word = words[1].lower().strip(",")
        third_word = words[2].lower().strip(",")
        second_word = second_word.replace("–", "-").replace("—", "-")

        if re.match(r"^\d+(?:\.\d+)?-ounce$", second_word) and third_word in {"can", "cans"}:
            return "oz"

        if re.match(r"^\d+(?:\.\d+)?-oz$", second_word) and third_word in {"can", "cans"}:
            return "oz"

    if len(words) > 2:
        second_word = words[1].lower().strip(",")
        third_word = words[2].lower().strip(",")
        third_word = singularize_unit(third_word)

        if first_word.replace(".", "", 1).isdigit():
            if "/" in second_word or second_word in UNICODE_FRACTIONS:
                return unit_map.get(third_word)

    if len(words) > 1:
        second_word = words[1].lower().strip(",")
        second_word = singularize_unit(second_word)

        if first_word.replace(".", "", 1).isdigit():
            return unit_map.get(second_word)

        if "/" in first_word:
            return unit_map.get(second_word)

        if first_word in UNICODE_FRACTIONS:
            return unit_map.get(second_word)

        if first_word in WRITTEN_NUMBERS:
            return unit_map.get(second_word)

    first_word = singularize_unit(first_word)
    return unit_map.get(first_word)

def remove_leading_unit(ingredient):
    words = ingredient.split()

    if not words:
        return ingredient

    first_word = words[0].lower().strip(",.")
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

def remove_parenthetical_text(text):
    return re.sub(r"\([^)]*\)|\[[^\]]*\]", "", text).strip()

def normalize_quantity_ranges(ingredient):
    pattern = r'^\s*(\d+(?:\.\d+)?|\d+/\d+|[¼½¾⅓⅔⅛⅜⅝⅞])\s*(?:to|-|–|—)\s*(\d+(?:\.\d+)?|\d+/\d+|[¼½¾⅓⅔⅛⅜⅝⅞])\s+'
    return re.sub(pattern, r'\1 ', ingredient).strip()

def collect_ingredients(all_recipes):
    all_ingredients = []

    for recipe in all_recipes:
        ingredients = recipe["ingredients"]

        for ingredient in ingredients:
            normalized = normalize_text(ingredient)
            normalized = normalize_written_fractions(normalized)
            no_parentheses = remove_parenthetical_text(normalized)
            normalized_ranges = normalize_quantity_ranges(no_parentheses)
            cleaned = remove_filler_words(normalized_ranges)

            quantity = extract_quantity(cleaned)
            unit = extract_unit(cleaned)

            no_amount = remove_leading_quantity(cleaned)
            no_amount = remove_leading_written_number(no_amount)
            no_unit = remove_leading_unit(no_amount)
            no_unit = remove_leading_plus_quantity_phrase(no_unit)
            no_packaging = remove_leading_packaging_words(no_unit)

            final_ingredient = normalize_text(no_packaging)
            final_ingredient = clean_ingredient_phrase(final_ingredient)
            final_ingredient = remove_duplicate_adjacent_words(final_ingredient)
            final_ingredient = remove_leading_container_words(final_ingredient)
            final_ingredient = remove_leading_packaging_phrases(final_ingredient)
            final_ingredient = normalize_text(final_ingredient)

            if final_ingredient in {"garlic clove", "garlic cloves"}:
                final_ingredient = "garlic"
                if unit is None:
                    unit = "clove"

            if final_ingredient == "warm water" or final_ingredient == "white pepper":
                print("TRACE")
                print("original:", ingredient)
                print("quantity:", quantity)
                print("unit:", unit)
                print("final_ingredient:", final_ingredient)
                print()

            if final_ingredient != "" and not is_invalid_standalone_ingredient(final_ingredient):
                all_ingredients.append((quantity, unit, final_ingredient))

    return all_ingredients

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

    for quantity, unit, ingredient in all_ingredients:
        name = ingredient.strip()
        name = singularize_ingredient(name)
        key = (name, unit)

        if key in ingredient_counts:
            if quantity is not None:
                if ingredient_counts[key] is None:
                    ingredient_counts[key] = quantity
                else:
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
                display_name = ingredient

                if quantity == 1:
                    if ingredient == "bay leaves":
                        display_name = "bay leaf"
                else:
                    if ingredient != "bay leaves" and not ingredient.endswith("s"):
                        display_name = ingredient + "s"

                print(quantity, display_name)
            else:
                print(quantity, unit, ingredient)

    print()