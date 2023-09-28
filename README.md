# aif-fep-db
A database of publications related to active inference and the free energy principle.

## Features
* Helper functions for filtering and sorting.
* Removal/cleaning functions for papers that should not be in the database.
* Custom tags to add to the database.

## Downloading the database

## Examples
See how to add the database and add your own tags.
See how to cite and download papers.

## Possible future features
* `squlite3` support as an alternative to CSV database

## TODO and Features
* Separate tags file + db. In other words, the db stays intact always. Separate file is created.
* Tag file is now just a metadata file. 
* Removing papers is in the tag file will the remove tag or maybe a separate section
* Adding papers should happen in a separate way. One way is the through auto-download from pubmed and Arxiv. The other is manually adding for papers that are found in neither place.
* Support for books or book chapters and masters theses/disserations
* Summary field (i.e. even shorter abstract.)
* Download PDF functionality (Paperpile or otherwise?). Maybe from my current repository of PDFs. GoogleDrive request?
* Interactive add tag mode. Goes through the table one at a time in terminal, displaying the row. Lists all current tags. The user can then add tags. Accepted commands include "add tag [tag]" and "next file" or "previous file". Only lists files without tags yet.
* ArXiv and BioArXiv support for preprints or open-access material
* Bib-tex export and or citation support. Perhaps option for APA as well.
* Links to all open access papers.
* Get abstract method?
* Switch to UUID instead of pmid to account for ArXiv papers, preprints, and open access papers
* DOI links
* Layout needs pages for about/info, tag reference, minimal data stats, and perhaps even a section on possible queries of interest (like early AIF papers)
* SQL support or some way to search the table other than just filtering by clicking the columns
* Work on auto-refresh. Should check the database to ensure that the paper is not already there. Then it adds to the database. Then the website will auto-refresh and add papers every week or so.
* Eventually expansion to an ontology of tags
* Public and private modes for editing the table or custom tags
* timestamp on website to show when data was last download from pubmed. How recent the db is.
* Small ArXiv paper to cite later. Put this in the about section.
* Preloaded libraries for Paperpile, Zotoro, or Mendeley?
* Network analysis of authors and labs. 