import logging
import pandas as pd

from typing import List, Union
from paperscraper.arxiv import get_arxiv_papers_api
from paperscraper.arxiv.utils import get_query_from_keywords
from paperscraper.pubmed import get_pubmed_papers
from paperscraper.pubmed.utils import get_query_from_keywords_and_date

from src.enums import Scrapers
from src.utils import split_camel_case

LOGGER = logging.getLogger(__name__)
logging.basicConfig(level = logging.INFO)


class Scraper:
    def __init__(self, 
                 keywords: List[Union[str, List[str]]], 
                 start_date: str, 
                 end_date: str,
                 archives: List[str],
                 return_results: bool=False,
                 outpath: str=None) -> None:
        
        self.keywords = keywords
        self.start_date = start_date
        self.end_date = end_date
        self.archives = archives
        self._return_results = return_results
        self.outpath = outpath
        
        self._check_archives()
    
    def run(self):
        """ Scrapes papers from all requested archives """
        
        df_list = []
        
        for archive in self.archives:
            if archive == "pubmed":
                df = self._pubmed_scraper()
            elif archive == "arxiv":
                df = self._arxiv_scraper()

            df_list.append(df)
            
        df = pd.concat(df_list).drop_duplicates()
        
        if self.outpath:
            # TODO: Export to given outpath
            ...
        else:
            # TODO: create timestamp and export to data folder
            ...
        
        if self._return_results:
            return df
    
    def _check_archives(self):
        """ Checks if the input archives to scrape are currently supported or not. """
        
        # TODO: Catch case where an archive is not in the list. See scraper notebook.
        
        supported = []
        unsupported = []
        
        for archive in self.archives:
            if Scrapers[archive].value is False:
                unsupported.append(archive)
            else:
                supported.append(archive)
                
        assert len(unsupported) == 0, f"Archives {unsupported} are not currently supported. Currently supported archives: {supported}."
    
    def _pubmed_scraper(self):
        """ Scrapes papers from PubMed """
        
        # Prepare query and scrape
        query = get_query_from_keywords_and_date(
                    keywords=self.keywords, 
                    start_date=self.start_date, 
                    end_date=self.end_date)
        
        LOGGER.info("Scraping from PubMed...")
        
        df = get_pubmed_papers(
            query=query, 
            fields=["title", "authors", "date", "journal", "doi"])
        
        df = self._process_dates(df=df)
        
        # Format author column
        df['authors'] = df['authors'].apply(lambda name_list: [split_camel_case(name) for name in name_list])
        df["authors"] = df["authors"].apply(lambda name_list: ", ".join(name_list))
        
        # Reorder and rename columns
        df = self._reorder_columns(df=df)
        
        return df
    
    def _arxiv_scraper(self):
        """ Scrapes papers from ArXiv """
        
        # Prepare query and scrape
        query = get_query_from_keywords(
            keywords=self.keywords, 
            start_date=self.start_date.replace("/", "-"), 
            end_date=self.end_date.replace("/", "-"))
        
        LOGGER.info("Scraping from ArXiv...")
        
        df = get_arxiv_papers_api(
            query=query, 
            fields=["title", "authors", "date", "journal", "doi"])
        
        df = self._process_dates(df=df)
        
        # Fill journal
        df["journal"] = ["arXiv"] * len(df)
        
        # Reorder and rename columns
        df = df[["title", "authors", "journal", "date", "doi"]]
        df.columns = ["title", "authors", "where_published", "year", "doi"]
        
        return df
    
    def _psyarxiv_scraper(self):
        raise NotImplementedError
    
    def _bioarxiv_scraper(self):
        raise NotImplementedError
    
    def _osf_scraper(self):
        raise NotImplementedError
    
    def _zenodo_scraper(self):
        raise NotImplementedError
        
    def _process_dates(self, df: pd.DataFrame):
        """ Replaces date column with just year"""
        
        df["date"] = pd.to_datetime(df["date"])
        df["date"] = df["date"].dt.year
        
        return df
    
    def _reorder_columns(self, df: pd.DataFrame):
        """ Reorders and renames scraped columns """
        
        df = df[["title", "authors", "journal", "date", "doi"]]
        df.columns = ["title", "authors", "where_published", "year", "doi"]
        
        return df
