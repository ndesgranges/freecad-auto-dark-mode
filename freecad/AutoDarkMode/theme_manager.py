# SPDX-License-Identifier: MIT
# SPDX-FileNotice: Part of the Auto Dark Mode addon.
"""
Theme manager for Auto Dark Mode addon.
Handles applying themes and monitoring system theme changes.
"""

import os
import xml.etree.ElementTree as ET
import FreeCAD
import FreeCADGui
from . import preferences
from . import theme_detector
from PySide import QtCore


class ThemeManager:
    """Manages automatic theme switching based on system appearance."""

    _instance = None

    @classmethod
    def instance(cls):
        """Get singleton instance."""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def __init__(self):
        self._timer = None
        self._last_dark_mode = None

    def apply_theme(self, theme_name: str):
        """
        Apply a FreeCAD theme.

        Args:
            theme_name: Name of the theme to apply.
        """
        if theme_name == "No stylesheet":
            self._clear_theme()
            return

        stylesheet_path = preferences.get_stylesheet_path(theme_name)
        if not stylesheet_path:
            FreeCAD.Console.PrintWarning(
                f"Auto Dark Mode: Stylesheet '{theme_name}' not found\n"
            )
            return

        self._apply_freecad_theme(theme_name, stylesheet_path)

    def _clear_theme(self):
        """Clear any applied stylesheet."""
        params = FreeCAD.ParamGet("User parameter:BaseApp/Preferences/MainWindow")
        params.SetString("Theme", "")
        params.SetString("StyleSheet", "")
        params.NotifyAll()
        FreeCADGui.runCommand('Std_ReloadStyleSheet', 0)
        FreeCAD.Console.PrintMessage("Auto Dark Mode: Cleared stylesheet\n")

    def _find_theme_cfg(self, theme_name: str, stylesheet_path: str):
        """
        Find the theme's .cfg file.

        Args:
            theme_name: The theme name.
            stylesheet_path: Path to the stylesheet file.

        Returns:
            Path to .cfg file or None if not found.
        """
        # Check in same directory as stylesheet
        theme_dir = os.path.dirname(stylesheet_path)
        cfg_path = os.path.join(theme_dir, f"{theme_name}.cfg")
        if os.path.exists(cfg_path):
            return cfg_path

        # Check in user Mod folder
        user_mod = os.path.join(FreeCAD.getUserAppDataDir(), "Mod")
        if os.path.exists(user_mod):
            for addon in os.listdir(user_mod):
                cfg_path = os.path.join(user_mod, addon, theme_name, f"{theme_name}.cfg")
                if os.path.exists(cfg_path):
                    return cfg_path

        return None

    def _apply_params_recursive(self, xml_group, param_path: str):
        """
        Recursively apply all parameters from XML group to FreeCAD.

        Args:
            xml_group: XML element containing FCParamGroup.
            param_path: FreeCAD parameter path.
        """
        fc_params = FreeCAD.ParamGet(param_path)

        # Apply all parameter types
        for param in xml_group.findall("FCUInt"):
            fc_params.SetUnsigned(param.get("Name"), int(param.get("Value")))
        for param in xml_group.findall("FCInt"):
            fc_params.SetInt(param.get("Name"), int(param.get("Value")))
        for param in xml_group.findall("FCBool"):
            fc_params.SetBool(param.get("Name"), param.get("Value") == "1")
        for param in xml_group.findall("FCFloat"):
            fc_params.SetFloat(param.get("Name"), float(param.get("Value")))
        for param in xml_group.findall("FCText"):
            fc_params.SetString(param.get("Name"), param.text or "")

        # Recurse into subgroups
        for subgroup in xml_group.findall("FCParamGroup"):
            subgroup_name = subgroup.get("Name")
            self._apply_params_recursive(subgroup, f"{param_path}/{subgroup_name}")

    def _apply_cfg_file(self, cfg_path: str):
        """
        Apply all parameters from a theme's .cfg file.

        Args:
            cfg_path: Path to the .cfg file.
        """
        try:
            tree = ET.parse(cfg_path)
            root = tree.getroot()

            # Find BaseApp in cfg and apply to User parameter:BaseApp
            base_app_xml = root.find(".//FCParamGroup[@Name='BaseApp']")
            if base_app_xml:
                self._apply_params_recursive(base_app_xml, "User parameter:BaseApp")

            # NotifyAll on key parameter groups to trigger UI updates
            notify_paths = [
                "User parameter:BaseApp/Preferences/View",
                "User parameter:BaseApp/Preferences/MainWindow",
                "User parameter:BaseApp/Preferences/General",
                "User parameter:BaseApp/Preferences/Editor",
                "User parameter:BaseApp/Preferences/Mod/Sketcher",
                "User parameter:BaseApp/Preferences/Mod/Draft",
                "User parameter:BaseApp/Preferences/Mod/TechDraw",
                "User parameter:BaseApp/Preferences/Mod/Part",
                "User parameter:BaseApp/Preferences/TreeView",
            ]
            for path in notify_paths:
                try:
                    FreeCAD.ParamGet(path).NotifyAll()
                except Exception:
                    pass

        except Exception as e:
            FreeCAD.Console.PrintWarning(
                f"Auto Dark Mode: Could not apply cfg file: {e}\n"
            )

    def _apply_freecad_theme(self, theme_name: str, stylesheet_path: str):
        """
        Apply theme: all parameters from cfg and reload stylesheet.

        Args:
            theme_name: The theme name.
            stylesheet_path: Full path to the .qss stylesheet file.
        """
        try:
            # 1. Apply all parameters from cfg file
            cfg_path = self._find_theme_cfg(theme_name, stylesheet_path)
            if cfg_path:
                self._apply_cfg_file(cfg_path)

            # 2. Set MainWindow params (in case not in cfg)
            params = FreeCAD.ParamGet("User parameter:BaseApp/Preferences/MainWindow")
            params.SetString("Theme", theme_name)
            params.SetString("StyleSheet", os.path.basename(stylesheet_path))
            params.NotifyAll()

            # 3. Reload UI stylesheet
            FreeCADGui.runCommand('Std_ReloadStyleSheet', 0)

            FreeCAD.Console.PrintMessage(
                f"Auto Dark Mode: Applied theme '{theme_name}'\n"
            )
        except Exception as e:
            FreeCAD.Console.PrintError(
                f"Auto Dark Mode: Failed to apply theme: {e}\n"
            )

    def update_theme(self):
        """Check system theme and update FreeCAD theme if needed."""
        if not preferences.is_enabled():
            return

        is_dark = theme_detector.is_dark_mode()
        if is_dark == self._last_dark_mode:
            return

        self._last_dark_mode = is_dark
        theme = preferences.get_dark_theme() if is_dark else preferences.get_light_theme()
        mode = "dark" if is_dark else "light"
        FreeCAD.Console.PrintMessage(
            f"Auto Dark Mode: System {mode} mode detected, applying '{theme}'\n"
        )
        self.apply_theme(theme)

    def start_monitoring(self):
        """Start monitoring system theme changes."""
        if self._timer is not None:
            self.stop_monitoring()

        self._timer = QtCore.QTimer()
        self._timer.timeout.connect(self.update_theme)
        self._timer.start(preferences.get_poll_interval())
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
