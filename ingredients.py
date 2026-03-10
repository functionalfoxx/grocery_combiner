from fractions import Fraction

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
    parts = text.split(",")
    return parts[0].strip()

def remove_leading_descriptors(text):
    words = text.split()

    if len(words) == 0:
        return text

    leading_descriptors = [
        "chopped",
        "diced",
        "minced",
        "grated",
        "sliced",
        "halved",
        "quartered",
        "peeled",
        "packed",
        "leveled",
        "levelled",
        "melted",
        "sauteed",
        "sautéed",
        "softened",
        "cooled"
    ]

    if words[0] in leading_descriptors:
        return " ".join(words[1:])

    return text

def extract_quantity(ingredient):
    words = ingredient.split()

    if len(words) == 0:
        return None

    first_word = words[0]

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

    if first_word in unicode_fractions:
        return round(float(Fraction(unicode_fractions[first_word])), 2)

    if "/" in first_word:
        return round(float(Fraction(first_word)), 2)
    
    try:
        return float(first_word)
    except ValueError:
        return None
    
def remove_leading_quantity(ingredient):
    words = ingredient.split()

    if len(words) == 0:
        return ingredient
    
    first_word = words[0]

    unicode_fractions = "¼½¾⅓⅔⅛⅜⅝⅞"

    if first_word[0].isdigit() or "/" in first_word or first_word in unicode_fractions:
        return " ".join(words[1:])
    
    return ingredient

def extract_unit(ingredient):
    words = ingredient.split()

    if len(words) == 0:
        return None

    first_word = words[0]
    clean_word = first_word.rstrip(".,;:").lower()

    unit_map = {
        "tsp": "tsp",
        "tsps": "tsp",
        "teaspoon": "tsp",
        "teaspoons": "tsp",
        "tbsp": "tbsp",
        "tbsps": "tbsp",
        "tablespoon": "tbsp",
        "tablespoons": "tbsp",
        "c": "cup",
        "cup": "cup",
        "cups": "cup",
        "lb": "lb",
        "lbs": "lb",
        "pound": "lb",
        "pounds": "lb"
    }

    if clean_word in unit_map:
        return unit_map[clean_word]

    return None

def remove_leading_unit(ingredient):
    words = ingredient.split()

    if len(words) <= 1:
        return ingredient

    unit = extract_unit(ingredient)

    if unit is not None:
        return " ".join(words[1:])

    return ingredient

def remove_filler_words(ingredient):
    filler_words = ["optional", "to", "taste", "for", "garnish", "serve", "serving"]

    words = ingredient.split()
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

def collect_ingredients(all_recipes):
    all_ingredients = []

    for recipe in all_recipes:
        ingredients = recipe["ingredients"]

        for ingredient in ingredients:
            quantity = extract_quantity(ingredient)
            normalized = normalize_ingredient(ingredient)
            no_parentheses = remove_parentheses(normalized)
            cleaned = remove_filler_words(no_parentheses)
            no_amount = remove_leading_quantity(cleaned)
            unit = extract_unit(no_amount)
            no_unit = remove_leading_unit(no_amount)
            final_ingredient = normalize_spaces(no_unit)
            final_ingredient = remove_comma_descriptors(final_ingredient)
            final_ingredient = remove_leading_descriptors(final_ingredient)
            final_ingredient = remove_trailing_punctuation(final_ingredient)

            if final_ingredient != "":
                all_ingredients.append((quantity, unit, final_ingredient))

    return all_ingredients

def get_ingredient_name(ingredient):
    return ingredient.strip()

def singularize_ingredient(name):

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

    for (ingredient, unit) in sorted(ingredient_counts):
        quantity = round(ingredient_counts[(ingredient, unit)], 2)

        if unit is None:
            print(quantity, ingredient)
        else:
            print(quantity, unit, ingredient)

    print()