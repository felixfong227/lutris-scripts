# Need for Speed: The Run

This installer extracts the 2011 PC game from the [game archive on Internet Archive](https://archive.org/details/need-for-speed-the-run_202512).
The archive contains the game directory, so installation does not require a setup program or key generator.

## Requirements

- Lutris with a Wine runner.
- Approximately 29 GB of free space during installation.

The archive is 11.2 GB. The extracted game needs approximately 17.5 GB.
The installer uses the default Wine version configured in Lutris.

## Installation

Run one of these commands from the repository root.

For native Lutris:

```sh
lutris -i need-for-speed-the-run/need-for-speed-the-run.yaml
```

For Flatpak Lutris:

```sh
flatpak run net.lutris.Lutris -i need-for-speed-the-run/need-for-speed-the-run.yaml
```

The installer performs these steps:

1. It downloads the archive and checks its MD5 hash.
2. It creates a 64-bit Wine prefix in the selected installation directory.
3. It extracts the game into `Need for Speed The Run/` inside that directory.
4. It sets the `dinput8` override to `n,b` so Wine loads the included ASI loader.

The ASI loader loads Fusion Fix from the game's `plugins/` directory.

## Included files

The archive includes:

- Official Update 1.
- The Neo crack, which removes EA's activation check.
- ThirteenAG's Fusion Fix and Ultimate ASI Loader.

## Fusion Fix settings

Edit this file inside the installation directory:

```text
Need for Speed The Run/plugins/NFSTheRun.FusionFix.ini
```

The archive's configuration unlocks all cars and challenge series.
Set `UnlockEverything = 0` if you want to unlock them through gameplay.

The same file contains `SkipIntro` for intro videos and `ImproveWindowedMode` for borderless windowed mode.

## Troubleshooting

### Change the Wine version

1. Open the game's **Configure** dialog in Lutris.
2. Select **Runner options**.
3. Select a build under **Wine version**.

### Fusion Fix does not load

Check **Configure > Runner options > DLL overrides**.
The `dinput8` entry must contain `n,b`.
The game directory must also contain the included `dinput8.dll` and `plugins/` directory.

For Wine extraction errors, see the [repository troubleshooting guide](../README.md#troubleshooting).
