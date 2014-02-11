"""
Manage and display help messages.
"""

import widely
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


def _help(arguments):
    """
    Look up help messages.

    Usage:
    widely help <TOPIC>

    where <TOPIC> is one of the following:

    """
    help_messages = {
        'version': version.__doc__,
        'help': _help.__doc__,
        'auth:login': auth_login.__doc__,
        'login': auth_login.__doc__,
        'auth:logout': auth_logout.__doc__,
        'logout': auth_logout.__doc__,
        'auth:whoami': auth_whoami.__doc__,
        'domains': domains.__doc__,
        'local': local.__doc__,
        'logs': logs.__doc__,
        'open': _open.__doc__,
        'sites': sites.__doc__,
        'sites:create': sites_create.__doc__,
        'sites:info': sites_info.__doc__,
        'sites:delete': sites_delete.__doc__,
        'sites:copy': sites_copy.__doc__,
        'sites:rename': sites_rename.__doc__,
        'status': status.__doc__,
        'push': push.__doc__,
        'pull': pull.__doc__
    }
    topic = arguments['<TOPIC>']
    if topic and topic in help_messages:
        message = 'help about {0}\n'.format(topic)
        message += help_messages[topic]
        if topic == 'help':
            message += '\n    '.join(help_messages.keys())
        print(message)
    else:
        print(widely.__doc__.strip("\n"))
