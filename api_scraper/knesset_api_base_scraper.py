from BeautifulSoup import BeautifulStoneSoup
from okscraper.base import BaseScraper
from okscraper.sources import UrlSource
import re

SELF_CLOSING_TAGS = ['link', 'category']


class KnessetApiBaseScraper(BaseScraper):

    def __init__(self, base_svc, suffix):
        super(KnessetApiBaseScraper, self).__init__()
        self.base_svc = base_svc
        self.source = UrlSource(base_svc  + suffix)

    def build_entries_list(self, raw):
        entries = []
        soup = BeautifulStoneSoup(raw, selfClosingTags=SELF_CLOSING_TAGS)

        for entry_data in soup.findAll('entry'):
            entries.append(self.build_entry(str(entry_data)))

        return entries

    def build_entry(self, entry_raw):
        soup = BeautifulStoneSoup(entry_raw, selfClosingTags=SELF_CLOSING_TAGS)
        links = []
        props_dict = {}
        for links_tag in soup.findAll('link'):
            if links_tag['rel'] != 'edit': # this is a link to self
                links_dict = {'title': links_tag['title'], 'params': re.findall(self.base_svc + links_tag['href'], '\(\d+\)')}
                print links_dict
                links.append(links_dict)
        entry_properties = soup.findAll('m:properties')[0]
        for prop in entry_properties.findChildren():
            props_dict[prop.name[2:]] = prop.text

        return links, props_dict
