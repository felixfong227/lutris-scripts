# Need for Speed: Undercover

This installer uses the 2008 PC release from the [RELOADED DVD image on Internet Archive](https://archive.org/details/need-for-speed-undercover_202201).
It extracts the image, runs game setup, and installs the release's patched executable.

## Requirements

- Lutris with a Wine runner.
- Approximately 20 GB of free space during installation.

The download is 5.2 GB. The extracted image needs another 5.2 GB, and the installed game needs approximately 10 GB.
On a Steam Deck, use Desktop Mode to access both setup windows.

## Installation

Run one of these commands from the repository root.

For native Lutris:

```sh
lutris -i need-for-speed-undercover/need-for-speed-undercover.yaml
```

For Flatpak Lutris:

```sh
flatpak run net.lutris.Lutris -i need-for-speed-undercover/need-for-speed-undercover.yaml
```

Lutris downloads `rld-nfuc.iso` and checks its MD5 hash.
It creates a 64-bit Wine prefix in the selected installation directory.
A Wine prefix contains the game's Windows files and settings.
The installer extracts the image with 7-Zip without mounting it.

Setup and the included key generator open together.
Complete these steps:

1. Generate a key in the key generator.
2. Paste the key into setup when it requests one.
3. Keep the default destination inside setup.
4. Skip EA registration.
5. Complete setup.
6. Close the key generator after setup finishes.

Lutris waits for both programs to close before it continues.
It copies the original `nfs.exe` into the game's `backup/` directory, then installs the patched executable from the image.

## Game files

The game directory is relative to the selected installation directory:

```text
drive_c/Program Files (x86)/EA Games/Need for Speed Undercover/
```

The patched executable removes the release's SecuROM disc check.
The installer does not apply the official `1.0.1.17` patch.
That patch replaces `nfs.exe` and does not match the bundled patched executable.

## Troubleshooting

### Setup requests a key

The key generator can appear behind the setup window.
Use the desktop taskbar or `Alt+Tab` to select it.

### Installation waits after setup closes

Close the key generator so Lutris can continue.

### The backup step reports "Source does not exist"

The script expects the default destination inside setup.
This error can occur if you change that destination or cancel setup.
Repeat the installation with the default destination.

For Wine extraction errors, see the [repository troubleshooting guide](../README.md#troubleshooting).
