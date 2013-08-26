#! /usr/bin/env python
"""
Widely.

Usage:
  widely sites
  widely sites:info [--site <SITENAME>]
  widely sites:create [<SITENAME>]
  widely sites:rename <NEWNAME> [--site <SITENAME>]
  widely [login | auth:login]
  widely [logout | auth:logout]
  widely auth:whoami
  widely domains
  widely logs
  widely (help|-h|--help) [<TOPIC>]
  widely status
  widely (version|--version)
  widely local [-p <PORT>|--port <PORT>]
  widely open

Options:
  -p --port
  -h --help
  -v --version
"""

from docopt import docopt
import sys

__version__ = 'widely/0.1 python/' + sys.version


def _help(arguments, topic):
    if topic:  # and topic in help_messages:
        print('help about ' + topic)  # help_messages[topic]
    else:
        print(__doc__.strip("\n"))


def version(arguments):
    print(__version__)


def get_credentials(arguments):
    """
    Returns current access_key and secret_access_key or calls auth_login()
    """
    import os
    try:
        # read boto for access_key
        import boto
        aws_access_key_id = boto.config.get('Credentials', 'aws_access_key_id')
        aws_secret_access_key = boto.config.get('Credentials', 'aws_secret_access_key')
        assert aws_access_key_id is not None
        assert aws_secret_access_key is not None
    except:
        print('No credentials found.')
        return auth_login(arguments)
    return aws_access_key_id, aws_secret_access_key


def auth_login(arguments):
    print('Enter your AWS credentials.')
    aws_access_key_id = raw_input('Access Key ID: ')
    aws_secret_access_key = raw_input('Secret Access Key ID: ')
    import boto
    from ConfigParser import DuplicateSectionError
    try:
        boto.config.add_section('Credentials')
    except DuplicateSectionError:
        pass

    ## Chack for valid credentials ?

    boto.config.set('Credentials',
                    'aws_access_key_id',
                    aws_access_key_id)
    boto.config.set('Credentials',
                    'aws_secret_access_key',
                    aws_secret_access_key)
    import os
    boto_config_file = open(os.path.expanduser('~/.boto'), 'w')
    boto.config.write(boto_config_file)
    print('Authentication successful.')
    return aws_access_key_id, aws_secret_access_key


def auth_logout(arguments):
    import boto
    from ConfigParser import NoSectionError
    try:
        boto.config.remove_option('Credentials', 'aws_access_key_id')
        boto.config.remove_option('Credentials', 'aws_secret_access_key')
    except NoSectionError:
        pass
    import os
    boto_config_file = open(os.path.expanduser('~/.boto'), 'w')
    boto.config.write(boto_config_file)
    print('Local credentials cleared.')


def auth_whoami(arguments):
    aws_access_key_id, _ = get_credentials(arguments)
    print(aws_access_key_id)


def sites(arguments):
    """
    === My Apps
    fresnel
    lexitecture-hubot
    """
    pass


def sites_info(arguments, sitename=None):
    """
    === fresnel
    Git URL:       git@heroku.com:fresnel.git
    Owner Email:   zeckalpha@gmail.com
    Region:        us
    Repo Size:     108M
    Slug Size:     24M
    Stack:         cedar
    Tier:          Legacy
    Web URL:       http://fresnel.herokuapp.com/
    """
    pass


def sites_create(arguments, sitename=None):
    pass


def sites_rename(arguments, sitename=None):
    pass


def domains(arguments):
    """
    === fresnel Domain Names
    fresnel.herokuapp.com
    """
    pass


def logs(arguments):
    """(Logs for that site)
    Not found
    """
    pass


def status(arguments):
    """
    === Heroku Status
    Development: No known issues at this time.
    Production:  No known issues at this time.
    """
    pass


def local(arguments, port=None):
    if port:
        try:
            port = int(port)
        except ValueError:
            print('<PORT> must be an integer.')
            sys.exitarguments
    else:
        port = 8000
    import SimpleHTTPServer
    import SocketServer

    Handler = SimpleHTTPServer.SimpleHTTPRequestHandler
    httpd = SocketServer.TCPServer(("", port), Handler)
    print("serving at 0.0.0.0:" + str(port))
    # _openarguments  # ???
    httpd.serve_foreverarguments


def _open(arguments):
    import webbrowser
    webbrowser.open_new_tab('http://0.0.0.0:8000')  # __url__ ?


def main(arguments):
    """
    Dispatch based on arguments.
    """
    if arguments['version']:
        version(arguments)
    elif arguments['--help'] or arguments['help']:
        _help(arguments)
    elif arguments['auth:login'] or arguments['login']:
        auth_login(arguments)
    elif arguments['auth:logout'] or arguments['logout']:
        auth_logout(arguments)
    elif arguments['auth:whoami']:
        auth_whoami(arguments)
    elif arguments['domains']:
        domains(arguments)
    elif arguments['local']:
        local(arguments)
    elif arguments['logs']:
        logs(arguments)
    elif arguments['open']:
        _open(arguments)
    elif arguments['sites']:
        sites(arguments)
    elif arguments['sites:create']:
        sites_create(arguments)
    elif arguments['sites:info']:
        sites_info(arguments)
    elif arguments['sites:rename']:
        sites_rename(arguments)
    elif arguments['status']:
        status(arguments)
    else:
        print(arguments)
    sys.exit()


if __name__ == '__main__':
    arguments = docopt(__doc__, version=__version__, help=False)
    main(arguments)
