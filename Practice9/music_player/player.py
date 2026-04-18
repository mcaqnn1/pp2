import pygame
import os
import time


class MusicPlayer:
    """
    Manages playlist, playback state, and track position.
    Uses pygame.mixer for audio.
    """

    STOPPED  = "STOPPED"
    PLAYING  = "PLAYING"
    PAUSED   = "PAUSED"

    def __init__(self, music_dir: str = "music"):
        pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)

        self.music_dir    = music_dir
        self.playlist     = []          
        self.track_index  = 0           
        self.state        = self.STOPPED
        self._play_start  = 0.0         
        self._pause_pos   = 0.0         

        self._scan_directory()


    def _scan_directory(self):
        """Load all .mp3 / .wav files from music_dir."""
        supported = (".mp3", ".wav", ".ogg", ".flac")
        if os.path.isdir(self.music_dir):
            files = sorted(
                f for f in os.listdir(self.music_dir)
                if f.lower().endswith(supported)
            )
            self.playlist = [os.path.join(self.music_dir, f) for f in files]

    def reload(self):
        self._scan_directory()


    def play(self):
        """Play current track from the beginning (or resume if paused)."""
        if not self.playlist:
            return

        if self.state == self.PAUSED:
            pygame.mixer.music.unpause()
            self._play_start = time.time() - self._pause_pos
            self.state = self.PLAYING
            return

        path = self.playlist[self.track_index]
        try:
            pygame.mixer.music.load(path)
            pygame.mixer.music.play()
            self._play_start = time.time()
            self._pause_pos  = 0.0
            self.state       = self.PLAYING
        except pygame.error as e:
            print(f"[Player] Could not load '{path}': {e}")

    def stop(self):
        pygame.mixer.music.stop()
        self._pause_pos = 0.0
        self.state      = self.STOPPED

    def pause(self):
        if self.state == self.PLAYING:
            pygame.mixer.music.pause()
            self._pause_pos = time.time() - self._play_start
            self.state      = self.PAUSED

    def toggle_play_pause(self):
        if self.state == self.PLAYING:
            self.pause()
        else:
            self.play()

    def next_track(self):
        if not self.playlist:
            return
        self.track_index = (self.track_index + 1) % len(self.playlist)
        if self.state in (self.PLAYING, self.PAUSED):
            self.state = self.STOPPED
            self.play()

    def prev_track(self):
        if not self.playlist:
            return
        self.track_index = (self.track_index - 1) % len(self.playlist)
        if self.state in (self.PLAYING, self.PAUSED):
            self.state = self.STOPPED
            self.play()


    @property
    def current_path(self) -> str:
        if not self.playlist:
            return ""
        return self.playlist[self.track_index]

    @property
    def current_name(self) -> str:
        if not self.playlist:
            return "No tracks found"
        name = os.path.basename(self.current_path)
        return os.path.splitext(name)[0]

    @property
    def position_seconds(self) -> float:
        """Elapsed seconds for the current track."""
        if self.state == self.PLAYING:
            return time.time() - self._play_start
        if self.state == self.PAUSED:
            return self._pause_pos
        return 0.0

    @property
    def progress(self) -> float:
        """Fraction 0.0–1.0 (caps at 1.0). Needs sound length info."""
        length = self.track_length_seconds
        if length <= 0:
            return 0.0
        return min(self.position_seconds / length, 1.0)

    @property
    def track_length_seconds(self) -> float:
        """Duration of current track (requires mixer to have loaded it)."""
        try:
            snd = pygame.mixer.Sound(self.current_path)
            return snd.get_length()
        except Exception:
            return 0.0

    @staticmethod
    def fmt_time(seconds: float) -> str:
        seconds = max(0, int(seconds))
        m, s = divmod(seconds, 60)
        return f"{m:02d}:{s:02d}"

    def check_track_ended(self):
        """Call each frame; auto-advance when a track finishes naturally."""
        if self.state == self.PLAYING and not pygame.mixer.music.get_busy():
            self.next_track()
            
