import customtkinter as ctk
from PIL import Image, ImageDraw
import threading
import os
import logging
from enum import Enum
from typing import Optional, Tuple
import requests
from io import BytesIO

logger = logging.getLogger(__name__)


class Emotion(Enum):
    """Character emotions"""
    HAPPY = "happy"
    SAD = "sad"
    THINKING = "thinking"
    CONFUSED = "confused"
    EXCITED = "excited"
    NEUTRAL = "neutral"
    ANGRY = "angry"
    LOVE = "love"


class AvatarService:
    """Avatar display service with emotions and animations"""

    def __init__(self, window_width: int = 1000, window_height: int = 700):
        self.window_width = window_width
        self.window_height = window_height
        
        # Avatar configuration
        self.avatar_width = 300
        self.avatar_height = 400
        self.current_emotion = Emotion.NEUTRAL
        self.animation_frame = 0
        self.is_animating = False
        
        # Character image URL
        self.character_url = "https://images2.alphacoders.com/918/thumb-1920-918885.jpg"
        self.character_image = None
        self.current_avatar_image = None
        
        # Load character
        self._load_character()

    def _load_character(self):
        """Load character image from URL"""
        try:
            response = requests.get(self.character_url, timeout=10)
            if response.status_code == 200:
                img = Image.open(BytesIO(response.content))
                # Resize to avatar dimensions
                self.character_image = img.resize(
                    (self.avatar_width, self.avatar_height),
                    Image.Resampling.LANCZOS
                )
                logger.info("Character image loaded successfully")
            else:
                logger.error(f"Failed to load image: {response.status_code}")
                self._create_fallback_avatar()
        except Exception as e:
            logger.error(f"Error loading character: {str(e)}")
            self._create_fallback_avatar()

    def _create_fallback_avatar(self):
        """Create fallback avatar if image load fails"""
        self.character_image = Image.new(
            'RGB',
            (self.avatar_width, self.avatar_height),
            color=(200, 200, 255)
        )
        draw = ImageDraw.Draw(self.character_image)
        # Draw simple face
        draw.ellipse([50, 50, 250, 250], fill=(255, 200, 100))
        draw.ellipse([100, 120, 140, 160], fill=(0, 0, 0))  # Left eye
        draw.ellipse([160, 120, 200, 160], fill=(0, 0, 0))  # Right eye

    def set_emotion(self, emotion: Emotion):
        """Set character emotion"""
        self.current_emotion = emotion
        self.animation_frame = 0
        self.is_animating = True
        logger.info(f"Emotion changed to: {emotion.value}")

    def _apply_emotion_effect(self, image: Image.Image, emotion: Emotion) -> Image.Image:
        """Apply visual effects based on emotion"""
        # Create a copy to modify
        modified = image.copy()
        draw = ImageDraw.Draw(modified, 'RGBA')
        
        width, height = modified.size
        center_x, center_y = width // 2, height // 2
        
        if emotion == Emotion.HAPPY:
            # Add happy aura (yellow glow)
            for i in range(5, 0, -1):
                alpha = int(50 * (5 - i) / 5)
                draw.ellipse(
                    [center_x - 160 - i*5, center_y - 200 - i*5,
                     center_x + 160 + i*5, center_y + 200 + i*5],
                    outline=(255, 255, 0, alpha),
                    width=2
                )
        
        elif emotion == Emotion.SAD:
            # Add sad aura (blue glow)
            for i in range(5, 0, -1):
                alpha = int(50 * (5 - i) / 5)
                draw.ellipse(
                    [center_x - 160 - i*5, center_y - 200 - i*5,
                     center_x + 160 + i*5, center_y + 200 + i*5],
                    outline=(0, 0, 255, alpha),
                    width=2
                )
            # Add teardrops
            tear_x = center_x + 50
            tear_y = center_y - 50
            for j in range(3):
                draw.ellipse(
                    [tear_x - 3, tear_y + j*15, tear_x + 3, tear_y + j*15 + 6],
                    fill=(173, 216, 230, 200)
                )
        
        elif emotion == Emotion.THINKING:
            # Add thinking aura (purple glow with question mark)
            for i in range(5, 0, -1):
                alpha = int(50 * (5 - i) / 5)
                draw.ellipse(
                    [center_x - 160 - i*5, center_y - 200 - i*5,
                     center_x + 160 + i*5, center_y + 200 + i*5],
                    outline=(200, 100, 200, alpha),
                    width=2
                )
            # Add thinking bulb
            bulb_x, bulb_y = center_x - 120, center_y - 180
            draw.ellipse([bulb_x - 10, bulb_y - 15, bulb_x + 10, bulb_y + 5], fill=(255, 255, 0, 200))
        
        elif emotion == Emotion.EXCITED:
            # Add excited aura (rainbow-like effect)
            for i in range(5, 0, -1):
                alpha = int(50 * (5 - i) / 5)
                draw.ellipse(
                    [center_x - 160 - i*5, center_y - 200 - i*5,
                     center_x + 160 + i*5, center_y + 200 + i*5],
                    outline=(255, 100, 255, alpha),
                    width=3
                )
            # Add sparkles
            for j in range(4):
                spark_x = center_x + (100 if j % 2 == 0 else -100)
                spark_y = center_y - 150 + (j % 2) * 100
                draw.polygon(
                    [(spark_x, spark_y - 10), (spark_x + 5, spark_y), 
                     (spark_x, spark_y + 10), (spark_x - 5, spark_y)],
                    fill=(255, 255, 100, 200)
                )
        
        elif emotion == Emotion.CONFUSED:
            # Add confused aura (swirl effect)
            for i in range(5, 0, -1):
                alpha = int(50 * (5 - i) / 5)
                draw.ellipse(
                    [center_x - 160 - i*5, center_y - 200 - i*5,
                     center_x + 160 + i*5, center_y + 200 + i*5],
                    outline=(255, 165, 0, alpha),
                    width=2
                )
        
        elif emotion == Emotion.LOVE:
            # Add love hearts
            heart_positions = [
                (center_x - 100, center_y - 150),
                (center_x + 100, center_y - 150),
                (center_x, center_y - 100),
            ]
            for hx, hy in heart_positions:
                # Simple heart shape
                draw.ellipse([hx - 8, hy - 8, hx + 8, hy], fill=(255, 0, 0, 200))
                draw.ellipse([hx - 15, hy - 8, hx - 1, hy], fill=(255, 0, 0, 200))
                draw.polygon([(hx - 15, hy), (hx + 8, hy), (hx - 3, hy + 15)], fill=(255, 0, 0, 200))
        
        elif emotion == Emotion.ANGRY:
            # Add angry aura (red glow)
            for i in range(5, 0, -1):
                alpha = int(50 * (5 - i) / 5)
                draw.ellipse(
                    [center_x - 160 - i*5, center_y - 200 - i*5,
                     center_x + 160 + i*5, center_y + 200 + i*5],
                    outline=(255, 0, 0, alpha),
                    width=3
                )
            # Add fire effect
            for j in range(3):
                fire_x = center_x + (120 if j % 2 == 0 else -120)
                fire_y = center_y - 100 + j * 30
                draw.polygon(
                    [(fire_x, fire_y), (fire_x + 15, fire_y + 20), 
                     (fire_x - 15, fire_y + 20)],
                    fill=(255, 100, 0, 200)
                )
        
        return modified

    def get_avatar_image(self) -> Image.Image:
        """Get current avatar image with emotion effect"""
        if self.character_image is None:
            return None
        
        # Apply emotion effect
        self.current_avatar_image = self._apply_emotion_effect(
            self.character_image,
            self.current_emotion
        )
        
        return self.current_avatar_image

    def animate(self):
        """Animate avatar (for future frame-based animations)"""
        if self.is_animating:
            self.animation_frame += 1
            if self.animation_frame > 30:  # 30 frames of animation
                self.animation_frame = 0
                self.is_animating = False

    def create_avatar_widget(self, parent_frame: ctk.CTkFrame) -> ctk.CTkLabel:
        """Create avatar widget for UI"""
        avatar_label = ctk.CTkLabel(
            parent_frame,
            text="",
            width=self.avatar_width,
            height=self.avatar_height
        )
        return avatar_label

    def update_avatar_display(self, label: ctk.CTkLabel):
        """Update avatar display on label"""
        try:
            avatar_img = self.get_avatar_image()
            if avatar_img:
                # Convert PIL image to PhotoImage
                photo = ctk.CTkImage(
                    light_image=avatar_img,
                    dark_image=avatar_img,
                    size=(self.avatar_width, self.avatar_height)
                )
                label.configure(image=photo, text="")
                label.image = photo
                self.animate()
        except Exception as e:
            logger.error(f"Error updating avatar: {str(e)}")


class AvatarManager:
    """Manager for avatar lifecycle and updates"""
    
    def __init__(self, parent_frame: ctk.CTkFrame):
        self.service = AvatarService()
        self.parent_frame = parent_frame
        self.avatar_label = self.service.create_avatar_widget(parent_frame)
        self.avatar_label.pack(pady=20)
        
        self.update_thread = None
        self.is_running = True

    def set_emotion(self, emotion: Emotion):
        """Set avatar emotion"""
        self.service.set_emotion(emotion)

    def start_update_loop(self, update_interval: int = 100):
        """Start avatar update loop"""
        self.update_thread = threading.Thread(
            target=self._update_loop,
            args=(update_interval,),
            daemon=True
        )
        self.update_thread.start()

    def _update_loop(self, interval: int):
        """Update avatar display periodically"""
        while self.is_running:
            try:
                self.service.update_avatar_display(self.avatar_label)
                threading.Event().wait(interval / 1000)
            except Exception as e:
                logger.error(f"Update loop error: {str(e)}")

    def stop(self):
        """Stop avatar updates"""
        self.is_running = False
        if self.update_thread:
            self.update_thread.join(timeout=2)

    def get_emotion(self) -> Emotion:
        """Get current emotion"""
        return self.service.current_emotion
