
import os
from pathlib import Path


class SoundManager:
    """
    Oriri sound manager.

    Supports:
    - WAV audio
    - OGG audio
    - MP3 audio (depending on pygame's audio support)
    - Sound previews
    - Continuous alarm playback
    - Volume control
    - Stopping playback
    """

    SUPPORTED_FORMATS = {
        ".wav",
        ".ogg",
        ".mp3"
    }

    def __init__(self, sound_folder=None, volume=0.75):

        self.base_dir = Path(__file__).resolve().parent.parent

        self.sound_folder = (
            Path(sound_folder)
            if sound_folder
            else self.base_dir / "assets" / "sounds"
        )

        self.volume = max(0.0, min(1.0, float(volume)))

        self.current_sound = None
        self.is_playing = False
        self.pygame = None
        self.mixer_ready = False

        self.sound_folder.mkdir(
            parents=True,
            exist_ok=True
        )

    # ------------------------------------------------------
    # SOUND LIBRARY
    # ------------------------------------------------------

    def get_available_sounds(self):

        sounds = []

        if not self.sound_folder.exists():
            return sounds

        for file in sorted(self.sound_folder.iterdir()):

            if not file.is_file():
                continue

            if file.suffix.lower() not in self.SUPPORTED_FORMATS:
                continue

            sounds.append({
                "id": file.name,
                "name": file.stem.replace("_", " ").replace("-", " ").title(),
                "filename": file.name,
                "path": str(file.resolve()),
                "format": file.suffix.lower()
            })

        return sounds

    def get_sound(self, sound_id):

        if not sound_id:
            return None

        for sound in self.get_available_sounds():

            if sound["id"] == sound_id:
                return sound

        return None

    # ------------------------------------------------------
    # AUDIO INITIALIZATION
    # ------------------------------------------------------

    def initialize(self):

        if self.mixer_ready:
            return True

        try:
            import pygame

            self.pygame = pygame

            pygame.mixer.init()
            pygame.mixer.music.set_volume(self.volume)

            self.mixer_ready = True

            return True

        except ImportError as error:
            raise RuntimeError(
                "Pygame is not installed. Run: pip install pygame"
            ) from error

        except Exception as error:
            raise RuntimeError(
                f"Could not initialize the audio system: {error}"
            ) from error

    # ------------------------------------------------------
    # PLAY SOUND
    # ------------------------------------------------------

    def play(self, sound_id, loop=False):

        sound = self.get_sound(sound_id)

        if sound is None:
            raise FileNotFoundError(
                f"Sound '{sound_id}' was not found in the sound library."
            )

        self.initialize()

        try:
            self.stop()

            self.pygame.mixer.music.load(sound["path"])

            self.pygame.mixer.music.set_volume(self.volume)

            self.pygame.mixer.music.play(
                loops=-1 if loop else 0
            )

            self.current_sound = sound_id
            self.is_playing = True

            return True

        except Exception as error:
            self.current_sound = None
            self.is_playing = False

            raise RuntimeError(
                f"Could not play {sound['name']}: {error}"
            ) from error

    # ------------------------------------------------------
    # PREVIEW SOUND
    # ------------------------------------------------------

    def preview(self, sound_id):

        return self.play(
            sound_id,
            loop=False
        )

    # ------------------------------------------------------
    # PLAY ALARM
    # ------------------------------------------------------

    def play_alarm(self, sound_id):

        return self.play(
            sound_id,
            loop=True
        )

    # ------------------------------------------------------
    # STOP PLAYBACK
    # ------------------------------------------------------

    def stop(self):

        if not self.mixer_ready:
            self.current_sound = None
            self.is_playing = False
            return

        try:
            self.pygame.mixer.music.stop()

        finally:
            self.current_sound = None
            self.is_playing = False

    # ------------------------------------------------------
    # VOLUME
    # ------------------------------------------------------

    def set_volume(self, volume):

        self.volume = max(
            0.0,
            min(1.0, float(volume))
        )

        if self.mixer_ready:
            self.pygame.mixer.music.set_volume(
                self.volume
            )

    def get_volume(self):

        return self.volume

    # ------------------------------------------------------
    # PLAYBACK STATUS
    # ------------------------------------------------------

    def get_status(self):

        if not self.mixer_ready:
            return {
                "playing": False,
                "sound": None,
                "volume": self.volume
            }

        playing = self.pygame.mixer.music.get_busy()

        self.is_playing = playing

        return {
            "playing": playing,
            "sound": self.current_sound if playing else None,
            "volume": self.volume
        }

    # ------------------------------------------------------
    # CLEANUP
    # ------------------------------------------------------

    def shutdown(self):

        self.stop()

        if self.mixer_ready:
            self.pygame.mixer.quit()

        self.mixer_ready = False
        self.pygame = None


# Shared sound manager for Oriri
sound_manager = SoundManager()
