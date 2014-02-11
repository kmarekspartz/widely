"""
Get the status of various S3 regions.
"""

import feedparser
from prettytable import PrettyTable


def status():
    """
    Displays AWS S3 status.

    Usage: widely status
    """
    s3_status_rss_feeds = {
        "N. California": "http://status.aws.amazon.com/rss/s3-us-west-1.rss",
        "Oregon": "http://status.aws.amazon.com/rss/s3-us-west-2.rss",
        "US Standard": "http://status.aws.amazon.com/rss/s3-us-standard.rss",
        "Sao Paulo": "http://status.aws.amazon.com/rss/s3-sa-east-1.rss",
        "Ireland": "http://status.aws.amazon.com/rss/s3-eu-west-1.rss",
        "Singapore": "http://status.aws.amazon.com/rss/s3-ap-southeast-1.rss",
        "Sydney": "http://status.aws.amazon.com/rss/s3-ap-southeast-2.rss",
        "Tokyo": "http://status.aws.amazon.com/rss/s3-ap-northeast-1.rss"
    }
    print('=== S3 Status')
    table = PrettyTable(['Region', 'Status'])
    for region_name, rss_url in s3_status_rss_feeds.iteritems():
        feed = feedparser.parse(rss_url)
        if feed.entries:
            region_status = feed.entries[0].title
        else:
            region_status = 'Unknown.'
        table.add_row([region_name, region_status])
    print(table)
