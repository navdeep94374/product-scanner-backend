import cv2
import easyocr
import numpy as np
import tkinter as tk
from tkinter import Label, Button, filedialog, messagebox, Text, Scrollbar
from PIL import Image, ImageTk
import re
import pandas as pd
import joblib
import os

# Load trained model and vectorizer
model = joblib.load("carcinogen_model.pkl")
vectorizer = joblib.load("tfidf_vectorizer.pkl")

def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s-]', '', text)
    text = text.strip()
    return text

class OCRApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Carcinogen Detector")
        
        self.label = Label(root, text="Upload or Capture an image to detect carcinogens", font=("Arial", 14))
        self.label.pack(pady=10)
        
        self.upload_btn = Button(root, text="Upload Image", command=self.upload_image)
        self.upload_btn.pack()
        
        self.capture_btn = Button(root, text="Capture Image", command=self.capture_image)
        self.capture_btn.pack()
        
        self.result_label = Label(root, text="", font=("Arial", 12), fg="red")
        self.result_label.pack(pady=10)
        
        self.canvas = tk.Canvas(root, width=400, height=400)
        self.canvas.pack()

    def upload_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", ".jpg;.png;*.jpeg")])
        if file_path:
            self.process_image(file_path)

    def capture_image(self):
        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # Use DirectShow backend for Windows
        if not cap.isOpened():
            messagebox.showerror("Error", "Could not access webcam")
            return
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            cv2.imshow("Press 'c' to capture, 'q' to cancel", frame)
            key = cv2.waitKey(1) & 0xFF
            
            if key == ord('c'):  # Capture image on pressing 'c'
                file_path = "captured_image.jpg"
                cv2.imwrite(file_path, frame)
                break
            elif key == ord('q'):  # Quit without capturing
                cap.release()
                cv2.destroyAllWindows()
                return
        
        cap.release()
        cv2.destroyAllWindows()
        self.process_image(file_path)

    def process_image(self, file_path):
        reader = easyocr.Reader(['en'])
        image = cv2.imread(file_path)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        results = reader.readtext(gray)
        extracted_text = " ".join([clean_text(res[1]) for res in results])
        
        self.display_image(file_path)
        self.check_carcinogen(extracted_text)

    def check_carcinogen(self, text):
        words = text.split()
        carcinogenic_ingredients = [word for word in words if model.predict(vectorizer.transform([word]))[0] == 1]
        
        if carcinogenic_ingredients:
            result_text = "Potential carcinogens detected:\n" + "\n".join(carcinogenic_ingredients)
        else:
            result_text = "No known carcinogens detected."
        
        self.result_label.config(text=result_text)

    def display_image(self, file_path):
        img = Image.open(file_path)
        img = img.resize((400, 400), Image.LANCZOS)
        img_tk = ImageTk.PhotoImage(img)
        self.canvas.create_image(200, 200, anchor=tk.CENTER, image=img_tk)
        self.canvas.image = img_tk

if __name__ == "__main__":
    root = tk.Tk()
    app = OCRApp(root)
    root.mainloop()