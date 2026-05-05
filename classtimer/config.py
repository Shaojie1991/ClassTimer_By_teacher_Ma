from __future__ import annotations

import json
import os
import sys
from pathlib import Path

from PySide6.QtCore import QStandardPaths

APP_NAME = "ClassTimer"
CONFIG_FILE = "settings.json"
DEFAULT_THEME = "light"
DEFAULT_VOLUME_PERCENT = 80


def resource_path(relative_path: str) -> str:
    base_path = getattr(sys, "_MEIPASS", None)
    if base_path:
        return os.path.join(str(base_path), relative_path)
    base_dir = Path(__file__).resolve().parents[1]
    return str(base_dir / relative_path)


def _config_dir() -> Path:
    location = QStandardPaths.writableLocation(
        QStandardPaths.StandardLocation.AppConfigLocation
    )
    if location:
        return Path(location)
    return Path.home() / "AppData" / "Local" / APP_NAME


def _config_path() -> Path:
    return _config_dir() / CONFIG_FILE


def _load_config() -> dict:
    path = _config_path()
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    return data if isinstance(data, dict) else {}


def _save_config(data: dict) -> None:
    path = _config_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def load_theme_name() -> str:
    data = _load_config()
    theme = data.get("theme")
    return theme if theme in {"light", "dark"} else DEFAULT_THEME


def save_theme_name(theme_name: str) -> None:
    if theme_name not in {"light", "dark"}:
        theme_name = DEFAULT_THEME
    data = _load_config()
    data["theme"] = theme_name
    _save_config(data)


def load_volume_percent() -> int:
    data = _load_config()
    try:
        value = int(data.get("volume_percent", DEFAULT_VOLUME_PERCENT))
    except (TypeError, ValueError):
        return DEFAULT_VOLUME_PERCENT
    return max(0, min(100, value))


def save_volume_percent(volume_percent: int) -> None:
    data = _load_config()
    data["volume_percent"] = max(0, min(100, int(volume_percent)))
    _save_config(data)
