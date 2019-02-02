#!/usr/bin/env python3

import sys
import fire


# You should never get here via poetry run because you must set up the entry point explicitly in pyproject.toml.
def no_function(*argv):
    print(f"{sys.argv[0]} not defined")
    return 1

def echo(*argv):
    print("echo", argv)
    return 0

def say(*argv):
    print("say", argv)
    return 0

# Add additional entry points here.

# A "setup entry point" style function. It uses the first argument to dispatch to the right function above and consumes
# that first argument.
def dispatch():
    name = sys.argv[0]
    sys.exit(fire.Fire(dict(echo=echo, say=say).get(name, no_function)))

if __name__ == '__main__':
    # main(sys.argv)
    dispatch()
