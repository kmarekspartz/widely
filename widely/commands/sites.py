"""
Work with sites, which are abstracted S3 buckets.
"""

import sys
import os.path

from boto.s3.connection import S3Connection
from boto.exception import S3CreateError

from widely.commands.push import push
from widely.bucket import get_buckets, websites_from_buckets, \
    get_current_or_specified_bucket, get_current_bucket, \
    get_specified_bucket, readable_bucket_size


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
    print('Size:    {0}'.format(readable_bucket_size(bucket)))
    print('Web URL: {0}'.format(bucket.get_website_endpoint()))


def sites_create(arguments):
    """
    Creates a new site for the specified sitename.

    Usage: widely sites:create <SITENAME>
    """
    ## Randomly assigned site names.
    # make sure there is no .widely file locally

    if os.path.exists('.widely'):
        print('This directory is already a widely site.')
        sys.exit(1)
    sitename = arguments['<SITENAME>']
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
    sites_create(arguments)
    new_bucket = get_specified_bucket(new_bucket_name)
    for key in current_bucket.get_all_keys():
        new_bucket.copy_key(key.name, current_bucket.name, key.name)
    print('{0} copied to {1}'.format(current_bucket.name, new_bucket_name))


def sites_rename(arguments):
    """
    Renames the site in the current directory to the new sitename.

    Usage: widely sites:rename <SITENAME>
    """
    sites_copy(arguments)
    new_sitename = arguments['<SITENAME>']
    bucket = get_current_bucket()

    decision = None
    while True:
        # Verify the deletion of the old sitename
        response = raw_input(
            'Would you like to delete {0}? '.format(bucket.name)
        )
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
        bucket.delete_keys(bucket.get_all_keys())
        bucket.delete()


def sites_delete(arguments):
    """
    Deletes specified bucket from AWS S3.

    Usage: widely sites:delete <SITENAME>
    """
    bucket = get_specified_bucket(arguments['<SITENAME>'])
    bucket.delete_keys(bucket.get_all_keys())
    bucket.delete()
    print('{0} is deleted'.format(bucket.name))
