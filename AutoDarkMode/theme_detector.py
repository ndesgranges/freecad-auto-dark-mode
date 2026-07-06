"""
System theme detection module for Auto Dark Mode addon.
Handles cross-platform detection of system light/dark theme.
"""

import platform
import subprocess


def is_dark_mode() -> bool:
    """
    Detect if the system is currently in dark mode.

    Returns:
        bool: True if dark mode is active, False otherwise.
    """
    system = platform.system()

    if system == "Darwin":
        return _is_dark_mode_macos()
    elif system == "Windows":
        return _is_dark_mode_windows()
    else:
        return _is_dark_mode_linux()


def _is_dark_mode_macos() -> bool:
    """Detect dark mode on macOS."""
    try:
        result = subprocess.run(
            ["defaults", "read", "-g", "AppleInterfaceStyle"],
            capture_output=True,
            text=True,
            timeout=5
        )
        return result.stdout.strip().lower() == "dark"
    except (subprocess.TimeoutExpired, subprocess.SubprocessError, FileNotFoundError):
        return False


def _is_dark_mode_windows() -> bool:
    """Detect dark mode on Windows."""
    try:
        import winreg
        registry = winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER)
        key = winreg.OpenKey(
            registry,
            r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize"
        )
        value, _ = winreg.QueryValueEx(key, "AppsUseLightTheme")
        winreg.CloseKey(key)
        return value == 0
    except (ImportError, FileNotFoundError, OSError):
        return False


def _is_dark_mode_linux() -> bool:
    """Detect dark mode on Linux (supports GNOME, KDE, and others)."""
    # Try GNOME/GTK
    try:
        result = subprocess.run(
            ["gsettings", "get", "org.gnome.desktop.interface", "color-scheme"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if "dark" in result.stdout.lower():
            return True
    except (subprocess.TimeoutExpired, subprocess.SubprocessError, FileNotFoundError):
        pass

    # Try GTK theme name
    try:
        result = subprocess.run(
            ["gsettings", "get", "org.gnome.desktop.interface", "gtk-theme"],
            capture_output=True,
            text=True,
            timeout=5
        )
        theme = result.stdout.strip().lower()
        if "dark" in theme:
            return True
    except (subprocess.TimeoutExpired, subprocess.SubprocessError, FileNotFoundError):
        pass

    # Try KDE Plasma
    try:
        result = subprocess.run(
            ["kreadconfig5", "--group", "General", "--key", "ColorScheme"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if "dark" in result.stdout.lower():
            return True
    except (subprocess.TimeoutExpired, subprocess.SubprocessError, FileNotFoundError):
        pass

    return False
