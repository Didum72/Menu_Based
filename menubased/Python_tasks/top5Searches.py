from flask import Flask, render_template, request, jsonify
from googlesearch import search

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('searchTop5.html')  # This renders the HTML form

@app.route('/get_top5_results', methods=['POST'])
def get_top5_results():
    query = request.form.get('query')
    
    # Get top 5 Google search results
    search_results = []
    try:
        for result in search(query, num_results=5):
            search_results.append(result)
    except Exception as e:
        return jsonify({'error': str(e)})

    return jsonify({'results': search_results})

if __name__ == '__main__':
    app.run(debug=True)
