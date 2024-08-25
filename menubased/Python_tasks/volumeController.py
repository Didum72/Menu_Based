from flask import Flask, request, jsonify
from pycaw.pycaw import AudioUtilities, ISimpleAudioVolume
import comtypes

app = Flask(__name__)

def get_volume_control():
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(comtypes.GUID('{BCDE0395-E52F-467C-8E3D-C4579291692E}'), comtypes.CLSCTX_ALL, None)
    volume_control = interface.QueryInterface(ISimpleAudioVolume)
    return volume_control

@app.route('/volume', methods=['POST'])
def set_volume():
    volume_control = get_volume_control()
    action = request.json.get('action')
    volume = volume_control.GetMasterVolumeLevelScalar()
    
    if action == 'increase':
        new_volume = min(volume + 0.1, 1.0)
    elif action == 'decrease':
        new_volume = max(volume - 0.1, 0.0)
    else:
        return jsonify({'error': 'Invalid action'}), 400
    
    volume_control.SetMasterVolumeLevelScalar(new_volume, None)
    return jsonify({'volume': new_volume})

if __name__ == '__main__':
    app.run(debug=True)
