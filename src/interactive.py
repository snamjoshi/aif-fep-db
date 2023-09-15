import logging
import math
import pandas as pd

from src.utils import progress_bar

LOGGER = logging.getLogger(__name__)
logging.basicConfig(level = logging.INFO)


class InteractiveTagging:
    """ Implements the user-input interactive tag loop.
    Features:
    """
    def __init__(self, db, tags) -> None:
        self._run = True
        self._tags = pd.DataFrame(tags["tagged_papers"])
        
        db = db.db.merge(self._tags, on='id', how='outer')
        self._db = db[db['tag'].isnull()]
        
        self._current_paper = 0
        
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
                    - [t] to add tags
                    - [q] to quit interactive mode
        
                """)
            
            if inpt == "a":
                self._show_abstract()
            elif inpt == "f":
                self._show_fields()
            elif inpt == "k":
                self._next_paper()
            elif inpt == "l":
                self._previous_paper()
            elif inpt == "t":
                self._add_tags()
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
        # [ ] Show the title, author, and year.
        paper_row = self._db.loc[self._current_paper]
        title = paper_row["title"]
        authors = paper_row["authors"]
        year = paper_row["publication_year"]
        
        print("\n\n")
        print(f"Title: {title}")
        print(f"Authors: {authors}")
        print(f"Year: {year}")
    
    def _current_tags(self):
        # [ ] Prints current tags at the bottom of the output with numbers associated so it's easy to write which tag to add
        ...
    
    def _time_estimation(self):
        # [ ] Tic toc time elasped
        # [ ] Tic toc time total
        ...

    def _show_abstract(self):
        # [ ] Pull abstract with "show abstract"
        ...
        
    def _show_fields(self):
        # [ ] Prompt: Which fields to show?
        # Another while loop here?
        options = ['id', 'citation', 'journal_book', 'publication_year', 'create_date', 'pmcid', 'nihms_id', 'doi']
        inpt = input("Which field to show? Options include: ")
        
        if input not in options:
            print("Command not recognized.\n")
        
    def _next_paper(self):
        # [ ] Move forward a paper
        # If at the end, set counter equal to itself and say no more papers
        self._current_paper +=1
        print("\n")
        print(''.join(["*"] * 100))
        
    def _previous_paper(self):
        # [ ] Move backward a paper
        # If at the beginning, set counter equal to irself and say no more papers
        ...
        
    def _add_tags(self):
        # [ ] Average time with tic toc to finish. Give estimate of remaning items at end of method call.
        # [ ] Prompt: Which tags to add?
        # [ ] Add a new tag on the fly. Terminal will refresh to show the new tag added.
        # [ ] Saves new tags in the tag list mid-stream
        # [ ] Notification of which tags were added and to which category
        ...
        
    def _quit(self):
        # self._time_estimation(self)
        self._run = False