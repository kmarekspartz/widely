#! /usr/bin/env python
"""
Widely.

Usage:
  widely [login | auth:login]
  widely [logout | auth:logout]
  widely auth:whoami
  widely sites
  widely sites:info [--site <SITENAME>]
  widely sites:create [<SITENAME>]
  widely sites:rename <NEWNAME> [--site <SITENAME>]
  widely domains [--site <SITENAME>]
  widely open
  widely local [-p <PORT>|--port <PORT>]
  widely status
  widely logs
  widely (help|-h|--help) [<TOPIC>]
  widely (version|--version)

Options:
  -p --port
  -h --help
  -v --version
"""

from docopt import docopt
import sys

__version__ = 'widely/0.1 python/' + sys.version


def sizeof_fmt(num):
    """
    Formats number of bytes into a human readable form.

    From: http://stackoverflow.com/questions/1094841/reusable-library-to-get-human-readable-version-of-file-size
    """
    for x in ['bytes','KB','MB','GB']:
        if -1024.0 < num < 1024.0:
            return "%3.1f %s" % (num, x)
        num /= 1024.0
    return "%3.1f %s" % (num, 'TB')


def _help(arguments):
    topic = arguments['<TOPIC>']
    help_messages = {}
    if topic and topic in help_messages:
        print('help about ' + topic)
        print(help_messages[topic])
    else:
        print(__doc__.strip("\n"))


def version(arguments):
    print(__version__)


def get_credentials(arguments):
    """
    Returns current access_key and secret_access_key or calls auth_login()
    """
    try:
        import boto
        aws_access_key_id = boto.config.get('Credentials', 'aws_access_key_id')
        aws_secret_access_key = boto.config.get('Credentials', 'aws_secret_access_key')
        assert aws_access_key_id is not None
        assert aws_secret_access_key is not None
    except AssertionError:
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

    ## Check for valid credentials ?

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


def get_buckets():
    ## if not logged in, login

    from boto.s3.connection import S3Connection
    conn = S3Connection()
    buckets = conn.get_all_buckets()
    return buckets


class NoSuchBucket(Exception):
    pass


class NoWidelyDotfile(Exception):
    pass


def get_specified_bucket(sitename):
    from boto.s3.connection import S3Connection
    conn = S3Connection()
    from boto.exception import S3ResponseError
    try:
        bucket = conn.get_bucket(sitename)
        bucket.get_website_configuration()
    except S3ResponseError:
        raise NoSuchBucket
    return bucket


def get_current_bucket():
    try:
        sitename = open('.widely', 'r').read()
    except IOError:
        raise NoWidelyDotfile
    return get_specified_bucket(sitename)


def get_current_or_specified_bucket(arguments):
    try:
        sitename = arguments['<SITENAME>']
        if sitename:
            return get_specified_bucket(sitename)
        else:
            return get_current_bucket()
    except NoSuchBucket:
        print(' !\tSite not found')
        sys.exit()
    except NoWidelyDotfile:
        print(' !\tNo site specified.')
        print(' !\tRun this command from a site folder or specify which site to use with --site SITENAME.')
        sys.exit()


def websites_from_buckets(buckets):
    from boto.exception import S3ResponseError
    for bucket in buckets:
        try:
            bucket.get_website_configuration()
            yield bucket
        except S3ResponseError:
            continue


def bucket_size(bucket):
    """
    Return the number of bytes in a bucket.
    """
    return sum(map(lambda x: x.size, bucket.get_all_keys()))


def sites(arguments):
    """
    Displays sites, which are simply the set of buckets which are web sites.
    """
    buckets = get_buckets()
    websites = websites_from_buckets(buckets)
    print('=== My sites')
    for site in websites:
        print(site.name)


def sites_info(arguments):
    """
    Displays detailed information about the current or specified site.
    """
    bucket = get_current_or_specified_bucket(arguments)
    print('=== {0}'.format(bucket.name))
    print('Owner:   {0}'.format(bucket.get_acl().owner.display_name))
    print('Size:    {0}'.format(sizeof_fmt(bucket_size(bucket))))
    print('Web URL: {0}'.format(bucket.get_website_endpoint()))


def sites_create(arguments):
    """
    Creates a new site for the specified or current site, or a randomly assigned site name.
    """
    f = open('.widely', 'w')


def sites_rename(arguments):
    """
    Renames the specified or current site to the new name.
    """
    # Create a new bucket with the new name
    # Copy the configuration over
    # Change the .widely
    # Verify the deletion of the old sitename
    pass


def domains(arguments):
    """
    Lists domains for the specified or current site.
    """
    bucket = get_current_or_specified_bucket(arguments)
    print('=== {0} Domain Names'.format(bucket.name))
    print(bucket.get_website_endpoint())


def logs(arguments):
    """
    Shows access and status logs for the specified or current site.
    """
    # (Logs for sitename)
    # Not found
    pass


def status(arguments):
    """
    Shows the S3 system status.
    """
    import feedparser
    from prettytable import PrettyTable
    s3_status_rss_feeds = {
        "N. California": "http://status.aws.amazon.com/rss/s3-us-west-1.rss",
        "Oregon": "http://status.aws.amazon.com/rss/s3-us-west-2.rss",
        "US Standard": "http://status.aws.amazon.com/rss/s3-us-standard.rss",
        "Sao Paulo": "http://status.aws.amazon.com/rss/s3-sa-east-1.rss",
        "Ireland": "http://status.aws.amazon.com/rss/s3-eu-west-1.rss",
        "Singapore": "http://status.aws.amazon.com/rss/s3-ap-southeast-1.rss",
        "Sydney": "http://status.aws.amazon.com/rss/s3-ap-southeast-2.rss",
        "Tokyo": "http://status.aws.amazon.com/rss/s3-ap-northeast-1.rss"
    }
    print('=== S3 Status')
    table = PrettyTable(['Region', 'Status'])
    for region_name, rss_url in s3_status_rss_feeds.iteritems():
        d = feedparser.parse(rss_url)
        if d.entries:
            status = d.entries[0].title
        else:
            status = 'Unknown.'
        table.add_row([region_name, status])
    print(table)


def local(arguments):
    """
    Runs the site in a local server, on the specified port if there is one.
    """
    port = arguments['<PORT>']
    if port:
        try:
            port = int(port)
        except ValueError:
            print('<PORT> must be an integer.')
            sys.exit()
    else:
        port = 8000
    import SimpleHTTPServer
    import SocketServer

    Handler = SimpleHTTPServer.SimpleHTTPRequestHandler
    httpd = SocketServer.TCPServer(("", port), Handler)
    print("serving at 0.0.0.0:" + str(port))
    import webbrowser
    webbrowser.open_new_tab('http://0.0.0.0:' + str(port))
    httpd.serve_forever()




def _open(arguments):
    """
    Loads the running specified or current site in the webbrowser.
    """
    import webbrowser
    url = 'someurl'
    webbrowser.open_new_tab(url)


def main():
    """
    Dispatch based on arguments.
    """
    arguments = docopt(__doc__, version=__version__, help=False)
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
        print('We did not recognize your specified arguments.')
        print(arguments)
    sys.exit()


if __name__ == '__main__':
    main()
