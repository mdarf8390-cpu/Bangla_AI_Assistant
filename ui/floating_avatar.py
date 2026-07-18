import tkinter as tk
from tkinter import Canvas
from PIL import Image, ImageDraw, ImageFont
import threading
import math
import random
import logging
from enum import Enum
from typing import Tuple
import requests
from io import BytesIO
import json
import os

logger = logging.getLogger(__name__)


class Emotion(Enum):
    """Character emotions with behaviors"""
    HAPPY = "happy"
    SAD = "sad"
    THINKING = "thinking"
    CONFUSED = "confused"
    EXCITED = "excited"
    NEUTRAL = "neutral"
    ANGRY = "angry"
    LOVE = "love"


class AnimatedCharacter:
    """Animated 2D character with emotions"""

    def __init__(self, width: int = 300, height: int = 400):
        self.width = width
        self.height = height
        self.base_image = None
        self.current_image = None
        
        # Animation parameters
        self.animation_frame = 0
        self.animation_speed = 1
        self.current_emotion = Emotion.NEUTRAL
        self.idle_animation = True
        
        # Character position for movement
        self.head_offset_x = 0
        self.head_offset_y = 0
        self.left_arm_angle = 0
        self.right_arm_angle = 0
        self.left_leg_angle = 0
        self.right_leg_angle = 0
        
        # Eyes and mouth
        self.left_eye_x = 0
        self.left_eye_y = 0
        self.right_eye_x = 0
        self.right_eye_y = 0
        self.mouth_open = 0
        
        # Load character
        self._load_character()

    def _load_character(self):
        """Load character from image or create fallback"""
        try:
            url = "https://images2.alphacoders.com/918/thumb-1920-918885.jpg"
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                img = Image.open(BytesIO(response.content))
                self.base_image = img.resize((self.width, self.height), Image.Resampling.LANCZOS)
                logger.info("Character image loaded")
            else:
                self._create_character()
        except Exception as e:
            logger.warning(f"Failed to load character: {e}")
            self._create_character()

    def _create_character(self):
        """Create simple character drawing"""
        self.base_image = Image.new('RGBA', (self.width, self.height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(self.base_image)
        
        # Body
        draw.ellipse([100, 150, 200, 280], fill=(255, 200, 100), outline=(200, 100, 0), width=2)
        
        # Head
        draw.ellipse([80, 50, 220, 150], fill=(255, 200, 100), outline=(200, 100, 0), width=2)
        
        # Eyes
        draw.ellipse([110, 80, 130, 100], fill=(0, 0, 0))
        draw.ellipse([170, 80, 190, 100], fill=(0, 0, 0))
        draw.ellipse([115, 85, 125, 95], fill=(255, 255, 255))
        draw.ellipse([175, 85, 185, 95], fill=(255, 255, 255))
        
        # Mouth
        draw.arc([130, 100, 170, 120], 0, 180, fill=(0, 0, 0), width=2)

    def _draw_character_with_animation(self) -> Image.Image:
        """Draw character with current animation state"""
        # Start with base image
        if self.base_image:
            img = self.base_image.copy().convert('RGBA')
        else:
            img = Image.new('RGBA', (self.width, self.height), (0, 0, 0, 0))
        
        draw = ImageDraw.Draw(img, 'RGBA')
        center_x, center_y = self.width // 2, self.height // 2
        
        # Draw animated body parts based on emotion and frame
        self._draw_animation(draw, center_x, center_y)
        
        # Apply emotion effects
        self._apply_emotion_effects(draw, center_x, center_y)
        
        return img

    def _draw_animation(self, draw, cx: int, cy: int):
        """Draw animated body parts"""
        frame = self.animation_frame % 60
        
        # Idle bobbing
        bob_offset = math.sin(frame * math.pi / 30) * 3
        
        if self.current_emotion == Emotion.HAPPY:
            # Dancing animation
            sway = math.sin(frame * math.pi / 15) * 10
            self.head_offset_x = sway
            self.head_offset_y = bob_offset - 5
            self.left_arm_angle = math.sin(frame * math.pi / 10) * 30
            self.right_arm_angle = math.cos(frame * math.pi / 10) * 30
            self.left_leg_angle = math.sin(frame * math.pi / 12) * 15
            self.right_leg_angle = math.cos(frame * math.pi / 12) * 15
            self.mouth_open = abs(math.sin(frame * math.pi / 20)) * 20
        
        elif self.current_emotion == Emotion.SAD:
            # Sad drooping
            self.head_offset_y = bob_offset + 5
            self.left_arm_angle = 25
            self.right_arm_angle = 25
            self.mouth_open = -10
        
        elif self.current_emotion == Emotion.THINKING:
            # Head scratch animation
            scratch_angle = math.sin(frame * math.pi / 15) * 20
            self.left_arm_angle = 90 + scratch_angle
            self.head_offset_y = bob_offset - 2
        
        elif self.current_emotion == Emotion.EXCITED:
            # Jumping animation
            jump = abs(math.sin(frame * math.pi / 10)) * 20
            self.head_offset_y = -jump + bob_offset
            self.left_arm_angle = math.sin(frame * math.pi / 8) * 50
            self.right_arm_angle = math.sin(frame * math.pi / 8 + math.pi) * 50
            self.mouth_open = 25
        
        elif self.current_emotion == Emotion.CONFUSED:
            # Head tilting
            tilt = math.sin(frame * math.pi / 20) * 15
            self.head_offset_x = tilt
            self.left_eye_x = abs(math.sin(frame * math.pi / 15)) * 5
            self.right_eye_x = -abs(math.cos(frame * math.pi / 15)) * 5
        
        elif self.current_emotion == Emotion.ANGRY:
            # Angry pacing
            pace = math.sin(frame * math.pi / 12) * 15
            self.head_offset_x = pace
            self.left_leg_angle = -math.sin(frame * math.pi / 12) * 20
            self.right_leg_angle = math.sin(frame * math.pi / 12) * 20
        
        elif self.current_emotion == Emotion.LOVE:
            # Spinning animation
            spin = (frame / 60) * 360
            self.head_offset_y = math.sin(frame * math.pi / 15) * 5
            self.left_arm_angle = 30
            self.right_arm_angle = -30
        
        else:  # NEUTRAL
            # Idle breathing
            self.head_offset_y = bob_offset
            self.left_arm_angle = 0
            self.right_arm_angle = 0
        
        # Draw arms
        self._draw_limb(draw, cx, cy + 100, 50, self.left_arm_angle, (255, 200, 100))
        self._draw_limb(draw, cx, cy + 100, 50, self.right_arm_angle, (255, 200, 100))
        
        # Draw legs
        self._draw_limb(draw, cx - 20, cy + 200, 40, self.left_leg_angle, (100, 100, 200))
        self._draw_limb(draw, cx + 20, cy + 200, 40, self.right_leg_angle, (100, 100, 200))

    def _draw_limb(self, draw, x: int, y: int, length: int, angle: float, color: Tuple):
        """Draw animated limb"""
        rad = math.radians(angle)
        end_x = int(x + length * math.cos(rad))
        end_y = int(y + length * math.sin(rad))
        draw.line([(x, y), (end_x, end_y)], fill=color + (255,), width=8)
        # Joint
        draw.ellipse([end_x - 6, end_y - 6, end_x + 6, end_y + 6], fill=color)

    def _apply_emotion_effects(self, draw, cx: int, cy: int):
        """Apply visual effects based on emotion"""
        frame = self.animation_frame
        
        if self.current_emotion == Emotion.HAPPY:
            # Yellow happy glow
            alpha = int(100 + 50 * math.sin(frame * math.pi / 30))
            for i in range(3, 0, -1):
                draw.ellipse(
                    [cx - 160 - i*5, cy - 200 - i*5, cx + 160 + i*5, cy + 200 + i*5],
                    outline=(255, 255, 0, alpha),
                    width=2
                )
        
        elif self.current_emotion == Emotion.SAD:
            # Blue sad glow + tears
            for i in range(3, 0, -1):
                draw.ellipse(
                    [cx - 160 - i*5, cy - 200 - i*5, cx + 160 + i*5, cy + 200 + i*5],
                    outline=(100, 150, 255, 100),
                    width=2
                )
            # Tears
            tear_x1, tear_y1 = cx - 40, cy - 50
            tear_x2, tear_y2 = cx + 40, cy - 50
            for j in range(4):
                draw.ellipse(
                    [tear_x1 - 2, tear_y1 + j*10, tear_x1 + 2, tear_y1 + j*10 + 5],
                    fill=(100, 150, 255, 200)
                )
                draw.ellipse(
                    [tear_x2 - 2, tear_y2 + j*10, tear_x2 + 2, tear_y2 + j*10 + 5],
                    fill=(100, 150, 255, 200)
                )
        
        elif self.current_emotion == Emotion.THINKING:
            # Purple thinking aura
            for i in range(3, 0, -1):
                draw.ellipse(
                    [cx - 160 - i*5, cy - 200 - i*5, cx + 160 + i*5, cy + 200 + i*5],
                    outline=(200, 100, 200, 100),
                    width=2
                )
            # Thinking bubble
            bubble_x, bubble_y = cx + 100, cy - 150
            draw.ellipse([bubble_x - 15, bubble_y - 20, bubble_x + 15, bubble_y + 10], fill=(255, 255, 100, 200))
            draw.ellipse([bubble_x - 8, bubble_y - 10, bubble_x + 8, bubble_y + 3], fill=(255, 255, 100, 200))
        
        elif self.current_emotion == Emotion.EXCITED:
            # Rainbow sparkles
            for i in range(3, 0, -1):
                draw.ellipse(
                    [cx - 160 - i*5, cy - 200 - i*5, cx + 160 + i*5, cy + 200 + i*5],
                    outline=(255, 100 + int(155 * math.sin(frame * math.pi / 15)), 255, 150),
                    width=3
                )
            # Sparkles
            for j in range(6):
                angle = (frame / 30 + j * 60) * math.pi / 180
                spark_x = cx + 130 * math.cos(angle)
                spark_y = cy - 170 + 50 * math.sin(angle)
                draw.polygon(
                    [(spark_x, spark_y - 8), (spark_x + 6, spark_y), (spark_x, spark_y + 8), (spark_x - 6, spark_y)],
                    fill=(255, 255, 100, 200)
                )
        
        elif self.current_emotion == Emotion.CONFUSED:
            # Orange swirl
            for i in range(5, 0, -1):
                angle = (frame / 60) * 360
                draw.ellipse(
                    [cx - 160 - i*4, cy - 200 - i*4, cx + 160 + i*4, cy + 200 + i*4],
                    outline=(255, 165, 0, int(100 - i * 15)),
                    width=1
                )
        
        elif self.current_emotion == Emotion.ANGRY:
            # Red angry aura + fire
            for i in range(5, 0, -1):
                draw.ellipse(
                    [cx - 160 - i*5, cy - 200 - i*5, cx + 160 + i*5, cy + 200 + i*5],
                    outline=(255, 0, 0, 100),
                    width=3
                )
            # Fire
            for j in range(4):
                fire_x = cx + (130 if j % 2 == 0 else -130)
                fire_y = cy - 100 + j * 40
                draw.polygon(
                    [(fire_x, fire_y), (fire_x + 15, fire_y + 25), (fire_x - 15, fire_y + 25)],
                    fill=(255, 100 + int(155 * random.random()), 0, 200)
                )
        
        elif self.current_emotion == Emotion.LOVE:
            # Hearts rotating
            for j in range(4):
                angle = (frame / 60) * 360 + j * 90
                rad = math.radians(angle)
                hx = cx + 120 * math.cos(rad)
                hy = cy - 150 + 60 * math.sin(rad)
                self._draw_heart(draw, hx, hy, 12)

    def _draw_heart(self, draw, x: float, y: float, size: int):
        """Draw heart shape"""
        # Simple heart shape
        points = [
            (x, y - size),
            (x - size, y - size // 2),
            (x - size // 2, y + size // 2),
            (x, y + size),
            (x + size // 2, y + size // 2),
            (x + size, y - size // 2),
        ]
        draw.polygon(points, fill=(255, 0, 0, 200))

    def update(self, emotion: Emotion = None):
        """Update animation frame and emotion"""
        if emotion:
            self.current_emotion = emotion
        
        self.animation_frame += self.animation_speed
        self.animation_frame %= 360
        
        self.current_image = self._draw_character_with_animation()

    def get_image(self) -> Image.Image:
        """Get current character image"""
        if self.current_image is None:
            self.update()
        return self.current_image


class FloatingCharacterWindow:
    """Floating transparent window with animated character"""

    def __init__(self, on_emotion_change=None):
        self.root = tk.Tk()
        self.root.title("Ayesha Avatar")
        self.root.geometry("300x400+100+100")
        self.root.config(bg='black')
        self.root.attributes('-transparentcolor', 'black')
        self.root.attributes('-topmost', True)
        
        # Make window draggable
        self.drag_data = {"x": 0, "y": 0}
        
        # Canvas for animation
        self.canvas = Canvas(
            self.root,
            width=300,
            height=400,
            bg='black',
            highlightthickness=0
        )
        self.canvas.pack(fill="both", expand=True)
        self.canvas.bind("<Button-1>", self._start_drag)
        self.canvas.bind("<B1-Motion>", self._drag)
        
        # Character
        self.character = AnimatedCharacter(300, 400)
        self.photo_image = None
        
        # Animation thread
        self.running = True
        self.update_thread = threading.Thread(target=self._animation_loop, daemon=True)
        self.update_thread.start()
        
        # Emotion callback
        self.on_emotion_change = on_emotion_change
        
        # Position persistence
        self.config_file = "avatar_config.json"
        self._load_position()
        
        # Close handler
        self.root.protocol("WM_DELETE_WINDOW", self._on_closing)

    def _start_drag(self, event):
        """Start window dragging"""
        self.drag_data["x"] = event.x_root - self.root.winfo_x()
        self.drag_data["y"] = event.y_root - self.root.winfo_y()

    def _drag(self, event):
        """Drag window"""
        x = event.x_root - self.drag_data["x"]
        y = event.y_root - self.drag_data["y"]
        self.root.geometry(f"+{x}+{y}")
        self._save_position()

    def _save_position(self):
        """Save window position"""
        try:
            config = {
                "x": self.root.winfo_x(),
                "y": self.root.winfo_y()
            }
            with open(self.config_file, 'w') as f:
                json.dump(config, f)
        except Exception as e:
            logger.error(f"Error saving position: {e}")

    def _load_position(self):
        """Load saved window position"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                    x, y = config.get("x", 100), config.get("y", 100)
                    self.root.geometry(f"+{x}+{y}")
        except Exception as e:
            logger.error(f"Error loading position: {e}")

    def _animation_loop(self):
        """Animation update loop"""
        while self.running:
            try:
                self.character.update()
                img = self.character.get_image()
                
                # Convert to PhotoImage
                from PIL import ImageTk
                self.photo_image = ImageTk.PhotoImage(img)
                
                # Update canvas
                self.canvas.create_image(150, 200, image=self.photo_image)
                
                # Small delay for smooth animation
                threading.Event().wait(0.05)
            except Exception as e:
                logger.error(f"Animation error: {e}")

    def set_emotion(self, emotion: Emotion):
        """Set character emotion"""
        self.character.current_emotion = emotion
        if self.on_emotion_change:
            self.on_emotion_change(emotion)

    def show(self):
        """Show the window"""
        self.root.mainloop()

    def _on_closing(self):
        """Handle window close"""
        self.running = False
        self._save_position()
        self.root.destroy()

    def update_emotion_external(self, emotion: Emotion):
        """Update emotion from external source"""
        self.set_emotion(emotion)


# Test if running directly
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    window = FloatingCharacterWindow()
    
    # Demo: Change emotions
    import time
    def demo_emotions():
        emotions = [Emotion.NEUTRAL, Emotion.HAPPY, Emotion.THINKING, Emotion.EXCITED, 
                   Emotion.SAD, Emotion.ANGRY, Emotion.CONFUSED, Emotion.LOVE]
        while True:
            for emotion in emotions:
                window.set_emotion(emotion)
                time.sleep(3)
    
    demo_thread = threading.Thread(target=demo_emotions, daemon=True)
    demo_thread.start()
    
    window.show()
