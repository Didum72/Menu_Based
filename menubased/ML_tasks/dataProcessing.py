# dataProcessing.py
from flask import Flask, request, jsonify
import pandas as pd
import io

app = Flask(__name__)

@app.route('/process_data', methods=['POST'])
def process_data():
    file = request.files['file']
    if not file:
        return jsonify({'status': 'error', 'message': 'No file uploaded'})

    try:
        # Read the file into a DataFrame
        df = pd.read_csv(file)
        
        # Perform data processing
        summary = {
            'mean': df.mean().to_dict(),
            'median': df.median().to_dict(),
            'std_dev': df.std().to_dict()
        }
        
        return jsonify({'status': 'success', 'summary': summary})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
