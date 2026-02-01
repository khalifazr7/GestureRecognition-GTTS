const videoElement = document.getElementById('input_video');
const canvasElement = document.getElementById('output_canvas');
const canvasCtx = canvasElement.getContext('2d');
const gestureOverlay = document.getElementById('gesture-overlay');
const speechText = document.getElementById('speech-text');

let isSpeaking = false;
let lastGesture = "";
let lastSpokenTime = 0;
let voiceEnabled = true;

// Gesture Dictionary
const GESTURES = {
    'halo': { icon: '☝️', text: '{icon} Halo! Senang bertemu denganmu.', color: '#22c55e' },
    'perkenalan': { icon: '✌️', text: '{icon} Perkenalkan, nama saya Khalifa.', color: '#eab308' },
    'terima': { icon: '🖐️', text: '{icon} Terimakasih banyak!', color: '#f97316' },
    'baik': { icon: '👍', text: '{icon} Bagus! Siap dilaksanakan.', color: '#06b6d4' },
    'tidak': { icon: '👎', text: '{icon} Maaf, saya tidak setuju.', color: '#ef4444' },
    'semangat': { icon: '✊', text: '{icon} Semangat! Kamu pasti bisa!', color: '#8b5cf6' },
    'ok': { icon: '👌', text: '{icon} Oke sip! Semuanya aman.', color: '#ec4899' },
    'love': { icon: '🤟', text: '{icon} I love you! Sayang kamu.', color: '#d946ef' },
};

// Smooth UI Helper
function updateUI(gesture) {
    if (!GESTURES[gesture]) return;

    const data = GESTURES[gesture];
    const displayText = data.text.replace('{icon}', '');
    
    // Update Overlay
    gestureOverlay.querySelector('.emoji').textContent = data.icon;
    gestureOverlay.querySelector('.text').textContent = gesture.charAt(0).toUpperCase() + gesture.slice(1);
    gestureOverlay.style.borderColor = data.color;
    gestureOverlay.style.boxShadow = `0 4px 20px ${data.color}40`; // 40 is opacity in hex

    // Update Speech Bubble
    speechText.textContent = `"${displayText}"`;
    speechText.style.borderColor = data.color;
    
    // Speak
    speak(displayText);
}

// TTS Logic
function speak(text) {
    if (!voiceEnabled) return;
    
    const now = Date.now();
    // Prevent spamming (wait 3 seconds)
    if (text === lastGesture && now - lastSpokenTime < 3000) return;
    
    // If different gesture, speak immediately
    window.speechSynthesis.cancel(); // Stop current speech
    
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = 'id-ID'; // Indonesian
    utterance.rate = 1.0;
    
    window.speechSynthesis.speak(utterance);
    
    lastGesture = text;
    lastSpokenTime = now;
}

// Logic: Finger Config
function countFingers(landmarks) {
    const tips = [8, 12, 16, 20]; // Index, Middle, Ring, Pinky
    const pips = [6, 10, 14, 18]; // Joints below tips
    
    let fingers = [0, 0, 0, 0, 0]; // Thumb, Index, Middle, Ring, Pinky

    // Thumb (Check X distance)
    // Assuming Right Hand roughly: Tip x < IP x (if palm facing camera)
    // Better heuristic: Distance of tip from Pinky Base (17) vs IP from Pinky Base
    const thumbTip = landmarks[4];
    const thumbIP = landmarks[3];
    const pinkyBase = landmarks[17];
    
    const distTip = Math.hypot(thumbTip.x - pinkyBase.x, thumbTip.y - pinkyBase.y);
    const distIP = Math.hypot(thumbIP.x - pinkyBase.x, thumbIP.y - pinkyBase.y);
    
    if (distTip > distIP * 1.1) {
        fingers[0] = 1; // Thumb Open
    }

    // Other Fingers (Check Y coordinates)
    for (let i = 0; i < 4; i++) {
        if (landmarks[tips[i]].y < landmarks[pips[i]].y) {
            fingers[i + 1] = 1;
        }
    }
    
    return fingers;
}

function detectGesture(fingers) {
    const f = fingers; // [Th, In, Mi, Ri, Pi]
    const count = f.reduce((a, b) => a + b, 0);

    // Logic Tree
    if (count === 5) return 'terima';
    if (f[1] && f[2] && !f[3] && !f[4]) return 'perkenalan'; // Peace (Index+Middle)
    if (f[1] && !f[2] && !f[3] && !f[4]) return 'halo'; // Pointing (Index)
    if (f[0] && !f[1] && !f[2] && !f[3] && !f[4]) return 'baik'; // Thumb
    if (!f[0] && !f[1] && !f[2] && !f[3] && !f[4]) return 'semangat'; // Fist
    if (f[1] && f[2] && f[3] && !f[4]) return 'ok'; // 3 Fingers
    if (f[0] && f[1] && !f[2] && !f[3] && f[4]) return 'love'; // Spider/Love
    if (f[0] && !f[1] && !f[2] && !f[3] && f[4]) return 'love'; // Rock/Love Variant
    
    // Thumb Down logic (Tip below IP) is tricky with simple < y check if hand is rotated.
    // Let's assume basic set for now.
    
    return null;
}

// MediaPipe Results
function onResults(results) {
    // Hide Loading
    document.getElementById('loading').style.display = 'none';

    // Output Canvas Size
    canvasElement.width = videoElement.videoWidth;
    canvasElement.height = videoElement.videoHeight;
    
    canvasCtx.save();
    canvasCtx.clearRect(0, 0, canvasElement.width, canvasElement.height);
    canvasCtx.drawImage(results.image, 0, 0, canvasElement.width, canvasElement.height);
    
    if (results.multiHandLandmarks) {
        for (const landmarks of results.multiHandLandmarks) {
            // Draw Connectors
            drawConnectors(canvasCtx, landmarks, HAND_CONNECTIONS,
                           {color: '#00FF00', lineWidth: 3});
            drawLandmarks(canvasCtx, landmarks, {color: '#FF0000', lineWidth: 1});
            
            // Logic
            const fingers = countFingers(landmarks);
            const gesture = detectGesture(fingers);
            
            if (gesture) {
                updateUI(gesture);
            } else {
                // Reset/Idle
                gestureOverlay.querySelector('.text').textContent = "Mendeteksi...";
                gestureOverlay.style.borderColor = 'rgba(255,255,255,0.2)';
            }
        }
    }
    canvasCtx.restore();
}

// Initialize MediaPipe Hands
const hands = new Hands({locateFile: (file) => {
    return `https://cdn.jsdelivr.net/npm/@mediapipe/hands/${file}`;
}});

hands.setOptions({
    maxNumHands: 1,
    modelComplexity: 0,
    minDetectionConfidence: 0.5,
    minTrackingConfidence: 0.5
});

hands.onResults(onResults);

// Setup Camera
const camera = new Camera(videoElement, {
    onFrame: async () => {
        await hands.send({image: videoElement});
    },
    width: 1280,
    height: 720
});

camera.start();

// Controls
function toggleVoice() {
    voiceEnabled = !voiceEnabled;
    const btn = document.getElementById('toggle-voice');
    if (voiceEnabled) {
        btn.innerHTML = '<i class="ri-volume-up-line"></i> Suara Aktif';
        btn.style.opacity = '1';
    } else {
        btn.innerHTML = '<i class="ri-volume-mute-line"></i> Suara Mati';
        btn.style.opacity = '0.5';
    }
}

function toggleCamera() {
    // MediaPipe camera utils doesn't have a simple stop/start toggle exposed easily 
    // without stopping the requestAnimationFrame loop.
    // For now, we can simple reload usage or pause video.
    alert("Fitur stop kamera belum diimplementasikan di demo ini. Silakan refresh halaman.");
}
