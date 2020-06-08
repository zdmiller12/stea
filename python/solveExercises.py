import basicFunctions as bf

class SolveExercises():
    def __init__(self, parent=None):
        self.solved = False
        
            
    def solve_exercises(self):
        feedback = "Solving exercises."
        print(feedback)
        self.show_status_message(feedback)
        
        for book in self.books:
            self.solve(book)
            
    def solve(self, book):
        F = self.get_value("08_01_FV", book)
        i = self.get_value("08_01_i", book)
        n = self.get_value("08_01_periods", book)
        self.set_value("08_01_PV", book, bf.find_P_given_F(F, i, n))
    
    def get_value(self, variable, book):
        """
        Gets the value of the variable from the CSV file.

        Parameters
        ----------
        variable : string
            The variable to return. Must match the CSV file.
            
        book : string
            From which book ('SEA', or 'STEA') the value should be returned.

        Returns
        -------
        The value of the variable.

        """
        return self.df[self.df[self.variable_header] == variable][book].iloc[0]
    
    def set_value(self, variable, book, value):
        """
        

        Parameters
        ----------
        variable : string
            The variable to set. Must match the CSV file.
            
        book : string
            For which book ('SEA', or 'STEA') the value should be set.
            
        value : numeric (int, float)
            The value to set.

        Returns
        -------
        None.

        """
        self.df.loc[self.df[self.variable_header] == variable, book] = value
    

