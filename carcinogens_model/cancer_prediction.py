import cv2
import easyocr
import numpy as np
import tkinter as tk
from tkinter import Label, Button, filedialog, messagebox, Text, Scrollbar
from PIL import Image, ImageTk
import re
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report


# ✅ Step 1: Data Cleaning
def clean_iarc_dataset(file_path):
    """ 
    Cleans the IARC dataset by keeping only 'Agent' and 'Risk_Label' columns. 
    Saves the cleaned dataset for training.
    """

    df = pd.read_csv(file_path)
    df.columns = df.columns.str.strip()

    # 🔹 Assign Risk_Label based on classification groups
    if 'Risk_Label' not in df.columns:
        if 'Group' not in df.columns:
            raise KeyError("❌ ERROR: 'Group' column not found!")

        df['Risk_Label'] = df['Group'].apply(lambda x: 1 if str(x).strip() in ["1", "2A"] else 0)

    df = df[['Agent', 'Risk_Label']].dropna()

    # ✅ Save cleaned dataset
    df.to_csv("cleaned_iarc_dataset.csv", index=False)
    print("\nCleaned dataset saved as 'cleaned_iarc_dataset.csv'")
    
    return df


# ✅ Step 2: Train Model
def train_model(cleaned_file):
    """ Train a carcinogen detection model using TF-IDF and RandomForest. """

    df = pd.read_csv(cleaned_file)

    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(df['Agent'])
    y = df['Risk_Label']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # ✅ Save model and vectorizer
    joblib.dump(model, "carcinogen_model.pkl")
    joblib.dump(vectorizer, "tfidf_vectorizer.pkl")

    # ✅ Model evaluation
    y_pred = model.predict(X_test)
    print("\nModel Accuracy:", accuracy_score(y_test, y_pred))
    print("\nClassification Report:\n", classification_report(y_test, y_pred))

    return model, vectorizer


# ✅ Step 3: OCR App
class OCRApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Live Camera OCR - Carcinogen Detection")

        # ✅ Load trained model and vectorizer
        self.model = joblib.load("carcinogen_model.pkl")
        self.vectorizer = joblib.load("tfidf_vectorizer.pkl")

        # OpenCV Camera Setup
        self.cap = cv2.VideoCapture(0)
        self.cap.set(3, 640)
        self.cap.set(4, 480)
        self.is_captured = False

        # UI Elements
        self.label = Label(root)
        self.label.pack()

        self.capture_button = Button(root, text="Capture & Analyze", command=self.capture_image)
        self.capture_button.pack(pady=5)

        self.load_button = Button(root, text="Load Image", command=self.load_image)
        self.load_button.pack(pady=5)

        self.exit_button = Button(root, text="Exit", command=self.close_app)
        self.exit_button.pack(pady=5)

        self.text_display = Text(root, wrap="word", height=10, width=70, font=("Arial", 12))
        self.text_display.pack(pady=10)

        self.scrollbar = Scrollbar(root, command=self.text_display.yview)
        self.scrollbar.pack(side="right", fill="y")
        self.text_display.config(yscrollcommand=self.scrollbar.set)

        # OCR Reader
        self.reader = easyocr.Reader(['en'], verbose=False)

        # Start webcam feed
        self.update_camera()

    def update_camera(self):
        """ Update camera feed in Tkinter window. """
        if not self.is_captured:
            ret, frame = self.cap.read()
            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame = Image.fromarray(frame)
                frame = ImageTk.PhotoImage(frame)
                self.label.config(image=frame)
                self.label.image = frame
        self.root.after(10, self.update_camera)

    def capture_image(self):
        """ Capture image and extract text using EasyOCR. """
        ret, frame = self.cap.read()
        if ret:
            self.is_captured = True
            self.process_image(frame)

    def load_image(self):
        """ Load image from file and analyze text. """
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", ".png;.jpg;.jpeg;.bmp")])
        if not file_path:
            return

        image = cv2.imread(file_path)
        if image is None:
            messagebox.showerror("Error", "Invalid image file!")
            return

        self.is_captured = True
        self.process_image(image)

    def process_image(self, image):
        """ Extracts text from an image, processes it, and classifies ingredients for carcinogens. """
        
        # Convert image to grayscale for better OCR accuracy
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Extract text using EasyOCR
        results = self.reader.readtext(gray)
        extracted_text = " ".join([self.clean_text(res[1]) for res in results])
        
        # Debugging: Print extracted text
        print("\nExtracted OCR Text:", extracted_text)

        # Split the extracted text into individual words (as ingredients might be separate)
        words = extracted_text.split()
        
        # ✅ Process each ingredient individually and classify
        carcinogenic_ingredients = []
        
        for word in words:
            transformed_word = self.vectorizer.transform([word])  # Vectorize word
            prediction = self.model.predict(transformed_word)[0]  # Predict (1 = Carcinogenic, 0 = Non-Carcinogenic)

            if prediction == 1:
                carcinogenic_ingredients.append(word)
        
        # ✅ Display Results in GUI
        self.text_display.delete("1.0", tk.END)
        
        if carcinogenic_ingredients:
            for ingredient in words:
                if ingredient in carcinogenic_ingredients:
                    self.text_display.insert(tk.END, ingredient + " ", "carcinogen")
                else:
                    self.text_display.insert(tk.END, ingredient + " ")
            self.text_display.tag_config("carcinogen", foreground="red", font=("Arial", 12, "bold"))
        else:
            self.text_display.insert(tk.END, extracted_text)

        # Debugging: Print predictions
        print("Carcinogenic Ingredients Found:", carcinogenic_ingredients)
        
        # ✅ Show image in Tkinter GUI
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image_pil = Image.fromarray(image_rgb)
        image_pil.thumbnail((400, 400))
        image_tk = ImageTk.PhotoImage(image_pil)

        self.label.config(image=image_tk)
        self.label.image = image_tk

    def clean_text(self, text):
        """ Clean extracted text by removing special characters and converting to lowercase. """
        text = text.lower()
        text = re.sub(r'[^a-z0-9\s-]', '', text)
        return text.strip()

    def close_app(self):
        """ Close the application and release the camera. """
        self.cap.release()
        self.root.destroy()


# ✅ Step 4: Run Everything
if __name__ == "__main__":
    file_path = r"D:\cancer_research\MLmodel\List of Classifications – IARC Monographs on the Identification of Carcinogenic Hazards to Humans.csv"
    clean_iarc_dataset(file_path)
    train_model("cleaned_iarc_dataset.csv")

    root = tk.Tk()
    app = OCRApp(root)
    root.mainloop()