import mediapipe as mp
import math
from collections import deque
import config

class GestureRecognizer:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            max_num_hands=1,
            min_detection_confidence=config.DETECTION_CONFIDENCE,
            min_tracking_confidence=config.TRACKING_CONFIDENCE
        )
        self.history = deque(maxlen=5) # Smoothing window

    def process_frame(self, frame_rgb):
        return self.hands.process(frame_rgb)

    def _get_finger_states(self, landmarks):
        """
        Returns a list of 5 booleans indicating if each finger is open.
        Order: Thumb, Index, Middle, Ring, Pinky
        """
        # Landmark indices
        # Thumb: 4, Index: 8, Middle: 12, Ring: 16, Pinky: 20
        # Bases: Thumb: 2, Index: 5, Middle: 9, Ring: 13, Pinky: 17
        
        fingers_open = []
        
        # Thumb check (x-axis comparison for right/left hand agnostic if needed, 
        # but here assuming palm facing camera generally)
        # Better simple check: compare tip x to ip x relative to wrist
        # For simplicity in this demo, we assume "up" orientation mostly or check distance from wrist
        
        # WRIST = 0
        # THUMB_CMC = 1, THUMB_MCP = 2, THUMB_IP = 3, THUMB_TIP = 4
        # INDEX_MCP = 5, ...
        
        # General logic: Tip is higher (smaller y) than PIP (second joint from top)
        
        lms = landmarks.landmark
        
        # Thumb is tricky. Let's use a simpler distance heuristic from pinky base or checks
        # If thumb tip is further from pinky base (17) than thumb ip (3), it's likely open
        # But `gesture_speech.py` used x-comparison. Let's make it slightly more robust.
        
        # Check if hand is facing front or back? 
        # For simple robust static gestures:
        
        # Thumb: Compare tip X with knuckle X. 
        # CAUTION: This depends on hand (Left/Right). 
        # Let's assume Right Hand for now or checking relative to wrist.
        
        # Using the logic from previous code but cleaning it up:
        # Thumb: Open if tip.x is 'outside' relative to knuckle? 
        # Let's stick to standard Y-axis check for fingers 2-5
        
        # Fingers 2-5 (Index, Middle, Ring, Pinky)
        finger_tips = [8, 12, 16, 20]
        finger_pips = [6, 10, 14, 18] # PIP joints
        
        # Thumb
        # Check if thumb tip (4) is to the left or right of IP (3) depending on hand side
        # A simple approximation: compare distance to index finger mcp (5).
        # If thumb tip is far from index mcp, it's open.
        dist_thumb_index = math.hypot(lms[4].x - lms[5].x, lms[4].y - lms[5].y)
        dist_thumb_ip_index = math.hypot(lms[3].x - lms[5].x, lms[3].y - lms[5].y)
        
        # Heuristic: Thumb open if tip is further from index base than the IP joint is
        # or simplified: generic x check works okay for basic "Hi"
        
        # Let's use the X-check but adapt for Handedness if possible, but mediapipe usually gives right hand
        # fallback to simple "is tip far from palm center?"
        
        # Palm Center roughly avg of 0, 5, 17
        center_x = (lms[0].x + lms[5].x + lms[17].x) / 3
        center_y = (lms[0].y + lms[5].y + lms[17].y) / 3
        
        thumb_tip_dist = math.hypot(lms[4].x - center_x, lms[4].y - center_y)
        thumb_ip_dist = math.hypot(lms[2].x - center_x, lms[2].y - center_y)
        fingers_open.append(thumb_tip_dist > thumb_ip_dist * 1.1)
        
        # Other fingers: Tip y < PIP y (assuming hand is upright)
        for tip, pip in zip(finger_tips, finger_pips):
            fingers_open.append(lms[tip].y < lms[pip].y)
            
        return fingers_open

    def recognize(self, landmarks):
        if not landmarks:
            return None

        states = self._get_finger_states(landmarks)
        # states = [Thumb, Index, Middle, Ring, Pinky]
        
        # Logic Mapping
        # 1. Halo / Open Palm: All Open -> [1,1,1,1,1]
        
        # Count open fingers detection
        count = sum(states)
        
        gesture = None
        
        # Specific Pattern Matching
        if all(states): 
            gesture = "terima" # 5 Fingers
            
        elif states == [0, 1, 1, 0, 0] or states == [1, 1, 1, 0, 0]: # Peace sign logic
            gesture = "perkenalan" # 2 Fingers (Index, Middle)
            
        elif states == [0, 1, 0, 0, 0] or states == [1, 1, 0, 0, 0]: # Pointing
            gesture = "halo" # 1 Finger
            
        elif states == [1, 0, 0, 0, 0]: # Thumbs Up (others closed)
            gesture = "baik"
            
        elif states == [1, 0, 0, 0, 1] or states == [0, 1, 0, 0, 1]: # Rock/ILY
            gesture = "love"
            
        elif states == [0, 0, 0, 0, 0]: # Fist
            gesture = "semangat"
        
        elif states == [0, 1, 1, 1, 0]: # 3 Fingers
             gesture = "ok"

        elif states == [0, 0, 0, 0, 1]: # Pinky
            gesture = "salam"

        elif states == [1, 1, 0, 0, 1]: # Spiderman / ILY variant
            gesture = "love"

        elif count == 0:
            gesture = "semangat" # Fallback for fist
        
        # Fallback for simple counting if no pattern matched
        if gesture is None:
            if count == 1: gesture = "halo"
            elif count == 2: gesture = "perkenalan"
            elif count == 5: gesture = "terima"
            else: gesture = "diam" # Default idle
            
        return self._smooth_gesture(gesture)

    def _smooth_gesture(self, gesture):
        """
        Reduces flickering by taking the most common gesture in the last N frames.
        """
        self.history.append(gesture)
        if len(self.history) < 2:
            return gesture
            
        # Find most common
        try:
            return max(set(self.history), key=self.history.count)
        except:
            return gesture
