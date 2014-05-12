import re

from BeautifulSoup import BeautifulStoneSoup
from okscraper.base import BaseScraper
from okscraper.sources import UrlSource


SELF_CLOSING_TAGS = ['link', 'category']


class KnessetApiBaseScraper(BaseScraper):
    """
    This is the base class for every entity repository in the knesset API
    Is scrapes the properties of any entity and it's linked entities links.
    """
    def __init__(self, url):
        super(KnessetApiBaseScraper, self).__init__()
        self.source = UrlSource(url)

    def build_entries_list(self, raw):
        entries = []
        soup = BeautifulStoneSoup(raw, selfClosingTags=SELF_CLOSING_TAGS)

        for entry_data in soup.findAll('entry'):
            entries.append(self.build_entry(str(entry_data)))

        return entries

    def build_entry(self, entry_raw):
        soup = BeautifulStoneSoup(entry_raw, selfClosingTags=SELF_CLOSING_TAGS)
        props_dict = {}
        entry_properties = soup.findAll('m:properties')[0]
        for prop in entry_properties.findChildren():
            props_dict[prop.name[2:]] = prop.text
        return props_dict
