from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Theme:
    name: str
    background: str
    card: str
    surface: str
    surface_alt: str
    text_primary: str
    text_secondary: str
    accent: str
    accent_hover: str
    accent_soft: str
    ring_track: str
    border: str
    shadow: str
    disabled: str


LIGHT_THEME = Theme(
    name="light",
    background="#F3F7FC",
    card="#FFFFFF",
    surface="#FFFFFF",
    surface_alt="#F7FAFF",
    text_primary="#071B3A",
    text_secondary="#71819E",
    accent="#2F80ED",
    accent_hover="#1F6FE5",
    accent_soft="#EAF3FF",
    ring_track="#DFE8F5",
    border="#D9E3F2",
    shadow="#9EADBF",
    disabled="#A8B4C6",
)

DARK_THEME = Theme(
    name="dark",
    background="#1A2432",
    card="#1E2A3A",
    surface="#253245",
    surface_alt="#2C3A4F",
    text_primary="#F8FAFC",
    text_secondary="#C7D2E2",
    accent="#3794FF",
    accent_hover="#5AA8FF",
    accent_soft="#17375E",
    ring_track="#3B4658",
    border="#3E4A5F",
    shadow="#101722",
    disabled="#6B7688",
)

THEMES = {
    LIGHT_THEME.name: LIGHT_THEME,
    DARK_THEME.name: DARK_THEME,
}


def theme_by_name(name: str) -> Theme:
    return THEMES.get(name, LIGHT_THEME)


def build_stylesheet(theme: Theme) -> str:
    return f"""
* {{
    font-family: "Microsoft YaHei UI", "Segoe UI", Arial, sans-serif;
}}

QMainWindow, QWidget#root {{
    background: {theme.background};
}}

QFrame#contentCard {{
    background: {theme.card};
    border: 1px solid {theme.border};
    border-radius: 26px;
}}

QFrame#avatarFrame {{
    background: {theme.surface};
    border: 3px solid {theme.card};
    border-radius: 68px;
}}

QLabel#titleLabel {{
    color: {theme.text_primary};
    font-size: 32px;
    font-weight: 800;
}}

QLabel#subtitleLabel, QLabel#footerLabel, QLabel#sectionLabel, QLabel#volumeLabel, QLabel#volumeValue {{
    color: {theme.text_secondary};
}}

QLabel#subtitleLabel {{
    font-size: 17px;
    font-weight: 600;
}}

QLabel#sectionLabel {{
    font-size: 15px;
    font-weight: 600;
}}

QLabel#footerLabel {{
    font-size: 14px;
}}

QLabel#volumeLabel, QLabel#volumeValue {{
    font-size: 15px;
    font-weight: 650;
}}

QPushButton {{
    background: {theme.surface};
    border: 1px solid {theme.border};
    border-radius: 14px;
    color: {theme.text_secondary};
    font-size: 18px;
    font-weight: 650;
    padding: 8px 16px;
}}

QPushButton:hover {{
    background: {theme.surface_alt};
    color: {theme.text_primary};
}}

QPushButton:pressed {{
    background: {theme.accent_soft};
}}

QPushButton:checked {{
    background: {theme.accent_soft};
    border: 2px solid {theme.accent};
    color: {theme.accent};
}}

QPushButton:disabled {{
    color: {theme.disabled};
    background: {theme.surface_alt};
}}

QPushButton#primaryButton, QPushButton#focusPrimaryButton {{
    background: {theme.accent};
    border: 0;
    color: white;
    font-size: 22px;
    font-weight: 750;
    padding: 10px 24px;
}}

QPushButton#primaryButton:hover, QPushButton#focusPrimaryButton:hover {{
    background: {theme.accent_hover};
}}

QPushButton#secondaryButton, QPushButton#focusButton {{
    min-height: 42px;
}}

QToolButton#themeButton {{
    background: {theme.surface_alt};
    border: 1px solid {theme.border};
    border-radius: 22px;
    color: {theme.text_secondary};
    font-size: 21px;
    font-weight: 700;
}}

QToolButton#themeButton:hover {{
    background: {theme.accent_soft};
    color: {theme.accent};
}}

QWidget#timeInput {{
    background: {theme.surface_alt};
    border: 1px solid {theme.border};
    border-radius: 16px;
}}

QWidget#timeInput[hovered="true"] {{
    border: 2px solid {theme.accent};
}}

QLabel#timeInputLabel {{
    color: {theme.text_secondary};
    font-size: 15px;
    font-weight: 650;
}}

QLabel#timeInputValue {{
    color: {theme.text_primary};
    font-size: 22px;
    font-weight: 750;
}}

QLineEdit#timeInputEditor {{
    background: transparent;
    border: 0;
    color: {theme.text_primary};
    selection-background-color: {theme.accent};
    selection-color: white;
    font-size: 22px;
    font-weight: 750;
    padding: 0;
}}

QToolButton#stepButton {{
    background: transparent;
    border: 0;
    color: {theme.text_secondary};
    font-size: 18px;
    font-weight: 800;
}}

QToolButton#stepButton:hover {{
    color: {theme.accent};
}}

QFrame#volumeFrame {{
    background: {theme.surface_alt};
    border: 1px solid {theme.border};
    border-radius: 16px;
}}

QSlider#volumeSlider::groove:horizontal {{
    background: {theme.ring_track};
    border: 0;
    border-radius: 4px;
    height: 8px;
}}

QSlider#volumeSlider::sub-page:horizontal {{
    background: {theme.accent};
    border: 0;
    border-radius: 4px;
    height: 8px;
}}

QSlider#volumeSlider::handle:horizontal {{
    background: {theme.card};
    border: 2px solid {theme.accent};
    border-radius: 9px;
    height: 18px;
    width: 18px;
    margin: -6px 0;
}}

QSlider#volumeSlider::handle:horizontal:hover {{
    background: {theme.accent_soft};
}}

QFrame#focusControls {{
    background: {theme.surface_alt};
    border: 1px solid {theme.border};
    border-radius: 18px;
}}

QLabel#hintLabel {{
    color: {theme.accent};
    font-size: 14px;
    font-weight: 650;
}}
"""
