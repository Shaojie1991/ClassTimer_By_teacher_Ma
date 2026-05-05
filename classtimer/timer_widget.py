from __future__ import annotations

import math

from PySide6.QtCore import QRectF, QSize, Qt, QTimer
from PySide6.QtGui import QColor, QFont, QPainter, QPen
from PySide6.QtWidgets import QSizePolicy, QWidget

from .theme import LIGHT_THEME, Theme


class TimerWidget(QWidget):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._remaining_seconds = 25 * 60.0
        self._total_seconds = 25 * 60
        self._theme: Theme = LIGHT_THEME
        self._flash_enabled = False
        self._flash_on = False

        self._flash_timer = QTimer(self)
        self._flash_timer.setInterval(180)
        self._flash_timer.timeout.connect(self._toggle_flash)

        self.setMinimumSize(220, 220)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

    def sizeHint(self) -> QSize:
        return QSize(270, 270)

    def set_time(self, remaining_seconds: float, total_seconds: int) -> None:
        self._total_seconds = max(0, int(total_seconds))
        if self._total_seconds <= 0:
            self._remaining_seconds = 0.0
        else:
            self._remaining_seconds = max(
                0.0, min(float(remaining_seconds), float(self._total_seconds))
            )
        self.update()

    def set_theme(self, theme: Theme) -> None:
        self._theme = theme
        self.update()

    def set_flash_enabled(self, enabled: bool) -> None:
        self._flash_enabled = enabled
        if enabled:
            self._flash_timer.start()
        else:
            self._flash_timer.stop()
            self._flash_on = False
        self.update()

    def _toggle_flash(self) -> None:
        self._flash_on = not self._flash_on
        self.update()

    def _formatted_time(self) -> str:
        seconds = int(math.ceil(self._remaining_seconds)) if self._remaining_seconds > 0 else 0
        minutes, seconds = divmod(seconds, 60)
        return f"{minutes:02d}:{seconds:02d}"

    def _progress(self) -> float:
        if self._total_seconds <= 0:
            return 0.0
        return max(0.0, min(1.0, self._remaining_seconds / self._total_seconds))

    def paintEvent(self, event) -> None:  # noqa: N802
        del event

        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)

        width = self.width()
        height = self.height()
        side = min(width, height)
        margin = max(18.0, side * 0.08)
        pen_width = max(10.0, side * 0.035)
        diameter = side - margin * 2
        left = (width - diameter) / 2
        top = (height - diameter) / 2
        rect = QRectF(left, top, diameter, diameter)

        track_pen = QPen(QColor(self._theme.ring_track), pen_width)
        track_pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        painter.setPen(track_pen)
        painter.drawArc(rect, 0, 360 * 16)

        progress = self._progress()
        if progress > 0:
            accent = QColor(self._theme.accent_hover if self._flash_on else self._theme.accent)
            progress_pen = QPen(accent, pen_width)
            progress_pen.setCapStyle(Qt.PenCapStyle.RoundCap)
            painter.setPen(progress_pen)
            painter.drawArc(rect, 90 * 16, int(-360 * 16 * progress))

        text = self._formatted_time()
        text_color = QColor(self._theme.accent if self._flash_on else self._theme.text_primary)
        painter.setPen(text_color)

        font_size = max(42, int(side * (0.19 if len(text) <= 5 else 0.15)))
        font = QFont("Segoe UI", font_size, QFont.Weight.Black)
        painter.setFont(font)
        painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, text)
