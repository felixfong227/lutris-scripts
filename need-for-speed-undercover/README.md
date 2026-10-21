# Need for Speed: Undercover

Installs the 2008 PC version of Need for Speed: Undercover from the RELOADED DVD image on archive.org:
https://archive.org/details/need-for-speed-undercover_202201

Status: not tested end to end yet. The steps were checked against the Lutris source, but nobody has run a full install with this script.

## Requirements

- Lutris with its default Wine runner.
- About 20 GB of free space during the install. The ISO is 5.2 GB, the unpacked copy takes another 5.2 GB, and the installed game needs about 10 GB.

## Install

From the repo root:

```
lutris -i need-for-speed-undercover/need-for-speed-undercover.yaml
```

The script does this:

1. Downloads `rld-nfuc.iso` and checks its md5.
2. Creates a 64-bit Wine prefix in the install folder and unpacks the ISO with 7z. Nothing gets mounted.
3. Opens EA's setup and the release's keygen side by side.
4. Copies the original `nfs.exe` into `backup/` and replaces it with the patched `nfs.exe` from the ISO's `Crack` folder.

Step 3 is the only part you do by hand. Generate a key in the keygen and paste it into setup when it asks. Keep the default install location and skip EA registration. When setup finishes, close the keygen. Lutris waits for both windows to close before it moves on.

After a successful install Lutris deletes the ISO and the unpacked files. After a failed one it keeps the ISO in `~/.cache/lutris/installer/`, so a retry doesn't download it again.

The game ends up in `drive_c/Program Files (x86)/EA Games/Need for Speed Undercover` inside the install folder.

## About the release

The archive.org upload is a cracked scene release by RELOADED. The game shipped with SecuROM disc protection, and the patched `nfs.exe` from the release skips that check. The script follows the release's own install notes: use the keygen during setup, then copy the `Crack` files into the game folder. The original `nfs.exe` stays in `backup/`.

The official 1.0.1.17 patch is not included. It replaces `nfs.exe` with a version the patched exe doesn't match, so the game stays on the launch version.

## Troubleshooting

"Source does not exist" at the backup step means setup didn't install to the default path. Usually the install location was changed, or setup was cancelled. Run the script again and keep the default location.

If the installer looks stuck after setup closes, the keygen is probably still open. Close it.

If setup asks for the disc, it won't run from an unpacked folder. The script would then need an `insert-disc` step in place of the 7z extract, so you mount `rld-nfuc.iso` yourself and setup runs from the mount.
