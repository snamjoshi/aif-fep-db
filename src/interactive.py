



class InteractiveTagging:
    """ Implements the user-input interactive tag loop.
    Features:
    """
    def __init__(self, db, tags) -> None:
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
                    - [f] to see a specific field
                    - [k] to view next paper
                    - [p] to view previous paper
                    - [t] to add tags
                    - [q] to quit interactive mode
        
                """)
            
            # [ ] Show "field" to see other fields
            
            self._progress()
            self._title_author_year()
            self._current_tags()
            
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
                print("Command not recognized.")

    def _progress(self):
        # [ ] Progress bar / % left to add or counts out of total
        # Get nrows in table
        # Get tags in Tag
        total = self._db.shape[0]
    
    def _title_author_year(self):
        # [ ] Show the title, author, and year.
        # [ ] Only includes non-tagged papers (need a counter maybe for which row?)
        ...
    
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
        ...
        
    def _next_paper(self):
        # [ ] Move forward a paper
        ...
        
    def _previous_paper(self):
        # [ ] Move backward a paper
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