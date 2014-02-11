"""
Diffs are used to compare and reconcile local and remote data.
"""

from glob import glob
import hashlib
import os
from prettytable import PrettyTable


class Diff(object):
    """
    Diff class. Diff is used to track changes between current
    directory and AWS S3.
    """
    NotRemote = 'NotRemote'
    NotLocal = 'NotLocal'
    Modified = 'Modified'


def generate_diffs(bucket):
    """
    Returns a list of diffs or changes between current directory and AWS S3.
    """
    ## Use difflib?
    ## Don't use MD5!
    ignored = set(['.widely', '.widelyignore'])

    try:
        with open('.widelyignore', 'r') as f:
            _ignored = [glob(line) for line in f.read().splitlines()]
            specified_ignored = set(item
                                    for sublist in _ignored
                                    for item in sublist)
            ignored = ignored | specified_ignored
    except IOError:
        pass

    def get_local_keys():
        """
        Walk the current directory, recursively yielding the paths and
        hashes for each non-ignored file.
        """
        for root, _, files in os.walk(os.curdir):
            for _file in files:
                path = os.path.join(root, _file)[2:]
                if path not in ignored:
                    with open(path, 'r') as f:
                        yield path, '"' + hashlib.md5(
                            f.read()).hexdigest() + '"'

    def get_remote_keys():
        """
        Gets the list of keys and hashes from the bucket.
        """
        remote_keys = bucket.get_all_keys()
        for key in remote_keys:
            yield key.name, key.etag

    local_keys = dict(get_local_keys())
    remote_keys = dict(get_remote_keys())

    diffs = list()

    for key in local_keys:
        if os.path.isdir(key):
            continue
        if key in remote_keys:
            # The file is in both places
            if local_keys[key] == remote_keys[key]:
                continue
            else:
                diffs.append((Diff.Modified, key))
        else:
            # The file is local but not remote.
            diffs.append((Diff.NotRemote, key))
    for key in remote_keys:
        if key not in local_keys:
            # The file is remote but not local.
            diffs.append((Diff.NotLocal, key))

    return diffs


def show_diffs(diffs):
    """
    Prints a table of diffs.
    """

    print('This would make the following changes:')
    table = PrettyTable(['Diff', 'Key'])
    for diff, key in diffs:
        table.add_row([diff, key])
    print(table)


def run_diffs(diffs, bucket, local_changes=None):
    """
    Takes diffs and makes the necessary changes, either pushing or
    pulling files.
    """
    if type(local_changes) is not bool:
        raise ValueError('local_changes must be set to a bool')

    if local_changes:
        for diff, key in diffs:
            if diff == Diff.NotRemote:
                # Delete local file
                print('removing (local): {0}'.format(key))
                os.remove(key)
            elif diff == Diff.NotLocal or diff == Diff.Modified:
                # Pull remote file
                print('pulling: {0}'.format(key))
                with open(key, 'w') as f:
                    bucket.get_key(key).get_contents_to_file(f)
    else:
        # Remote changes
        for diff, key in diffs:
            if diff == Diff.NotRemote or diff == Diff.Modified:
                # Push local file
                print('pushing: {0}'.format(key))
                with open(key, 'r') as f:
                    k = bucket.new_key(key)
                    k.set_contents_from_file(f)
                    k.make_public()
            elif diff == Diff.NotLocal:
                # Delete remote file
                print('removing (remote): {0}'.format(key))
                bucket.get_key(key).delete()
