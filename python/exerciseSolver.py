"""

"""
import os
import sys

import numpy  as np
import pandas as pd

import basicFunctions as bf


class ExerciseSolver():
    def __init__(self, books=["SEA", "STEA"], dataFrame=pd.DataFrame(), 
                 solved_file="../problems/variables_solved.csv", latex_header="latex_{}", 
                 units_header="units", variable_header="ch_pr_var", parent=None):
        self.books           = books
        self.df              = dataFrame
        self.latex_header    = latex_header
        self.saved           = False
        self.solved          = False
        self.solved_file     = solved_file
        self.units_header    = units_header
        self.variable_header = variable_header
        
    def solve_exercises(self):
        """
        Solves for unknown variables in the dataframe by applying fixed solution.

        Returns
        -------
        None.

        """
        feedback = "Exercises already solved."
        if not self.solved:
            feedback = "Exercises solved."
            for book in self.books:
                self.solve(book)
                self.format_for_latex(book)
            
        self.solved = True
        return self.df, feedback
        
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
        Sets the value of calculated variables in the pandas DataFrame.

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
    
    def solve(self, book):
        """
        Tediously written-out solutions.

        Parameters
        ----------
        book : string
            Either "SEA" or "STEA", to whichever book the solution corresponds.

        Returns
        -------
        None.
        
        """
        
        """08_01
        
        P = P/F, i, n
        """
        F = self.get_value("08-01-F", book)
        i = self.get_value("08-01-i", book)
        n = self.get_value("08-01-n", book)
        # factor = ?
        self.set_value("08-01-P", book, bf.find_P_given_F(F, i, n))
        
        """08_02a
        
        F = F/P, i, n
        """
        
        """08_02b
        
        F = F/P, i, n
        """
        
    def format_for_latex(self, book):
        self.df[self.latex_header.format(book)] = self.df.apply(lambda row: self.format_value_with_units(book, row), axis=1)
        
    def format_value_with_units(self, book, row):
        """
        Formats the variable with units.
        
        Parameters
        ----------
        value : numeric
            Variable value.
        units : string
            Variable units.

        Returns
        -------
        string
            The variable, formatted with appropriate units.
        """
        units = row[self.units_header]
        value = row[book]
        
        if isinstance(units, float) and np.isnan(units):
            return value
        
        elif units == "$":
            return "\${:,.2f}".format(value)
        
        elif units == "%":
            return "{:.2f}\%".format(100 * value)
        
        elif units[0] == "n":
            return "{:g} {}".format(value, units[2:])
        
        else:
            return value
        
        
    def save(self):
        """
        Saves the dataframe to the self.solved_file.

        Returns
        -------
        None.

        """
        if self.saved:
            return "Solved CSV already saved."
        
        self.saved = True
        self.df.to_csv(self.solved_file, index=False)
        return "Solved CSV file saved."
        
            
if __name__ == "__main__":
    #SE = ExerciseSolver(sys.argv[0])
    print("HEY\nJUST\nMAKING\nSURE\nNOPRINT")
    ### For testing
    this_directory = os.path.dirname(os.path.realpath(__file__))
    var_csv_path   = os.path.join(this_directory, "..", "problems", "variables.csv")
    SE = ExerciseSolver(dataFrame=pd.read_csv(var_csv_path))
    ###
    
    SE.solve_exercises()
