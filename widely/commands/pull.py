"""
Get the content from the specified bucket and put it in the local directory.
"""

from widely.bucket import get_current_or_specified_bucket, \
    get_current_or_specified_sitename
from widely.diff import generate_diffs, show_diffs, run_diffs
from widely.util import get_y_or_n


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
        if get_y_or_n("Would you like to make the changes locally?"):
            run_diffs(diffs, bucket, local_changes=True)
            # Set the .widely file (or create it) with the bucket name
            with open('.widely', 'w') as f:
                f.write(sitename)
    else:
        print('There are no changes to pull.')
