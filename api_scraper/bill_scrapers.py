from okscraper.storages import ListStorage

from api_scraper.models import BillData
from knesset_api_base_scraper import KnessetApiBaseScraper
from bill_type_scrapers import BillTypeScraper

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
        super(BillDataScraper, self).__init__('http://online.knesset.gov.il/WsinternetSps/KnessetDataService/BillsData.svc/View_bill?$top=<<top>>&$skip=<<skip>>')
        self.storage = BillDataStorage()


    def _scrape(self, top, skip):
        raw = self.source.fetch(top, skip)
        entries = self.build_entries_list(raw)
        for props in entries:
            bill_id = props['bill_id']
            self._getLogger().info('Scraped bill data (bill id %s)', bill_id)
            self.storage.store(props)
            bill_type_scraper = BillTypeScraper()
            bill_type_scraper.scrape(bill_id)


BillDataScraper().scrape(5,0)
