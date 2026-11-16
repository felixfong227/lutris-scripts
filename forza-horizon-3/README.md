# Forza Horizon 3

This YAML downloads the prebuilt Wine-UWP `v2026.11.14` release, built from `75b99e6`, and verifies its SHA-256 hash.
No Wine compilation or Flatpak SDK installation is required.
On 2026-11-16, the prebuilt runtime launched FH3 in Desktop Mode and Steam Deck Game Mode through Flatpak Lutris.
The tests used an isolated copy of an existing prefix and save, with shared game assets.
They do not establish that a clean installation from this YAML completes.
It uses official DXVK 3.1.1 with Wine-UWP's CoreWindow adapter.

Both prebuilt launch tests loaded an existing profile and reached the outdoor driving scene.
Earlier tests of the Wine-side adapter also reached driving gameplay and wrote updated save data.
Loaded-module hashes confirmed official DXVK 3.1.1 and vkd3d-proton 2.14.
The reported SUV purchase/colour-confirmation crash is not verified fixed.
Both tests exited through the game's Exit to Desktop menu.
New save writes and longer gameplay stability remain unverified on the prebuilt runtime.

Earlier runtime tests showed late road textures and a crash when disconnecting the external display.
Those issues have not been revalidated on the upstream revision.
The launcher selected the Steam controller layout and restored desktop controls in earlier tests.

This installer downloads prebuilt Wine-UWP and graphics binaries, then installs the PC version of Forza Horizon 3 through Lutris.
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
- Space for the Windows image, downloaded runtimes, two repack copies, extracted game, and imported game.

The installer combines the prebuilt Wine-UWP runtime with GE-Proton 11-12 support files.
The Wine-UWP release requires glibc 2.38 or later.
Stock Wine and Proton do not provide the UWP support that this installer requires.
A Wine prefix contains an application's Windows files and settings.

The YAML declares shared command dependencies with Lutris's `require-binaries`, including `7z | 7zz` as alternatives.
Lutris checks these commands before downloading files. It does not install missing system packages.
The YAML also checks host `xprop`/`xdotool`, Python 3.10 or later, and the installed SDL2 runtime library.

### Flatpak Lutris and Steam Deck

Launch the installer through normal Flatpak Lutris.
Host X11 commands require Lutris's `flatpak-spawn` host permission.
The installer uses the libraries supplied by Lutris's runtime and does not install SDKs or compilers.

### Native Lutris

Install Python 3.10 or later, curl, tar, xz, zstd, 7-Zip with WIM support, SDL2, and Wine's runtime libraries through your distribution's package manager.
Native launches also require `unshare` with permission to create user and network namespaces.
Game Mode window identification requires `xprop` and `xdotool` on the host.
The installer checks commands but does not install native system packages.
Native Lutris remains untested.

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
2. Wait for the downloads and runtime extraction to finish.
3. Select the retained offline archive when Lutris requests it.
4. Complete any setup dialogs that appear.

The repack requests silent installation, but some dialogs can still require input.
The installer stops if runtime preparation fails.
It launches game setup after the prebuilt runtime is assembled.
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

In Steam Deck Game Mode, the launcher associates FH3's window with the current Steam shortcut.
It uses Bash, `xdotool`, and `xprop` to set `STEAM_GAME` on the game's X11 display.
It checks the window's class, title, visibility, and a unique launch ID in the owning process before changing the property.
For Flatpak Lutris, the X11 commands run on the host through the existing `flatpak-spawn` permission.
The tested SteamOS installation supplies these commands. Other systems need both commands installed for this Game Mode fix.
The game stays in its offline network namespace.
The Bash helper handles existing and recreated game windows, then stops when the launcher exits.
It does not run in Desktop Mode.

The launcher calls the unmodified `umu-run` directly. It has no embedded Python code or UMU override.
UMU and Proton still use their own Python implementations.
The repository's Python regression script is only for development; the installer does not download or run it.

The window fix passed isolated X11 regression tests and an actual Steam Deck Game Mode launch with this generated launcher.
Gamescope reported FH3 as the focused window under the Steam shortcut's application ID.
The game remained visible through loading the copied save and entering the outdoor driving scene.

Resolution is a separate setting.
Wine-UWP's `WINE_UWP_WINDOW_SIZE` defaults to `1280x800` for the startup window.
Its full-screen path uses the monitor reported by Wine, which is Gamescope's virtual display in Game Mode.
Steam's per-shortcut **Maximum Game Resolution** controls that virtual display's available size.
A 1920x1080 physical output alone does not make that mode available to FH3.
The launcher does not change the startup size, Steam's resolution setting, or the game's graphics settings.

The launcher selects your Documents folder automatically and records its absolute path in `save-folder.txt`.
To use existing progress, put the original save's parent folder in that file before you launch the game.
The game creates its `Forza Horizon 3` directory inside that parent folder.
The selected folder must already exist.
Keep the same `uwp_emu.xml` and `xbox_live.json` files when restoring a profile.
These files contain the offline identity that the game uses for saves.

## Runtime and Windows components

The installer downloads [Wine-UWP v2026.11.14](https://github.com/designgears/wine-uwp/releases/tag/v2026.11.14).
Its Wine 11.20 runtime supports x86-64 and i386 Windows programs through WoW64.
The release archive's pinned SHA-256 is `d75b36c77044555c41938fda60d1b6ed96e45a8e1e23cd27561b44ef0a16a1de`.

The installer downloads official DXVK 3.1.1 and verifies its archive's SHA-256 hash.
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
It copies the complete Wine-UWP runtime over the GE support files and includes the installed SDL2 runtime library.
The Wine-UWP archive does not include the notification component used by this launcher.
The installer downloads [WineGDK 11.18-15-winrt](https://github.com/BedrockNative/WineGDK/releases/tag/11.18-15-winrt), verifies its archive, and extracts only its x86-64 `windows.networking.connectivity.dll`.
It stores this DLL separately as `wineuwp-push-notifications.dll` and verifies the extracted file's SHA-256.
The notification source is unchanged from the WineGDK revision previously compiled by this installer.
After verifying the extracted DLL, the installer clears one byte of its Wine built-in marker in the DOS stub.
This lets the native override load the separate component instead of Wine-UWP's connectivity module; it does not change executable code.
The notification factory and asynchronous-error probe passed with this packaged DLL on the Deck.
This adds a roughly 450 MiB download.
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
| `runtime/` | The extracted prebuilt Wine-UWP runtime |
| `proton-wine-uwp/` | Wine-UWP with GE support files and SDL2 |
| `ext/` | Graphics runtimes, notification component, Appx Portable, umu, and Steam runtime |
| `windows/` | Extracted Windows components |
| `prefix/` | The Wine prefix and extracted game files |
| `dlc-source/` | Extracted expansion packages |
| `stage/` | Imported game and expansion packages |
| `logs/` | Runtime preparation, installation, and launch logs |
| `launch-fh3.sh` and `launch-fh3.cmd` | Generated scripts that launch the game |

The save folder can be outside the installation directory.
Game settings also reside under `prefix/drive_c/users/<user>/AppData/Local/Packages/Microsoft.OpusPG_8wekyb3d8bbwe/`.
Back up both locations and the offline identity files before uninstalling.

## Troubleshooting

Choose a new installation directory if it already contains `prefix/`, `windows/`, or `stage/`.
The installer stops before overwriting those directories.

For missing tools or libraries, read the Lutris installation log.
These failures can occur before runtime preparation creates its log file.

For other errors, read the corresponding log inside the installation directory:

| Operation | Log |
| --- | --- |
| Prebuilt runtime preparation | `logs/runtime-setup.log` |
| Game installation | `logs/install.log` and `prefix/drive_c/fh3-setup.log` |
| Launcher startup | `logs/launch.log` |
| Wine and Proton | `logs/steam-0.log` |
| Direct3D 12 | `logs/vkd3d.log` |
