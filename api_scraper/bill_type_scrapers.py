from BeautifulSoup import BeautifulStoneSoup
from okscraper.base import BaseScraper
from okscraper.sources import UrlSource
from okscraper.storages import ListStorage
from api_scraper.knesset_api_base_scraper import KnessetApiBaseScraper

from api_scraper.models import BillType

class BillTypeStorage(ListStorage):
    _commitInterval = 1
    
    def _addValueToData(self, data, value):
        # TODO: logger
        bill_type, created = BillType.objects.get_or_create(bill_type_id=value["bill_type_id"])
        print created
        bill_type.__dict__.update(value)
        bill_type.save()
        super(BillTypeStorage, self)._addValueToData(data, value)
    
            
class BillTypeScraper(KnessetApiBaseScraper):
    
    def __init__(self):
        super(BillTypeScraper, self).__init__('http://online.knesset.gov.il/WsinternetSps/KnessetDataService/BillsData.svc/View_bill(<<bill_id>>)/bill_type')
        self.storage = BillTypeStorage()

    def _scrape(self, bill_id):
        raw = self.source.fetch(bill_id)

        entries = self.build_entries_list(raw)
        for props in entries:
            self._getLogger().info('Scraped bill type data (bill id %s)', bill_id)
            self.storage.store(props)

print BillType.objects.all()