import cv2
import time
import config
from gestures import GestureRecognizer
from speech import SpeechEngine
from ui_overlay import UIOverlay

def main():
    # Initialize components
    recognizer = GestureRecognizer()
    speaker = SpeechEngine()
    ui = UIOverlay()
    
    # Setup Camera
    cap = cv2.VideoCapture(config.CAMERA_ID)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, config.FRAME_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, config.FRAME_HEIGHT)
    
    if not cap.isOpened():
        print("Error: Could not open camera.")
        return

    print("Gesture Recognition System Started...")
    print("Press 'q' to exit.")
    
    frame_count = 0
    current_gesture = None
    
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break
                
            # Mirror frame
            frame = cv2.flip(frame, 1)
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Process gesture every N frames to save CPU
            if frame_count % config.PROCESS_EVERY_N_FRAMES == 0:
                results = recognizer.process_frame(frame_rgb)
                
                if results.multi_hand_landmarks:
                    hand_landmarks = results.multi_hand_landmarks[0]
                    current_gesture = recognizer.recognize(hand_landmarks)
                else:
                    hand_landmarks = None
                    current_gesture = None
            
            frame_count += 1
            
            # Logic: Handle Speech
            if current_gesture:
                if current_gesture in config.GESTURES:
                    gesture_data = config.GESTURES[current_gesture]
                    # Speak automatically
                    speaker.speak(gesture_data["text"])
            
            # Rendering: Draw UI
            # 1. Landmarks
            if 'hand_landmarks' in locals() and hand_landmarks:
                 ui.draw_landmarks(frame, hand_landmarks, recognizer.mp_hands)
            
            # 2. Overlay info
            frame = ui.draw_overlay(frame, current_gesture, speaker.is_speaking)
            
            # Display
            cv2.imshow("Gesture Recognition AI By Khalifa", frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
                
    except KeyboardInterrupt:
        print("Stopping...")
    finally:
        cap.release()
        cv2.destroyAllWindows()
        speaker.stop()
        print("System stopped.")

if __name__ == "__main__":
    main()
