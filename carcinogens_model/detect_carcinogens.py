
import joblib
import os

def check_carcinogen(text):
    model_file = os.path.join(os.getcwd(), "carcinogens_model", "carcinogen_model.pkl")
    vectors_file = os.path.join(os.getcwd(), "carcinogens_model", "tfidf_vectorizer.pkl")
    model = joblib.load(model_file)
    vectorizer = joblib.load(vectors_file)
    words = text.split()
    carcinogenic_ingredients = [word for word in words if model.predict(vectorizer.transform([word]))[0] == 1]
    if carcinogenic_ingredients:
        result_text = "Potential carcinogens detected:\n" + ", ".join(carcinogenic_ingredients)
    else:
        result_text = "No known carcinogens detected."
    
    return result_text
