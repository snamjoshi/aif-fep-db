# aif-fep-db
A database of publications related to active inference and the free energy principle.

## Features
* Helper functions for filtering and sorting

## TODO and Features
* Separate tags file + db. In other words, the db stays intact always. Separate file is created.
* Summary field (i.e. even shorter abstract.)
* Add and remove row functionality based on PMID (drop). 
* Auto remove rows for papers that are clearly incorrect.
* Add and remove tags functionality
* Download PDF functionality (Paperpile or otherwise?). Maybe from my current repository of PDFs. GoogleDrive request?
* List all current tags
* Interactive add tag mode. Goes through the table one at a time in terminal, displaying the row. Lists all current tags. The user can then add tags. Accepted commands include "add tag [tag]" and "next file" or "previous file". Only lists files without tags yet.
* ArXiv and BioArXiv support for preprints or open-access material
* Bib-tex export and or citation support
* Get abstract method?
* Tags (separate tag class?)
* [?] Use database (`sqlite3`) instead of CSV
* Switch to UUID instead of pmid to account for ArXiv papers, preprints, and open access papers
