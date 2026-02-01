import cv2
import streamlit as st
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase, RTCConfiguration
import mediapipe as mp
import config
from gestures import GestureRecognizer
import av

# Page Config
st.set_page_config(page_title="AI Gesture Recognition", page_icon="🖐️", layout="wide")

# Sidebar
st.sidebar.title("🖐️ AI Gesture Config")
st.sidebar.info("Aplikasi ini mendeteksi gesture tangan Anda dan menerjemahkannya ke teks.")
show_landmarks = st.sidebar.checkbox("Show Landmarks", value=True)
confidence = st.sidebar.slider("Confidence Threshold", 0.0, 1.0, 0.7, 0.1)

# Main Title
st.title("AI Gesture Recognition & Voice Assistant")
st.markdown("""
<style>
.big-font {
    font-size:30px !important;
    font-weight: bold;
    color: #4CAF50;
}
</style>
""", unsafe_allow_html=True)

# Initialize Recognizer (Global for efficiency if needed, but per-session usually)
# We need to initialize it inside the transformer or pass it
# Streamlit re-runs script, but VideoTransformer persists in webrtc context

class GestureTransformer(VideoTransformerBase):
    def __init__(self):
        self.recognizer = GestureRecognizer()
        self.latest_gesture = None
        
    def transform(self, frame):
        img = frame.to_ndarray(format="bgr24")
        
        # Mirror
        img = cv2.flip(img, 1)
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
        # Process
        results = self.recognizer.process_frame(img_rgb)
        
        gesture = None
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                if show_landmarks:
                    self.recognizer.mp_hands.solutions.drawing_utils.draw_landmarks(
                        img, hand_landmarks, self.recognizer.mp_hands.solutions.hands.HAND_CONNECTIONS)
                
                gesture = self.recognizer.recognize(hand_landmarks)
        
        self.latest_gesture = gesture
        
        return av.VideoFrame.from_ndarray(img, format="bgr24")

# WebRTC Streamer
rtc_configuration = RTCConfiguration(
    {"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]}
)

webrtc_ctx = webrtc_streamer(
    key="gesture-recognition",
    video_transformer_factory=GestureTransformer,
    rtc_configuration=rtc_configuration,
    media_stream_constraints={"video": True, "audio": False},
)

# Display Detected Gesture (This runs in the Streamlit Main Thread)
st.subheader("Detected Gesture:")
status_placeholder = st.empty()

if webrtc_ctx.video_transformer:
    # Use a loop via streamlit's experimental rerun or just static display
    # Real-time data sync from webrtc thread to streamlit thread is tricky.
    # We display the last known gesture.
    gesture = webrtc_ctx.video_transformer.latest_gesture
    
    if gesture and gesture in config.GESTURES:
        data = config.GESTURES[gesture]
        text = data["text"]
        icon = data["icon"]
        status_placeholder.markdown(f'<p class="big-font">{icon} {text}</p>', unsafe_allow_html=True)
    elif gesture:
        status_placeholder.write(f"Gesture: {gesture} (No Text Mapped)")
    else:
        status_placeholder.write("Waiting for gesture...")
else:
    status_placeholder.info("Start the camera above to begin.")

st.markdown("---")
st.markdown("### 📝 Panduan Gesture")
cols = st.columns(4)
keys = list(config.GESTURES.keys())
for i, key in enumerate(keys):
    with cols[i % 4]:
        st.caption(f"{config.GESTURES[key]['icon']} **{key.title()}**")

