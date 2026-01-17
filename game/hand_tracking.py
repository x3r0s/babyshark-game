"""
Hand tracking module using MediaPipe.
"""
import mediapipe as mp
from .config import (
    MAX_NUM_HANDS,
    MIN_DETECTION_CONFIDENCE,
    MIN_TRACKING_CONFIDENCE,
    PALM_LANDMARK_INDEX
)


class HandTracker:
    """Handles hand detection and tracking using MediaPipe."""
    
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            max_num_hands=MAX_NUM_HANDS,
            min_detection_confidence=MIN_DETECTION_CONFIDENCE,
            min_tracking_confidence=MIN_TRACKING_CONFIDENCE
        )
    
    def detect(self, frame_rgb):
        """Detect hands in a frame.
        
        Args:
            frame_rgb: RGB frame to process
            
        Returns:
            MediaPipe results object
        """
        frame_rgb.flags.writeable = False
        return self.hands.process(frame_rgb)
    
    def get_palm_position(self, results, new_w, new_h, offset_x, offset_y):
        """Extract palm position from detection results.
        
        Args:
            results: MediaPipe detection results
            new_w, new_h: Scaled frame dimensions
            offset_x, offset_y: Crop offsets
            
        Returns:
            tuple: (x, y) screen coordinates or None if no hand detected
        """
        if not results.multi_hand_landmarks:
            return None
        
        for hand_landmarks in results.multi_hand_landmarks:
            # Get normalized coordinates
            norm_x = hand_landmarks.landmark[PALM_LANDMARK_INDEX].x
            norm_y = hand_landmarks.landmark[PALM_LANDMARK_INDEX].y
            
            # Map to resized frame
            scaled_x = norm_x * new_w
            scaled_y = norm_y * new_h
            
            # Adjust for crop offset
            screen_x = scaled_x - offset_x
            screen_y = scaled_y - offset_y
            
            return (int(screen_x), int(screen_y))
        
        return None
    
    def close(self):
        """Release resources."""
        self.hands.close()
