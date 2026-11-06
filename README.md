# Lutris installers

This repository contains Lutris installers for PC games on Linux.
Each game has one YAML installer and a README with its requirements and installation steps.

## Games

| Game | Installer guide | Download source |
| --- | --- | --- |
| Need for Speed: Undercover, 2008 | [Undercover](need-for-speed-undercover/README.md) | RELOADED DVD image on Internet Archive |
| Need for Speed: The Run, 2011 | [The Run](need-for-speed-the-run/README.md) | Game archive on Internet Archive |
| Forza Horizon 3 | [Forza Horizon 3](forza-horizon-3/README.md) | FitGirl repack on Internet Archive |

## Installation

Install [Lutris](https://lutris.net) before you use these scripts.
Run the commands from the repository root.

For native Lutris:

```sh
lutris -i need-for-speed-undercover/need-for-speed-undercover.yaml
```

For Flatpak Lutris:

```sh
flatpak run net.lutris.Lutris -i need-for-speed-undercover/need-for-speed-undercover.yaml
```

1. Select the game installation directory in Lutris.
2. Wait for Lutris to download the required files.
3. Complete the steps in the game's installation guide.

Lutris can remove cached downloads after installation.
Keep a separate copy of large downloads if you want to reuse them.

## Repository layout

```text
<game-slug>/
  <game-slug>.yaml
  README.md
```

The folder name matches the game's slug on Lutris.net.
The slug is the part of the game URL after `lutris.net/games/`.

## Troubleshooting

An incomplete Wine runner directory can cause `[Errno 17] File exists` during runner extraction.
This error occurs before the game installation steps start.

1. Close Lutris.
2. Remove the incomplete runner directory named in the error.
3. Remove the cached Wine runner archive associated with that directory.
4. Start the installer again.

For Flatpak Lutris, Wine runners are under `~/.var/app/net.lutris.Lutris/data/lutris/runners/wine/`.
Its download cache is under `~/.var/app/net.lutris.Lutris/cache/lutris/`.

## Add an installer

Use Lutris's standalone YAML format.
Place `name`, `game_slug`, `version`, `slug`, and `runner` at the top level.
Place the remaining settings under `script`.

See the [Lutris installer reference](https://github.com/lutris/lutris/blob/master/docs/installers.rst) for the format and available commands.
