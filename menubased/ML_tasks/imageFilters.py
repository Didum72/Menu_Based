# imageFilters.py
from flask import Flask, request, jsonify
import cv2
import numpy as np
from PIL import Image
from io import BytesIO
import base64

app = Flask(__name__)

def apply_sunglasses_filter(image):
    # Draw sunglasses on the image
    h, w = image.shape[:2]
    sunglasses = np.zeros((h, w, 3), dtype=np.uint8)
    cv2.ellipse(sunglasses, (int(w / 2), int(h / 2)), (w // 4, h // 8), 0, 0, 180, (0, 0, 0), -1)
    combined_image = cv2.addWeighted(image, 0.7, sunglasses, 0.3, 0)
    return combined_image

def apply_stars_filter(image):
    # Create star filter effect
    h, w = image.shape[:2]
    stars = np.zeros((h, w, 3), dtype=np.uint8)
    for _ in range(100):
        x, y = np.random.randint(0, w), np.random.randint(0, h)
        cv2.circle(stars, (x, y), np.random.randint(5, 15), (255, 255, 255), -1)
    combined_image = cv2.add(image, stars)
    return combined_image

def apply_filter(image, filter_type):
    if filter_type == 'sunglasses':
        return apply_sunglasses_filter(image)
    elif filter_type == 'stars':
        return apply_stars_filter(image)
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
