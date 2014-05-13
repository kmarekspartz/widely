"""
Put the content from the local directory and put it in the remote bucket.
"""

from widely.bucket import get_current_bucket
from widely.diff import generate_diffs, show_diffs, run_diffs
from widely.util import get_y_or_n


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
        decision = get_y_or_n(
            'Would you like to make the changes in {0}?'.format(
                bucket.name
            )
        )
        if decision:
            run_diffs(diffs, bucket, local_changes=False)
    else:
        print('There are no changes to push.')
