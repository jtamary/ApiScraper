from BeautifulSoup import BeautifulStoneSoup
from api_scraper.models import BillData
from okscraper.base import BaseScraper
from okscraper.sources import UrlSource
from okscraper.storages import ListStorage
from knesset_api_base_scraper import KnessetApiBaseScraper


class BillDataStorage(ListStorage):
    _commitInterval = 1

    def _addValueToData(self, data, value):
        # TODO: logger
        bill_data, created = BillData.objects.get_or_create(bill_id=value['bill_id'])
        print created
        bill_data.__dict__.update(value)
        bill_data.save()
        super(BillDataStorage, self)._addValueToData(data, value)
        # self._getLogger().info('Stored bill data (bill id %s)', value['bill_id'])


class BillDataScraper(KnessetApiBaseScraper):

    def __init__(self):
        super(BillDataScraper, self).__init__('http://online.knesset.gov.il/WsinternetSps/KnessetDataService/BillsData.svc/', 'View_bill?$top=<<top>>&$skip=<<skip>>')
        self.storage = BillDataStorage()


    def _scrape(self, top, skip):
        raw = self.source.fetch(top, skip)
        # entries = scrapers_common.build_entries_list(raw)
        entries = self.build_entries_list(raw)
        for links, props in entries:
            self._getLogger().info('Scraped bill data (bill id %s)', props['bill_id'])
            # get links

            self.storage.store(props)
            for link in links:
                if link['title'] == 'bill_type':
                    # BillTypeScraper()
                    # self.bill_type_scraper.scrape(link['href'])
                    pass

BillDataScraper().scrape(5,0)
