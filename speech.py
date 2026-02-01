import threading
import time
from io import BytesIO
from gtts import gTTS
import pygame
import config

class SpeechEngine:
    def __init__(self):
        pygame.mixer.init()
        self.last_speak_time = 0
        self.last_text = ""
        self.is_speaking = False

    def speak(self, text, force=False):
        """
        Speak the given text.
        
        Args:
            text (str): The text to speak.
            force (bool): If True, ignore the interval cooldown.
        """
        current_time = time.time()
        
        # Don't repeat same text too quickly unless forced
        if not force and text == self.last_text and (current_time - self.last_speak_time < config.SPEAK_INTERVAL):
            return

        # If currently speaking, don't interrupt unless needed (logic can be adjusted)
        if self.is_speaking and pygame.mixer.music.get_busy():
            return

        self.last_text = text
        self.last_speak_time = current_time
        self.is_speaking = True
        
        # Run TTS in a separate thread to avoid blocking main loop
        threading.Thread(target=self._play_audio, args=(text,), daemon=True).start()

    def _play_audio(self, text):
        try:
            mp3_fp = BytesIO()
            tts = gTTS(text=text, lang=config.SPEECH_LANG)
            tts.write_to_fp(mp3_fp)
            mp3_fp.seek(0)
            
            pygame.mixer.music.load(mp3_fp)
            pygame.mixer.music.play()
            
            while pygame.mixer.music.get_busy():
                time.sleep(0.1)
                
            self.is_speaking = False
            
        except Exception as e:
            print(f"Error in speech engine: {e}")
            self.is_speaking = False

    def stop(self):
        if pygame.mixer.get_init():
            pygame.mixer.music.stop()
