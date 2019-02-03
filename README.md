# xonshit

## hacking

Install python on your local machine. I prefer `pyenv`, but you could use your platform's package manager if you prefer:

* Install [pyenv](https://github.com/pyenv/pyenv#installation) manually or using the 
  [pyenv-installer](https://github.com/pyenv/pyenv-installer#pyenv-installer). This is optional but useful.
  Depending on the shell (bash, fish, zsh, xonsh) you may need to source the right file so that the `pyenv` command works.

* Install python 3.7 using `pyenv`:

```bash

$ id  ## not root, you are you                                                                                                                                                                                                               
uid=1000(mcarifio) gid=1000(mcarifio) groups=1000(mcarifio), ...

$ pyenv --version  ## confirm pyenv works, you'll get a version, doesn't matter what
pyenv 1.2.5-41-g6309aaf

$ pyenv install 3.7.0  ## lotsa output
$ pyenv global 3.7.0  ## set the global python, you can set a local one below
$ python -V
Python 3.7.0
```

Confirm that python is coming from where you expect. If `pyenv` or your package manager "just works"
you don't really need this. Good to know however and all three methods should yield the same answer.

```bash
$ which python                                                                                                                                                                                                               
/home/mcarifio/.pyenv/versions/3.7.0/bin/python

$ pyenv which python                                                                                                                                                                                                         
/home/mcarifio/.pyenv/versions/3.7.0/bin/python

$ python -c 'import sys; print(sys.executable)'
/home/mcarifio/.pyenv/versions/3.7.0/bin/python
```


First time for `xonshit`, get the sources, pin a pyenv version to the git root and install the project dependencies in a python virtualenv using `poetry`:

```bash
$ git clone https://www.github.com/mcarifio/xonshit && cd xonshit  ## get the repo
```

Optionally, define a "directory local" python version, pinning it so it doesn't change out from under you.

```bash
$ pyenv local 3.7.0
$ pyenv local
3.7.0
$ python -V 
```

Bootstrap python [poetry]()

```bash
$ python -m pip install poetry  # install poetry into your working venv

$ which poetry                                                                                                                                                                                                               
/home/mcarifio/.pyenv/versions/3.7.0/bin/poetry

$ poetry --version                                                                                                                                                                                                           
Poetry 0.12.11

$ poetry check
All set!
$ poetry update  # update poetry.lock
$ poetry install # build the virtualenv and populate with this module and all the dependencies
```

Do a quick smoke test of the environment you just created:

```bash
python -c 'import toml; print(toml.load("pyproject.toml")["tool"]["poetry"]["name"])'  ## parse out the module name
xonshit

python -c 'import toml, json; print(json.dumps(toml.load("pyproject.toml"), indent=2))'
```
```json
{
  "tool": {
    "poetry": {
      "name": "xonshit",
      "version": "0.1.0",
      "description": "xonsh community environment similar to bash-it",
      "authors": [
        "Mike Carifio <mike@carif.io>"
      ],
      "license": "MIT",
      "readme": "xonshit/README.md",
      "homepage": "https://www.github.com/mcarifio/xonsh-it",
      "dependencies": {
        "python": "^3.7",
        "xonsh": "^0.8.9",
        "poetry": "^0.12.11",
        "prompt_toolkit": "^2.0",
        "fire": "^0.1.3",
        "pytest": "^4.1",
        "hypothesis": "^4.4",
        "distro": {
          "version": "^1.3",
          "platform": "Linux"
        }
      },
      "dev-dependencies": {
        "black": {
          "version": "^18.3-alpha.0",
          "allows-prereleases": true
        },
        "pypiserver": "^1.2",
        "passlib": "^1.7",
        "xonsh": {
          "version": "^0.8.9",
          "optional": true
        }
      },
      "scripts": {
        "echo": "xonshit.runner:echo",
        "say": "xonshit.runner:say",
        "testing": "xonshit.runner:testing"
      },
      "source": [
        {
          "name": "xonshit",
          "url": "http://localhost:9090/",
          "username": "xonshit",
          "password": "xonshit"
        }
      ]
    }
  },
  "build-system": {
    "requires": [
      "poetry>=0.12"
    ],
    "build-backend": "poetry.masonry.api"
  }
}
```

Note that some of the specifics above might change as `pyproject.toml` evolves. You're confirming that the `pyproject.toml` is well formed.


Optionally the first time:
```
htpasswd -b project/build/resources/pypiserver/htpasswd.txt ${USER} xonshit
```

Afterwards:
```bash
```