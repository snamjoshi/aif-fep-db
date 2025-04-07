# aif-fep-db
A database of publications related to active inference and the free energy principle.

This tool was developed while I was writing *Fundamentals of Active Inference* and needed to do a complete literature review of all papers published around active inference, the free energy principle, Bayesian mechanics, and predictive processing. The primary purpose of this tool is to facilitate easy and flexible methods for scraping papers related to active inference and tagging them. The tool is completely general and could be used for a literature search on any area of interest.

Although the repo is designed around updating and maintaining a current list of tagged papers in the literature, the major programs are general enough to apply to your own project. For example, if you are writing a review on a specific area of active inference and want to have your results easily reproducible, you could use this repo to scrape the relevant papers, tag them, and then perform downstream analysis.

You will find tools that make it easy to scrape new papers from online archive, tag them, store them as serialized `Pandas` DataFrames, and then display them in a simple `Dash` app.

## General workflow for updating database and tags

A typical workflow supported by functions defined in this codebase is as follows:

1. Scrape new papers from online archives (PubMed, ArXiv, etc.).
2. Load the papers into the database.
3. Review the resulting papers and remove the unwanted ones.
4. Create a new tag file (or modify an existing tag file) and add tags to papers in the database.
5. Attach the tags to the database.
6. Save the database.
7. Run the app to view the database.

This workflow is shown in detail in `examples/0_workflow.ipynb`.

## Running the app

The most current version of the active inference database can be accessed as a `Dash` app which can be viewed in the browser. This app allows you to filter papers by column, remove papers, or select specific tags to filter down papers of interest. The filtered table can be exported to CSV.

You must have Docker installed to run the app. Please follow the installation instructions on the website before proceeding. Once Docker is installed, run the shell script `sh bin/build_and_run.sh` to build and run the Docker container. If the Docker container already exists on your machine you may use `sh bin/run.sh` to just run the container.

The Dash app displaying the table will be accessible on localhost at port 5000.

## Brief documentation

There are three main classes used in this database tool. They are described below along with a brief description of the methods. For more detail on these classes, and how to use them in a workflow, see the `examples/` directory.

### `Scraper` class

The `Scraper` class is used to scrape papers from one or more supported online archives based on a list of keywords and a start/end date. This class has the following public methods:
* `run()`: Runs the scraper with settings specified during initialization and outputs as Python object or to a specified directory.

### `Database` class

The `Database` class is used to store the paper database and allow for manipulation of its contents. This class has the following public methods:
* `attach_tags()`: Adds tags to an existing database loaded with `load()` or newly created with `create()`.
* `create()`: Creates a new database object from tables output from the `Scraper`.
* `detach()`: Detaches a current loaded database by clearing all data.
* `load()`: Loads a database from a database file serialized using `save()`.
* `remove()`: Removes papers from the database by the DOI.
* `save()`: Saves (exports) the database using serialization along with metadata.
* `update_from_dicts_list()`: Updates the database by adding papers from a list of dicts.
* `update_from_CSV()`: Updates the database by adding papers from a CSV.

### `Tags` class

The `Tags` class is used to tag papers using the DOI as the identifier. It has the following public methods:
* `add_to_tag_list()`: Appends new tags to the list of possible tags.
* `create()`: Creates an empty tag file storred in the `Tag` class.
* `detach()`: Detaches a current loaded tag file by clearing all data.
* `link_tags_to_doi`: Associates tags in the tag list with a specific DOI and stores it in the tag file.
* `load()`: Loads a tag file from a specified path.
* `save()`: Saves (exports) the tag file as YAML.
* `set_tag_list_category()`: Creates a new tag list category for the tag file.
* `view_tag_list()`: Prints the current tag list for a loaded tag file.

## TODO list

This is a list of items that I plan to finish before passing the project on to others for further work.
- [ ] Remove autoreload from notebooks
- [ ] Fix downloading filtered database with Dash app
- [ ] Test workflow notebook
- [ ] Clean up current database and make it up to date
- [ ] Config file or Docker command to specify the path to the current database
- [X] Redo README
- [ ] Type hints, doc strings, better documentation in general
- [ ] Clean up the interactive database file
- [ ] Double check outer requirements text
- [ ] Check remaining TODOs in codebase
- [ ] Move stuff in `dash.ipynb` into the app layout
- [ ] Documentation for the meaning behind each tag
- [ ] Display timestamp and tag file hash in layout
- [ ] About section for the app
- [ ] Delete old files and final cleanup.

## Future planned features / fixes

There are many more features I would like to add to this repo but I do not have time to commit to it and could benefit from volunteers. Below are a set of features I would like to add to this repo:

### Future features
* Support for books, book chapters, and master's theses.
* Test cases and more robust code.
* Host the database on an external website
* Create consistency among author formats. At the moment, authors come in different formats depending on which archive they were downloaded from.
* Implement CI/CD (assuming database is hosted on a website). This would allow automatically updating the website that hosts the database and making sure code tests pass.
* `squlite3` support as an alternative to CSV database. Unlikely to be necessary unless database becomes large or there is a demand for it.
* Add support for pulling abstracts
* Add support for BioArXiv, PsyArXiv, Zenodo, and OSF archives.
* Add support for a "summary field" or condensed abstract. This could come from LLM summary.
* Ability to download PDFs for each paper. The PDFs would need to be hosted somewhere external which might cost a bit of money if we have a few gigabytes of stored papers. The other issue to consider is the legality of freely hosting papers that are behind a paywall.
* Citation support. Ideally, there should be a column for the citation in BibTex format and tools to convert to other citation formats like APA etc.
* Statistics and analysis page in the app. Some basic bar charts for number of papers, top authors, etc could be a useful overview.
* A guide page that tells you about some useful searches such as the `core` tag.
* SQL query support in the app to search the database properly.
* Establish a tag ontology and more formal system.

### Fixes
* Add checks to ensure that the author field is input as a list and not a string of authors.
* If no DOI is returned after scraping, create a DOI using a hash of the paper information that is available to use as the ID.
* Cleanup and filter out erroneous papers from current database.
* Tag untagged papers in current database.
