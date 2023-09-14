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
* Summary field (i.e. even shorter abstract.)
* Download PDF functionality (Paperpile or otherwise?). Maybe from my current repository of PDFs. GoogleDrive request?
* Interactive add tag mode. Goes through the table one at a time in terminal, displaying the row. Lists all current tags. The user can then add tags. Accepted commands include "add tag [tag]" and "next file" or "previous file". Only lists files without tags yet.
* ArXiv and BioArXiv support for preprints or open-access material
* Bib-tex export and or citation support
* Get abstract method?
* Switch to UUID instead of pmid to account for ArXiv papers, preprints, and open access papers
