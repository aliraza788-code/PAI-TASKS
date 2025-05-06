from flask import Flask, render_template, request, jsonify
import os
import cv2
import torch
from datetime import datetime

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Load YOLOv5 model (you can also use custom trained model)
model = torch.hub.load('ultralytics/yolov5', 'yolov5s')  

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/detect", methods=["POST"])
def detect_animals():
    file = request.files["image"]
    filename = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filename)

    # Run YOLOv5 inference
    results = model(filename)
    detected_classes = results.pandas().xyxy[0]["name"].tolist()

    # Filter only animals (basic example)
    animals = ["cat", "dog", "cow", "sheep", "horse", "deer","Lion"]
    animal_detections = [obj for obj in detected_classes if obj in animals]

    count = len(animal_detections)
    alert = "ALERT: Animal herd detected!" if count > 0 else "No herd detected."

    # Simulate map coordinates
    location = {"lat": 31.5204, "lng": 74.3587}  

    return jsonify({
        "alert": alert,
        "count": count,
        "location": location,
        "Name": animals

    })

if __name__ == "__main__":
    app.run(debug=True)
