import logging
import math
import pandas as pd

# from Bio import Entrez
# from Bio.Entrez import efetch

from src.utils import progress_bar

LOGGER = logging.getLogger(__name__)
logging.basicConfig(level = logging.INFO)


# TODO: Refactor into a main method.

# def add_tags_interactive(self, db, tags):
#     """ Interactive tag adding mode        
#     """
#     # TODO: Remove interacting tagging mode altogether... separate into a different standalone module in the interactive file?
#     # TODO: Allow multiple loaded tags (categories) to the passed in as a list
#     self._check_tag_exists()
#     interactive = InteractiveTagging(db, self.tags)
#     interactive.run()

# tags.add_tags_interactive(db=database, tags=tags)

""" Features to add 
- Separate out the Interactive class so it is not called through the Tags class
- Ability to add new tags to tag list on the fly
- Do not filter the table from the beginning. Instead, give the user the option to skip to the next
  non-tagged entry.
- Option to remove tags from an entry
- Automatically filters added/removed row
- Maybe the tag class can be called "metadata" and also lists rows that are to be added and removed.
  Then it's possible to just add a column specifiying a bool for whether or not the row is to be
  removed or not. Only list removed rows. Upon joining, rows without a remove tag will be filled as
  false. 
"""

class InteractiveTagging:
    """ Implements the user-input interactive tag loop.
    Features:
    """
    def __init__(self, db, tags) -> None:
        self._run = True
        self._tags = pd.DataFrame(tags["tagged_papers"])
        self._db = db.db.merge(self._tags, on='id', how='outer')
        # self._db = db[db['tag'].isnull()]
        
        self._current_paper = 0
        
        # Setup                                                                                                                                                                                
        Entrez.email = 'sanjeev.namjoshi@gmail.com'  
        
        # print(self._tags)
        # print(self._db)
        
        # self._tagged_papers = [tags["id"] for tags in self._tags["tagged_papers"]]
        # self._db_tag: Appended tags to database
        # self._db = self._db[~self._db["id"].isin(self._tagged_papers)]
    
    def run(self):
        """ Begin main interactive loop """
        
        while self._run == True:
            
            # Display progress bar, the title/author/year for current paper, and current tags
            self._progress()
            self._title_author_year()
            self._current_tags()
            
            inpt = input(
                """ 
                INTERACTIVE TAG ADDING MODE. Please select an action:
                    - [a] to show abstract
                    - [f] to see a specific field
                    - [k] to view next paper
                    - [p] to view previous paper
                    - [n] to jump to the next untagged paper
                    - [l] to add a new tag to the tag list
                    - [t] to add tags to paper
                    - [r] to remove tags from paper
                    - [x] to mark paper as "remove"
                    - [q] to quit interactive mode
        
                """)
            
            self._menu(inpt)
                
    def _menu(self, inpt):
        if inpt == "a":
            self._show_abstract()  
        elif inpt == "f":
            self._show_fields()
        elif inpt == "k":
            self._next_paper()
        elif inpt == "p":
            self._previous_paper()
        elif inpt == "n":
            self._jump_to_untagged()
        elif inpt == "l":
            self._add_to_tag_list()
        elif inpt == "t":
            self._add_tags()
        elif inpt == "r":
            self._remove_tags()
        elif inpt == "x":
            self._remove_paper()
        elif inpt == "q":
            self._quit()
        else:
            print("Command not recognized.\n")
            print(''.join(["*"] * 100))        

    def _progress(self):
        total_papers = self._db.shape[0]
        n_tagged_papers = sum(~self._db["tag"].isnull())
        percent_tagged = math.floor((n_tagged_papers / total_papers) * 100)
        
        bar = progress_bar(percent_tagged)
        LOGGER.info(f"Currently {n_tagged_papers}/{total_papers} papers tagged.")
        print(bar)
    
    def _title_author_year(self):
        paper_row = self._db.loc[self._current_paper]
        title = paper_row["title"]
        authors = paper_row["authors"]
        year = paper_row["publication_year"]
        pmid = paper_row["id"]
        
        print("\n\n")
        print(f"ID: {pmid}")
        print(f"Title: {title}")
        print(f"Authors: {authors}")
        print(f"Year: {year}")
    
    def _current_tags(self):
        current_tags_list = self._db.loc[self._current_paper]["tag"]
        
        if math.isnan(current_tags_list):
            current_tags_list = "no tags added"
        print(f"Current tags: {current_tags_list}")
        
    def _jump_to_untagged(self):
        # [ ] Jumps to the next untagged paper
        ...
    
    def _time_estimation(self):
        # [ ] Tic toc time elasped
        # [ ] Tic toc time total
        ...

    def _show_abstract(self):
        
        LOGGER.info("Pulling abstract, this may take up to a minute...")
        paper_id = self._db.loc[self._current_paper]["id"]
        
        handle = efetch(db='pubmed', id=paper_id, retmode='text', rettype='abstract')
        print(handle.read())
        
    def _show_fields(self):
        # [ ] Prompt: Which fields to show?
        # Another while loop here?
        options = ['id', 'citation', 'journal_book', 'publication_year', 'create_date', 'pmcid', 'nihms_id', 'doi']
        show_fields = True
        
        while show_fields == True:
            # TODO: Include number for each option to pick.
            inpt = input(f"Which field to show? Options include: {options}")
        
        if inpt not in options:
            print("Command not recognized.\n")
        
    def _next_paper(self):
        # If at the end, set counter equal to itself and say no more papers
        if self._current_paper == self._db.shape[0]:
            self._current_paper += 0
            print("You have reached the final paper in the database. There are no more papers.")
        else:
            self._current_paper +=1
        print("\n")
        print(''.join(["*"] * 100))
        
    def _previous_paper(self):
        # [ ] Move backward a paper
        # If at the beginning, set counter equal to irself and say no more papers
        if self._current_paper == 0:
            self._current_paper -= 0
            print("You are at the first paper in the database. There are no previous papers.")
        else:
            self._current_paper -= 1
        print("\n")
        print(''.join(["*"] * 100))
        
    def _remove_paper(self):
        ...
        
    def _add_tags(self):
        # [ ] Average time with tic toc to finish. Give estimate of remaning items at end of method call.
        # [ ] Prompt: Which tags to add?
        # [ ] Add a new tag on the fly. Terminal will refresh to show the new tag added.
        # [ ] Saves new tags in the tag list mid-stream
        # [ ] Notification of which tags were added and to which category
        # [ ] Prints current tags at the bottom of the output with numbers associated so it's easy to write which tag to add
        ...
        
    def _quit(self):
        # self._time_estimation(self)
        self._run = False