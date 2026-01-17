"""
Shark entity with AI behavior.
"""
import math
import random
import pygame
from .config import (
    SHARK_SIZE, MAX_SPEED, ACCEL, DAMPING, ESCAPE_RADIUS,
    WALL_MARGIN, CORNER_MARGIN, WALL_FORCE, WANDER_FORCE, PANIC_ESCAPE_SPEED,
    BLUE
)


class Shark:
    """Shark entity with escape AI and swimming animation."""
    
    def __init__(self, x, y, assets_path="assets"):
        self.pos = [x, y]
        self.vel = [0, 0]
        self.angle = 0  # Current rotation angle in degrees (0 = pointing up)
        self.target_angle = 0  # Target angle for smooth rotation
        self.rotation_speed = 8  # Degrees per frame for smooth rotation
        
        # Animation settings
        self.animation_frames = []  # List of original (unrotated) frames
        self.current_frame = 0
        self.animation_timer = 0
        self.base_animation_speed = 0.15  # Base frames per game tick
        
        # Load animation frames (left, middle, right tail positions)
        frame_names = ["shark-left.png", "shark-middle.png", "shark-right.png"]
        
        try:
            for frame_name in frame_names:
                img = pygame.image.load(f"{assets_path}/{frame_name}")
                original_size = img.get_size()
                scale_factor = SHARK_SIZE / original_size[0]
                self.size = (
                    int(original_size[0] * scale_factor),
                    int(original_size[1] * scale_factor)
                )
                scaled_img = pygame.transform.scale(img, self.size)
                self.animation_frames.append(scaled_img)
            
            # Animation sequence: left -> middle -> right -> middle (for smooth wave)
            self.animation_sequence = [0, 1, 2, 1]
            self.sequence_index = 0
            
        except FileNotFoundError as e:
            print(f"Shark image not found: {e}, using placeholder")
            self.animation_frames = []
            self.size = (50, 50)
    
    @property
    def center(self):
        """Get shark center position."""
        return (
            self.pos[0] + self.size[0] / 2,
            self.pos[1] + self.size[1] / 2
        )
    
    def update(self, hand_pos, screen_width, screen_height):
        """Update shark position based on AI behavior.
        
        Args:
            hand_pos: (x, y) tuple of hand position or None
            screen_width: Current screen width
            screen_height: Current screen height
        """
        center_x, center_y = self.center
        
        # --- Follow Hand ---
        if hand_pos:
            hx, hy = hand_pos
            
            # Direction towards hand
            dx = hx - center_x
            dy = hy - center_y
            dist = math.hypot(dx, dy)
            
            # Only move if not too close (prevents jittering)
            if dist > 30:
                if dist == 0:
                    dist = 1
                
                # Normalize direction
                dx /= dist
                dy /= dist
                
                # Acceleration towards hand (stronger when farther)
                follow_strength = ACCEL * (1 + min(dist / 200, 2))
                
                self.vel[0] += dx * follow_strength
                self.vel[1] += dy * follow_strength
        else:
            # Random wandering when no hand detected
            self.vel[0] += (random.random() - 0.5) * WANDER_FORCE
            self.vel[1] += (random.random() - 0.5) * WANDER_FORCE
        
        # Speed limit
        self._limit_speed()
        
        # Apply velocity
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        
        # Bounds checking
        self._check_bounds(screen_width, screen_height)
        
        # Damping
        self.vel[0] *= DAMPING
        self.vel[1] *= DAMPING
        
        # Update rotation based on velocity
        self._update_rotation()
    
    def _panic_escape(self, hx, hy, width, height,
                      near_left, near_right, near_top, near_bottom):
        """Execute panic escape to a safe zone."""
        safe_zones = []
        
        if near_left or near_top:
            safe_zones.append((width * 0.7, height * 0.7))
        if near_right or near_top:
            safe_zones.append((width * 0.3, height * 0.7))
        if near_left or near_bottom:
            safe_zones.append((width * 0.7, height * 0.3))
        if near_right or near_bottom:
            safe_zones.append((width * 0.3, height * 0.3))
        
        safe_zones.append((width * 0.5, height * 0.5))
        
        # Find zone farthest from hand
        best_zone = max(safe_zones,
                        key=lambda z: math.hypot(z[0] - hx, z[1] - hy))
        
        target_x = best_zone[0] + random.uniform(-100, 100)
        target_y = best_zone[1] + random.uniform(-100, 100)
        
        escape_dx = target_x - self.center[0]
        escape_dy = target_y - self.center[1]
        escape_dist = math.hypot(escape_dx, escape_dy)
        
        if escape_dist > 0:
            self.vel[0] = (escape_dx / escape_dist) * PANIC_ESCAPE_SPEED
            self.vel[1] = (escape_dy / escape_dist) * PANIC_ESCAPE_SPEED
    
    def _normal_escape(self, dx, dy, dist,
                       near_left, near_right, near_top, near_bottom):
        """Execute normal escape behavior."""
        if dist == 0:
            dist = 1
        
        escape_dir_x = dx / dist
        escape_dir_y = dy / dist
        
        # Adjust for walls
        if near_left:
            escape_dir_x = max(escape_dir_x, 0.5)
        if near_right:
            escape_dir_x = min(escape_dir_x, -0.5)
        if near_top:
            escape_dir_y = max(escape_dir_y, 0.5)
        if near_bottom:
            escape_dir_y = min(escape_dir_y, -0.5)
        
        # Renormalize
        norm = math.hypot(escape_dir_x, escape_dir_y)
        if norm > 0:
            escape_dir_x /= norm
            escape_dir_y /= norm
        
        escape_strength = ACCEL * (1.5 + (ESCAPE_RADIUS - dist) / ESCAPE_RADIUS)
        
        self.vel[0] += escape_dir_x * escape_strength
        self.vel[1] += escape_dir_y * escape_strength
    
    def _move_to_center(self, width, height):
        """Gently move towards screen center."""
        center_dx = width / 2 - self.center[0]
        center_dy = height / 2 - self.center[1]
        center_dist = math.hypot(center_dx, center_dy)
        
        if center_dist > 0:
            self.vel[0] += (center_dx / center_dist) * 0.3
            self.vel[1] += (center_dy / center_dist) * 0.3
    
    def _limit_speed(self):
        """Limit velocity to MAX_SPEED."""
        speed = math.hypot(self.vel[0], self.vel[1])
        if speed > MAX_SPEED:
            self.vel[0] = (self.vel[0] / speed) * MAX_SPEED
            self.vel[1] = (self.vel[1] / speed) * MAX_SPEED
    
    def _check_bounds(self, width, height):
        """Keep shark within screen bounds."""
        if self.pos[0] < 0:
            self.pos[0] = 0
            self.vel[0] = abs(self.vel[0]) * 0.5
        if self.pos[0] > width - self.size[0]:
            self.pos[0] = width - self.size[0]
            self.vel[0] = -abs(self.vel[0]) * 0.5
        
        if self.pos[1] < 0:
            self.pos[1] = 0
            self.vel[1] = abs(self.vel[1]) * 0.5
        if self.pos[1] > height - self.size[1]:
            self.pos[1] = height - self.size[1]
            self.vel[1] = -abs(self.vel[1]) * 0.5
    
    def _update_rotation(self):
        """Update shark rotation to face movement direction."""
        speed = math.hypot(self.vel[0], self.vel[1])
        
        # Only update target angle if moving fast enough
        if speed > 0.5:
            # Calculate angle from velocity
            # atan2 gives angle from positive X axis, but our image points up (negative Y)
            # So we need to adjust: heading up = 0 degrees
            # atan2(vx, -vy) gives us the angle where up is 0
            self.target_angle = math.degrees(math.atan2(self.vel[0], -self.vel[1]))
        
        # Smooth rotation interpolation
        angle_diff = self.target_angle - self.angle
        
        # Normalize angle difference to -180 to 180
        while angle_diff > 180:
            angle_diff -= 360
        while angle_diff < -180:
            angle_diff += 360
        
        # Apply rotation with speed limit
        if abs(angle_diff) < self.rotation_speed:
            self.angle = self.target_angle
        else:
            self.angle += self.rotation_speed if angle_diff > 0 else -self.rotation_speed
        
        # Normalize angle to 0-360
        self.angle = self.angle % 360
    
    def _update_animation(self):
        """Update swimming animation based on movement speed."""
        speed = math.hypot(self.vel[0], self.vel[1])
        
        # Animation speed increases with movement speed
        # Minimum speed for animation, faster swimming = faster tail
        animation_speed = self.base_animation_speed * (1 + speed / 3)
        
        self.animation_timer += animation_speed
        
        if self.animation_timer >= 1.0:
            self.animation_timer = 0
            self.sequence_index = (self.sequence_index + 1) % len(self.animation_sequence)
    
    def draw(self, screen):
        """Draw the shark on the screen with rotation and animation."""
        if self.animation_frames:
            # Update animation
            self._update_animation()
            
            # Get current frame from animation sequence
            frame_index = self.animation_sequence[self.sequence_index]
            current_frame = self.animation_frames[frame_index]
            
            # Rotate image around its center
            rotated_image = pygame.transform.rotate(current_frame, -self.angle)
            
            # Get new rect to center the rotated image properly
            rotated_rect = rotated_image.get_rect()
            
            # Calculate position to keep shark centered at self.pos + size/2
            center_x = self.pos[0] + self.size[0] / 2
            center_y = self.pos[1] + self.size[1] / 2
            
            rotated_rect.center = (int(center_x), int(center_y))
            
            screen.blit(rotated_image, rotated_rect)
        else:
            pygame.draw.rect(screen, BLUE, (*self.pos, *self.size))
