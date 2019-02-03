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

Install python [poetry](https://poetry.eustace.io/docs/) into your python installation, then bootstrap a virtualenv
with dependencies installed. 

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

It's useful to test `poetry publish` before you publish to your official python repository or even `pypi`. For that, you will need a `pypiserver` that has a password file:

```
htpasswd -b project/build/resources/pypiserver/htpasswd.txt ${USER} xonshit
```

You can then run the local `pypiserver` directly or indirectly. Directly:
```bash
$ pypi-server -v --overwrite -P project/build/resources/pypiserver/htpasswd.txt -v --port=9090 project/build/resources/pypiserver/packages
2019-02-03 16:43:04,766|pypiserver.core|INFO|139854031225152|+++Pypiserver invoked with: Configuration:
             VERSION = 1.2.7
       authenticated = ['update']
              auther = None
       cache_control = None
        fallback_url = None
           hash_algo = md5
                host = 0.0.0.0
        log_err_frmt = %(body)s: %(exception)s 
%(traceback)s
            log_file = None
            log_frmt = %(asctime)s|%(name)s|%(levelname)s|%(thread)d|%(message)s
        log_req_frmt = %(bottle.request)s
        log_res_frmt = %(status)s
           overwrite = False
       password_file = project/build/resources/pypiserver/htpasswd.txt
                port = 9090
redirect_to_fallback = True
                root = ['/home/mcarifio/src/mcarifio/xonshit/project/build/resources/pypiserver/packages']
              server = auto
           verbosity = 2
        welcome_file = None
2019-02-03 16:43:04,790|pypiserver.core|INFO|139854031225152|+++Pypiserver started with: Configuration:
             VERSION = 1.2.7
       authenticated = ['update']
              auther = functools.partial(<function auth_by_htpasswd_file at 0x7f324c588a60>, <HtpasswdFile 0x7f324d59e198 path='project/build/resources/pypiserver/htpasswd.txt'>)
       cache_control = None
        fallback_url = https://pypi.org/simple
           hash_algo = md5
                host = 0.0.0.0
        log_err_frmt = %(body)s: %(exception)s 
%(traceback)s
            log_file = None
            log_frmt = %(asctime)s|%(name)s|%(levelname)s|%(thread)d|%(message)s
        log_req_frmt = %(bottle.request)s
        log_res_frmt = %(status)s
           overwrite = False
       password_file = project/build/resources/pypiserver/htpasswd.txt
                port = 9090
redirect_to_fallback = True
                root = ['/home/mcarifio/src/mcarifio/xonshit/project/build/resources/pypiserver/packages']
              server = auto
           verbosity = 2
        welcome_file = welcome.html
         welcome_msg = <html><head><title>Welcome to pypiserver!</title></head><body>
<h1>Welcome to pypiserver!</h1>
<p>This is a PyPI compatible package index serving {{NUMPKGS}} packages.</p>

<p> To use this server with pip, run the the following command:
<blockquote><pre>
pip install --extra-index-url {{URL}} PACKAGE [PACKAGE2...]
</pre></blockquote></p>

<p> To use this server with easy_install, run the the following command:
<blockquote><pre>
easy_install -i {{URL}}simple/ PACKAGE
</pre></blockquote></p>

<p>The complete list of all packages can be found <a href="{{PACKAGES}}">here</a>
or via the <a href="{{SIMPLE}}">simple</a> index.</p>

<p>This instance is running version {{VERSION}} of the
  <a href="https://pypi.org/project/pypiserver/">pypiserver</a> software.</p>
</body></html>

2019-02-03 16:43:04,790|pypiserver.bottle|INFO|139854031225152|Bottle v0.13-dev server starting up (using AutoServer())...
2019-02-03 16:43:04,790|pypiserver.bottle|INFO|139854031225152|Listening on http://0.0.0.0:9090/
2019-02-03 16:43:04,790|pypiserver.bottle|INFO|139854031225152|Hit Ctrl-C to quit.
```

Indirectly (to be supplied):
```bash
poetry run pypiserver
```

With a local server running, you can publish and then search for the result:

```bash
$ poetry config repositories.xonshit http://localhost:9090/  # temporary, poetry bug?

$ poetry config repositories
{'xonshit': {'url': 'http://localhost:9090/'}}

$ poetry publish  --repository=xonshit --build                                                                                                                                                                               
Building xonshit (0.1.1)
 - Building sdist
 - Built xonshit-0.1.1.tar.gz

 - Building wheel
 - Built xonshit-0.1.1-py3-none-any.whl

Publishing xonshit (0.1.1) to xonshit
 - Uploading xonshit-0.1.1-py3-none-any.whl 100%
 - Uploading xonshit-0.1.1.tar.gz 100%
 
 $ pip search --index http://localhost:9090 xonshit                                                                                                                                                                           
xonshit (0.1.1)  - 0.1.1
```

Note that a local pypiserver isn't necessary. You can install `xonshit` directly from github with the "module name" `git+ssh://git@github.com/mcarifio/xonshit.git` (this borders on magical). 
This is a useful way to confirm that your last git commit (or any commit for that matter) can be installed. To do this, create a sacrificial virtualenv using the 
[venv](https://docs.python.org/3/library/venv.html) module:

```bash
$ mkdir /tmp/venv                                                                                                                                                                                                            
$ python -m venv /tmp/venv                                                                                                                                                                                                   
$ pushd /tmp/venv  ## simplifies inspecting the installed module xonshit
$ source bin/activiate  

(venv) $ pip install -U pip  ## the latest pip groks pyproject.toml. very useful.                                                                                                                                                                                                                      
Collecting pip
  Using cached https://files.pythonhosted.org/packages/46/dc/7fd5df840efb3e56c8b4f768793a237ec4ee59891959d6a215d63f727023/pip-19.0.1-py2.py3-none-any.whl
Installing collected packages: pip
  Found existing installation: pip 10.0.1
    Uninstalling pip-10.0.1:
      Successfully uninstalled pip-10.0.1
Successfully installed pip-19.0.1

$ pip install git+ssh://git@github.com/mcarifio/xonshit.git                                                                                                                                                                               
Collecting git+ssh://git@github.com/mcarifio/xonshit.git
  Cloning ssh://git@github.com/mcarifio/xonshit.git to /tmp/pip-req-build-2a2vgu6k
  Installing build dependencies ... done
  Getting requirements to build wheel ... done
  Installing backend dependencies ... done
    Preparing wheel metadata ... done
Collecting fire<0.2.0,>=0.1.3 (from xonshit==0.1.1)
Collecting pytest<5.0,>=4.1 (from xonshit==0.1.1)
  Using cached https://files.pythonhosted.org/packages/0d/c4/8093b4ffdde66628d4cb138d1d53726e2c21c23ac397cb75494e3f4310c9/pytest-4.2.0-py2.py3-none-any.whl
Collecting xonsh<0.9.0,>=0.8.9 (from xonshit==0.1.1)
  Using cached https://files.pythonhosted.org/packages/f6/fc/b417b1a49c2e1a53b5df016132b7957cb316e048416398574b4b5d41b1a2/xonsh-0.8.9.tar.gz
Collecting hypothesis<5.0,>=4.4 (from xonshit==0.1.1)
  Using cached https://files.pythonhosted.org/packages/a9/85/4e82b04126d75e7463c2d152528ef1e46fe8069b07d7e858433035bc8b29/hypothesis-4.5.0-py3-none-any.whl
Collecting prompt_toolkit<3.0,>=2.0 (from xonshit==0.1.1)
  Using cached https://files.pythonhosted.org/packages/65/c2/e676da701cda11b32ff42eceb44aa7d8934b597d604bb5e94c0283def064/prompt_toolkit-2.0.8-py3-none-any.whl
Collecting poetry<0.13.0,>=0.12.11 (from xonshit==0.1.1)
  Using cached https://files.pythonhosted.org/packages/64/2d/8221b951085667039cc45b4a9013f7cd4efd34f13dfcca04a90ed4046c72/poetry-0.12.11-py2.py3-none-any.whl
Collecting six (from fire<0.2.0,>=0.1.3->xonshit==0.1.1)
  Using cached https://files.pythonhosted.org/packages/73/fb/00a976f728d0d1fecfe898238ce23f502a721c0ac0ecfedb80e0d88c64e9/six-1.12.0-py2.py3-none-any.whl
Collecting py>=1.5.0 (from pytest<5.0,>=4.1->xonshit==0.1.1)
  Using cached https://files.pythonhosted.org/packages/3e/c7/3da685ef117d42ac8d71af525208759742dd235f8094221fdaafcd3dba8f/py-1.7.0-py2.py3-none-any.whl
Requirement already satisfied: setuptools in ./lib/python3.7/site-packages (from pytest<5.0,>=4.1->xonshit==0.1.1) (39.0.1)
Collecting pluggy>=0.7 (from pytest<5.0,>=4.1->xonshit==0.1.1)
  Using cached https://files.pythonhosted.org/packages/2d/60/f58d9e8197f911f9405bf7e02227b43a2acc2c2f1a8cbb1be5ecf6bfd0b8/pluggy-0.8.1-py2.py3-none-any.whl
Collecting more-itertools>=4.0.0 (from pytest<5.0,>=4.1->xonshit==0.1.1)
  Using cached https://files.pythonhosted.org/packages/a4/a6/42f17d065bda1fac255db13afc94c93dbfb64393eae37c749b4cb0752fc7/more_itertools-5.0.0-py3-none-any.whl
Collecting atomicwrites>=1.0 (from pytest<5.0,>=4.1->xonshit==0.1.1)
  Using cached https://files.pythonhosted.org/packages/52/90/6155aa926f43f2b2a22b01be7241be3bfd1ceaf7d0b3267213e8127d41f4/atomicwrites-1.3.0-py2.py3-none-any.whl
Collecting attrs>=17.4.0 (from pytest<5.0,>=4.1->xonshit==0.1.1)
  Using cached https://files.pythonhosted.org/packages/3a/e1/5f9023cc983f1a628a8c2fd051ad19e76ff7b142a0faf329336f9a62a514/attrs-18.2.0-py2.py3-none-any.whl
Collecting wcwidth (from prompt_toolkit<3.0,>=2.0->xonshit==0.1.1)
  Using cached https://files.pythonhosted.org/packages/7e/9f/526a6947247599b084ee5232e4f9190a38f398d7300d866af3ab571a5bfe/wcwidth-0.1.7-py2.py3-none-any.whl
Collecting jsonschema<4.0,>=3.0a3 (from poetry<0.13.0,>=0.12.11->xonshit==0.1.1)
  Using cached https://files.pythonhosted.org/packages/90/4f/2589f027887ec1daadcfd11e175bd808c8b0bac7f9a2796997cc45f6df78/jsonschema-3.0.0b3-py2.py3-none-any.whl
Collecting pkginfo<2.0,>=1.4 (from poetry<0.13.0,>=0.12.11->xonshit==0.1.1)
  Using cached https://files.pythonhosted.org/packages/e6/d5/451b913307b478c49eb29084916639dc53a88489b993530fed0a66bab8b9/pkginfo-1.5.0.1-py2.py3-none-any.whl
Collecting shellingham<2.0,>=1.1 (from poetry<0.13.0,>=0.12.11->xonshit==0.1.1)
  Using cached https://files.pythonhosted.org/packages/74/b7/36cdb13e9ecf1e9584cd78a47a1853831cf8817da3438aeec550cd83619c/shellingham-1.2.8-py2.py3-none-any.whl
Collecting cachy<0.3,>=0.2 (from poetry<0.13.0,>=0.12.11->xonshit==0.1.1)
  Using cached https://files.pythonhosted.org/packages/26/37/8ce3e7b330078b6797a34e79a80a8ad6935e404a3b903765417182c9ce19/cachy-0.2.0-py2.py3-none-any.whl
Collecting cachecontrol[filecache]<0.13.0,>=0.12.4 (from poetry<0.13.0,>=0.12.11->xonshit==0.1.1)
  Using cached https://files.pythonhosted.org/packages/5e/f0/2c193ed1f17c97ae539da7e1c2d48b80d8cccb1917163b26a91ca4355aa6/CacheControl-0.12.5.tar.gz
Collecting tomlkit<0.6.0,>=0.5.1 (from poetry<0.13.0,>=0.12.11->xonshit==0.1.1)
  Using cached https://files.pythonhosted.org/packages/71/c6/06c014b92cc48270765d6a9418d82239b158d8a9b69e031b0e2c6598740b/tomlkit-0.5.3-py2.py3-none-any.whl
Collecting pyparsing<3.0,>=2.2 (from poetry<0.13.0,>=0.12.11->xonshit==0.1.1)
  Using cached https://files.pythonhosted.org/packages/de/0a/001be530836743d8be6c2d85069f46fecf84ac6c18c7f5fb8125ee11d854/pyparsing-2.3.1-py2.py3-none-any.whl
Collecting cleo<0.7.0,>=0.6.7 (from poetry<0.13.0,>=0.12.11->xonshit==0.1.1)
  Using cached https://files.pythonhosted.org/packages/a7/b9/270301a3a87587f09bc3985973f2e362ffa45fa5fcd5128501516b2f5e31/cleo-0.6.8-py2.py3-none-any.whl
Collecting requests-toolbelt<0.9.0,>=0.8.0 (from poetry<0.13.0,>=0.12.11->xonshit==0.1.1)
  Using cached https://files.pythonhosted.org/packages/97/8a/d710f792d6f6ecc089c5e55b66e66c3f2f35516a1ede5a8f54c13350ffb0/requests_toolbelt-0.8.0-py2.py3-none-any.whl
Collecting pyrsistent<0.15.0,>=0.14.2 (from poetry<0.13.0,>=0.12.11->xonshit==0.1.1)
  Using cached https://files.pythonhosted.org/packages/45/5a/a1a446eba4b5bf9f823fd863605df24327e49241d6b5c43d82b429228caa/pyrsistent-0.14.9.tar.gz
Collecting requests<3.0,>=2.18 (from poetry<0.13.0,>=0.12.11->xonshit==0.1.1)
  Using cached https://files.pythonhosted.org/packages/7d/e3/20f3d364d6c8e5d2353c72a67778eb189176f08e873c9900e10c0287b84b/requests-2.21.0-py2.py3-none-any.whl
Collecting html5lib<2.0,>=1.0 (from poetry<0.13.0,>=0.12.11->xonshit==0.1.1)
  Using cached https://files.pythonhosted.org/packages/a5/62/bbd2be0e7943ec8504b517e62bab011b4946e1258842bc159e5dfde15b96/html5lib-1.0.1-py2.py3-none-any.whl
Collecting msgpack (from cachecontrol[filecache]<0.13.0,>=0.12.4->poetry<0.13.0,>=0.12.11->xonshit==0.1.1)
  Using cached https://files.pythonhosted.org/packages/a8/7b/630049fc4af9e68a625738612edc264ce7cb586c5001a2d4d2209a4f61c1/msgpack-0.6.1-cp37-cp37m-manylinux1_x86_64.whl
Collecting lockfile>=0.9 (from cachecontrol[filecache]<0.13.0,>=0.12.4->poetry<0.13.0,>=0.12.11->xonshit==0.1.1)
  Using cached https://files.pythonhosted.org/packages/c8/22/9460e311f340cb62d26a38c419b1381b8593b0bb6b5d1f056938b086d362/lockfile-0.12.2-py2.py3-none-any.whl
Collecting pylev<2.0,>=1.3 (from cleo<0.7.0,>=0.6.7->poetry<0.13.0,>=0.12.11->xonshit==0.1.1)
  Using cached https://files.pythonhosted.org/packages/40/1c/7dff1d242bf1e19f9c6202f0ba4e6fd18cc7ecb8bc85b17b2d16c806e228/pylev-1.3.0-py2.py3-none-any.whl
Collecting pastel<0.2.0,>=0.1.0 (from cleo<0.7.0,>=0.6.7->poetry<0.13.0,>=0.12.11->xonshit==0.1.1)
  Using cached https://files.pythonhosted.org/packages/9b/7e/7d701686013c0d7dae62e0977467232a6adc2e562c23878eb3cd4f97d02e/pastel-0.1.0-py3-none-any.whl
Collecting chardet<3.1.0,>=3.0.2 (from requests<3.0,>=2.18->poetry<0.13.0,>=0.12.11->xonshit==0.1.1)
  Using cached https://files.pythonhosted.org/packages/bc/a9/01ffebfb562e4274b6487b4bb1ddec7ca55ec7510b22e4c51f14098443b8/chardet-3.0.4-py2.py3-none-any.whl
Collecting idna<2.9,>=2.5 (from requests<3.0,>=2.18->poetry<0.13.0,>=0.12.11->xonshit==0.1.1)
  Using cached https://files.pythonhosted.org/packages/14/2c/cd551d81dbe15200be1cf41cd03869a46fe7226e7450af7a6545bfc474c9/idna-2.8-py2.py3-none-any.whl
Collecting certifi>=2017.4.17 (from requests<3.0,>=2.18->poetry<0.13.0,>=0.12.11->xonshit==0.1.1)
  Using cached https://files.pythonhosted.org/packages/9f/e0/accfc1b56b57e9750eba272e24c4dddeac86852c2bebd1236674d7887e8a/certifi-2018.11.29-py2.py3-none-any.whl
Collecting urllib3<1.25,>=1.21.1 (from requests<3.0,>=2.18->poetry<0.13.0,>=0.12.11->xonshit==0.1.1)
  Using cached https://files.pythonhosted.org/packages/62/00/ee1d7de624db8ba7090d1226aebefab96a2c71cd5cfa7629d6ad3f61b79e/urllib3-1.24.1-py2.py3-none-any.whl
Collecting webencodings (from html5lib<2.0,>=1.0->poetry<0.13.0,>=0.12.11->xonshit==0.1.1)
  Using cached https://files.pythonhosted.org/packages/f4/24/2a3e3df732393fed8b3ebf2ec078f05546de641fe1b667ee316ec1dcf3b7/webencodings-0.5.1-py2.py3-none-any.whl
Building wheels for collected packages: xonshit
  Building wheel for xonshit (PEP 517) ... done
  Stored in directory: /tmp/pip-ephem-wheel-cache-_z5otj7k/wheels/07/91/d6/a3bba3d6466cf616ba110890ce3ddca8a422fe3ddb3f63025f
Successfully built xonshit
Installing collected packages: six, fire, py, pluggy, more-itertools, atomicwrites, attrs, pytest, xonsh, hypothesis, wcwidth, prompt-toolkit, pyrsistent, jsonschema, pkginfo, shellingham, cachy, chardet, idna, certifi, urllib3, requests, msgpack, lockfile, cachecontrol, tomlkit, pyparsing, pylev, pastel, cleo, requests-toolbelt, webencodings, html5lib, poetry, xonshit
  Running setup.py install for xonsh ... done
  Running setup.py install for pyrsistent ... done
  Running setup.py install for cachecontrol ... done
Successfully installed atomicwrites-1.3.0 attrs-18.2.0 cachecontrol-0.12.5 cachy-0.2.0 certifi-2018.11.29 chardet-3.0.4 cleo-0.6.8 fire-0.1.3 html5lib-1.0.1 hypothesis-4.5.0 idna-2.8 jsonschema-3.0.0b3 lockfile-0.12.2 more-itertools-5.0.0 msgpack-0.6.1 pastel-0.1.0 pkginfo-1.5.0.1 pluggy-0.8.1 poetry-0.12.11 prompt-toolkit-2.0.8 py-1.7.0 pylev-1.3.0 pyparsing-2.3.1 pyrsistent-0.14.9 pytest-4.2.0 requests-2.21.0 requests-toolbelt-0.8.0 shellingham-1.2.8 six-1.12.0 tomlkit-0.5.3 urllib3-1.24.1 wcwidth-0.1.7 webencodings-0.5.1 xonsh-0.8.9 xonshit-0.1.1

$ python -m xonshit.runner testing                                                                                                                                                                    
=========================================================================================================================== test session starts ============================================================================================================================
platform linux -- Python 3.7.0, pytest-4.2.0, py-1.7.0, pluggy-0.8.1 -- /tmp/venv/bin/python
cachedir: .pytest_cache
hypothesis profile 'default' -> database=DirectoryBasedExampleDatabase('/tmp/venv/lib/python3.7/site-packages/xonshit/.hypothesis/examples')
rootdir: /tmp/venv/lib/python3.7/site-packages/xonshit, inifile: /tmp/venv/lib/python3.7/site-packages/xonshit/pytest.ini
plugins: xonsh-0.8.9, hypothesis-4.5.0
collected 1 item                                                                                                                                                                                                                                                           

testing/test_runner.py::runner_test PASSED                                                                                                                                                                                                                           [100%]

========================================================================================================================= 1 passed in 0.01 seconds =========================================================================================================================
0
``` 

