from BeautifulSoup import BeautifulStoneSoup
from api_scraper.models import BillData
from okscraper.base import BaseScraper
from okscraper.sources import UrlSource
from okscraper.storages import ListStorage
import scrapers_common


class BillDataStorage(ListStorage):
    _commitInterval = 1

    def _addValueToData(self, data, value):
        # TODO: logger
        bill_data, created = BillData.objects.get_or_create(bill_id=value["bill_id"])
        print created
        bill_data.__dict__.update(value)
        bill_data.save()
        super(BillDataStorage, self)._addValueToData(data, value)


class BillDataScraper(BaseScraper):

    def __init__(self):
        super(BillDataScraper, self).__init__(self)
        self.source = UrlSource("http://online.knesset.gov.il/WsinternetSps/KnessetDataService/BillsData.svc/View_bill?$top=<<top>>&$skip=<<skip>>")
        self.storage = BillDataStorage()


    def _scrape(self, top, skip):
        raw = self.source.fetch(top, skip)
        entries = scrapers_common.build_entries_list(raw)
        for entry in entries:
            print entry
            self.storage.store(entry)

BillDataScraper().scrape(2,0)
