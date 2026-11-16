# Forza Horizon 3

Install the PC version of Forza Horizon 3 through Lutris using prebuilt Wine-UWP binaries. No compilation is required.
The game runs offline in Desktop Mode or Steam Deck Game Mode.

## Requirements

- An x86-64 Linux system with Lutris and Vulkan drivers. Steam Deck users should use Flatpak Lutris.
- A fresh installation directory with no spaces in its path.
- Enough disk space for downloads, Windows components, and both extracted and imported game files.
- The `fh3-rune-files.7z` offline archive requested during installation. Its required checksum is in the YAML.

Flatpak Lutris needs permission to run host commands through `flatpak-spawn`.
For native Lutris, install Python 3.10+, zstd, 7-Zip with WIM support, SDL2, and Wine's runtime libraries.
Native launches require glibc 2.38+ and `unshare` with permission to create user and network namespaces.
Game Mode also requires `xprop` and `xdotool` on the host.

## Installation

Run from the repository root with Flatpak Lutris:

```sh
flatpak run net.lutris.Lutris -i forza-horizon-3/forza-horizon-3.yaml
```

Or with native Lutris:

```sh
lutris -i forza-horizon-3/forza-horizon-3.yaml
```

1. Choose a fresh installation directory without spaces.
2. Select `fh3-rune-files.7z` when prompted.
3. Let installation finish and complete any setup dialogs that appear.
4. Launch Forza Horizon 3 from Lutris.

The installer downloads the [FitGirl PC repack](https://archive.org/download/c-537-f-9902741647534-f-33-fd-3-a-5-c-817-a-89-c-48-a-19-d), runtimes, and Windows components, and verifies their checksums.
It includes English speech, Hot Wheels, and Blizzard Mountain, but excludes optional 4K videos and other languages.
Downloaded archives remain in `downloads/`.
Installer music is muted temporarily; game audio is restored before the first launch.

## Steam Deck Game Mode

Add the installed game as a non-Steam shortcut and select a Gamepad controller layout.
For Flatpak Lutris, set the shortcut target to `/usr/bin/flatpak` and use these launch options:

```text
run --unshare=network --command=bash --env=FH3_OFFLINE=1 net.lutris.Lutris /absolute/game/path/launch-fh3.sh
```

Replace `/absolute/game/path` with the installation directory.
For native Lutris, use the generated `launch-fh3.sh` as the shortcut target.
The launcher selects the shortcut's controller layout and restores desktop controls on exit.

To use a higher resolution, set the shortcut's **Maximum Game Resolution** in Steam, then select the resolution in FH3.
Connecting a higher-resolution display alone does not make that resolution available to the game.

## Saves

Saves go into `Forza Horizon 3` under your Documents folder by default.
To use another location, put the existing parent folder's absolute path in `save-folder.txt` before launching.

When restoring progress, keep the matching `uwp_emu.xml` and `xbox_live.json` files in `stage/opuspg/`.
Back up the save folder, those identity files, and the game settings before uninstalling.
Game settings are under `prefix/drive_c/users/<user>/AppData/Local/Packages/Microsoft.OpusPG_8wekyb3d8bbwe/`.

## Troubleshooting

Use a fresh directory if installation reports existing game data.
For missing tools or libraries, check the Lutris installation log; the installer does not install system packages.

Other logs are inside the installation directory:

| Operation | Log |
| --- | --- |
| Runtime preparation | `logs/runtime-setup.log` |
| Installation | `logs/install.log` and `prefix/drive_c/fh3-setup.log` |
| Launcher | `logs/launch.log` |
| Wine and Proton | `logs/steam-0.log` |
| Graphics | `logs/vkd3d.log` |

## Development

Run the launcher regression tests on Linux with Python 3, PyYAML, Xvfb, `xprop`, and `xdotool`:

```sh
python3 forza-horizon-3/tests/test_gamemode.py /path/to/umu/umu-run
```
