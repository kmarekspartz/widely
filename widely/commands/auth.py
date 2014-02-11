"""
Manage the authorization tokens.
"""

import os
from ConfigParser import DuplicateSectionError, NoSectionError

import boto


def auth_login():
    """
    Saves user authentication data for AWS S3 using boto. This does not
    verify your credentials.

    Usage: widely auth:login
    """
    print('Enter your AWS credentials.')
    aws_access_key_id = raw_input('Access Key ID: ')
    aws_secret_access_key = raw_input('Secret Access Key ID: ')
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
    try:
        boto.config.remove_option('Credentials', 'aws_access_key_id')
        boto.config.remove_option('Credentials', 'aws_secret_access_key')
    except NoSectionError:
        pass
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


def get_credentials():
    """
    Returns current access_key and secret_access_key or asks the user to
    login.
    """
    try:
        aws_access_key_id = boto.config.get('Credentials',
                                            'aws_access_key_id')
        aws_secret_access_key = boto.config.get('Credentials',
                                                'aws_secret_access_key')
        assert aws_access_key_id is not None
        assert aws_secret_access_key is not None
    except AssertionError:
        print('No credentials found.')
        return auth_login()
    return aws_access_key_id, aws_secret_access_key
