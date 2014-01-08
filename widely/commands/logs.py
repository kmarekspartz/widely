from widely.bucket import get_current_or_specified_bucket


def logs(arguments):
    """
    Displays access and status logs for the current site or specified
    sitename.

    Usage: widely logs [--site <SITENAME>]
    """
    bucket = get_current_or_specified_bucket(arguments)
    print('Logs for {0}'.format(bucket.name))
    ## Get the logs
    ## Reformat them (in chronological order)
    ## Print them
    print('Sorry, this is not yet implemented!')
