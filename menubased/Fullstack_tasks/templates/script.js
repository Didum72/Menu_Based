const video = document.getElementById('video');
const startButton = document.getElementById('start-button');
const stopButton = document.getElementById('stop-button');
const labelsDiv = document.getElementById('labels');

let stream;
let peerConnection;
let dataChannel;

startButton.addEventListener('click', async () => {
    try {
        stream = await navigator.mediaDevices.getUserMedia({ video: true, audio: true });
        video.srcObject = stream;
        video.play();

        peerConnection = new RTCPeerConnection();
        peerConnection.addStream(stream);

        dataChannel = peerConnection.createDataChannel('liveStream');
        dataChannel.onmessage = event => {
            console.log(`Received message from backend: ${event.data}`);
            labelsDiv.innerText = `Detected labels: ${event.data.labels.join(', ')}`;
        };

        // Send the live stream to the backend
        dataChannel.send(stream);
    } catch (error) {
        console.error('Error accessing camera and microphone:', error);
    }
});

stopButton.addEventListener('click', () => {
    stream.getTracks().forEach(track => track.stop());
    peerConnection.close();
    dataChannel.close();
});