



from src.db import Database
from src.tags import Tags


class InteractiveTagging:
    """ Implements the user-input interactive tag loop.
    Features:
        [ ] Show the title, author, and year.
        [ ] Pull abstract with "show abstract"
        [ ] Show "field" to see other fields
        [ ] Only includes non-tagged papers
        [ ] Move forward a paper
        [ ] Move backward a paper
        [ ] Prints current tags at the bottom of the output with numbers associated so it's easy to 
            write which tag to add
        [ ] Saves new tags in the tag list mid-stream
        [ ] Add a new tag on the fly. Terminal will refresh to show the new tag added.
        [ ] Stop interactive mode
        [ ] Notification of which tags were added
        [ ] Average time with tic toc to finish. Give estimate of remaning items
        [ ] New field in YAML tag for "category" to separate different tag files
    """
    def __init__(self, db: Database, tags: Tags) -> None:
        self._run = True
        self._db = db.db
        self._tags = tags
    
    def run(self):
        """ Begin main interactive loop """
        
        while self._run == True:
            
            inpt = input(
                """ 
                INTERACTIVE TAG ADDING MODE. Please select an action:
                    - [a] to show abstract
                    - [k] to view next paper
                    - [p] to view previous paper
                    - [t] to add tags
                    - [q] to quit interactive mode
                    
                """)
            
            self._progress()
            
            if inpt == "a":
                self._show_abstract()
            elif inpt == "k":
                self._next_paper()
            elif inpt == "l":
                self._previous_paper()
            elif inpt == "t":
                self._add_tags()
            elif inpt == "q":
                self._quit()
            else:
                print("Command not recognized.")

    def _progress(self):
        # [ ] Progress bar / % left to add or counts out of total
        # Get nrows in table
        # Get tags in Tag
        total = self._db.shape[0]
        
        
    def _time_estimation(self):
        # [ ] Tic toc time elasped
        # [ ] Tic toc time total
        ...

    def _show_abstract(self):
        ...
        
    def _next_paper(self):
        ...
        
    def _previous_paper(self):
        ...
        
    def _add_tags(self):
        ...
        
    def _quit(self):
        # self._time_estimation(self)
        self._run = False