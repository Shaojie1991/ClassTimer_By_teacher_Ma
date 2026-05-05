from __future__ import annotations

import os
import threading
from pathlib import Path

from PySide6.QtCore import QObject, QUrl

from .config import resource_path


def _play_winsound_fallback(volume_percent: int) -> None:
    if volume_percent <= 0:
        return

    def play() -> None:
        try:
            import winsound

            winsound.MessageBeep(winsound.MB_ICONASTERISK)
        except Exception:
            return

    threading.Thread(target=play, daemon=True).start()


class SoundManager(QObject):
    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self._volume_percent = 80
        self._cat_path = Path(resource_path("assets/cat.mp3"))
        self._player = None
        self._audio_output = None

        try:
            from PySide6.QtMultimedia import QAudioOutput, QMediaPlayer

            self._audio_output = QAudioOutput(self)
            self._player = QMediaPlayer(self)
            self._player.setAudioOutput(self._audio_output)
            if self._cat_path.exists():
                self._player.setSource(QUrl.fromLocalFile(str(self._cat_path)))
        except Exception as exc:
            print(f"Warning: QtMultimedia unavailable, using fallback beep: {exc}")
            self._player = None
            self._audio_output = None

    def set_volume_percent(self, volume_percent: int) -> None:
        self._volume_percent = max(0, min(100, int(volume_percent)))
        if self._audio_output is not None:
            self._audio_output.setVolume(self._volume_percent / 100.0)

    def play_finish_sound(self) -> None:
        if self._volume_percent <= 0:
            self.stop()
            return
        if not self._cat_path.exists():
            print(f"Warning: finish sound file not found: {self._cat_path}")
            _play_winsound_fallback(self._volume_percent)
            return
        if self._player is None or self._audio_output is None:
            _play_winsound_fallback(self._volume_percent)
            return

        self._audio_output.setVolume(self._volume_percent / 100.0)
        self._player.stop()
        self._player.setSource(QUrl.fromLocalFile(str(self._cat_path)))
        self._player.setPosition(0)
        self._player.play()

    def stop(self) -> None:
        if self._player is not None:
            self._player.stop()
