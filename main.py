"""
Baby Shark Escape - Main Game Entry Point

A simple interactive game for babies where a shark runs away from hand movements.
"""
import pygame
from game import Camera, HandTracker, Shark
from game.config import DEFAULT_WIDTH, DEFAULT_HEIGHT, GAME_TITLE


def main():
    # Initialize Pygame
    pygame.init()
    
    # Screen setup - Maximized window (fills screen resolution)
    display_info = pygame.display.Info()
    width, height = display_info.current_w, display_info.current_h
    screen = pygame.display.set_mode((width, height), pygame.NOFRAME)
    pygame.display.set_caption(GAME_TITLE)
    clock = pygame.time.Clock()
    
    # Hide mouse cursor for better immersion
    pygame.mouse.set_visible(False)
    
    # Initialize components
    camera = Camera()
    hand_tracker = HandTracker()
    shark = Shark(width // 2, height // 2)
    
    running = True
    
    try:
        while running:
            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    # ESC key to exit fullscreen
                    if event.key == pygame.K_ESCAPE:
                        running = False
            
            # Read camera frame
            success, frame_rgb = camera.read_frame()
            if not success:
                continue
            
            # Process frame for display
            frame_display, offset_x, offset_y, new_w, new_h = \
                camera.process_frame_for_display(frame_rgb, width, height)
            
            # Detect hands
            results = hand_tracker.detect(frame_rgb)
            hand_pos = hand_tracker.get_palm_position(
                results, new_w, new_h, offset_x, offset_y
            )
            
            # Render camera background
            frame_surface = pygame.surfarray.make_surface(frame_display.swapaxes(0, 1))
            screen.blit(frame_surface, (0, 0))
            
            # Update and draw shark
            shark.update(hand_pos, width, height)
            shark.draw(screen)
            
            # Debug: Draw hand position
            # if hand_pos:
            #     pygame.draw.circle(screen, (255, 0, 0), hand_pos, 15)
            
            pygame.display.flip()
            clock.tick(60)
    
    finally:
        # Cleanup
        camera.release()
        hand_tracker.close()
        pygame.quit()


if __name__ == "__main__":
    main()
