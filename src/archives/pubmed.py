from paperscraper.pubmed import get_pubmed_papers
from src.archives.scrape import Scrapper

class PubMedScrapper(Scrapper):
    def __init__(self) -> None:
        Scrapper.__init__(self)
    
    def scrape(self):
        get_pubmed_papers(query, field)