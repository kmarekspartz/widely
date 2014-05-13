"""
Helper functions not widely specific.
"""


def get_y_or_n(message=None):
    """
    Asks the user whether to proceed.
    """
    if not message:
        message = "Continue? (y/n)"
    while True:
        response = raw_input(message + ' ')
        if response in set(['y', 'Y', 'Yes', 'yes']):
            return True
        elif response in set(['n', 'N', 'No', 'no']):
            return False
        print('Please enter y/n.')
