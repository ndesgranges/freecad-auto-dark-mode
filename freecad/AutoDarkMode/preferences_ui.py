# SPDX-License-Identifier: MIT
# SPDX-FileNotice: Part of the Auto Dark Mode addon.
"""
Preferences UI panel for Auto Dark Mode addon.
"""

import FreeCAD
from . import preferences
from . import theme_detector
from . import theme_manager
from PySide import QtWidgets


class AutoDarkModePreferencesPage:
    """Preferences page for Auto Dark Mode settings."""

    def __init__(self, parent=None):
        self.form = QtWidgets.QWidget(parent)
        self.form.setObjectName("AutoDarkModePreferences")
        self._setup_ui()
        self._load_settings()

    def _setup_ui(self):
        """Set up the preferences UI."""
        layout = QtWidgets.QVBoxLayout(self.form)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(12)

        # Title
        title = QtWidgets.QLabel("<h2>Auto Dark Mode</h2>")
        layout.addWidget(title)

        description = QtWidgets.QLabel(
            "Automatically switch FreeCAD theme based on your system's "
            "light/dark appearance setting."
        )
        description.setWordWrap(True)
        layout.addWidget(description)

        layout.addSpacing(10)

        # Enable checkbox
        self.enable_checkbox = QtWidgets.QCheckBox("Enable automatic theme switching")
        layout.addWidget(self.enable_checkbox)

        layout.addSpacing(10)

        # Theme selection group
        theme_group = QtWidgets.QGroupBox("Theme Configuration")
        theme_layout = QtWidgets.QFormLayout(theme_group)
        theme_layout.setSpacing(8)

        # Light theme selector
        self.light_theme_combo = QtWidgets.QComboBox()
        self.light_theme_combo.setMinimumWidth(200)
        theme_layout.addRow("Light mode theme:", self.light_theme_combo)

        # Dark theme selector
        self.dark_theme_combo = QtWidgets.QComboBox()
        self.dark_theme_combo.setMinimumWidth(200)
        theme_layout.addRow("Dark mode theme:", self.dark_theme_combo)

        layout.addWidget(theme_group)

        # Poll interval group
        interval_group = QtWidgets.QGroupBox("Advanced Settings")
        interval_layout = QtWidgets.QFormLayout(interval_group)

        self.interval_spinbox = QtWidgets.QSpinBox()
        self.interval_spinbox.setRange(1, 60)
        self.interval_spinbox.setSuffix(" seconds")
        self.interval_spinbox.setToolTip(
            "How often to check for system theme changes"
        )
        interval_layout.addRow("Check interval:", self.interval_spinbox)

        layout.addWidget(interval_group)

        # Current status
        self.status_label = QtWidgets.QLabel()
        self.status_label.setStyleSheet("color: gray; font-style: italic;")
        layout.addWidget(self.status_label)

        # Apply now button
        apply_btn = QtWidgets.QPushButton("Apply Theme Now")
        apply_btn.clicked.connect(self._apply_now)
        layout.addWidget(apply_btn)

        layout.addStretch()

        # Populate theme combos
        self._populate_themes()

        # Update status
        self._update_status()

    def _populate_themes(self):
        """Populate theme combo boxes with available stylesheets."""
        themes = preferences.get_available_stylesheets()

        self.light_theme_combo.clear()
        self.dark_theme_combo.clear()

        for theme in themes:
            self.light_theme_combo.addItem(theme)
            self.dark_theme_combo.addItem(theme)

    def _load_settings(self):
        """Load current settings into UI."""
        self.enable_checkbox.setChecked(preferences.is_enabled())

        light_theme = preferences.get_light_theme()
        dark_theme = preferences.get_dark_theme()

        light_idx = self.light_theme_combo.findText(light_theme)
        if light_idx >= 0:
            self.light_theme_combo.setCurrentIndex(light_idx)

        dark_idx = self.dark_theme_combo.findText(dark_theme)
        if dark_idx >= 0:
            self.dark_theme_combo.setCurrentIndex(dark_idx)

        interval_ms = preferences.get_poll_interval()
        self.interval_spinbox.setValue(interval_ms // 1000)

    def _update_status(self):
        """Update the current status label."""
        is_dark = theme_detector.is_dark_mode()
        mode = "dark" if is_dark else "light"
        self.status_label.setText(f"Current system theme: {mode} mode")

    def _apply_now(self):
        """Apply theme immediately based on current system setting."""
        manager = theme_manager.ThemeManager.instance()
        manager._last_dark_mode = None  # Force reapply
        manager.update_theme()
        self._update_status()

    def saveSettings(self):
        """Save settings from UI to preferences."""
        preferences.set_enabled(self.enable_checkbox.isChecked())
        preferences.set_light_theme(self.light_theme_combo.currentText())
        preferences.set_dark_theme(self.dark_theme_combo.currentText())
        preferences.set_poll_interval(self.interval_spinbox.value() * 1000)

        # Restart monitoring with new settings
        manager = theme_manager.ThemeManager.instance()
        if preferences.is_enabled():
            manager.restart_monitoring()
        else:
            manager.stop_monitoring()

        FreeCAD.Console.PrintMessage("Auto Dark Mode: Settings saved\n")
