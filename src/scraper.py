import logging
import os
import pandas as pd

from datetime import datetime
from typing import List, Union
from paperscraper.arxiv import get_arxiv_papers_api
from paperscraper.arxiv.utils import get_query_from_keywords
from paperscraper.pubmed import get_pubmed_papers
from paperscraper.pubmed.utils import get_query_from_keywords_and_date

from src.enums import Scrapers
from src.utils import flatten_keywords, split_camel_case

LOGGER = logging.getLogger(__name__)
logging.basicConfig(level = logging.INFO)


class Scraper:
    """ 
    Scrapes papers from archives of interest and exports the resulting tables to CSV. 
    Supported archives shown in enums.py 
    """
    
    def __init__(self, 
                 keywords: List[Union[str, List[str]]], 
                 start_date: str, 
                 end_date: str,
                 archives: List[str]) -> None:
        
        self.keywords = keywords
        self.start_date = start_date
        self.end_date = end_date
        self.archives = archives
        
        self._check_archives()
    
    def run(self, return_results: bool=False, outpath: str=None) -> Union[None, pd.DataFrame]:
        """ Scrapes papers from all requested archives and assembles from a single DataFrame """
        
        df_list = []
        
        # Loop over archive and scrape - store in df_list
        for archive in self.archives:
            if archive == "pubmed":
                df = self._pubmed_scraper()
            elif archive == "arxiv":
                df = self._arxiv_scraper()

            df_list.append(df)
        
        # Concat all DataFrames into a single DataFrame
        df = pd.concat(df_list).drop_duplicates()
        
        # If returning results, exit function early
        if return_results:
            return df
        
        # If not returning results and outpath not specified
        if not outpath:
            creation_time = datetime.now()
            
            # Create file name by concating keyword list and timestamp
            keyword_string = '__'.join(flatten_keywords(keywords=self.keywords))
            file_name = keyword_string + "__" + str(creation_time).replace(" ", "__") + ".csv"

            # Create directory
            date = str(creation_time).split(" ")[0].replace("-", "_")
            dir_path = os.path.join("data/tables", date)
            os.makedirs(dir_path, exist_ok=True) 
            
            # Assemble outpath
            outpath = os.path.join(dir_path, file_name)
        
        # Export to outpath
        df.to_csv(outpath, index=False)
        
        LOGGER.info(f"Scraped tables exported to {outpath}.")
    
    def _check_archives(self) -> None:
        """ Checks if the input archives to scrape are currently supported or not. """
        
        archive_options = list(Scrapers.__members__)
        supported = []
        unsupported = []
        
        for archive in self.archives:
            # Check if input archives is one of the possible options
            if archive not in archive_options:
                raise Exception(f"'{archive}' unrecgonized. Archive must be one of {archive_options}.")

            # Determine the list of supported and unsupported archives submitted
            if Scrapers[archive].value is False:
                unsupported.append(archive)
            else:
                supported.append(archive)
        
        # If any unsupported archives were submitted: assertion error      
        assert len(unsupported) == 0, f"Archives {unsupported} are not currently supported. Currently supported archives: {supported}."
    
    def _pubmed_scraper(self) -> pd.DataFrame:
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
    
    def _arxiv_scraper(self) -> pd.DataFrame:
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
        
    def _process_dates(self, df: pd.DataFrame) -> pd.DataFrame:
        """ Replaces date column with just year"""
        
        df["date"] = pd.to_datetime(df["date"])
        df["date"] = df["date"].dt.year
        
        return df
    
    def _reorder_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """ Reorders and renames scraped columns """
        
        df = df[["title", "authors", "journal", "date", "doi"]]
        df.columns = ["title", "authors", "where_published", "year", "doi"]
        
        return df
