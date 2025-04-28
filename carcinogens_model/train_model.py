import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import os

# Step 1: Data Cleaning
def clean_iarc_dataset(file_path):
    df = pd.read_csv(file_path)
    df.columns = df.columns.str.strip()

    if 'Group' not in df.columns:
        raise KeyError("ERROR: 'Group' column not found!")

    # 🔹 Create Risk_Label: 1 if Group is 1 or 2A, else 0
    df['Risk_Label'] = df['Group'].apply(lambda x: 1 if str(x).strip() in ["1", "2A"] else 0)

    df = df[['Agent', 'Group', 'Risk_Label']].dropna()

    df.to_csv( os.path.join(os.getcwd(), "carcinogens_model","cleaned_iarc_dataset.csv"), index=False)
    print("\n✅ Cleaned dataset saved as 'cleaned_iarc_dataset.csv'")

    return df

# Step 2: Train Model
def train_model(cleaned_file):
    df = pd.read_csv(cleaned_file)

    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(df['Agent'])
    y = df['Group']  # 🔥 Predicting Group now

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # ✅ Save model and vectorizer
   
    joblib.dump(model, os.path.join(os.getcwd(), "carcinogens_model", "carcinogen_model.pkl"))
    joblib.dump(vectorizer,  os.path.join(os.getcwd(), "carcinogens_model", "tfidf_vectorizer.pkl"))

    # ✅ Model evaluation
    y_pred = model.predict(X_test)
    print("\n✅ Model Accuracy:", accuracy_score(y_test, y_pred))
    print("\n✅ Classification Report:\n", classification_report(y_test, y_pred))

    return model, vectorizer

# ✅ Step 3: Run Everything
if __name__ == "__main__":
    file_path = os.path.join(os.getcwd(), "carcinogens_model", "data.csv")
    clean_iarc_dataset(file_path)
    train_model("cleaned_iarc_dataset.csv")
