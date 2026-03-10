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
        return float(Fraction(unicode_fractions[first_word]))

    if "/" in first_word:
        return float(Fraction(first_word))
    
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


def remove_filler_words(ingredient):
    filler_words = ["optional", "to", "taste", "for", "garnish", "serve", "serving"]

    words = ingredient.split()
    cleaned_words = []

    for word in words:
        if word not in filler_words:
            cleaned_words.append(word)

    return " ".join(cleaned_words)

def remove_leading_amount(ingredient):
    words = ingredient.split()

    if len(words) == 0:
        return ""
    
    first_word = words [0]
    fraction_chars = "¼½¾⅓⅔⅛⅜⅝⅞"

    is_fraction = "/" in first_word

    if first_word [0].isdigit() or first_word[0] in fraction_chars or is_fraction:
            if len(words) >= 3:
                return " ".join(words[2:])
            if len(words) == 2:
                return words[1]
            return ""
        
    return ingredient

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
            final_ingredient = normalize_spaces(no_amount)

            if final_ingredient != "":
                all_ingredients.append((quantity, final_ingredient))

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
        quantity, ingredient = item
        name = get_ingredient_name(ingredient)
        name = singularize_ingredient(name)

        if name in ingredient_counts:
            ingredient_counts[name] += 1
        else:
            ingredient_counts[name] = 1
    
    return ingredient_counts

def display_grocery_list(ingredient_counts):
    print("\nGROCERY LIST\n")

    for ingredient in sorted(ingredient_counts):
        count = ingredient_counts[ingredient]
        print(ingredient, "-", count)

    print()