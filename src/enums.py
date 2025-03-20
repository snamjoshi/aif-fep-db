from enum import Enum

from src.archives.pubmed import PubMedScrapper

class Scrappers(Enum):
    PUBMED   = PubMedScrapper()
    # ARXIV    = ArXivScrapper()
    # PSYARXIV = BioArXivScrapper()
    # BIOARXIV = PsyArXivScrapper()
    # OSF      = OSFScrapper()
    # ZENODO   = ZenodoScrapper()
    