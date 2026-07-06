![icon](resources/icons/auto_dark_mode.svg)

# Auto Dark Mode for FreeCAD

Automatically switch FreeCAD themes based on your system's light/dark
appearance setting.

## Installation

1. Open `Preferences...` > `Addon Manager`
2. Add an item in `Custom Repositories` :
    | Repository URL                                        | Branch name |
    | ----------------------------------------------------- | ----------- |
    | https://github.com/ndesgranges/freecad-auto-dark-mode | master      |
3. Press **OK** and open `Tools` > `Addon Manager`
4. Search for `freecad-auto-dark-mode` and click install
5. Reboot when asked.

You can now configure your themes, see [Configuration](#configuration)


## Configuration

1. Open FreeCAD
2. Go to `Edit` > `Auto Dark Mode Settings...`
3. Configure your preferences:
   - **Enable automatic theme switching**: Toggle the feature on/off
   - **Light mode theme**: Select the theme to use when system is in light mode
   - **Dark mode theme**: Select the theme to use when system is in dark mode
   - **Check interval**: How often to check for system theme changes
4. Click **OK** to save

<img width="414" height="499" alt="Configuration window screenshot" src="https://github.com/user-attachments/assets/599d27e1-7481-47a3-83a1-d7602668d557" />



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
- On Linux, make sure you have `gsettings` (GNOME) or `kreadconfig5` (KDE)
- The addon checks theme every few seconds; changes may take a moment to apply.
  See [Configuration](#configuration)

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit issues and pull requests.
