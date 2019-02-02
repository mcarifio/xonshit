# ln -s ~/path/to/xonshit/rc.xsh ~/.config/xonsh/rc.xsh

import logging

# TODO mike@carif.io: connect this up to the sourcer's stderr. How?
logger = logging.getLogger('rc')
logger.setLevel(logging.WARN)

from pathlib import Path
import xonsh.environ as xe


# Get the environment whether you are sourced or run in python directly.
try:
    env = __xonsh__.env
except NameError as ne:
    # Not sourced. Construct a starting environ
    env = xe.Env()

def ls_colors():
    env['LS_COLORS'] = 'rs=0:di=01;36:ln=01;36:mh=00:pi=40;33:so=01;35:do=01;35:bd=40;33;01:cd=40;33;01:or=40;31;01:su=37;41:sg=30;43:ca=30;41:tw=30;42:ow=34;42:st=37;44:ex=01;32:'

def append_PATH(path:Path, shell_env = env):
    env['PATH'].add(str(path))
    logger.debug(f"appended {path}")

def prepend_PATH(path:Path, shell_env = env):
    env['PATH'].insert(0, str(path))
    logger.debug(f"prepended {path}")


def is_snappy_installed(): return True

def load_xontrib():
    # xontrib load apt_tabcomplete autoxsh coreutils docker_tabcomplete prompt_ret_code whole_word_jumping vox vox_tabcomplete
    pass

additional_paths = list()
if is_snappy_installed(): additional_paths.append(Path('/snap/bin'))

def append_paths(paths):
    for p in paths:
        if p.exists():
            append_PATH(p)
        else:
            logger.warn(f"{p} does't exist, skipping")

# TODO mike@carif.io: better way to signal an rc file?
if __name__.endswith('.xonshrc') or __name__.endswith('rc.xsh'):
    append_paths(additional_paths)
