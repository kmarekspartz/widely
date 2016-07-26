"""
Helper functions not widely specific.
"""

from __future__ import print_function


YES_RESPONSES = set(['y', 'Y', 'Yes', 'yes'])
NO_RESPONSES = set(['n', 'N', 'No', 'no'])

def get_y_or_n(message=None, input=raw_input, output=print):
    """
    Asks the user whether to proceed.
    """
    if not message:
        message = "Continue? (y/n)"
    while True:
        response = input(message + ' ')
        if response in YES_RESPONSES:
            return True
        elif response in NO_RESPONSES:
            return False
        output('Please enter y/n.')

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
