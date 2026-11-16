#!/usr/bin/env python3
"""Check the generated Bash launcher on Linux with Xvfb, xprop and xdotool.

python3 test_gamemode.py /path/to/umu-run
Requires PyYAML. The UMU ZIPAPP supplies Xlib for test windows only. Wine/UMU and Steam commands
are replaced by fixtures. The installed launcher never runs this test script.
"""
from contextlib import closing
import json
import os
from pathlib import Path
import shutil
from string import Template
import subprocess
import sys
import tempfile
import time

import yaml

APPID = 0xCAFE1234
GAME_CLASS = 'forza_x64_release_final.exe'


def window_child(config):
    from Xlib import X, Xatom, display

    with closing(display.Display(':96')) as d:
        root = d.screen().root
        foreign = subprocess.Popen(['sleep', '30'], env=dict(os.environ, FH3_LAUNCH_ID='another-launch'))

        def create(name='Forza Horizon 3', wm_class=GAME_CLASS, pid=None, mapped=True, properties=True):
            w = root.create_window(0, 0, 100, 100, 0, X.CopyFromParent)
            if properties:
                w.set_wm_name(name)
                w.set_wm_class(wm_class, wm_class)
                w.change_property(d.intern_atom('_NET_WM_PID'), Xatom.CARDINAL, 32,
                                  [os.getpid() if pid is None else pid])
            if mapped:
                w.map()
            d.sync()
            return w

        def tag(w):
            prop = w.get_full_property(d.intern_atom('STEAM_GAME'), Xatom.CARDINAL)
            return list(prop.value) if prop else None

        def wait_tag(w):
            deadline = time.monotonic() + 5
            while time.monotonic() < deadline:
                if tag(w) == [APPID]:
                    return
                time.sleep(0.05)
            raise AssertionError(f'FH3 window has {tag(w)}, expected {APPID}')

        try:
            game = create(properties=not config.get('late'))
            unrelated = [create(name='cmd.exe', wm_class='conhost.exe'),
                         create(pid=foreign.pid), create(name='Default IME'),
                         create(wm_class='other.exe'), create(mapped=False), create(pid=0)]
            Path(os.environ['FH3_TEST_READY']).touch()
            if config.get('late'):
                time.sleep(0.75)
                game.set_wm_name('Forza Horizon 3')
                game.set_wm_class(GAME_CLASS, GAME_CLASS)
                game.change_property(d.intern_atom('_NET_WM_PID'), Xatom.CARDINAL, 32, [os.getpid()])
                d.sync()
            if config['tagged']:
                wait_tag(game)
                if config.get('recreate'):
                    game.destroy()
                    d.sync()
                    game = create()
                    wait_tag(game)
            else:
                time.sleep(0.8)
                assert tag(game) is None, f'Unexpected tag {tag(game)}'
            for w in unrelated:
                assert tag(w) is None, f'Unrelated/hidden window {w.id:#x} was tagged'
            print('WINDOW_CHECK_PASS', flush=True)
            return config.get('exit_code', 0)
        except AssertionError as exc:
            print(str(exc), flush=True)
            return 31
        finally:
            foreign.terminate()
            foreign.wait()


def main():
    archive = Path(sys.argv[1]).resolve()
    sys.path.insert(0, str(archive))
    from Xlib import display, error

    source = (Path(__file__).resolve().parents[1] / 'forza-horizon-3.yaml').read_text()
    installer = yaml.safe_load(source)['script']['installer']
    launcher = next(step['write_file']['content'] for step in installer
                    if step.get('write_file', {}).get('file') == '$GAMEDIR/launch-fh3.sh')
    # Lutris write_file uses string.Template, which turns $$ into a literal $.
    # Exercise the generated script rather than the raw YAML content.
    launcher = Template(launcher).safe_substitute(HOME='/home/test-user')
    assert 'python' not in launcher.lower() and 'FH3_UMU' not in launcher
    assert 'run_in_steammode' not in source, 'Do not patch UMU'
    subprocess.run(['bash', '-n'], input=launcher, text=True, check=True)
    # Substitute only the Flatpak marker path, so the test never writes to /.
    launcher = launcher.replace('/.flatpak-info', '$base/fake-flatpak-info')
    with tempfile.TemporaryDirectory(prefix='fh3-bash-test-') as tmp:
        root = Path(tmp)
        tools = root / 'bin'
        tools.mkdir()

        def script(path, body):
            path.write_text('#!/usr/bin/env bash\nset -eu\n' + body)
            path.chmod(0o755)

        script(tools / 'steam', 'printf "%s\\n" "$@" >> "$FH3_TEST_STEAM_LOG"\n')
        script(tools / 'flatpak-spawn', 'test "$1" = --host\nshift\nprintf "host\\n" >> "$FH3_TEST_BRIDGE_LOG"\nexec "$@"\n')
        for tool in ('xprop', 'xdotool'):
            real = shutil.which(tool)
            assert real, f'Install {tool} for this test'
            # Hold the first search until the game window already exists.
            gate = ('if [ "${1:-}" = search ]; then\n'
                    '  while [ ! -f "$FH3_TEST_READY" ]; do sleep 0.02; done\nfi\n') if tool == 'xdotool' else ''
            script(tools / tool, f'printf "{tool}\\n" >> "$FH3_TEST_X11_LOG"\n' + gate + f'exec "{real}" "$@"\n')
        server = subprocess.Popen(['Xvfb', ':96', '-screen', '0', '800x600x24', '-nolisten', 'tcp', '-ac'],
                                  stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        try:
            for _ in range(100):
                try:
                    with closing(display.Display(':96')):
                        break
                except error.DisplayConnectionError:
                    assert server.poll() is None, 'Xvfb failed to start'
                    time.sleep(0.02)
            else:
                raise AssertionError('Xvfb did not become ready')

            def run_case(name, *, env_changes=None, flatpak=False, prepare=False, **options):
                base = root / name
                for directory in ('logs', 'save', 'ext/umu'):
                    (base / directory).mkdir(parents=True)
                (base / 'save-folder.txt').write_text(str(base / 'save') + '\n')
                launch = base / 'launch-fh3.sh'
                script(launch, launcher)
                if flatpak:
                    (base / 'fake-flatpak-info').touch()
                config = dict(tagged=True)
                config.update(options)
                script(base / 'ext/umu/umu-run', '''test "$1" = "$WINEPREFIX/drive_c/windows/system32/cmd.exe"
if [ "${FH3_TEST_PREPARE:-}" = 1 ]; then
  test "$2" = /c && test "$3" = exit
  exit 19
fi
test "$2" = /c && test "$3" = "$FH3_DATA_WIN\\launch-fh3.cmd"
export SteamAppId=0 SteamGameId=0
if [ "${FH3_TEST_DROP_ID:-}" = 1 ]; then unset FH3_LAUNCH_ID; fi
exec "$FH3_TEST_PYTHON" "$FH3_TEST_SCRIPT" --child "$FH3_TEST_CONFIG"
''')
                env = dict(os.environ, PATH=f'{tools}:{os.environ["PATH"]}', DISPLAY=':96',
                           XDG_CURRENT_DESKTOP='gamescope', XDG_SESSION_DESKTOP='gamescope',
                           STEAM_MULTIPLE_XWAYLANDS='1', SteamAppId=str(APPID), FH3_OFFLINE='1',
                           FH3_TEST_UMU=str(archive), FH3_TEST_SCRIPT=str(Path(__file__).resolve()),
                           FH3_TEST_PYTHON=sys.executable, FH3_TEST_CONFIG=json.dumps(config),
                           FH3_TEST_READY=str(base / 'ready'), FH3_TEST_PREPARE='1' if prepare else '',
                           FH3_TEST_STEAM_LOG=str(base / 'steam.log'), FH3_TEST_X11_LOG=str(base / 'x11.log'),
                           FH3_TEST_BRIDGE_LOG=str(base / 'bridge.log'))
                env.update(env_changes or {})
                result = subprocess.run(['bash', str(launch)] + (['--prepare'] if prepare else []),
                                        env=env, capture_output=True, text=True, timeout=15)
                expected = 19 if prepare else config.get('exit_code', 0)
                log = (base / 'logs/launch.log').read_text() if (base / 'logs/launch.log').exists() else ''
                assert result.returncode == expected, (name, result.returncode, result.stderr, log)
                if not prepare:
                    assert 'WINDOW_CHECK_PASS' in log, (name, log)
                    assert ('FH3: set STEAM_GAME=' in log) == config['tagged'], (name, log)
                if prepare or env.get('XDG_CURRENT_DESKTOP') == 'KDE':
                    assert not (base / 'x11.log').exists(), 'X tools ran outside Game Mode'
                if not prepare and env['SteamAppId'].isdigit() and int(env['SteamAppId']) != 0:
                    calls = (base / 'steam.log').read_text().splitlines()
                    assert calls[-2:] == ['steam://forceinputappid/413080', 'steam://forceinputappid/0'], calls
                if flatpak:
                    assert (base / 'bridge.log').is_file(), 'Flatpak did not use host tools'
                for proc in Path('/proc').glob('[0-9]*/cmdline'):
                    try:
                        assert str(launch).encode() not in proc.read_bytes().split(b'\0'), f'Launcher helper survived: {proc}'
                    except (FileNotFoundError, ProcessLookupError, PermissionError):
                        pass
                print(f'PASS: {name}', flush=True)

            run_case('already-created-window-and-exit-status', exit_code=23)
            run_case('late-properties-and-recreated-window', late=True, recreate=True)
            run_case('flatpak-host-tools', flatpak=True)
            run_case('missing-id', env_changes={'SteamAppId': '0'}, tagged=False)
            run_case('invalid-id', env_changes={'SteamAppId': 'invalid'}, tagged=False)
            run_case('oversized-id', env_changes={'SteamAppId': '4294967296'}, tagged=False)
            run_case('missing-launch-token', env_changes={'FH3_TEST_DROP_ID': '1'}, tagged=False)
            run_case('unavailable-display', env_changes={'DISPLAY': ':95'}, tagged=False, exit_code=17)
            run_case('desktop-mode', env_changes={'XDG_CURRENT_DESKTOP': 'KDE', 'XDG_SESSION_DESKTOP': 'KDE'}, tagged=False)
            run_case('prefix-prepare', prepare=True)
            print('ALL_BASH_GAME_MODE_TESTS_PASS', flush=True)
        finally:
            server.terminate()
            server.wait()


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == '--child':
        sys.path.insert(0, os.environ['FH3_TEST_UMU'])
        sys.exit(window_child(json.loads(sys.argv[2])))
    main()
