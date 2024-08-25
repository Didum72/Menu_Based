# audioVolumeControl.py
from flask import Flask, request, jsonify
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL

app = Flask(__name__)

def get_default_audio_device():
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    return cast(interface, POINTER(IAudioEndpointVolume))

def get_current_volume():
    volume = get_default_audio_device()
    current_volume = volume.GetMasterVolumeLevelScalar()
    return int(current_volume * 100)

def set_volume(level):
    volume = get_default_audio_device()
    if 0 <= level <= 100:
        volume.SetMasterVolumeLevelScalar(level / 100, None)
        return 'success'
    else:
        return 'error'

@app.route('/get_volume', methods=['GET'])
def get_volume():
    volume = get_current_volume()
    return jsonify({'volume': volume})

@app.route('/set_volume', methods=['POST'])
def set_volume_route():
    data = request.json
    level = data.get('level')
    result = set_volume(level)
    if result == 'success':
        return jsonify({'status': 'success', 'message': f"Volume set to {level}%"})
    else:
        return jsonify({'status': 'error', 'message': "Volume level must be between 0 and 100"})

if __name__ == '__main__':
    app.run(debug=True)
