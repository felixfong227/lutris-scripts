# Need for Speed: The Run

Installs the 2011 PC version of Need for Speed: The Run from a ready-to-play copy on archive.org:
https://archive.org/details/need-for-speed-the-run_202512

Status: not tested yet.

## What's in the download

The upload is the installed game folder, packed as one 11.2 GB `.7z`. It's already set up:

- Update 1, the last official patch.
- The Neo crack, which removes EA's activation check.
- ThirteenAG's Fusion Fix mod, loaded by the `dinput8.dll` in the game folder. That file is ThirteenAG's Ultimate ASI Loader.

There's no setup or keygen, so the install needs nothing from you once it starts.

## Requirements

- Lutris with a Wine runner. The uploader recommends a recent GE-Proton on the Steam Deck. The script uses your default Wine version, so see Troubleshooting if the game won't start.
- About 29 GB of free space during the install. The archive is 11.2 GB and the unpacked game is 17.5 GB. After the install, the game takes 17.5 GB.

## Install

From the repo root:

```
lutris -i need-for-speed-the-run/need-for-speed-the-run.yaml
```

The script does this:

1. Downloads the archive and checks its md5. On an 11 GB file the check takes a few minutes.
2. Creates a 64-bit Wine prefix in the install folder.
3. Unpacks the game into `Need for Speed The Run/` inside the install folder.
4. Sets the `dinput8` DLL override to native, so Wine loads the bundled ASI loader and Fusion Fix runs.

## Fusion Fix settings

The settings file is `Need for Speed The Run/plugins/NFSTheRun.FusionFix.ini` inside the install folder.

The upload comes with every car and challenge series unlocked. To unlock them by playing instead, change `UnlockEverything = 1` to `UnlockEverything = 0`.

The same file also skips the intro videos, `SkipIntro`, and makes windowed mode borderless, `ImproveWindowedMode`.

## Troubleshooting

The uploader warns that the game crashes now and then, on Windows too.

If the game won't start or crashes on launch, try GE-Proton. Right-click the game in Lutris, open Configure, go to Runner options, and pick a GE-Proton build under Wine version.

If Fusion Fix isn't doing anything, for example the intro videos still play, check that `dinput8` is set to `n,b` under Configure, Runner options, DLL overrides.

If Lutris fails to set up Wine with "File exists", see [Troubleshooting](../README.md#troubleshooting) in the main README.
