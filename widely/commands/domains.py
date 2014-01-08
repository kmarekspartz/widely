from widely.bucket import get_current_or_specified_bucket


def domains(arguments):
    """
    Displays a list of domains for the current or specified sitename.

    Usage: widely domains [--site <SITENAME>]
    """
    bucket = get_current_or_specified_bucket(arguments)
    print('=== {0} Domain Names'.format(bucket.name))
    print(bucket.get_website_endpoint())
