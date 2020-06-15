import glob
import os
import re

import pandas as pd

from pandasModel import PandasModel
from exerciseSolver import ExerciseSolver


class ContentHandler:
    def __init__(self, parent=None):        
        self.problems_filenames        = "problems*.tex"
        self.variables_filename        = "variables.csv"
        self.variables_solved_filename = "variables_solved.csv"
        self.template_path = os.path.join(self.qpe_directory, "..", "problems")

        self.excel_sol_header  = "excel_solution"
        self.latex_header      = "latex_{}"
        self.manual_sol_header = "igps_solution"
        self.units_header      = "units"
        self.variable_header   = "ch_pr_var"
        self.visible_columns   = [
            self.variable_header,
            self.excel_sol_header,
            self.manual_sol_header
        ]
        
        self.df = pd.read_csv(os.path.join(self.template_path, self.variables_filename))
        self.exercise_solver = ExerciseSolver(
            dataFrame=self.df, latex_header=self.latex_header, 
            units_header=self.units_header, variable_header=self.variable_header)

        self.regex_variable = re.compile("\\\\V{"r'\S*'"}")
        self.exercise_text  = {}
        self.solution_text  = {}
        self.set_texts()

    def get_exercise_text(self, chapter, problem, book):
        """
        Gets the string of exercise text.

        Returns
        -------
        string
            The exercise text, identified using regex from the *.tex files.
        
        """
        try:
            return re.sub(
                self.regex_variable, 
                lambda match: self.replace_variable(match.group(), book), 
                self.exercise_text[self.get_problem_formatted(chapter, problem)])
        
        except Exception as e:
            error = "Exercise {:0>2d}.{:0>2d} is not available.\n{}".format(chapter, problem, e)
            print(error)
            return error

    def get_solution_text(self, chapter, problem, book):
        """
        Gets the string of solution text.

        Returns
        -------
        string
            The solution text, identified using regex from the latex files.
        
        """
        try:
            return re.sub(
                self.regex_variable, 
                lambda match: self.replace_variable(match.group(), book), 
                self.solution_text[self.get_problem_formatted(chapter, problem)])

        except Exception as e:
            error = "Solution {:0>2d}.{:0>2d} is not available.\n{}".format(chapter, problem, e)
            print(error)
            return error

    def solve_exercises(self):
        """
        Uses the exerciseSolver to solve exercises and return feedback.

        Returns
        -------
        feedback : string
            Exercise solution status.

        """
        self.df, feedback = self.exercise_solver.solve_exercises()
        return feedback
        
    def save_exercises(self):
        """
        Saves the calculated variables to the solved CSV file and returns feedback.

        Returns
        -------
        string
            Solved CSV file save status.

        """
        return self.exercise_solver.save()

    def replace_variable(self, string, book):
        """
        Converts the input variable string into the appropriate value based on the book arg.

        Returns
        -------
        string
            The variable value, based on book, unless exception, then just return variable tag string.
        
        """
        variable = string[3: -1]
        try:
            return str(self.df.loc[self.df[self.variable_header] == variable, book].iloc[0])
        except:
            return variable

    def get_variable_model(self, chapter, problem, book):
        """
        Gets the pandas DataFrame of relevant variables.

        Returns
        -------
        pandas.DataFrame
            Relevant variabes, designated by self.visible_columns.
        
        """
        df_variables = self.df[self.df[self.variable_header].str.contains(
            self.get_problem_formatted(chapter, problem))]
        df_columns   = df_variables.loc[:, [self.latex_header.format(book)] + self.visible_columns]
        return PandasModel(df_columns)
            
    def get_problem_formatted(self, chapter, problem, book=None):
        """
        Gets the standard exercise tag string.

        Returns
        -------
        string
            The standard tag used to identify exercises.
            Format of "CH_PR" or "CH_PR_{SEA/STEA}" depending on whether or not book is given.
        
        """
        if book is not None:
            return "{:0>2d}-{:0>2d}-{}".format(chapter, problem, book)
        else:
            return "{:0>2d}-{:0>2d}".format(chapter, problem)

    def get_problem_tag_from_label(self, exercise):
        """
        Gets the standard exercise tag by reading the \\label from the latex text.

        Returns
        -------
        string
            The standard tag used to identify exercises.
        
        """
        chapter, problem = self.read_label(exercise)
        return "{}-{}".format(chapter, problem)

    def read_label(self, exercise):
        """
        Reads the chapter and problem from the \\label tag from the latex text.

        Returns
        -------
        string, string
            Chapter, Problem 
        
        """
        regex_exercise_label = re.compile("(?<=\\\\label{)"r'\S*'"(?=})")
        exercise_label       = re.findall(regex_exercise_label, exercise)

        if exercise_label == []:
            return "", ""
        
        exercise_label = exercise_label[0]
        return exercise_label[4:6], exercise_label[7:9]

    def set_texts(self):
        """
        Populate the exercise and solution dictionaries with text per problem tag.

        Returns
        -------
        None.
        
        """
        regex_exercise_full = re.compile("    \\\\begin\{exercise\}"r'.*?'"\\\\end\{solution\}", re.DOTALL)
        regex_exercise      = re.compile("(?<=    \\\\begin\{exercise\})"r'.*?'"(?=\\\\end\{exercise\})", re.DOTALL)
        regex_solution      = re.compile("(?<=    \\\\begin\{solution\})"r'.*?'"(?=\\\\end\{solution\})", re.DOTALL)

        # for problems_file in glob.glob(os.path.join(self.template_path, self.problems_filenames))
        for exercise_file in glob.glob(os.path.join(self.template_path, "problems08.tex")):
            with open(exercise_file, "r", encoding="utf8") as file:
                for ex in [ex for ex in re.findall(regex_exercise_full, file.read())]:
                    try:
                        problem_tag = self.get_problem_tag_from_label(ex)
                        self.exercise_text[problem_tag] = re.findall(regex_exercise, ex)[0]
                        self.solution_text[problem_tag] = re.findall(regex_solution, ex)[0]
                    except Exception as e:
                        print("Error reading problem from file {}.\n{}".format(exercise_file, e))
                        continue         
