# generateImage.py
from flask import Flask, request, jsonify
import numpy as np
import matplotlib.pyplot as plt
import io
import base64
from PIL import Image

app = Flask(__name__)

def generate_custom_image(width, height, color):
    # Create a blank image with the given width, height, and color
    img_array = np.zeros((height, width, 3), dtype=np.uint8)
    img_array[:, :] = color  # Fill the image with the specified color
    
    # Convert to PIL Image and save to a buffer
    img = Image.fromarray(img_array)
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    img_data = buffer.getvalue()
    
    return base64.b64encode(img_data).decode('utf-8')

@app.route('/generate_image', methods=['POST'])
def generate_image_route():
    data = request.json
    width = int(data.get('width', 100))
    height = int(data.get('height', 100))
    color = [int(c) for c in data.get('color', '255,255,255').split(',')]
    
    try:
        image_data = generate_custom_image(width, height, color)
        return jsonify({
            'status': 'success',
            'image': 'data:image/png;base64,' + image_data
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
