import pandas as pd

# from enums import ArchiveOptions

class Scrapper:
    def __init__(self, terms: str, fields: list, outpath: str=None) -> None:
        self.terms = terms
        self.fields = fields
        self.outpath = outpath
    
    def scrape(self):
        raise NotImplementedError
    
    def _filter(self):
        # TODO: Function to filter by date
        raise NotImplementedError
    
    def _export(self):
        if not self.outpath:
            # TODO: create timestamp and export to data folder
            ...
        else:
            # TODO: Export to given outpath
            ...
    


# def scrape(archive: str, terms: list, outpath: str) -> pd.DataFrame:
#     """ Scrapes data from selected archive and outputs to data folder """
    
#     # Check that arrive is implemented
#     ARCHIVE_OPTIONS = [item.value for item in ArchiveOptions]
#     assert archive in ARCHIVE_OPTIONS, f"Archive must be one of {ARCHIVE_OPTIONS}."
    
#     # Check that outpath exists
#     # TODO: Check directory
    
#     scrapper_dict = {
#         "pubmed"  : PubMedScrapper(),
#         # "arxiv"   : ArXivScrapper(),
#         # "bioarxiv": BioArXivScrapper(),
#         # "psyarxiv": PsyArXivScrapper(),
#         # "osf"     : OSFScrapper(),
#         # "zenodo"  : ZenodoScrapper()
#     } 
    
#     scrapper = scrapper_dict[archive]
#     tables = scrapper.run()
    
#     if not outpath:
#         # TODO: create timestamp and export to data folder
#         ...
#     else:
#         # TODO: Export to given outpath
#         ...
    
#     return tables

