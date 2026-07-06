# SPDX-License-Identifier: MIT
# SPDX-FileNotice: Part of the Auto Dark Mode addon.
"""
Preferences management for Auto Dark Mode addon.
Handles configuration for light and dark theme selection.
"""

import FreeCAD
import os


# Preference parameter group path
PREF_GROUP = "User parameter:BaseApp/Preferences/Mod/AutoDarkMode"

# Cache for stylesheet paths
_stylesheet_cache = {}


def get_preferences():
    """Get the preferences parameter group."""
    return FreeCAD.ParamGet(PREF_GROUP)


def get_available_stylesheets() -> list:
    """
    Get list of available FreeCAD stylesheets.

    Returns:
        list: List of stylesheet names.
    """
    global _stylesheet_cache
    _stylesheet_cache = {"No stylesheet": ""}

    resource_base = FreeCAD.getResourceDir()
    user_base = FreeCAD.getUserAppDataDir()

    # Search in standard Gui/Stylesheets
    for base in [resource_base, user_base]:
        stylesheets_dir = os.path.join(base, "Gui", "Stylesheets")
        if os.path.isdir(stylesheets_dir):
            for f in os.listdir(stylesheets_dir):
                if f.endswith(".qss"):
                    name = os.path.splitext(f)[0]
                    if name not in _stylesheet_cache:
                        _stylesheet_cache[name] = os.path.join(stylesheets_dir, f)

    # Search in Mod folder for theme addons (like FreeCAD-themes, OpenTheme)
    mod_dir = os.path.join(user_base, "Mod")
    if os.path.isdir(mod_dir):
        for addon_name in os.listdir(mod_dir):
            addon_path = os.path.join(mod_dir, addon_name)
            if not os.path.isdir(addon_path):
                continue
            # Skip backup folders and our own addon
            if "backup" in addon_name.lower() or addon_name == "auto-dark-mode":
                continue
            # Look for .qss files (not in overlay subfolders)
            for item in os.listdir(addon_path):
                item_path = os.path.join(addon_path, item)
                if os.path.isdir(item_path):
                    # Check for theme.qss inside theme subfolder
                    qss_file = os.path.join(item_path, f"{item}.qss")
                    if os.path.isfile(qss_file):
                        if item not in _stylesheet_cache:
                            _stylesheet_cache[item] = qss_file
                elif item.endswith(".qss"):
                    name = os.path.splitext(item)[0]
                    if name not in _stylesheet_cache:
                        _stylesheet_cache[name] = item_path

    result = sorted(_stylesheet_cache.keys())
    FreeCAD.Console.PrintLog(f"Auto Dark Mode: Found {len(result)} stylesheets: {result}\n")
    return result


def get_stylesheet_path(name: str) -> str:
    """Get the full path to a stylesheet by name."""
    global _stylesheet_cache

    if not _stylesheet_cache:
        get_available_stylesheets()  # Populate cache

    return _stylesheet_cache.get(name, "")


def get_light_theme() -> str:
    """Get the configured theme for light mode."""
    prefs = get_preferences()
    return prefs.GetString("LightTheme", "No stylesheet")


def set_light_theme(theme: str):
    """Set the theme to use for light mode."""
    prefs = get_preferences()
    prefs.SetString("LightTheme", theme)


def get_dark_theme() -> str:
    """Get the configured theme for dark mode."""
    prefs = get_preferences()
    # Default to a common dark theme if available
    return prefs.GetString("DarkTheme", "Dark-Outline")


def set_dark_theme(theme: str):
    """Set the theme to use for dark mode."""
    prefs = get_preferences()
    prefs.SetString("DarkTheme", theme)


def is_enabled() -> bool:
    """Check if automatic theme switching is enabled."""
    prefs = get_preferences()
    return prefs.GetBool("Enabled", True)


def set_enabled(enabled: bool):
    """Enable or disable automatic theme switching."""
    prefs = get_preferences()
    prefs.SetBool("Enabled", enabled)


def get_poll_interval() -> int:
    """Get the system theme polling interval in milliseconds."""
    prefs = get_preferences()
    return prefs.GetInt("PollInterval", 5000)  # Default 5 seconds


def set_poll_interval(interval: int):
    """Set the system theme polling interval in milliseconds."""
    prefs = get_preferences()
    prefs.SetInt("PollInterval", max(1000, interval))  # Minimum 1 second
