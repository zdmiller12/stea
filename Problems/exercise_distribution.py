"""
  Script reads problems from the current directory and distributes them,
based on dictionary in exercise_map.py to the /sea/ & /stea/ subdirectories.
"""

def exercise_distribution(EM):
    books = ["SEA", "STEA"]
    chapter_max_N = 21
    match_dict = {
        "exercise_files" : "problems*.tex",
        "exercise_full"  : re.compile("    \\\\begin\{exercise\}"r'.*?'"\\\\end\{solution\}", re.DOTALL),
        "exercise_label" : re.compile("(?<=\\\\label{)"r'\S*'"(?=})")
    }

    for book in books:
        remove_old_files(book, match_dict)
        create_new_files(book, chapter_max_N)
        distribute_exercises(book, match_dict, EM)
        write_file_closing(book, match_dict)

def remove_old_files(book, match_dict):
    files = glob.glob(os.path.join(book.lower(), match_dict["exercise_files"]))
    for file in files:
        os.remove(file)

def create_new_files(book, chapter_max_N):
    header0 = "%%%%%%%%%%%%%%%%%%%%"
    header1 = "%% {} CHAPTER {:0>2d} %%"
    header2 = "%%% do not edit %%%%"
    header3 = "\\begin{exercises}"
    write_file_heading(book, chapter_max_N, header0, header1, header2, header3)

def write_file_heading(book, chapter_max_N, header0, header1, header2, header3):
    for i in range(1, 1 + chapter_max_N):
        output_file = os.path.join(book.lower(), "problems{:0>2d}.tex".format(i))
        header = header1.format(book, i)
        f = open(output_file, "w", encoding="utf-8")
        f.write("{}\n{}\n{}\n{}\n\n{}\n".format(header0, header, header2, header0, header3))
        f.close()

def distribute_exercises(book, match_dict, EM):
    for exercise_file in glob.glob(match_dict["exercise_files"]):
        with open(exercise_file, "r", encoding="utf8") as file:
            text = file.read()
            exercises = [ex for ex in re.findall(match_dict["exercise_full"], text)]
            
            for exercise in exercises:
                full_label, chapter, problem = read_label(exercise, match_dict)

                if (book == "STEA") and (full_label in EM.keys()):
                    new_chapter = "{:0>2d}".format(EM[full_label])
                else:
                    new_chapter = chapter

                output_file = os.path.join(book.lower(), "problems{}.tex".format(new_chapter))
                f = open(output_file, "a", encoding="utf-8")
                f.write("\n\n{}".format(exercise))
                f.close()

def read_label(exercise, match_dict):
    exercise_label = re.findall(match_dict["exercise_label"], exercise)
    if exercise_label == []:
        return "", ""
    exercise_label = exercise_label[0]
    return exercise_label, exercise_label[4:6], exercise_label[7:9]


def write_file_closing(book, match_dict):
    for new_exercise_file in glob.glob(os.path.join(book.lower(), match_dict["exercise_files"])):
        f = open(new_exercise_file, "a", encoding="utf-8")
        f.write("\n\\end{exercises}")
        f.close()

if __name__ == '__main__':

    import os, glob, re
    from exercise_map import EXERCISE_MAP as EM

    exercise_distribution(EM)
