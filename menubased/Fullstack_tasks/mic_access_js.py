from flask import Flask, request, jsonify
import speech_recognition as sr
from pydub import AudioSegment
import io
from pydub.utils import which

app = Flask(__name__)

# Explicitly set the path to ffmpeg if not detected automatically
ffmpeg_path = r"C:\Users\Anmol\OneDrive\Desktop\ffmpeg-master-latest-win64-gpl\bin\ffmpeg"
ffprobe_path = r"C:\Users\Anmol\OneDrive\Desktop\ffmpeg-master-latest-win64-gpl\bin\ffprobe"

AudioSegment.converter = ffmpeg_path
AudioSegment.ffmpeg = ffmpeg_path
AudioSegment.ffprobe = ffprobe_path

@app.route('/transcribe', methods=['POST'])
def transcribe():
    # Get the audio file from the request
    audio_file = request.files['audio'].read()

    try:
        # Convert the raw audio to a format usable by SpeechRecognition
        audio_segment = AudioSegment.from_file(io.BytesIO(audio_file), format="wav")
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    recognizer = sr.Recognizer()
    audio_chunks = audio_segment[::5000]  # chunks of 5 seconds

    text = ""
    for chunk in audio_chunks:
        chunk_audio = io.BytesIO()
        chunk.export(chunk_audio, format="wav")
        chunk_audio.seek(0)
        audio = sr.AudioFile(chunk_audio)
        
        with audio as source:
            audio_data = recognizer.record(source)
            try:
                text += recognizer.recognize_google(audio_data) + " "
            except sr.UnknownValueError:
                text += "[Unrecognized speech] "
            except sr.RequestError:
                return jsonify({"error": "API request error"}), 500
    
    return jsonify({"transcription": text.strip()})

if __name__ == '__main__':
    app.run(debug=True)
