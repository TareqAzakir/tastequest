# data_handler.py
import json
import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier

def load_recipes():
    """Load recipe data from recipes.json"""
    path = os.path.join(os.path.dirname(__file__), 'recipes.json')
    with open(path, 'r') as file:
        return json.load(file)

def build_training_data(recipes):
    """Convert recipe JSON into a structured training DataFrame"""
    rows = []

    for diet, contents in recipes.items():
        if diet == 'carnivore':
            for protein, flavors in contents.items():
                for flavor, items in flavors.items():
                    for item in items:
                        rows.append({
                            'diet': diet,
                            'flavor': flavor,
                            'protein': protein,
                            'time': item.get('time', 30),
                            'label': item['name']
                        })
        else:
            for flavor, items in contents.items():
                for item in items:
                    rows.append({
                        'diet': diet,
                        'flavor': flavor,
                        'protein': 'none',
                        'time': item.get('time', 30),
                        'label': item['name']
                    })

    return pd.DataFrame(rows)

def train_model(data):
    """Train ML model if data is available"""
    if data.empty:
        print("⚠️ No historical data available. Skipping model training.")
        return None, None, None

    le_diet = LabelEncoder()
    le_flavor = LabelEncoder()
    le_protein = LabelEncoder()

    data['diet_encoded'] = le_diet.fit_transform(data['diet'])
    data['flavor_encoded'] = le_flavor.fit_transform(data['flavor'])
    data['protein_encoded'] = le_protein.fit_transform(data['protein'])

    X = data[['diet_encoded', 'flavor_encoded', 'protein_encoded', 'time']]
    y = data['label']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = RandomForestClassifier()
    model.fit(X_train, y_train)

    return model, le_diet, le_flavor, le_protein

def load_model_and_data():
    """Load everything: recipe data, model, encoders"""
    recipes = load_recipes()
    data = build_training_data(recipes)
    model, le_diet, le_flavor, le_protein = train_model(data)
    return model, le_diet, le_flavor, le_protein, recipes
