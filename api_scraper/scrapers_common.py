from BeautifulSoup import BeautifulStoneSoup

def build_entries_list(raw):
    entries = []
    soup = BeautifulStoneSoup(raw)
    for entry_properties in soup.findAll("m:properties"):
        entry_dict = {}
        for prop in entry_properties.findChildren():
            entry_dict[prop.name[2:]] = prop.text
        entries.append(entry_dict)
    return entries
