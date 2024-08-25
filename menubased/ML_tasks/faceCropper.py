# faceCropper.py
from flask import Flask, request, jsonify
import cv2
import numpy as np
from PIL import Image
from io import BytesIO
import base64

app = Flask(__name__)

# Load the pre-trained Haar Cascade classifier for face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

@app.route('/upload_image', methods=['POST'])
def upload_image():
    file = request.files['file']
    if not file:
        return jsonify({'status': 'error', 'message': 'No file uploaded'})

    try:
        # Read the image file
        img = Image.open(file.stream)
        img = np.array(img)

        # Convert image to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Detect faces
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        if len(faces) == 0:
            return jsonify({'status': 'error', 'message': 'No faces detected'})

        # Crop the first detected face
        x, y, w, h = faces[0]
        face_img = img[y:y+h, x:x+w]

        # Convert back to PIL Image
        face_pil = Image.fromarray(face_img)
        buffer = BytesIO()
        face_pil.save(buffer, format="PNG")
        face_data = buffer.getvalue()

        # Convert original image with face overlay
        img_pil = Image.fromarray(img)
        img_pil.paste(face_pil, (x, y))

        # Save the modified image
        buffer = BytesIO()
        img_pil.save(buffer, format="PNG")
        img_data = buffer.getvalue()

        return jsonify({
            'status': 'success',
            'face_image': 'data:image/png;base64,' + base64.b64encode(face_data).decode('utf-8'),
            'modified_image': 'data:image/png;base64,' + base64.b64encode(img_data).decode('utf-8')
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
