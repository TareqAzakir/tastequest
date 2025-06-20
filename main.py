from preferences import get_user_preferences
from feedback import handle_feedback
from data_handler import load_model_and_data

if __name__ == "__main__":
    print("Hello, welcome to this AI-enhanced recipe suggestion program!")
    model, le_diet, le_flavor, data = load_model_and_data()
    preferences = get_user_preferences()
    handle_feedback(preferences, model, le_diet, le_flavor)
