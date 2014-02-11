"""
Opens a bucket in the webbrowser.
"""

import webbrowser

from widely.bucket import get_current_or_specified_bucket


def _open(arguments):
    """
    Loads the running specified or current site in the webbrowser.

    Usage: widely open [--site <SITENAME>]
    """
    bucket = get_current_or_specified_bucket(arguments)
    url = 'http://' + bucket.get_website_endpoint()
    print('Opening {0}...'.format(bucket.name)), # This line may not
    # be Python 3
    # compatible.
    webbrowser.open_new_tab(url)
    print('done')
