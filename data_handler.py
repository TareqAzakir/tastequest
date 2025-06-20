import json
from model import train_model

def load_recipes(filepath='recipes.json'):
    with open(filepath, 'r') as file:
        return json.load(file)

def load_model_and_data():
    recipes = load_recipes()
    model, le_diet, le_flavor = train_model()
    return model, le_diet, le_flavor, recipes
