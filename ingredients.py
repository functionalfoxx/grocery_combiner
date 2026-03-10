def add_recipe(all_recipes, recipe_data):
    if recipe_data is not None:
        all_recipes.append(recipe_data)
    return all_recipes

def normalize_ingredient(ingredient):
    normalized = ingredient.strip().lower()
    return normalized

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

    if first_word [0].isdigit():

        if first_word[0].isdigit():
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
            normalized = normalize_ingredient(ingredient)
            no_parentheses = remove_parentheses(normalized)
            cleaned = remove_filler_words(no_parentheses)
            no_amount = remove_leading_amount(cleaned)
            all_ingredients.append(no_amount)


    return all_ingredients

def get_ingredient_name(ingredient):
    return ingredient.strip()

def singularize_ingredient(name):
    if name.endswith("s"):
        return name [:-1]
    return name

def count_ingredients(all_ingredients):
    ingredient_counts = {}

    for ingredient in all_ingredients:
        name = get_ingredient_name(ingredient)
        name = singularize_ingredient(name)

        if name in ingredient_counts:
            ingredient_counts[name] += 1
        else:
            ingredient_counts[name] = 1
    
    return ingredient_counts

def display_grocery_list(ingredient_counts):
    print ("\nGROCERY LIST\n")

    for ingredient in sorted(ingredient_counts):
        count = ingredient_counts[ingredient]
        print(ingredient, "-", count)

    print()