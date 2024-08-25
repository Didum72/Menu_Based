from flask import Flask, request, send_file
from gtts import gTTS
import io

app = Flask(__name__)

@app.route('/convert', methods=['POST'])
def convert_text_to_audio():
    text = request.form['text']
    tts = gTTS(text)
    audio_file = io.BytesIO()
    tts.write_to_fp(audio_file)
    audio_file.seek(0)
    return send_file(audio_file, mimetype='audio/mp3', as_attachment=False, download_name='output.mp3')

if __name__ == '__main__':
    app.run(debug=True)
