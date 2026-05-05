from __future__ import annotations

from PySide6.QtCore import QEvent, Qt, QTimer, Signal
from PySide6.QtGui import QIntValidator
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QSizePolicy,
    QToolButton,
    QVBoxLayout,
    QWidget,
)


class WheelTimeInput(QWidget):
    stepped = Signal(int)
    valueChanged = Signal(int)
    valueCommitted = Signal(int)

    def __init__(
        self,
        label: str,
        minimum: int,
        maximum: int,
        parent: QWidget | None = None,
        edit_maximum: int | None = None,
    ) -> None:
        super().__init__(parent)
        self._minimum = minimum
        self._maximum = maximum
        self._edit_maximum = edit_maximum if edit_maximum is not None else maximum
        self._value = minimum
        self._committing = False

        self.setObjectName("timeInput")
        self.setProperty("hovered", False)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setMinimumSize(216, 74)
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        self.label = QLabel(label)
        self.label.setObjectName("timeInputLabel")

        self.editor = QLineEdit()
        self.editor.setObjectName("timeInputEditor")
        self.editor.setFrame(False)
        self.editor.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        self.editor.setValidator(QIntValidator(self._minimum, self._edit_maximum, self))
        self.editor.setMaxLength(4)
        self.editor.setText("00")
        self.editor.installEventFilter(self)

        self.up_button = QToolButton()
        self.up_button.setObjectName("stepButton")
        self.up_button.setText("^")
        self.up_button.setAutoRepeat(True)
        self.up_button.setAutoRepeatDelay(250)
        self.up_button.setAutoRepeatInterval(70)

        self.down_button = QToolButton()
        self.down_button.setObjectName("stepButton")
        self.down_button.setText("v")
        self.down_button.setAutoRepeat(True)
        self.down_button.setAutoRepeatDelay(250)
        self.down_button.setAutoRepeatInterval(70)

        text_layout = QVBoxLayout()
        text_layout.setContentsMargins(0, 0, 0, 0)
        text_layout.setSpacing(2)
        text_layout.addWidget(self.label)
        text_layout.addWidget(self.editor)

        step_layout = QVBoxLayout()
        step_layout.setContentsMargins(0, 0, 0, 0)
        step_layout.setSpacing(0)
        step_layout.addWidget(self.up_button)
        step_layout.addWidget(self.down_button)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(24, 9, 18, 9)
        layout.setSpacing(14)
        layout.addLayout(text_layout, 1)
        layout.addLayout(step_layout)

        for child in (self.label, self.up_button, self.down_button):
            child.installEventFilter(self)

        self.up_button.clicked.connect(lambda: self._emit_step(1))
        self.down_button.clicked.connect(lambda: self._emit_step(-1))
        self.editor.returnPressed.connect(self.commit_text)
        self.editor.editingFinished.connect(self.commit_text)
        self._refresh_editor()

    def value(self) -> int:
        if self.editor.hasFocus():
            return self._value_from_text()
        return self._value

    def raw_value(self) -> int:
        return self._value_from_text()

    def set_value(self, value: int) -> None:
        value = max(self._minimum, min(self._maximum, int(value)))
        if value == self._value:
            self._refresh_editor()
            return
        self._value = value
        self._refresh_editor()
        self.valueChanged.emit(self._value)

    def set_range(self, minimum: int, maximum: int, edit_maximum: int | None = None) -> None:
        self._minimum = minimum
        self._maximum = maximum
        self._edit_maximum = edit_maximum if edit_maximum is not None else maximum
        self.editor.setValidator(QIntValidator(self._minimum, self._edit_maximum, self))
        self.set_value(self._value)

    def commit_text(self) -> None:
        if self._committing:
            return
        self._committing = True
        try:
            raw_value = self._value_from_text()
            self.valueCommitted.emit(raw_value)
        finally:
            self._committing = False

    def _value_from_text(self) -> int:
        text = self.editor.text().strip()
        if not text:
            return self._minimum
        try:
            return max(self._minimum, int(text))
        except ValueError:
            return self._minimum

    def _refresh_editor(self) -> None:
        text = f"{self._value:02d}"
        if self.editor.text() != text:
            self.editor.setText(text)

    def _emit_step(self, step: int) -> None:
        self.editor.clearFocus()
        self.stepped.emit(step)

    def wheelEvent(self, event) -> None:  # noqa: N802
        delta = event.angleDelta().y()
        if delta == 0:
            return
        self.editor.clearFocus()
        steps = int(delta / 120)
        if steps == 0:
            steps = 1 if delta > 0 else -1
        self._emit_step(steps)
        event.accept()

    def enterEvent(self, event) -> None:  # noqa: N802
        del event
        self.setProperty("hovered", True)
        self.style().unpolish(self)
        self.style().polish(self)

    def leaveEvent(self, event) -> None:  # noqa: N802
        del event
        self.setProperty("hovered", False)
        self.style().unpolish(self)
        self.style().polish(self)

    def eventFilter(self, watched, event) -> bool:  # noqa: N802
        if event.type() == QEvent.Type.Wheel:
            self.wheelEvent(event)
            return True
        if event.type() == QEvent.Type.Enter:
            self.enterEvent(event)
        elif event.type() == QEvent.Type.Leave and not self.rect().contains(
            self.mapFromGlobal(self.cursor().pos())
        ):
            self.leaveEvent(event)
        elif watched is self.editor and event.type() == QEvent.Type.FocusIn:
            QTimer.singleShot(0, self.editor.selectAll)
        return super().eventFilter(watched, event)
