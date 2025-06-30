import os
import io
import json
from flask import Flask, request, jsonify
from PIL import Image
import tensorflow as tf # type: ignore
import numpy as np

# Initialize the Flask app
app = Flask(app)

# Load your pre-trained model (e.g., a model trained to classify products)
# Note: In this example, you can use a simple model like MobileNet or any other custom model.
model = tf.keras.applications.MobileNetV2(weights='imagenet')

# Utility function to process the image for model inference
def prepare_image(image_bytes):
    image = Image.open(io.BytesIO(image_bytes))
    image = image.resize((224, 224))  # Resizing to model's input size
    image = np.array(image) / 255.0  # Normalizing
    image = np.expand_dims(image, axis=0)  # Adding batch dimension
    return image

# Route for image classification
@app.route('/classify', methods=['POST'])
def classify_image():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    # Read image file and preprocess
    image_bytes = file.read()
    image = prepare_image(image_bytes)
    
    # Run inference
    predictions = model.predict(image)
    decoded_predictions = tf.keras.applications.mobilenet_v2.decode_predictions(predictions, top=1)[0]
    
    # Get top prediction
    product_name = decoded_predictions[0][1]
    product_price = "30"  # Dummy price, you can integrate a pricing system
    payment_link = f"https://pay.example.com/{product_name.lower().replace(' ', '-')}"
    
    # Return response
    return jsonify({
        'product': product_name,
        'price': product_price,
        'payment_link': payment_link
    })

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
