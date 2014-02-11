"""
Helper methods for working with S3 buckets.
"""

import sys

from boto.s3.connection import S3Connection
from boto.exception import S3ResponseError


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


def get_buckets():
    """
    Returns a list of all accessible buckets.
    """
    ## if not logged in, login
    conn = S3Connection()
    buckets = conn.get_all_buckets()
    return buckets


def get_specified_bucket(sitename):
    """
    Returns the bucket for the specified sitename.
    """

    conn = S3Connection()

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
        sys.exit(1)


def websites_from_buckets(buckets):
    """
    Filter a list of buckets into only those which are configured to
    be a website.
    """
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
    return sum(key.size for key in bucket.get_all_keys())


def readable_bucket_size(bucket):
    """
    Returns the number of bytes in a bucket in a human readable form.
    """
    return sizeof_fmt(bucket_size(bucket))


def sizeof_fmt(num):
    """
    Formats number of bytes into a human readable form.

    From:
    """
    for size in ['bytes', 'KB', 'MB', 'GB']:
        if -1024.0 < num < 1024.0:
            return "%3.1f %s" % (num, size)
        num /= 1024.0
    return "%3.1f %s" % (num, 'TB')


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
            sys.exit(1)
