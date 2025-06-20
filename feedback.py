import random
import pandas as pd

def get_available_recipes(recipes, diet, flavor, protein=None):
    if diet == 'carnivore' and protein:
        return recipes.get(diet, {}).get(protein, {}).get(flavor, [])
    return recipes.get(diet, {}).get(flavor, [])

def suggest_recipe(preferences, suggested_recipes, recipes):
    diet = preferences.get('diet')
    flavor = preferences.get('flavor')
    time = preferences.get('time')
    protein = preferences.get('protein', None)

    candidates = get_available_recipes(recipes, diet, flavor, protein)
    candidates = [r for r in candidates if r not in suggested_recipes]
    if not candidates:
        return "No suitable recipes found.", None

    recipe = random.choice(candidates)
    suggested_recipes.append(recipe)

    details = (
        f"Recipe Name: {recipe['name']}\n"
        f"Ingredients: {', '.join(recipe['ingredients'])}\n"
        f"Details: {recipe['details']}\n"
        f"Cuisine: {recipe['cuisine']}\n"
        f"Instructions: {recipe['instructions']}\n"
    )
    if time < 30:
        details += "Note: This is a quick and easy recipe."
    elif time < 60:
        details += "Note: This recipe takes a moderate amount of time."
    else:
        details += "Note: This recipe takes longer to prepare."

    return details, recipe

def handle_feedback(preferences, model, le_diet, le_flavor):
    from data_handler import load_recipes
    recipes = load_recipes()
    suggested_recipes = []

    while True:
        info, recipe = suggest_recipe(preferences, suggested_recipes, recipes)
        print(info)
        feedback = input("Do you like this recipe? (yes/no) ").strip().lower()
        
        if feedback in ['yes', 'no']:
            # Save feedback if model exists
            if model and le_diet and le_flavor:
                new_data = {
                    'diet': preferences['diet'],
                    'flavor': preferences['flavor'],
                    'time': preferences['time'],
                    'feedback': feedback
                }
                df = pd.DataFrame([new_data])
                df.to_csv('feedback_data.csv', mode='a', header=not pd.read_csv('feedback_data.csv').empty, index=False)
            if feedback == 'yes':
                print("Enjoy your meal!")
                break
        else:
            print("Invalid input. Please type 'yes' or 'no'.")
