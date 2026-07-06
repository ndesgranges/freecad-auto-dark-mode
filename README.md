# Auto Dark Mode for FreeCAD

Automatically switch FreeCAD themes based on your system's light/dark appearance setting.

## Features

- **Automatic Theme Switching**: Detects system theme changes and applies the appropriate FreeCAD stylesheet
- **Cross-Platform Support**: Works on macOS, Windows, and Linux (GNOME, KDE)
- **Configurable Themes**: Choose which FreeCAD theme to use for light mode and dark mode
- **Real-time Monitoring**: Continuously monitors system theme and reacts to changes
- **Supports Theme Addons**: Automatically detects themes from FreeCAD-themes, OpenTheme, and other theme addons

## Installation

### Manual Installation (FreeCAD 1.0+)

1. Download or clone this repository
2. Copy the `AutoDarkMode` folder to your FreeCAD Mod directory:
   - **macOS**: `~/Library/Application Support/FreeCAD/v1-1/Mod/`
   - **Windows**: `%APPDATA%\FreeCAD\v1-1\Mod\`
   - **Linux**: `~/.local/share/FreeCAD/v1-1/Mod/`
3. Restart FreeCAD

### Via Addon Manager

*Coming soon*

## Configuration

1. Open FreeCAD
2. Go to **Edit → Auto Dark Mode Settings...**
3. Configure your preferences:
   - **Enable automatic theme switching**: Toggle the feature on/off
   - **Light mode theme**: Select the stylesheet to use when system is in light mode
   - **Dark mode theme**: Select the stylesheet to use when system is in dark mode
   - **Check interval**: How often to check for system theme changes (default: 5 seconds)
4. Click **OK** to save

## Supported Platforms

> [!NOTE]
> Should work for the 3 listed platforms but only tested on MacOS.

### macOS
Detects the system appearance setting (System Settings → Appearance).

### Windows
Reads the Windows personalization settings from the registry.

### Linux
Supports multiple desktop environments:
- **GNOME**: Reads `color-scheme` and `gtk-theme` settings
- **KDE Plasma**: Reads the color scheme configuration
- Other environments may work if they follow similar conventions

## Troubleshooting

### Addon not loading
- Check the FreeCAD Report view (View → Panels → Report view) for error messages

### Theme not changing
- Ensure automatic theme switching is enabled in settings
- Check the Report view for any error messages
- Verify that the selected themes exist in your FreeCAD installation

### Themes not showing in list
- The addon searches for `.qss` files in:
  - FreeCAD's built-in `Gui/Stylesheets` folder
  - Theme addons in your Mod folder (FreeCAD-themes, OpenTheme, etc.)
- Check that your theme addons are properly installed

### System theme not detected correctly
- On Linux, make sure you have `gsettings` (GNOME) or `kreadconfig5` (KDE) available
- The addon checks theme every few seconds; changes may take a moment to apply

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit issues and pull requests.
