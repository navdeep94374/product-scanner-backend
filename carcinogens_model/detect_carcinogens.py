
import joblib
import os

def check_carcinogen(text):
    model_file = os.path.join(os.getcwd(), "carcinogens_model", "carcinogen_model.pkl")
    vectors_file = os.path.join(os.getcwd(), "carcinogens_model", "tfidf_vectorizer.pkl")
    model = joblib.load(model_file)
    vectorizer = joblib.load(vectors_file)
    words = text.split()
    predictions = {}
 
    for word in words:
        transformed_word = vectorizer.transform([word])
        predicted_group = model.predict(transformed_word)[0]
        predictions[word] = predicted_group
    print(predictions)
    return predictions

#check_carcinogen("Tobacco smoke, Asbestos, Aflatoxins, Benzene, Formaldehyde, Arsenic, Ultraviolet radiation (sunlight), Alcohol, Processed meats, Diesel engine exhaust, Human papillomavirus (HPV), Radon, Cadmium, Vinyl chloride, Polychlorinated biphenyls (PCBs), Benzidine, Chromium(VI) compounds, Soot, Coal tar, Aristolochic acid, Silica dust, Mustard gas, Dioxins, Wood dust, Helicobacter pylori (H. pylori), Occupational exposures in rubber production, and many others.")