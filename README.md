# lutris-scripts

Lutris installer scripts, one game per folder.

## Games

| Game | Folder | Source |
| --- | --- | --- |
| Need for Speed: Undercover, PC, 2008 | [need-for-speed-undercover](need-for-speed-undercover/) | DVD image on archive.org |
| Need for Speed: The Run, PC, 2011 | [need-for-speed-the-run](need-for-speed-the-run/) | Ready-to-play copy on archive.org |

## Running a script

Install [Lutris](https://lutris.net), then point it at a script:

```
lutris -i need-for-speed-undercover/need-for-speed-undercover.yaml
```

Lutris opens its install dialog and asks where to put the game. It then downloads the files the script lists and runs the steps in order. Each game's README covers anything you have to do by hand during the install.

## Layout

```
<game-slug>/
  <game-slug>.yaml   the Lutris script
  README.md          source, install steps, known problems
```

The folder name is the game's slug on lutris.net, the part after `lutris.net/games/`.

## Troubleshooting

Before a script's own steps run, Lutris downloads the Wine version it uses and unpacks it into `runners/wine/`. If an earlier try left that folder half-unpacked, Lutris fails with `[Errno 17] File exists`. Quit Lutris, delete the folder named in the error along with the downloaded archive, then run the script again. With dw-proton on the Steam Deck's Flatpak Lutris:

```
rm -rf ~/.var/app/net.lutris.Lutris/data/lutris/runners/wine/dw-proton-x86_64
rm -f ~/.var/app/net.lutris.Lutris/cache/lutris/dwproton-*.tar.xz
```

## Writing a new script

Scripts here use Lutris's standalone format. `name`, `game_slug`, `version`, `slug` and `runner` go at the top level, and everything else goes under `script`. The format is documented in [docs/installers.rst](https://github.com/lutris/lutris/blob/master/docs/installers.rst) in the Lutris repo.
