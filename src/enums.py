from enum import Enum


class Scrapers(Enum):
    pubmed   = True
    arxiv    = True
    psyarxiv = False
    bioarxiv = False
    osf      = False
    zenodo   = False
