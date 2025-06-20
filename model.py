import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import os

def train_model(data_path='feedback_data.csv'):
    if not os.path.exists(data_path):
        print("No historical data available. Skipping model training.")
        return None, None, None

    data = pd.read_csv(data_path)
    if data.empty:
        print("Empty dataset found. Skipping model training.")
        return None, None, None

    le_diet = LabelEncoder()
    le_flavor = LabelEncoder()
    le_feedback = LabelEncoder()

    X = pd.DataFrame({
        'diet': le_diet.fit_transform(data['diet']),
        'flavor': le_flavor.fit_transform(data['flavor']),
        'time': data['time']
    })
    y = le_feedback.fit_transform(data['feedback'])

    X_train, _, y_train, _ = train_test_split(X, y, test_size=0.2, random_state=42)

    model = RandomForestClassifier()
    model.fit(X_train, y_train)

    return model, le_diet, le_flavor
