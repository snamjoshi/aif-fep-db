""" Class that downloads and parses all Arxiv metadata into tables """

import arxiv


class ArxivDownload:
    def __init__(self) -> None:
        arxiv_db = None
    
    def run(self):
        self._download_arxiv()
    
    def _download_arxiv(self):
        pass
    
    def _download_psyarxiv(self):
        pass
    
    def _download_bioarxiv(self):
        pass
    
    def _assemble(self):
        pass