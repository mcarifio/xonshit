#!/usr/bin/env python3
f"""

This module ({__name__}) is consumed before deployment by poetry via `poetry run <something>` and after deployment
via `python -m {__name__} <something>` for example `python -m {__name__} echo here i am` |> `here i am`.
In particular `python -m {__name__} testing` runs the pytests deployed with the module.

You can also change the logging level with the environment variable `RUNNER_LOGLEVEL`, for example
```bash
env RUNNER_LOGLEVEL=DEBUG poetry run <something>  ## when developing
env RUNNER_LOGLEVEL=DEBUG python -m xonshit.runner <something>  ## after deployment
```

"""
import traceback
import pdb
import sys
import os
import os.path
import attrdict
import fire
import pytest
import logging
# TODO mike@carif.io: TBS inspect myproject.toml for configuration for pypiserver
import toml

# for debugging: RUNNER_LOGLEVEL=debug <command>
logging.basicConfig(level=os.environ.get('RUNNER_LOGLEVEL', 'INFO').upper())
logger = logging.getLogger(__name__)
logger.debug(f'file {__file__}')
logger.debug(f'module {__name__}')


def echo(*argv):
    """
    echo.poetry.usage: [RUNNER_LOGLEVEL=debug] poetry run say 1 2 3
    echo.python.usage: [RUNNER_LOGLEVEL=debug] python -m xonshit.runner say 1 2 3
    echo.python.usage.help: [RUNNER_LOGLEVEL=debug] python -m xonshit.runner say 1 2 3

    :param argv: tuple or array of argument from poetry or the command line respectively.
    :return: status code 0
    """
    # logger.debug(argv)
    me = sys._getframe().f_code.co_name
    logger.debug(f'in {me}')
    # logger.debug(f'argv: {sys.argv}')
    argv = argv if argv else sys.argv[1:]
    logger.debug(argv)
    for a in argv: print(a, end=' ')
    print()
    return 0




# Doesn't work because sys._getframe() gets echo's call frame
# say = echo
# Copy the function's body

def say(*argv):
    """
    say.poetry.usage: [RUNNER_LOGLEVEL=debug] poetry run say 1 2 3
    say.python.usage: [RUNNER_LOGLEVEL=debug] python -m xonshit.runner say 1 2 3
    say.python.usage.help: [RUNNER_LOGLEVEL=debug] python -m xonshit.runner say 1 2 3

    :param argv: tuple or array of argument from poetry or the command line respectively.
    :return: status code 0
    """
    me = sys._getframe().f_code.co_name
    logger.debug(f'in {me}')
    argv = argv if argv else sys.argv[1:]
    logger.debug(argv)
    for a in argv: print(a, end=' ')
    print()
    return 0



def testing(*argv):
    """
    testing.poetry.usage: [RUNNER_LOGLEVEL=debug] poetry run testing [--switch[=value]]*
    testing.python.usage: [RUNNER_LOGLEVEL=debug] python -m xonshit.runner testing [--switch[=value]]*
    testing.python.usage.help: [RUNNER_LOGLEVEL=debug] python -m xonshit.runner testing --help

    :param argv: additional argument to pytest after --roodir, --verbosity and pytest.ini
    :return:
    """
    # logger.debug(f'testing {argv}')
    me = sys._getframe(0).f_code.co_name
    logger.debug(f'in {me}')
    logger.debug(argv)
    pytest_args = list(argv) if argv else sys.argv[1:]
    here = os.path.dirname(__file__)
    pytest_args.insert(0, f'--rootdir={here}')
    pytest_args.insert(0, '--verbosity=4')
    conf = here + os.sep + 'pytest.ini'
    if os.path.exists(conf):
        pytest_args.append('-c')
        pytest_args.append(conf)

    logger.debug(pytest_args)
    return pytest.main(pytest_args)

def pypiserver(*argv):
    """
    pypiserver.poetry.usage: [RUNNER_LOGLEVEL=debug] poetry run pypiserver # pyproject.toml must be property configured
    pypiserver.python.usage: [RUNNER_LOGLEVEL=debug] python -m xonshit.runner pypiserver  # always fails

    """
    # python cookbook https://www.oreilly.com/library/view/python-cookbook/0596001673/ch14s08.html
    # Doesn't require module `inspect`
    me = sys._getframe(0).f_code.co_name
    logger.debug(f'in {me}')
    # TODO mike@carif.io: do you want to test this on an deployed system? I don't think so.
    print('pypiserver can only be run via poetry')
    return 1


def tomlck(pyproject_toml=None):
    """
    tomlck.poetry.usage: [RUNNER_LOGLEVEL=debug] poetry run tomlck [--pyproject_toml=path/to/pyproject.toml]
    tomlck.python.usage: [RUNNER_LOGLEVEL=debug] python -m xonshit.runner tomlck [--pyproject_toml=path/to/pyproject.toml]
    tomlck.python.usage.help: [RUNNER_LOGLEVEL=debug] python -m xonshit.runner tomlck --help

    Checks the pyproject.toml file for well-formedness. For installed packages, pyproject.toml is in the pockage root.
    For git repos, it's up one directory. You should create a symlink to it before calling this entry point.
    :return: status_code:int
    """
    me = sys._getframe(0).f_code.co_name
    here = os.path.dirname(__file__)
    # Note: in development mode, requires a symbolic link from pyproject.toml to xonshit/pyproject.toml
    pyproject_toml = pyproject_toml or os.path.join(here, "pyproject.toml")
    logger.debug(f'in {me} reading {pyproject_toml}')
    if not os.path.exists(pyproject_toml):
        raise FileNotFoundError(pyproject_toml)
    try:
        metadata = attrdict.AttrDict(toml.load(pyproject_toml))
        logger.info(f"'{pyproject_toml}' loaded successfully, describes project named '{metadata.tool.poetry.name}'")
        return 0
    except IOError as ioe:
        logger.error(ioe.message)
        return 1


# Add additional entry points here.


# You can call dispatch directly and you get no debugging if something bad happens
# Note well: poetry calls the functions above "directly"
def dispatch(*argv):
    logger.debug(sys.argv)
    logger.debug(f'dispatch {argv}')
    entries = dict(echo=echo, say=say, testing=testing, pypiserver=pypiserver, tomlck=tomlck)
    sys.exit(fire.Fire(entries))


# You can call main directly and get a trace and debugging on an unhandled exception.
# See https://news.ycombinator.com/item?id=19075325
def main():
    try:
        dispatch()
    except SystemExit as se:
        logger.debug(f'exit status: {se.code}')
    except Exception as e:
        logger.error(e.message)
        traceback.print_exc()
        pdb.post_mortem()

if __name__ == '__main__':
    main()
