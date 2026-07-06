# SPDX-License-Identifier: MIT
# SPDX-FileNotice: Part of the Auto Dark Mode addon.
"""
FreeCAD GUI initialization for Auto Dark Mode addon.

This module is executed when FreeCAD starts in GUI mode.
It sets up the automatic theme switching based on system appearance.
"""

from FreeCAD import Console
from FreeCAD import Gui
from PySide import QtCore


Console.PrintLog("freecad/AutoDarkMode/init_gui.py\n")


def _init_auto_dark_mode():
    """Initialize Auto Dark Mode addon."""
    
    Console.PrintMessage("Auto Dark Mode: Initializing...\n")

    class Handler:
        """Handles Auto Dark Mode initialization and callbacks."""

        def add_menu_item(self):
            """Add Auto Dark Mode settings to Edit menu."""
            try:
                mw = Gui.getMainWindow()
                if not mw:
                    Console.PrintWarning("Auto Dark Mode: No main window found\n")
                    return

                edit_menu = None
                menu_bar = mw.menuBar()
                for action in menu_bar.actions():
                    text = action.text().replace("&", "")
                    if text.lower() in ("edit", "édition", "bearbeiten"):
                        edit_menu = action.menu()
                        break

                if edit_menu:
                    edit_menu.addSeparator()
                    action = edit_menu.addAction("Auto Dark Mode Settings...")
                    action.triggered.connect(self.show_settings_dialog)
                    Console.PrintMessage("Auto Dark Mode: Menu item added to Edit menu\n")
                else:
                    for action in menu_bar.actions():
                        text = action.text().replace("&", "")
                        if text.lower() in ("view", "affichage", "ansicht"):
                            view_menu = action.menu()
                            view_menu.addSeparator()
                            action = view_menu.addAction("Auto Dark Mode Settings...")
                            action.triggered.connect(self.show_settings_dialog)
                            Console.PrintMessage("Auto Dark Mode: Menu item added to View menu\n")
                            return
                    Console.PrintWarning("Auto Dark Mode: Could not find Edit or View menu\n")
            except Exception as e:
                Console.PrintError(f"Auto Dark Mode: Failed to add menu item: {e}\n")

        def show_settings_dialog(self):
            """Show the settings dialog."""
            from . import preferences_ui
            from PySide import QtWidgets

            mw = Gui.getMainWindow()
            dialog = QtWidgets.QDialog(mw)
            dialog.setWindowTitle("Auto Dark Mode Settings")
            dialog.setMinimumWidth(400)

            layout = QtWidgets.QVBoxLayout(dialog)
            prefs_page = preferences_ui.AutoDarkModePreferencesPage()
            layout.addWidget(prefs_page.form)

            buttons = QtWidgets.QDialogButtonBox(
                QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel
            )
            buttons.accepted.connect(dialog.accept)
            buttons.rejected.connect(dialog.reject)
            layout.addWidget(buttons)

            if dialog.exec() == QtWidgets.QDialog.Accepted:
                prefs_page.saveSettings()

        def start_theme_monitoring(self):
            """Start the automatic theme monitoring."""
            try:
                from . import theme_manager
                from . import preferences

                if preferences.is_enabled():
                    manager = theme_manager.ThemeManager.instance()
                    manager.start_monitoring()
            except Exception as e:
                Console.PrintError(f"Auto Dark Mode: Failed to start monitoring: {e}\n")

        def delayed_init(self):
            """Delayed initialization to ensure FreeCAD is fully loaded."""
            Console.PrintMessage("Auto Dark Mode: Running delayed init...\n")
            self.add_menu_item()
            self.start_theme_monitoring()
            Console.PrintMessage("Auto Dark Mode: Initialized successfully\n")

    # Create handler and store to survive scope
    import sys
    handler = Handler()
    sys.modules['_auto_dark_mode_handler'] = handler

    # Schedule delayed init
    QtCore.QTimer.singleShot(2000, handler.delayed_init)
    Console.PrintMessage("Auto Dark Mode: Waiting for FreeCAD to fully load...\n")


# Run initialization
_init_auto_dark_mode()
