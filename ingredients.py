from fractions import Fraction
import re

FILLER_PHRASES = [
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

FILLER_WORDS = [
    "extra",
    "garnish",
    "optional",
    "roughly",
    "such",
]

INGREDIENTS_NO_SINGULARIZE = {
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
    "frozen",
    "grated",
    "ground",
    "halved",
    "juiced",
    "julienned",
    "levelled",
    "leveled",
    "melted",
    "minced",
    "optional",
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
    "softened",
    "steamed",
    "stemmed",
    "thinly",
    "toasted",
    "trimmed",
    "warmed",
    "zested"
}

PACKAGING_PHRASE_PATTERNS = [
    r'^\d+(?:\.\d+)?(?:-\d+/\d+)?\s*-\s*(?:ounce|oz\.?|gram)\s+(?:can|cans|container|containers|package|packages|pack|packs|jar|jars|box|boxes|bag|bags)\s+',
    r'^\d+(?:\.\d+)?(?:-\d+/\d+)?[- ]?(?:ounce|oz\.?|gram)\s+(?:can|cans|container|containers|package|packages|pack|packs|jar|jars|box|boxes|bag|bags)\s+',
    r'^(?:can|cans|container|containers|package|packages|pack|packs|jar|jars|box|boxes|bag|bags)\s+',
]

QUANTITY_TEXT_REPLACEMENTS = {
    "half": "1/2",
    "half a": "1/2",
    "half an": "1/2",
    "a half": "1/2",
    "an half": "1/2",
    "half of": "1/2",
    "a half of": "1/2",
    "one half": "1/2",
    "one-half": "1/2",

    "quarter": "1/4",
    "a quarter": "1/4",
    "an quarter": "1/4",
    "quarter of": "1/4",
    "a quarter of": "1/4",
    "one quarter": "1/4",
    "one-quarter": "1/4",

    "&": " ",
    " and ": " ",
    "-and-": " ",
    "-and": " ",
    "and-": " ",
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

UNIT_MAP = {
    "bag": "bag",
    "bags": "bag",

    "bottle": "bottle",
    "bottles": "bottle",

    "box": "box",
    "boxes": "box",

    "bulb": "bulb",
    "bulbs": "bulb",

    "bunch": "bunch",
    "bunches": "bunch",

    "c": "cup",
    "c.": "cup",
    "cp": "cup",
    "cp.": "cup",
    "cup": "cup",
    "cups": "cup",

    "can": "can",
    "cans": "can",

    "carton": "carton",
    "cartons": "carton",

    "clove": "clove",
    "cloves": "clove",

    "container": "container",
    "containers": "container",

    "dash": "dash",
    "dashes": "dash",

    "drizzle": "drizzle",
    "drizzles": "drizzle",

    "drop": "drop",
    "drops": "drop",

    "ear": "ear",
    "ears": "ear",

    "fl oz": "fl oz",
    "fluid ounce": "fl oz",
    "fluid ounces": "fl oz",

    "g": "g",
    "g.": "g",
    "gram": "g",
    "grams": "g",

    "gal": "gallon",
    "gal.": "gallon",
    "gallon": "gallon",
    "gallons": "gallon",

    "head": "head",
    "heads": "head",

    "jar": "jar",
    "jars": "jar",

    "kg": "kg",
    "kg.": "kg",
    "kilogram": "kg",
    "kilograms": "kg",

    "l": "l",
    "l.": "l",
    "liter": "l",
    "liters": "l",
    "litre": "l",
    "litres": "l",

    "lb": "lb",
    "lb.": "lb",
    "lbs": "lb",
    "lbs.": "lb",
    "pound": "lb",
    "pounds": "lb",

    "loaf": "loaf",
    "loaves": "loaf",

    "ml": "ml",
    "ml.": "ml",
    "milliliter": "ml",
    "milliliters": "ml",
    "millilitre": "ml",
    "millilitres": "ml",

    "ounce": "oz",
    "ounces": "oz",
    "oz": "oz",
    "oz.": "oz",

    "pack": "pack",
    "packs": "pack",

    "package": "package",
    "packages": "package",

    "packet": "packet",
    "packets": "packet",

    "piece": "piece",
    "pieces": "piece",

    "pinch": "pinch",
    "pinches": "pinch",

    "pkg": "package",
    "pkgs": "package",
    "pkg.": "package",
    "pkgs.": "package",

    "pouch": "pouch",
    "pouches": "pouch",

    "pt": "pint",
    "pt.": "pint",
    "pts": "pint",
    "pts.": "pint",
    "pint": "pint",
    "pints": "pint",

    "qt": "quart",
    "qt.": "quart",
    "qts": "quart",
    "qts.": "quart",
    "quart": "quart",
    "quarts": "quart",

    "rib": "rib",
    "ribs": "rib",

    "sheet": "sheet",
    "sheets": "sheet",

    "slice": "slice",
    "slices": "slice",

    "splash": "splash",
    "splashes": "splash",

    "sprig": "sprig",
    "sprigs": "sprig",

    "stalk": "stalk",
    "stalks": "stalk",

    "stick": "stick",
    "sticks": "stick",

    "tablespoon": "tbsp",
    "tablespoons": "tbsp",
    "tablespoonful": "tbsp",
    "tablespoonfuls": "tbsp",
    "tbsp": "tbsp",
    "tbsp.": "tbsp",
    "tbs": "tbsp",
    "tbs.": "tbsp",
    "tbl": "tbsp",
    "tbl.": "tbsp",

    "teaspoon": "tsp",
    "teaspoons": "tsp",
    "teaspoonful": "tsp",
    "teaspoonfuls": "tsp",
    "tsp": "tsp",
    "tsp.": "tsp",

    "tub": "tub",
    "tubs": "tub",

    "tube": "tube",
    "tubes": "tube",

    "wedge": "wedge",
    "wedges": "wedge",
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

RANGE_WORDS = {
    "to",
    "or",
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

    while words and words[-1] in LEADING_DESCRIPTORS:
        words.pop()

    while words and words[0] in LEADING_DESCRIPTORS:
        words.pop(0)

    cleaned = " ".join(words)

    if cleaned.startswith("toppings: "):
        cleaned = cleaned.replace("toppings: ", "", 1)

    return cleaned.rstrip(",.* ")

def normalize_specific_ingredients(name, unit):
    if name in {"garlic clove", "garlic cloves", "clove garlic"}:
        return "garlic", "clove"

    if name in {"basil leaves", "fresh basil"}:
        return "basil", unit

    if name in {"dill", "fresh dill"}:
        return "dill", unit

    if name in {"mint", "fresh mint"}:
        return "mint", unit

    if name in {"parsley", "fresh parsley"}:
        return "parsley", unit

    if name in {"thyme leaves", "fresh thyme leaves"}:
        return "thyme", unit

    if name in {"thyme sprig", "thyme sprigs", "fresh thyme sprig", "fresh thyme sprigs", "sprig thyme"}:
        return "thyme", "sprig"

    if name == "smoked mozzarella":
        return "smoked mozzarella", unit
    
    if name == "fresh stemmed kale":
        return "kale", unit

    if name == "thin slices smoked mozzarella":
        return "smoked mozzarella", "slice"

    return name, unit

def normalize_measurement_leftovers(name, quantity, unit):
    if name == "1/4 teaspoon table salt":
        return "salt", 0.25, "tsp"

    if name == "1/8 teaspoon pepper":
        return "pepper", 0.125, "tsp"

    if name == "4 cloves garlic":
        return "garlic", 4.0, "clove"

    if name == "4 tablespoons tomato paste":
        return "tomato paste", 4.0, "tbsp"

    if name == "7 sprigs mint":
        return "mint", 7.0, "sprig"

    if name == "7 sprigs rosemary":
        return "rosemary", 7.0, "sprig"

    if name == "2% milk" and quantity == 1.5 and unit is None:
        return "2% milk", 1.5, "cup"

    return name, quantity, unit

def remove_leading_packaging_phrases(text):
    cleaned = text

    for pattern in PACKAGING_PHRASE_PATTERNS:
        cleaned = re.sub(pattern, "", cleaned).strip()

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

def is_invalid_standalone_ingredient(text):
    return text.strip() in INVALID_STANDALONE_INGREDIENTS


def normalize_quantity_text(text):
    text = text.lower()

    for dash in ["‐", "‒", "–", "—", "−"]:
        text = text.replace(dash, "-")

    for sym, val in UNICODE_FRACTIONS.items():
        text = text.replace(sym, " " + val + " ")

    for k, v in QUANTITY_TEXT_REPLACEMENTS.items():
        text = text.replace(k, v)

    text = text.replace("(", " ").replace(")", " ")
    text = text.replace("[", " ").replace("]", " ")

    return " ".join(text.split())


def extract_quantity(text):
    text = normalize_quantity_text(text)
    words = text.split()

    if not words:
        return None

    first = words[0]

    attached_match = re.match(r"^(\d+(?:\.\d+)?|\.\d+)([a-zA-Z]+)\.?$", first)
    if attached_match:
        return float(attached_match.group(1))

    if re.match(r"^\d+[¼½¾⅓⅔⅛⅜⅝⅞]$", first):
        whole = float(first[:-1])
        frac = UNICODE_FRACTIONS[first[-1]]
        return whole + float(Fraction(frac))

    if first in {"1/2", "1/3", "2/3", "1/4", "3/4", "1/8", "3/8", "5/8", "7/8"}:
        return float(Fraction(first))

    if re.match(r"^\d+/\d+$", first):
        return float(Fraction(first))

    if re.match(r"^\d+(\.\d+)?-\d+/\d+$", first):
        whole, frac = first.split("-")
        return float(whole) + float(Fraction(frac))

    if re.match(r"^\d+(\.\d+)?$", first):
        value = float(first)

        if len(words) > 1 and re.match(r"^\d+/\d+$", words[1]):
            value += float(Fraction(words[1]))
            return value

        if len(words) > 2 and words[1] in RANGE_WORDS:
            second_value = None

            if re.match(r"^\d+(\.\d+)?$", words[2]):
                second_value = float(words[2])
            elif re.match(r"^\d+/\d+$", words[2]):
                second_value = float(Fraction(words[2]))
            elif words[2] in WRITTEN_NUMBERS:
                second_value = WRITTEN_NUMBERS[words[2]]

            if second_value is not None:
                return min(value, second_value)

        return value

    if first in WRITTEN_NUMBERS:
        value = WRITTEN_NUMBERS[first]

        if len(words) > 2 and words[1] in RANGE_WORDS:
            second_value = None

            if re.match(r"^\d+(\.\d+)?$", words[2]):
                second_value = float(words[2])
            elif re.match(r"^\d+/\d+$", words[2]):
                second_value = float(Fraction(words[2]))
            elif words[2] in WRITTEN_NUMBERS:
                second_value = WRITTEN_NUMBERS[words[2]]

            if second_value is not None:
                return min(value, second_value)

        return value

    return None

def normalize_unit_token(word):
    word = word.lower().strip(",. ")
    return UNIT_MAP.get(word)

def remove_leading_quantity(text):
    text = normalize_quantity_text(text).strip()

    while True:
        updated = re.sub(
            r'^\s*(?:plus\s+)?(?:\d+[¼½¾⅓⅔⅛⅜⅝⅞]|\d+(?:\.\d+)?-\d+/\d+|\d+/\d+|\d+(?:\.\d+)?(?:\s+\d+/\d+)?|\.\d+|[¼½¾⅓⅔⅛⅜⅝⅞]|one|two|three|four|five|six|seven|eight|nine|ten)(?:\s+(?:to|or)\s+(?:\d+(?:\.\d+)?|\d+/\d+|one|two|three|four|five|six|seven|eight|nine|ten))?\s*',
            '',
            text
        ).strip()

        if updated == text:
            break

        text = updated

    return text

def get_attached_unit(first_word):
    attached_match = re.match(r"^(\d+(?:\.\d+)?|\.\d+)([a-zA-Z]+)\.?$", first_word)
    if attached_match:
        return normalize_unit_token(attached_match.group(2))
    return None

def get_two_word_unit(word1, word2):
    return UNIT_MAP.get(f"{word1} {word2}")

def get_quantity_word_count(words):
    if not words:
        return 0

    if len(words) >= 2 and extract_quantity(f"{words[0]} {words[1]}") is not None:
        return 2

    if extract_quantity(words[0]) is not None:
        return 1

    return 0

def extract_unit(ingredient):
    ingredient = normalize_quantity_text(ingredient)
    words = ingredient.split()

    if not words:
        return None

    first_word = words[0].lower().strip(",.")
    attached_unit = get_attached_unit(first_word)
    if attached_unit is not None:
        return attached_unit

    quantity_word_count = get_quantity_word_count(words)

    if quantity_word_count == 0:
        return None

    if len(words) > quantity_word_count:
        unit_word = words[quantity_word_count].lower().strip(",.")
        normalized_unit = normalize_unit_token(unit_word)

        if normalized_unit is not None:
            return normalized_unit

    if len(words) > quantity_word_count + 1:
        unit_word_1 = words[quantity_word_count].lower().strip(",.")
        unit_word_2 = words[quantity_word_count + 1].lower().strip(",.")
        two_word_unit = get_two_word_unit(unit_word_1, unit_word_2)

        if two_word_unit is not None:
            return two_word_unit

    return None

def remove_leading_unit(ingredient):
    words = ingredient.split()

    if not words:
        return ingredient

    first_word = words[0].lower().strip(",")
    attached_unit = get_attached_unit(first_word)

    if attached_unit is not None:
        return " ".join(words[1:])

    if normalize_unit_token(first_word) is not None:
        return " ".join(words[1:])

    if len(words) > 1:
        second_word = words[1].lower().strip(",")
        if get_two_word_unit(first_word, second_word) is not None:
            return " ".join(words[2:])

    return ingredient

def remove_filler_words(ingredient):
    cleaned = ingredient

    for phrase in FILLER_PHRASES:
        cleaned = cleaned.replace(phrase, "")

    words = cleaned.split()

    cleaned_words = []

    for word in words:
        if word not in FILLER_WORDS:
            cleaned_words.append(word)

    return " ".join(cleaned_words)

def remove_parenthetical_text(text):
    return re.sub(r"\([^)]*\)|\[[^\]]*\]", "", text).strip()

def remove_leading_noise(text):
    text = text.strip()

    text = re.sub(r'^\s*[-–—]+\s*', '', text)
    text = re.sub(r'^\s*(?:plus\s+)?\d+/\d+ed\s+', '', text)
    text = re.sub(r'^\s*plus\s+', '', text)

    return text.strip()

def remove_leading_articles(text):
    return re.sub(r'^(?:a|an)\s+', '', text).strip()

def remove_leading_descriptors(text):
    words = text.split()

    while words and words[0] in LEADING_DESCRIPTORS:
        words.pop(0)

    return " ".join(words)

def strip_size_words(text):
    words = text.split()

    while words and words[0] in {"small", "medium", "large"}:
        words.pop(0)

    return " ".join(words)

def remove_leading_quantity_unit_phrase(text):
    text = normalize_quantity_text(text).strip()
    words = text.split()

    if not words:
        return text

    first_word = words[0].lower().strip(",.")
    attached_unit = get_attached_unit(first_word)

    if attached_unit is not None:
        return " ".join(words[1:]).strip()

    quantity_word_count = get_quantity_word_count(words)

    if quantity_word_count == 0:
        return text

    if len(words) > quantity_word_count:
        unit_word = words[quantity_word_count].lower().strip(",.")
        if normalize_unit_token(unit_word) is not None:
            return " ".join(words[quantity_word_count + 1:]).strip()

    if len(words) > quantity_word_count + 1:
        unit_word_1 = words[quantity_word_count].lower().strip(",.")
        unit_word_2 = words[quantity_word_count + 1].lower().strip(",.")
        if get_two_word_unit(unit_word_1, unit_word_2) is not None:
            return " ".join(words[quantity_word_count + 2:]).strip()

    return text

def strip_measurement_prefix(text):
    text = normalize_quantity_text(text).strip()
    words = text.split()

    if not words:
        return text

    quantity_word_count = get_quantity_word_count(words)

    if quantity_word_count == 0:
        return text

    if len(words) > quantity_word_count:
        unit_word = words[quantity_word_count].lower().strip(",.")
        if normalize_unit_token(unit_word) is not None:
            return " ".join(words[quantity_word_count + 1:]).strip()

    if len(words) > quantity_word_count + 1:
        unit_word_1 = words[quantity_word_count].lower().strip(",.")
        unit_word_2 = words[quantity_word_count + 1].lower().strip(",.")
        if get_two_word_unit(unit_word_1, unit_word_2) is not None:
            return " ".join(words[quantity_word_count + 2:]).strip()

    return text

def split_combined_seasonings(text):
    stripped = normalize_text(text)

    seasoning_lines = {
        "kosher salt freshly ground black pepper",
        "kosher salt freshly cracked black pepper",
        "kosher salt black pepper",
        "kosher salt pepper",
        "salt pepper",
    }

    if stripped in seasoning_lines:
        return ["kosher salt", "black pepper"]

    return [text]

def collect_ingredients(all_recipes):
    all_ingredients = []

    for recipe in all_recipes:
        ingredients = recipe["ingredients"]

        for ingredient in ingredients:
            normalized = normalize_text(ingredient)
            no_parentheses = remove_parenthetical_text(normalized)
            cleaned = remove_filler_words(no_parentheses)
            cleaned = normalize_quantity_text(cleaned)

            split_lines = split_combined_seasonings(cleaned)

            for item in split_lines:
                item = remove_leading_noise(item)

                quantity = extract_quantity(item)
                unit = extract_unit(item)

                no_amount = remove_leading_quantity(item)
                no_amount = remove_leading_noise(no_amount)

                no_unit = remove_leading_unit(no_amount)
                no_unit = remove_leading_quantity_unit_phrase(no_unit)
                no_unit = remove_leading_noise(no_unit)

                final_ingredient = normalize_text(no_unit)
                final_ingredient = strip_measurement_prefix(final_ingredient)
                final_ingredient = clean_ingredient_phrase(final_ingredient)
                final_ingredient = remove_leading_packaging_phrases(final_ingredient)
                final_ingredient = remove_duplicate_adjacent_words(final_ingredient)
                final_ingredient = remove_leading_noise(final_ingredient)
                final_ingredient = remove_leading_articles(final_ingredient)
                final_ingredient = remove_leading_descriptors(final_ingredient)
                final_ingredient = strip_size_words(final_ingredient)
                final_ingredient, unit = normalize_specific_ingredients(final_ingredient, unit)
                final_ingredient, quantity, unit = normalize_measurement_leftovers(final_ingredient, quantity, unit)

                if final_ingredient in {
                    "kosher salt freshly ground black pepper",
                    "kosher salt freshly cracked black pepper",
                    "kosher salt black pepper",
                    "kosher salt pepper",
                    "salt pepper",
                }:
                    all_ingredients.append((None, None, "kosher salt"))
                    all_ingredients.append((None, None, "black pepper"))
                    continue

                if final_ingredient != "" and not is_invalid_standalone_ingredient(final_ingredient):
                    all_ingredients.append((quantity, unit, final_ingredient))

    return all_ingredients

def singularize_ingredient(name):
    if " and " in name:
        return name

    if name in INGREDIENTS_NO_SINGULARIZE:
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
        name = singularize_ingredient(ingredient.strip())

        if name == "clove garlic":
            name = "garlic"
            unit = "clove"

        if name == "sprig thyme":
            name = "thyme"
            unit = "sprig"

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
                print(quantity, ingredient)
            else:
                print(quantity, unit, ingredient)

    print()