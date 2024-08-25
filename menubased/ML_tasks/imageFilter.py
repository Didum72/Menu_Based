# imageFilter.py
from flask import Flask, request, jsonify
import cv2
import numpy as np
from PIL import Image
from io import BytesIO
import base64

app = Flask(__name__)

def apply_filter(image, filter_type):
    if filter_type == 'grayscale':
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    elif filter_type == 'blur':
        return cv2.GaussianBlur(image, (15, 15), 0)
    elif filter_type == 'edge':
        return cv2.Canny(image, 100, 200)
    else:
        return image

@app.route('/apply_filter', methods=['POST'])
def apply_filter_route():
    file = request.files['file']
    filter_type = request.form.get('filter')

    if not file:
        return jsonify({'status': 'error', 'message': 'No file uploaded'})

    try:
        # Read the image file
        img = Image.open(file.stream)
        img = np.array(img)

        # Apply the chosen filter
        filtered_img = apply_filter(img, filter_type)

        # Convert back to PIL Image
        filtered_pil = Image.fromarray(filtered_img)
        buffer = BytesIO()
        filtered_pil.save(buffer, format="PNG")
        img_data = buffer.getvalue()

        return jsonify({
            'status': 'success',
            'filtered_image': 'data:image/png;base64,' + base64.b64encode(img_data).decode('utf-8')
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
