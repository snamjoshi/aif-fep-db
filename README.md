# aif-fep-db
A database of publications related to active inference and the free energy principle.
<!-- See: https://stackoverflow.com/questions/69723198/dash-datatable-drop-down-filter -->

## General workflow for updating database and tags

The database is designed to be easily updated either by scraping from online archives (PubMed, ArXiv, etc.) or manually adding papers to the database. A typical workflow supported by functions defined in this codebase is as follows:
1. Add new papers to database using one of the following two options:
   - Scraping new papers from supported online archives for a requested date range. For this option, returned papers and metadata may not all be active inference papers. The user is responsible for removing irrelevant papers.
   - Adding papers to existing database manually. This option requires supplying specific fields.
2. Create tags for all papers added to database. These new tags must be associated with a new or existing tag file.
3. Add tags to the database and save the database.
4. Launch the app to view and filter the database by tags. 

## Current planned features
* Helper functions for loading scraped tables and easily removing rows.
* Support for books or book chapters - maybe "add papers" or "add book/chapter" entries?
* Tag list has id associated with it which generated from a hash.
* Ensure that the author field is input as a list and not a string.
* If no DOI after scraping, create a DOI using a hash of the paper information that is available.

## Features
* Removal/cleaning functions for papers that should not be in the database.
* Custom tags to add to the database.
* Fix issues with inconsistent author formats
* Remove autoreload from notebooks
* Fix downloading filtered database with Dash app
* Clean up notebooks and add examples
* Clean up current database and make current
* Config file or Docker command to specify the path to the current database
* CI/CD
* Redo readme
* Type hints, doc strings, better documentation in general.
* Clean up the interactive database file
* Double check outer requirements text
* Check remaining todos

## Downloading the database

## Examples
See how to add the database and add your own tags.
See how to cite and download papers.

## Possible future features
* `squlite3` support as an alternative to CSV database

## TODO and Features
* Support for books or book chapters - maybe "add papers" or "add book/chapter" entries?
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
* Network analysis of authors and labs and further meta analysis

https://zenodo.org/record/7093837 -- this is more towards the crowdsourcing and coherence among annotations. Later stage.

https://publish.obsidian.md/active-inference/docs/guides/learning_paths/active_inference_ecological_learning_path

Examples of using Learning Paths for domains