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


import sys
import fire
import pytest
import os.path
import logging

logging.basicConfig(level=os.environ.get('RUNNER_LOGLEVEL', 'INFO').upper())
logger = logging.getLogger(__name__)
logger.debug(f'file {__file__}')

def echo(*argv):
    # logger.debug(argv)
    args = list(argv) if argv else list()
    logger.info(args)
    return 0

def say(*argv):
    args = list(argv) if argv else list()
    logger.info(args)
    return 0

def testing(*argv):
    logger.debug(f'testing {argv}')
    pytest_args = list(argv) if argv else list()
    here = os.path.dirname(__file__)
    pytest_args.insert(0, f'--rootdir={here}')
    pytest_args.insert(0, '--verbosity=4')
    conf = here + os.sep + 'pytest.ini'
    if os.path.exists(conf):
        pytest_args.insert(0, conf)
        pytest_args.insert(0, '-c')

    logger.debug(pytest_args)
    return pytest.main(pytest_args)

# Add additional entry points here.


# TODO mike@carif.io: describe the magic here
def dispatch(*argv):
    logger.debug(sys.argv)
    logger.debug(f'dispatch {argv}')
    entries = dict(echo=echo, say=say, testing=testing)
    return fire.Fire(entries)


if __name__ == '__main__':
    # sys.exit(dispatch(sys.argv[1:]))
    sys.exit(dispatch())
