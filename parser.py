from datetime import datetime
from time import mktime

import feedparser

from exceptions import ParserEmptyData
from constants import CFPLAND_FEED_URL


class FeedParser:
    def __init__(self, content=CFPLAND_FEED_URL):
        self.content = content

    def get_cfps(self):
        parsed_feed = feedparser.parse(self.content)
        items = parsed_feed.get('items')

        if not items:
            raise ParserEmptyData()

        data = []

        for item in items:
            if self.is_bad_cfp(item):
                continue

            published_at = datetime.fromtimestamp(mktime(item.get('published_parsed')))
            cfp = {
                'title': item.get('title'),
                'description': item.get('description'),
                'link': item.get('link'),
                'category': item.get('category'),
                'published_at': published_at,
                'event_start_date': item.get('eventstartdate'),
                'cfp_end_date': item.get('cfpenddate'),
                'location': item.get('location'),
                'perk_list': item.get('perkslist'),
            }

            data.append(cfp)

        return data

    def is_bad_cfp(self, item):
        """
        Ignore CFPs with known issues.
        """

        # TECHSPO Toronto has no link field
        if item.get('title') == 'TECHSPO Toronto':
            return True

        return
