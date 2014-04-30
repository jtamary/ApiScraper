from BeautifulSoup import BeautifulStoneSoup
from api_scraper.models import BillType
from okscraper.base import BaseScraper
from okscraper.sources import UrlSource
from okscraper.storages import ListStorage
import datetime
from api_scraper.knesset_api_base_scraper import build_entries_soup


def build_entries_list(raw):
    entries = []
    soup = BeautifulStoneSoup(raw)
    for entry_properties in soup.findAll("m:properties"):
        entry_dict = {}
        for prop in entry_properties.findChildren():
            entry_dict[prop.name[2:]] = prop.text
        entries.append(entry_dict)
    return entries

class BillTypeStorage(ListStorage):
    _commitInterval = 1
    
    def _addValueToData(self, data, value):
        # TODO: logger
        bill_type, created = BillType.objects.get_or_create(bill_type_id=value["bill_type_id"])
        print created
        bill_type.__dict__.update(value)
        bill_type.save()
        super(BillTypeStorage, self)._addValueToData(data, value)
    
            
class BillTypeScraper(BaseScraper):
    
    def __init__(self):
        super(BillTypeScraper, self).__init__(self)
        self.source = UrlSource("http://online.knesset.gov.il/WsinternetSps/KnessetDataService/BillsData.svc/View_Bill_type")
        self.storage = BillTypeStorage()

    
    def _scrape(self):
        raw = self.source.fetch()
        entries = build_entries_list(raw)
        for entry in entries:
            self.storage.store(entry)
        
BillTypeScraper().scrape()
print BillType.objects.all()