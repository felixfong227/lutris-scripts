# Forza Horizon 3 (experimental)

**Status: Experimental.** A clean installation from this YAML has not yet been verified.
Use a separate installation directory and back up existing saves before testing.

This YAML pins upstream Wine-UWP at `ba955ad4`, which includes the merged FH3 support.
It uses official DXVK 3.1.1 with Wine-UWP's CoreWindow adapter.

An isolated test runtime with the Wine-side adapter reached driving gameplay and wrote updated save data.
Loaded-module hashes confirmed official DXVK 3.1.1 and vkd3d-proton 2.14.
The reported SUV purchase/colour-confirmation crash is not verified fixed.
Normal exit, reload, and longer gameplay stability remain unverified on this combination.

Earlier runtime tests showed late road textures and a crash when disconnecting the external display.
Those issues have not been revalidated on the upstream revision.
The launcher selected the Steam controller layout and restored desktop controls in earlier tests.
Clean-installation tests remain incomplete.

This installer builds Wine UWP, downloads official graphics binaries, and installs the PC version of Forza Horizon 3 through Lutris.
Wine UWP adds Windows Store application support to Wine.
The installer uses one YAML file and requires no separate installer script from this repository.

## Game files

Lutris downloads the [FitGirl repack from Internet Archive](https://archive.org/download/c-537-f-9902741647534-f-33-fd-3-a-5-c-817-a-89-c-48-a-19-d).
The nine files contain the setup program, seven data files, and English speech.
They total approximately 29.1 GB. Lutris checks each file's MD5 hash.

The repack contains PC version `1.0.125.2`.
The installer imports Hot Wheels and Blizzard Mountain as separate packages.
It excludes optional 4K videos and other speech languages.

The installer also requests the retained `fh3-rune-files.7z` archive.
Its required SHA-256 is `b9084574234245d543a954a0ed1af5c6911a42cdba2078b676937ef6e51963e2`.
The installer copies its offline configuration, images, and `vcruntime140_1_app.dll` into the imported game.
It keeps all downloaded archives in `downloads/`.

## Requirements

- An x86-64 Linux system with Lutris and Vulkan drivers.
- A fresh installation directory with no spaces in its path.
- Space for the Windows image, Wine build, two repack copies, extracted game, and imported game.

The installer builds its own Wine UWP runtime and combines it with GE-Proton 11-12 support files.
Stock Wine and Proton do not provide the UWP support that this installer requires.
A Wine prefix contains an application's Windows files and settings.

### Flatpak Lutris and Steam Deck

Launch the installer through normal Flatpak Lutris.
The YAML installs the matching SDK and MinGW compiler extension when either package is absent.
An SDK contains the compilers, headers, and other tools required for the build.

The installer adds the user-level Flathub remote if necessary.
It reuses existing packages and installs missing packages in your home directory.
It does not require `sudo` or change the SteamOS system partition.

Automatic dependency setup requires Lutris's Flatpak host permission through `flatpak-spawn`.
The installer selects package versions from the installed Lutris application's SDK metadata.

### Native Lutris

Install these dependencies through your distribution's package manager:

- Git, GCC, G++, Make, Autoconf, Flex, Bison, and pkg-config.
- The x86-64 and i686 MinGW-w64 C compilers.
- Wine development libraries, including X11, Vulkan, GnuTLS, FreeType, and PulseAudio headers.
- Python 3, curl, tar, xz, zstd, and 7-Zip with WIM support.
- SDL2 development files, including the `sdl2` pkg-config entry.
- Standard Linux utilities, including `flock` and `nproc`.
- `unshare` with permission to create user and network namespaces.

On Debian or Ubuntu, enable source repositories before you run `sudo apt build-dep wine`.
Install any remaining tools separately. Package names differ between distributions.
The installer checks for required tools but does not install native system packages.
The current validation covers Flatpak Lutris on Steam Deck. Native Lutris remains untested.

## Installation

Run one of these commands from the repository root.

For Flatpak Lutris:

```sh
flatpak run net.lutris.Lutris -i forza-horizon-3/forza-horizon-3.yaml
```

For native Lutris:

```sh
lutris -i forza-horizon-3/forza-horizon-3.yaml
```

1. Select a fresh installation directory without spaces.
2. Wait for the downloads and runtime builds to finish.
3. Select the retained offline archive when Lutris requests it.
4. Complete any setup dialogs that appear.

The repack requests silent installation, but some dialogs can still require input.
The installer stops if a build command fails.
The installer launches game setup after the runtime build succeeds.
Lutris launches the installed game through the generated `launch-fh3.sh`.
That launcher uses umu and the assembled Proton runtime inside a network namespace with no external network access.

For Steam Input, add the launcher as a non-Steam game and select a Gamepad controller layout.
With Flatpak Lutris, set the shortcut target to `/usr/bin/flatpak` and use these launch options.
Replace `/absolute/game/path` with the installation directory:

```text
run --unshare=network --command=bash --env=FH3_OFFLINE=1 net.lutris.Lutris /absolute/game/path/launch-fh3.sh
```

With native Lutris, use the generated `launch-fh3.sh` as the shortcut target.
The launcher reads the shortcut's Steam application ID.
It uses [Steam's documented layout command](https://partner.steamgames.com/doc/features/steam_controller/getting_started_for_devs#3) to select that layout and restores desktop controls on exit.
Launches outside Steam do not select a Steam controller layout.

The launcher selects your Documents folder automatically and records its absolute path in `save-folder.txt`.
To use existing progress, put the original save's parent folder in that file before you launch the game.
The game creates its `Forza Horizon 3` directory inside that parent folder.
The selected folder must already exist.
Keep the same `uwp_emu.xml` and `xbox_live.json` files when restoring a profile.
These files contain the offline identity that the game uses for saves.

## Runtime and Windows components

The installer downloads Wine 11.20 and checks its SHA-256 hash.
It applies [upstream Wine-UWP at `ba955ad4`](https://github.com/designgears/wine-uwp/tree/ba955ad4d03f80dbde3682c1508606af5887f010), the merged revision of [PR #6](https://github.com/designgears/wine-uwp/pull/6).
The YAML pins the full commit ID instead of following changes to `main`.
The Wine build supports x86-64 and i386 and uses two parallel jobs.

The upstream graphics helper downloads official DXVK 3.1.1 and verifies its archive's SHA-256 hash.
The launcher enables `WINE_UWP_DXVK_COREWINDOW=1` so Wine-UWP handles CoreWindow presentation through stock DXVK.
It does not patch or compile DXVK.
FH3 uses the official [vkd3d-proton 2.14 release](https://github.com/HansKristian-Work/vkd3d-proton/releases/tag/v2.14), also checked by SHA-256.
The installer copies both graphics runtimes into the Proton bundle for x86-64 and i386, so Proton's prefix setup uses the selected versions.
Version 2.14 reports a tiled-resource tier that FH3's old hardware profiler recognizes, which removes warning FH204.

The launcher also uses Mesa's existing unified-memory option for DXVK only and caps shared-memory reporting at half the system RAM.
This removes the false FH401 warning on the tested Steam Deck without changing the D3D12 renderer's memory layout.
The launcher copies the installed Mesa configuration files into this installation before adding that option.
It does not change the system's Mesa configuration.
The isolated stock-DXVK test reached gameplay with this memory configuration.
Rendering and save/reload validation remain incomplete.

The installer downloads GE-Proton 11-12 and checks its SHA-256 hash.
It copies the complete Wine-UWP runtime over the GE support files and includes the build environment's SDL2 library.
Upstream Wine-UWP also builds the unchanged WineGDK notification component as `wineuwp-push-notifications.dll`.
The launcher selects that component and the extracted Windows authentication DLL in this game's prefix.

The installer downloads umu 1.4.4 and Steam runtime `4.0.20261007.263973` with SHA-256 checks.
It stores that Steam runtime inside this installation and disables automatic runtime updates.
Appx Portable `v2026.11.4` supplies the hardware-identification component.

Lutris also downloads Microsoft's 7.1 GB Windows 11 evaluation ISO for build `26200.6584`.
An ISO is an installation image.
The installer checks its SHA-256 hash before extracting the Windows components that Wine UWP needs.
You do not need an existing Windows ISO or Wine UWP installation.

## File locations

These paths are relative to the selected installation directory:

| Path | Contents |
| --- | --- |
| `build/` | Wine source and build output |
| `runtime/` | The compiled Wine UWP runtime |
| `proton-wine-uwp/` | Wine-UWP with GE support files and SDL2 |
| `ext/` | Graphics runtimes, notification component, Appx Portable, umu, and Steam runtime |
| `windows/` | Extracted Windows components |
| `prefix/` | The Wine prefix and extracted game files |
| `dlc-source/` | Extracted expansion packages |
| `stage/` | Imported game and expansion packages |
| `logs/` | Build, installation, and runtime logs |
| `launch-fh3.sh` and `launch-fh3.cmd` | Generated scripts that launch the game |

The save folder can be outside the installation directory.
Game settings also reside under `prefix/drive_c/users/<user>/AppData/Local/Packages/Microsoft.OpusPG_8wekyb3d8bbwe/`.
Back up both locations and the offline identity files before uninstalling.

## Troubleshooting

Choose a new installation directory if it already contains `prefix/`, `windows/`, or `stage/`.
The installer stops before overwriting those directories.

For SDK setup failures or missing tools, read the Lutris installation log.
These failures can occur before the build creates its log files.

For other errors, read the corresponding log inside the installation directory:

| Operation | Log |
| --- | --- |
| Wine compilation and DXVK download | `logs/build.log` |
| Wine configuration | `build/wine-build/config.log` |
| Game installation | `logs/install.log` and `prefix/drive_c/fh3-setup.log` |
| Launcher startup | `logs/launch.log` |
| Wine and Proton | `logs/steam-0.log` |
| Direct3D 12 | `logs/vkd3d.log` |
