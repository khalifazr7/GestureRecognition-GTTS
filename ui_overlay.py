import cv2
import numpy as np
import config
import time

class UIOverlay:
    def __init__(self):
        self.fps_start_time = time.time()
        self.fps_counter = 0
        self.fps = 0

    def draw_overlay(self, frame, gesture_name, is_speaking):
        """
        Draws the UI overlay on the frame.
        """
        h, w, _ = frame.shape
        overlay = frame.copy()
        
        # 1. Top Bar Background
        cv2.rectangle(overlay, (0, 0), (w, 80), (0, 0, 0), -1)
        
        # 2. Bottom Info Bar
        cv2.rectangle(overlay, (0, h - 60), (w, h), (0, 0, 0), -1)
        
        # Apply transparency
        cv2.addWeighted(overlay, config.OVERLAY_ALPHA, frame, 1 - config.OVERLAY_ALPHA, 0, frame)
        
        # 3. FPS Counter (Top Right)
        self._update_fps()
        cv2.putText(frame, f"FPS: {int(self.fps)}", (w - 170, 40), 
                    config.FONT, 0.7, (200, 200, 200), 1, cv2.LINE_AA)
        
        # 4. Main Gesture Display (Top Left)
        if gesture_name and gesture_name in config.GESTURES:
            g_data = config.GESTURES[gesture_name]
            text = g_data["text"]
            color = g_data["color"]
            icon = g_data["icon"]
            
            # Icon/Name
            display_text = f"{icon} {gesture_name.upper()}"
            cv2.putText(frame, display_text, (20, 50), 
                        config.FONT, 1.2, color, 2, cv2.LINE_AA)
            
            # Subtitles (Bottom)
            text_size = cv2.getTextSize(text, config.FONT, 0.8, 2)[0]
            text_x = (w - text_size[0]) // 2
            cv2.putText(frame, text, (text_x, h - 25), 
                        config.FONT, 0.8, (255, 255, 255), 2, cv2.LINE_AA)
        else:
            cv2.putText(frame, "Waiting for gesture...", (20, 50), 
                        config.FONT, 1.0, (150, 150, 150), 2, cv2.LINE_AA)

        # 5. Status Indicators
        if is_speaking:
            cv2.circle(frame, (w - 40, 40), 10, (0, 255, 0), -1) # Green dot for speaking
        else:
            cv2.circle(frame, (w - 40, 40), 10, (100, 100, 100), -1) # Gray dot idle

        return frame

    def _update_fps(self):
        self.fps_counter += 1
        elapsed = time.time() - self.fps_start_time
        if elapsed > 1.0:
            self.fps = self.fps_counter / elapsed
            self.fps_counter = 0
            self.fps_start_time = time.time()

    def draw_landmarks(self, frame, hand_landmarks, mp_hands):
        """
        Custom landmark drawing for better aesthetics.
        """
        if hand_landmarks:
            h, w, c = frame.shape
            
            # Draw connections
            for connection in mp_hands.HAND_CONNECTIONS:
                start_idx = connection[0]
                end_idx = connection[1]
                
                start_point = hand_landmarks.landmark[start_idx]
                end_point = hand_landmarks.landmark[end_idx]
                
                start_x, start_y = int(start_point.x * w), int(start_point.y * h)
                end_x, end_y = int(end_point.x * w), int(end_point.y * h)
                
                cv2.line(frame, (start_x, start_y), (end_x, end_y), (255, 255, 255), 2)
            
            # Draw keypoints with custom colors
            for id, lm in enumerate(hand_landmarks.landmark):
                cx, cy = int(lm.x * w), int(lm.y * h)
                
                # Different colors for fingertips (ids 4, 8, 12, 16, 20)
                if id in [4, 8, 12, 16, 20]:
                    cv2.circle(frame, (cx, cy), 8, (0, 255, 255), -1) # Yellow tips
                    cv2.circle(frame, (cx, cy), 8, (255, 255, 255), 1) 
                else:
                    cv2.circle(frame, (cx, cy), 5, (0, 100, 255), -1) # Orange joints
