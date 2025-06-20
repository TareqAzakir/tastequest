import spacy
from nltk.corpus import stopwords
from nltk.data import find

try:
    find('corpora/stopwords.zip')
except:
    import nltk
    nltk.download('stopwords')

stop_words = set(stopwords.words('english'))
nlp = spacy.load("en_core_web_sm")

def preprocess_text(text):
    doc = nlp(text.lower())
    return ' '.join([token.text for token in doc if token.text not in stop_words and token.is_alpha])

def get_user_preference(prompt, valid_options):
    while True:
        response = input(prompt).strip().lower()
        response = preprocess_text(response)
        if response in valid_options:
            return response
        print(f"Invalid choice. Please choose from {', '.join(valid_options)}.")

def get_user_preferences():
    preferences = {}
    preferences['diet'] = get_user_preference("Are you vegan, vegetarian, or carnivore? ", ['vegan', 'vegetarian', 'carnivore'])
    preferences['flavor'] = get_user_preference("How do you like the flavor? (spicy, sweet, savory) ", ['spicy', 'sweet', 'savory'])

    while True:
        try:
            time = int(input("How much time do you have to cook? (in minutes) ").strip())
            if time > 0:
                preferences['time'] = time
                break
        except ValueError:
            print("Please enter a valid number.")

    if preferences['diet'] == 'carnivore':
        preferences['protein'] = get_user_preference("Do you prefer meat, chicken, or fish? ", ['meat', 'chicken', 'fish'])

    return preferences
