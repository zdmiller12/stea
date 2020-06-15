"""
Script reads problems from the current directory and distributes them,
based on dictionary in exercise_map.py to the subdirectories
    self.path_to_problems + /sea/ 
    & 
    self.path_to_problems + /stea/
"""

import glob
import os
import re

from exerciseMap import EXERCISE_MAP


class ExerciseDistribution:
    def __init__(self, books=["SEA", "STEA"], exercise_map={}, parent=None):
        self.exercise_map     = exercise_map
        self.books            = books
        self.chapter_max_N    = 21
        self.path_to_problems = "../problems"
        self.match_dict       = {
            "exercise_files" : "problems*.tex",
            "exercise_full"  : re.compile("    \\\\begin\{exercise\}"r'.*?'"\\\\end\{solution\}", re.DOTALL),
            "exercise_label" : re.compile("(?<=\\\\label{)"r'\S*'"(?=})")
        }
        
    def distribute(self):
        """
        Removes old script-generated files, creates new ones, and distributes
        exercises according to the self.exercise_map.

        Returns
        -------
        None.

        """
        for book in self.books:
            self.remove_old_files(book)
            self.create_new_files(book)
            self.distribute_exercises(book)
            self.write_file_closing(book)
        print("Exercises distributed.")
    
    def remove_old_files(self, book):
        """
        Remove old script-generated *.tex files.

        Parameters
        ----------
        book : string
            Either "SEA" or "STEA", for whichever subdirectory is current.

        Returns
        -------
        None.

        """
        files = glob.glob(os.path.join(self.path_to_problems, book, 
                                       self.match_dict["exercise_files"]))
        
        for file in files:
            os.remove(file)
    
    def create_new_files(self, book):
        """
        Creates new *.tex files and write a standard header to each.

        Parameters
        ----------
        book : string
            Either "SEA" or "STEA", for whichever files are being created.

        Returns
        -------
        None.

        """
        header0 = "%%%%%%%%%%%%%%%%%%%%"
        header1 = "% {} CHAPTER {:0>2d} "
        header2 = "%%% do not edit %%%%"
        header3 = "\\begin{exercises}"
        self.write_file_heading(book, header0, header1, header2, header3)
    
    def write_file_heading(self, book, header0, header1, header2, header3):
        """
        Write file headings to new *.tex files.

        Parameters
        ----------
        book : string
            Either "SEA" or "STEA", for whichever headers are being written.
        header0 : string
            First header line.
        header1 : string
            Second header line.
        header2 : string
            Third header line.
        header3 : string
            Fourth header line.

        Returns
        -------
        None.

        """
        for i in range(1, 1 + self.chapter_max_N):
            output_file = os.path.join(self.path_to_problems, book, 
                                       "problems{:0>2d}.tex".format(i))
            
            header = header1.format(book, i)
            f = open(output_file, "w", encoding="utf-8")
            f.write("{}\n{}\n{}\n{}\n\n{}".format(header0, header, header2, header0, header3))
            f.close()
    
    def distribute_exercises(self, book):
        """
        Assigns each exercise from the template *.tex files to the appropriate
        *.tex file within "SEA" or "STEA" subdirectories.

        Parameters
        ----------
        book : string
            Either "SEA" or "STEA", for whichever subdirectory is current.

        Returns
        -------
        None.

        """
        for exercise_file in glob.glob(os.path.join(self.path_to_problems,
                                                    self.match_dict["exercise_files"])):
            with open(exercise_file, "r", encoding="utf8") as file:
                text = file.read()
                exercises = [ex for ex in re.findall(self.match_dict["exercise_full"], text)]
                for exercise in exercises:
                    full_label, chapter, problem = self.read_label(exercise)
    
                    if (book == "STEA") and (full_label in self.exercise_map.keys()):
                        if self.exercise_map[full_label] == 0:
                            continue
                        new_chapter = "{:0>2d}".format(self.exercise_map[full_label])
                    else:
                        new_chapter = chapter
    
                    output_file = os.path.join(self.path_to_problems, book,
                                               "problems{}.tex".format(new_chapter))
                    f = open(output_file, "a", encoding="utf-8")
                    f.write("\n\n{}".format(exercise))
                    f.close()
    
    def read_label(self, exercise):
        """
        Reads the label from the exercise string block to determine the
        chapter and problem.

        Parameters
        ----------
        exercise : string
            The entire block of string defining the exercise and solution.

        Returns
        -------
        string, string, string
            The full exercise "tag", the 2-digit chapter, and the 2-digit problem.

        """
        exercise_label = re.findall(self.match_dict["exercise_label"], exercise)
        
        if exercise_label == []:
            return "", ""
        
        exercise_label = exercise_label[0]
        return exercise_label, exercise_label[4:6], exercise_label[7:9]          
    
    def write_file_closing(self, book):
        """
        Write file closings to each new *.tex file and close.

        Parameters
        ----------
        book : string
            Either "SEA" or "STEA", for whichever subdirectory is current.

        Returns
        -------
        None.

        """
        for exercise_file in glob.glob(os.path.join(self.path_to_problems, book, 
                                                    self.match_dict["exercise_files"])):
            f = open(exercise_file, "a", encoding="utf-8")
            f.write("\n\\end{exercises}")
            f.close()


if __name__ == "__main__":
    ED = ExerciseDistribution(exercise_map=EXERCISE_MAP)
    ED.distribute()
