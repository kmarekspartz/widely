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
  widely (version | --version)

Options:
  -p --port
  -h --help
  -v --version
"""

import sys

from docopt import docopt

__version__ = 0.8

version_string = ''.join([
    'widely/',
    str(__version__),
    ' python/',
    sys.version
])


def sizeof_fmt(num):
    """
    Formats number of bytes into a human readable form.

    From:
    http://stackoverflow.com/questions/1094841/reusable-library-to-get-human-readable-version-of-file-size
    """
    for x in ['bytes', 'KB', 'MB', 'GB']:
        if -1024.0 < num < 1024.0:
            return "%3.1f %s" % (num, x)
        num /= 1024.0
    return "%3.1f %s" % (num, 'TB')


def version():
    """
    Displays current versions of Widely and Python.

    Usage: widely version
    """
    print(version_string)


def get_credentials():
    """
    Returns current access_key and secret_access_key or asks the user to login.
    """
    try:
        import boto

        aws_access_key_id = boto.config.get('Credentials', 'aws_access_key_id')
        aws_secret_access_key = boto.config.get('Credentials',
                                                'aws_secret_access_key')
        assert aws_access_key_id is not None
        assert aws_secret_access_key is not None
    except AssertionError:
        print('No credentials found.')
        return auth_login()
    return aws_access_key_id, aws_secret_access_key


def auth_login():
    """
    Saves user authentication data for AWS S3 using boto. This does not
    verify your credentials.

    Usage: widely auth:login
    """
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


def auth_logout():
    """
    Clears any locally stored authentication data from boto's config
    for AWS S3.

    Usage: widely auth:logout
    """
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


def auth_whoami():
    """
    Displays locally stored access key.

    Usage: widely auth:whoami
    """
    aws_access_key_id, _ = get_credentials()
    print(aws_access_key_id)


def get_buckets():
    """
    Returns a list of all accessible buckets.
    """
    ## if not logged in, login
    from boto.s3.connection import S3Connection

    conn = S3Connection()
    buckets = conn.get_all_buckets()
    return buckets


class NoSuchBucket(Exception):
    """
    Raised when there is no bucket for the specified sitename.
    """
    pass


class NoWidelyDotfile(Exception):
    """
    Raised when there is no .widely in the current directory.
    """
    pass


def get_specified_bucket(sitename):
    """
    Returns the bucket for the specified sitename.
    """
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
    """
    Returns the bucket associated with the current directory, if it is
    a widely directory.
    """
    try:
        sitename = open('.widely', 'r').read().split()[0]
    except IOError:
        raise NoWidelyDotfile
    return get_specified_bucket(sitename)


def get_current_or_specified_bucket(arguments):
    """
    Returns a bucket. If one was specified and it exists, it is that
    one, otherwise, it is the current directory's bucket if it exists.
    """
    sitename = get_current_or_specified_sitename(arguments)
    try:
        return get_specified_bucket(sitename)
    except NoSuchBucket:
        print(' !\tSite not found')
        sys.exit()


def get_current_or_specified_sitename(arguments):
    """
    Returns the bucket name/sitename from the arguments if there was
    one specified, otherwise from the .widely if it exists.
    """
    sitename = arguments['<SITENAME>']
    if sitename:
        return sitename
    else:
        try:
            with open('.widely', 'r') as f:
                return f.read().split()[0]
        except IOError:
            print(' !\tNo site specified.')
            print(" !\tRun this command from a site folder or specify which "
                  "site to use with --site SITENAME.")
            sys.exit()


def websites_from_buckets(buckets):
    """
    Filter a list of buckets into only those which are configured to
    be a website.
    """
    from boto.exception import S3ResponseError

    for bucket in buckets:
        try:
            bucket.get_website_configuration()
            yield bucket
        except S3ResponseError:
            continue


def bucket_size(bucket):
    """
    Returns the total number of bytes in a bucket.
    """
    return sum(map(lambda x: x.size, bucket.get_all_keys()))


def sites():
    """
    Displays sites, which are simply the set of buckets which are web sites.

    Usage: widely sites
    """
    buckets = get_buckets()
    websites = websites_from_buckets(buckets)
    print('=== My sites')
    for site in websites:
        print(site.name)


def sites_info(arguments):
    """
    Displays detailed information about the current or specified sitename.

    Usage: widely sites:info [--site <SITENAME>]

    """
    bucket = get_current_or_specified_bucket(arguments)
    print('=== {0}'.format(bucket.name))
    print('Owner:   {0}'.format(bucket.get_acl().owner.display_name))
    print('Size:    {0}'.format(sizeof_fmt(bucket_size(bucket))))
    print('Web URL: {0}'.format(bucket.get_website_endpoint()))


def status():
    """
    Displays AWS S3 status.

    Usage: widely status
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
    Runs the site in a local server on port 8000 or specified port.

    Usage: widely local [-p <PORT> | --port <PORT>]
    """
    ## is there any way to stop this damn thing from running? After spinning a
    ## server on default port 5000 and killing with keyboard interrupt; I
    ## burned that port for a good 30 seconds. Not sure why you would start
    ## stop and restart several times in a row, but it's not possible without
    ## changing port numbers.
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
    url = 'http://0.0.0.0:' + str(port)
    print("serving at " + url)
    import webbrowser

    webbrowser.open_new_tab(url)
    httpd.serve_forever()


def _open(arguments):
    """
    Loads the running specified or current site in the webbrowser.

    Usage: widely open [--site <SITENAME>]
    """
    bucket = get_current_or_specified_bucket(arguments)
    url = 'http://' + bucket.get_website_endpoint()
    print('Opening {0}...'.format(bucket.name)),  # This line may not
                                                  # be Python 3
                                                  # compatible.
    import webbrowser

    webbrowser.open_new_tab(url)
    print('done')


def domains(arguments):
    """
    Displays a list of domains for the current or specified sitename.

    Usage: widely domains [--site <SITENAME>]
    """
    bucket = get_current_or_specified_bucket(arguments)
    print('=== {0} Domain Names'.format(bucket.name))
    print(bucket.get_website_endpoint())


def sites_create(arguments):
    """
    Creates a new site for the specified sitename.

    Usage: widely sites:create <SITENAME>
    """
    ## Randomly assigned site names.
    # make sure there is no .widely file locally
    import os.path

    if os.path.exists('.widely'):
        print('This directory is already a widely site.')
        sys.exit()
    sitename = arguments['<SITENAME>']
    from boto.s3.connection import S3Connection
    from boto.exception import S3CreateError

    conn = S3Connection()
    try:
        bucket = conn.create_bucket(sitename)
        assert bucket.get_all_keys() == []
        # Set bucket configuration
        error_key = raw_input(
            'Please enter the key of your 404 page (default: 404.html): ')
        if not error_key:
            error_key = '404.html'
        bucket.configure_website(
            suffix='index.html',
            error_key=error_key
        )
        # Configure policy
        ## Ask user first?
        bucket.set_acl('public-read')
        ## Configure logging
        with open('.widely', 'w') as f:
            f.write(sitename)
        return push()
    except S3CreateError:
        print('A site with that name already exists.')
        sys.exit()
    except AssertionError:
        print('This bucket already has keys.')
        sys.exit()


def sites_copy(arguments):
    """
    Copies the site in the current directory to the new sitename.

    Usage: widely sites:copy <SITENAME>
    """
    current_bucket = get_current_bucket()
    new_bucket_name = arguments['<SITENAME>']
    try:
        assert current_bucket.name != new_bucket_name
    except AssertionError:
        print('Cannot rename current bucket to current bucket.')
        sys.exit()
    from boto.s3.connection import S3Connection
    from boto.exception import S3CreateError

    conn = S3Connection()
    try:
        # make sure there is no bucket with the name
        new_bucket = conn.create_bucket(new_bucket_name)
        # Make sure the new bucket is empty
        assert new_bucket.get_all_keys() == []
        error_key = raw_input(
            'Please enter the key of your 404 page (default: 404.html): ')
        if not error_key:
            error_key = '404.html'
        new_bucket.configure_website(
            suffix='index.html',
            error_key=error_key
        )
        # Configure policy
        ## Ask user first?
        new_bucket.set_acl('public-read')
        # Copy the keys over
        for key in current_bucket.get_all_keys():
            new_bucket.copy_key(key.name, current_bucket.name, key.name)
        print('{0} copied to {1}'.format(current_bucket.name, new_bucket_name))
    except S3CreateError:
        print('A site with that name already exists')
        sys.exit()
    except AssertionError:
        print('This bucket already has keys.')
        sys.exit()


def sites_rename(arguments):
    """
    Renames the site in the current directory to the new sitename.

    Usage: widely sites:rename <SITENAME>
    """
    sites_copy(arguments)
    new_sitename = arguments['<SITENAME>']
    b = get_current_bucket()

    decision = None
    while True:
        # Verify the deletion of the old sitename
        response = raw_input('Would you like to delete {0}? '.format(b.name))
        if response in set(['y', 'Y', 'Yes', 'yes']):
            decision = True
            break
        elif response in set(['n', 'N', 'No', 'no']):
            decision = False
            break
        print('Please enter y/n.')

    if decision:
        # Update the .widely to the new sitename
        with open('.widely', 'w') as f:
            f.write(new_sitename)
        b.delete_keys(b.get_all_keys())
        b.delete()

def sites_delete(arguments):
    """
    Deletes specified bucket from AWS S3.
    
    Usage: widely sites:delete <SITENAME>
    """
    b = get_specified_bucket(arguments['<SITENAME>'])
    b.delete_keys(b.get_all_keys())
    b.delete()
    print('{0} is deleted'.format(b.name))

def push():
    """
    Pushes local content to AWS S3 for publication.

    Usage: widely push
    """
    bucket = get_current_bucket()
    diffs = generate_diffs(bucket)
    if diffs: 
        show_diffs(diffs)
        # Ask for approval
        decision = None
        while True:
            # Verify the deletion of the old sitename
            response = raw_input(
                'Would you like to make the changes in {0}? '.format(bucket.name))
            if response in set(['y', 'Y', 'Yes', 'yes']):
                decision = True
                break
            elif response in set(['n', 'N', 'No', 'no']):
                decision = False
                break
            print('Please enter y/n.')

        if decision:
            run_diffs(diffs, bucket, local_changes=False)
    else:
        print('There are no changes to push.')


def pull(arguments):
    """
    Pulls content associated with the specified sitename from AWS S3
    to the current directory.

    Usage: widely pull --site <SITENAME>
    """
    sitename = get_current_or_specified_sitename(arguments)
    bucket = get_current_or_specified_bucket(arguments)
    diffs = generate_diffs(bucket)
    if diffs:
        show_diffs(diffs)
        # Ask for approval
        decision = None
        while True:
            # Verify the deletion of the old sitename
            response = raw_input('Would you like to make the changes locally? ')
            if response in set(['y', 'Y', 'Yes', 'yes']):
                decision = True
                break
            elif response in set(['n', 'N', 'No', 'no']):
                decision = False
                break
            print('Please enter y/n.')

        if decision:
            run_diffs(diffs, bucket, local_changes=True)
            # Set the .widely file (or create it) with the bucket name
            with open('.widely', 'w') as f:
                f.write(sitename)
    else:
        print('There are no changes to pull.')


def logs(arguments):
    """
    Displays access and status logs for the current site or specified sitename.

    Usage: widely logs [--site <SITENAME>]
    """
    bucket = get_current_or_specified_bucket(arguments)
    print('Logs for {0}'.format(bucket.name))
    ## Get the logs
    ## Reformat them (in chronological order)
    ## Print them
    print('Sorry, this is not yet implemented!')


class Diff(object):
    """
    Diff class. Diff is used to track changes between current
    directory and AWS S3.
    """
    NotRemote = 'NotRemote'
    NotLocal = 'NotLocal'
    Modified = 'Modified'


def generate_diffs(bucket):
    """
    Returns a list of diffs or changes between current directory and AWS S3.
    """
    ## Use difflib?
    ## Don't use MD5!
    from glob import glob
    import hashlib
    import os

    ignored = set(['.widely', '.widelyignore'])

    try:
        with open('.widelyignore', 'r') as f:
            _ignored = map(glob, f.read().splitlines())
            specified_ignored = set(item
                                    for sublist in _ignored
                                    for item in sublist)
            ignored = ignored | specified_ignored
    except IOError:
        pass

    def get_local_keys():
        """
        Walk the current directory, recursively yielding the paths and
        hashes for each non-ignored file.
        """
        for root, _, files in os.walk(os.curdir):
            for _file in files:
                path = os.path.join(root, _file)[2:]
                if path not in ignored:
                    with open(path, 'r') as f:
                        yield path, '"' + hashlib.md5(f.read()).hexdigest() + '"'

    def get_remote_keys():
        """
        Gets the list of keys and hashes from the bucket.
        """
        remote_keys = bucket.get_all_keys()
        for key in remote_keys:
            yield key.name, key.etag

    local_keys = dict(get_local_keys())
    remote_keys = dict(get_remote_keys())

    diffs = list()

    for key in local_keys:
        if os.path.isdir(key):
            continue
        if key in remote_keys:
            # The file is in both places
            if local_keys[key] == remote_keys[key]:
                continue
            else:
                diffs.append((Diff.Modified, key))
        else:
            # The file is local but not remote.
            diffs.append((Diff.NotRemote, key))
    for key in remote_keys:
        if key not in local_keys:
            # The file is remote but not local.
            diffs.append((Diff.NotLocal, key))

    return diffs


def show_diffs(diffs):
    """
    Prints a table of diffs.
    """
    from prettytable import PrettyTable

    print('This would make the following changes:')
    table = PrettyTable(['Diff', 'Key'])
    for diff, key in diffs:
        table.add_row([diff, key])
    print(table)


def run_diffs(diffs, bucket, local_changes=None):
    """
    Takes diffs and makes the necessary changes, either pushing or
    pulling files.
    """
    if type(local_changes) is not bool:
        raise ValueError('local_changes must be set to a bool')
    import os
    if local_changes:
        for diff, key in diffs:
            if diff == Diff.NotRemote:
                # Delete local file
                os.remove(key)
            elif diff == Diff.NotLocal or diff == Diff.Modified:
                # Pull remote file
                with open(key, 'w') as f:
                    bucket.get_key(key).get_contents_to_file(f)
    else:
        # Remote changes
        for diff, key in diffs:
            if diff == Diff.NotRemote or diff == Diff.Modified:
                # Push local file
                with open(key, 'r') as f:
                    k = bucket.new_key(key)
                    k.set_contents_from_file(f)
                    k.make_public()
            elif diff == Diff.NotLocal:
                # Delete remote file
                bucket.get_key(key).delete()


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
        print(__doc__.strip("\n"))


def main():
    """
    Dispatch based on arguments.
    """
    arguments = docopt(__doc__, version=version_string, help=False)
    if arguments['version']:
        version()
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
    sys.exit()


if __name__ == '__main__':
    main()
