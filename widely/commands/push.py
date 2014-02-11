"""
Put the content from the local directory and put it in the remote bucket.
"""

from widely.bucket import get_current_bucket
from widely.diff import generate_diffs, show_diffs, run_diffs


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
                'Would you like to make the changes in {0}? '.format(
                    bucket.name))
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
