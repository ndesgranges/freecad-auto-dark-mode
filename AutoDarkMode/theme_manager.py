"""
Theme manager for Auto Dark Mode addon.
Handles applying themes and monitoring system theme changes.
"""

import FreeCAD
import FreeCADGui
import preferences
import theme_detector
from PySide import QtCore


class ThemeManager:
    """Manages automatic theme switching based on system appearance."""

    _instance = None
    _timer = None
    _last_dark_mode = None

    @classmethod
    def instance(cls):
        """Get singleton instance."""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def __init__(self):
        self._last_dark_mode = None

    def apply_theme(self, theme_name: str):
        """
        Apply a FreeCAD stylesheet theme.

        Args:
            theme_name: Name of the stylesheet to apply.
        """
        mw = FreeCADGui.getMainWindow()
        if not mw:
            FreeCAD.Console.PrintWarning("Auto Dark Mode: No main window found\n")
            return

        if theme_name == "No stylesheet":
            mw.setStyleSheet("")
            FreeCAD.Console.PrintMessage("Auto Dark Mode: Cleared stylesheet\n")
            return

        # Get the stylesheet path
        stylesheet_path = preferences.get_stylesheet_path(theme_name)

        if stylesheet_path:
            self._apply_stylesheet_path(stylesheet_path)
        else:
            FreeCAD.Console.PrintWarning(
                f"Auto Dark Mode: Stylesheet '{theme_name}' not found\n"
            )

    def _apply_stylesheet_path(self, path: str):
        """Apply stylesheet from file path."""
        try:
            with open(path, "r", encoding="utf-8") as f:
                stylesheet = f.read()

            mw = FreeCADGui.getMainWindow()
            if mw:
                mw.setStyleSheet(stylesheet)
                FreeCAD.Console.PrintMessage(
                    f"Auto Dark Mode: Applied stylesheet from {path}\n"
                )
        except Exception as e:
            FreeCAD.Console.PrintError(
                f"Auto Dark Mode: Failed to apply stylesheet: {e}\n"
            )

    def update_theme(self):
        """Check system theme and update FreeCAD theme if needed."""
        if not preferences.is_enabled():
            return

        is_dark = theme_detector.is_dark_mode()

        # Only change if theme actually changed
        if is_dark != self._last_dark_mode:
            self._last_dark_mode = is_dark

            if is_dark:
                theme = preferences.get_dark_theme()
                FreeCAD.Console.PrintMessage(
                    f"Auto Dark Mode: System dark mode detected, applying '{theme}'\n"
                )
            else:
                theme = preferences.get_light_theme()
                FreeCAD.Console.PrintMessage(
                    f"Auto Dark Mode: System light mode detected, applying '{theme}'\n"
                )

            self.apply_theme(theme)

    def start_monitoring(self):
        """Start monitoring system theme changes."""
        if self._timer is not None:
            self.stop_monitoring()

        self._timer = QtCore.QTimer()
        self._timer.timeout.connect(self.update_theme)
        self._timer.start(preferences.get_poll_interval())

        # Apply current theme immediately
        self.update_theme()

        FreeCAD.Console.PrintMessage("Auto Dark Mode: Started monitoring system theme\n")

    def stop_monitoring(self):
        """Stop monitoring system theme changes."""
        if self._timer is not None:
            self._timer.stop()
            self._timer = None
            FreeCAD.Console.PrintMessage("Auto Dark Mode: Stopped monitoring system theme\n")

    def restart_monitoring(self):
        """Restart monitoring with updated interval."""
        if self._timer is not None:
            self.stop_monitoring()
            self.start_monitoring()
