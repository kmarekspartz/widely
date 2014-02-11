#! /usr/bin/env python
"""
Widely.

Usage:
  widely (help | -h | --help) [<TOPIC>]
  widely [login | auth:login]
  widely [logout | auth:logout]
  widely auth:whoami
  widely sites
  widely sites:info [--site <SITENAME>]
  widely sites:create <SITENAME>
  widely sites:copy <SITENAME>
  widely sites:rename <SITENAME>
  widely sites:delete <SITENAME>
  widely domains [--site <SITENAME>]
  widely local [-p <PORT> | --port <PORT>]
  widely push
  widely pull --site <SITENAME>
  widely open [--site <SITENAME>]
  widely status
  widely logs [--site <SITENAME>]
  widely (version | -v | --version)

Options:
  -p --port
  -h --help
  -v --version
"""

import sys
import pkg_resources

from docopt import docopt

from widely.commands.help import _help
from widely.commands.push import push
from widely.commands.pull import pull
from widely.commands.status import status
from widely.commands.sites import sites, sites_create, sites_info, \
    sites_delete, sites_rename, sites_copy
from widely.commands.local import local
from widely.commands.logs import logs
from widely.commands.version import version
from widely.commands.auth import auth_login, auth_logout, auth_whoami
from widely.commands.domains import domains
from widely.commands.open import _open


def main():
    """
    Dispatch based on arguments.

    """
    version_string = ''.join([
        'widely/',
        str(pkg_resources.require('widely')[0].version),
        ' python/',
        sys.version
    ])

    arguments = docopt(__doc__, version=version_string, help=False)
    if arguments['version']:
        version(version_string)
    elif arguments['--help'] or arguments['help']:
        _help(arguments)
    elif arguments['auth:login'] or arguments['login']:
        auth_login()
    elif arguments['auth:logout'] or arguments['logout']:
        auth_logout()
    elif arguments['auth:whoami']:
        auth_whoami()
    elif arguments['domains']:
        domains(arguments)
    elif arguments['local']:
        local(arguments)
    elif arguments['logs']:
        logs(arguments)
    elif arguments['open']:
        _open(arguments)
    elif arguments['sites']:
        sites()
    elif arguments['sites:create']:
        sites_create(arguments)
    elif arguments['sites:info']:
        sites_info(arguments)
    elif arguments['sites:rename']:
        sites_rename(arguments)
    elif arguments['sites:copy']:
        sites_copy(arguments)
    elif arguments['sites:delete']:
        sites_delete(arguments)
    elif arguments['status']:
        status()
    elif arguments['push']:
        push()
    elif arguments['pull']:
        pull(arguments)
    else:
        print('We did not recognize your specified arguments.')
        _help(arguments)
        sys.exit(2)
    sys.exit()


if __name__ == '__main__':
    main()
