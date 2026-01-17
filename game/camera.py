"""
Camera module for webcam capture and frame processing.
"""
import cv2
import numpy as np


class Camera:
    """Handles webcam capture and frame processing."""
    
    def __init__(self, camera_index=0):
        self.cap = cv2.VideoCapture(camera_index)
        
        # Request highest possible resolution for better quality
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
        
        # Disable auto-processing that might affect quality
        self.cap.set(cv2.CAP_PROP_AUTOFOCUS, 1)  # Enable autofocus
        self.cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1)  # Enable auto exposure
        
        if not self.cap.isOpened():
            raise RuntimeError("Cannot open camera")
        
        # Get actual resolution (camera might not support requested)
        self.actual_width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.actual_height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        print(f"Camera resolution: {self.actual_width}x{self.actual_height}")
    
    def read_frame(self):
        """Read and preprocess a frame from the camera.
        
        Returns:
            tuple: (success, rgb_frame) where rgb_frame is flipped and converted to RGB
        """
        success, frame = self.cap.read()
        if not success:
            return False, None
        
        # Flip for mirror effect
        frame = cv2.flip(frame, 1)
        # Convert BGR to RGB (using precise conversion)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        return True, frame_rgb
    
    def process_frame_for_display(self, frame_rgb, target_width, target_height):
        """Resize and crop frame to fit display while preserving aspect ratio.
        
        Args:
            frame_rgb: RGB frame from camera
            target_width: Target display width
            target_height: Target display height
            
        Returns:
            tuple: (processed_frame, offset_x, offset_y, new_w, new_h)
        """
        frame_h, frame_w, _ = frame_rgb.shape
        
        # Calculate scale (cover style - fill screen, crop excess)
        scale_w = target_width / frame_w
        scale_h = target_height / frame_h
        scale = max(scale_w, scale_h)
        
        new_w = int(frame_w * scale)
        new_h = int(frame_h * scale)
        
        # Choose interpolation based on scaling direction
        # INTER_AREA is best for shrinking (preserves sharpness)
        # INTER_LANCZOS4 is best for enlarging (high quality)
        if scale < 1.0:
            interpolation = cv2.INTER_AREA
        else:
            interpolation = cv2.INTER_LANCZOS4
        
        # Resize frame with high-quality interpolation
        resized = cv2.resize(frame_rgb, (new_w, new_h), interpolation=interpolation)
        
        # Calculate crop offsets
        offset_x = (new_w - target_width) // 2
        offset_y = (new_h - target_height) // 2
        
        # Crop to target size
        cropped = resized[offset_y:offset_y+target_height, offset_x:offset_x+target_width]
        
        # Ensure the array is contiguous for efficient pygame conversion
        cropped = np.ascontiguousarray(cropped)
        
        return cropped, offset_x, offset_y, new_w, new_h
    
    def release(self):
        """Release the camera resource."""
        self.cap.release()
