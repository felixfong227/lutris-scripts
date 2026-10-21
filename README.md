# lutris-scripts

Lutris installer scripts, one game per folder.

## Games

| Game | Folder | Source |
| --- | --- | --- |
| Need for Speed: Undercover, PC, 2008 | [need-for-speed-undercover](need-for-speed-undercover/) | DVD image on archive.org |

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

## Writing a new script

Scripts here use Lutris's standalone format. `name`, `game_slug`, `version`, `slug` and `runner` go at the top level, and everything else goes under `script`. The format is documented in [docs/installers.rst](https://github.com/lutris/lutris/blob/master/docs/installers.rst) in the Lutris repo.
