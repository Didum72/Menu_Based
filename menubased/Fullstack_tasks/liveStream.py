from flask import Flask, request, jsonify
import cv2
import boto3

app = Flask(__name__)

# Create an AWS Rekognition client
rekognition = boto3.client('rekognition')

@app.route('/liveStream', methods=['POST'])
def liveStream():
    # Receive the live stream from the frontend
    stream = request.get_json()

    # Process the live stream using OpenCV
    cap = cv2.VideoCapture(stream)
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Analyze the live stream using AWS Rekognition
        response = rekognition.detect_labels(Image={'Bytes': frame.tobytes()})
        labels = response['Labels']

        # Return the detected labels to the frontend
        return jsonify({'labels': [label['Name'] for label in labels]})

if __name__ == '__main__':
    app.run(debug=True)