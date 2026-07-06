"""
FreeCAD GUI initialization for Auto Dark Mode addon.
This file is executed when FreeCAD GUI starts.
"""

def _init_auto_dark_mode():
    """Initialize Auto Dark Mode - wrapped in function to survive FreeCAD's exec() scope."""
    import os
    import sys
    import FreeCAD
    import FreeCADGui

    FreeCAD.Console.PrintMessage("Auto Dark Mode: InitGui.py loading...\n")

    # Add this addon's folder to Python path for imports
    try:
        addon_dir = os.path.dirname(__file__)
    except NameError:
        addon_dir = None
        for folder_name in ["AutoDarkMode", "auto-dark-mode"]:
            for mod_path in [
                os.path.join(FreeCAD.getUserAppDataDir(), "Mod", folder_name),
                os.path.join(FreeCAD.getResourceDir(), "Mod", folder_name),
            ]:
                if os.path.isdir(mod_path):
                    addon_dir = mod_path
                    break
            if addon_dir:
                break

    if addon_dir and addon_dir not in sys.path:
        sys.path.insert(0, addon_dir)

    # Import PySide (FreeCAD provides this as an alias)
    from PySide import QtCore

    class Handler:
        """Handles Auto Dark Mode initialization and callbacks."""

        def add_menu_item(self):
            """Add Auto Dark Mode settings to Edit menu."""
            try:
                mw = FreeCADGui.getMainWindow()
                if not mw:
                    FreeCAD.Console.PrintWarning("Auto Dark Mode: No main window found\n")
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
                    FreeCAD.Console.PrintMessage("Auto Dark Mode: Menu item added to Edit menu\n")
                else:
                    for action in menu_bar.actions():
                        text = action.text().replace("&", "")
                        if text.lower() in ("view", "affichage", "ansicht"):
                            view_menu = action.menu()
                            view_menu.addSeparator()
                            action = view_menu.addAction("Auto Dark Mode Settings...")
                            action.triggered.connect(self.show_settings_dialog)
                            FreeCAD.Console.PrintMessage("Auto Dark Mode: Menu item added to View menu\n")
                            return
                    FreeCAD.Console.PrintWarning("Auto Dark Mode: Could not find Edit or View menu\n")
            except Exception as e:
                FreeCAD.Console.PrintError(f"Auto Dark Mode: Failed to add menu item: {e}\n")

        def show_settings_dialog(self):
            """Show the settings dialog."""
            import preferences_ui
            from PySide import QtWidgets

            mw = FreeCADGui.getMainWindow()
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
                import theme_manager
                import preferences

                if preferences.is_enabled():
                    manager = theme_manager.ThemeManager.instance()
                    manager.start_monitoring()
            except Exception as e:
                FreeCAD.Console.PrintError(f"Auto Dark Mode: Failed to start monitoring: {e}\n")

        def delayed_init(self):
            """Delayed initialization to ensure FreeCAD is fully loaded."""
            FreeCAD.Console.PrintMessage("Auto Dark Mode: Running delayed init...\n")
            self.add_menu_item()
            self.start_theme_monitoring()
            FreeCAD.Console.PrintMessage("Auto Dark Mode: Initialized successfully\n")

    # Create handler and store in sys.modules to survive exec() scope
    handler = Handler()
    sys.modules['_auto_dark_mode_handler'] = handler

    # Schedule delayed init
    QtCore.QTimer.singleShot(2000, handler.delayed_init)
    FreeCAD.Console.PrintMessage("Auto Dark Mode: Waiting for FreeCAD to fully load...\n")

# Run initialization
_init_auto_dark_mode()
