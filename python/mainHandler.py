from contentHandler import ContentHandler

class MainHandler(ContentHandler):

    def __init__(self, parent=None):
        ContentHandler.__init__(self)


    def current_chapter(self):
        """
        Returns
        -------
        int
            SEA chapter number (international edition).
        """
        return self.spinBox_chapter.value()

    def current_problem(self):
        """
        Returns
        -------
        int
            SEA problem number (international edition).
        """
        return self.spinBox_problem.value()

    def current_book(self):
        """
        Returns
        -------
        str
            'SEA' or 'STEA'
        """
        return self.comboBox_book.currentText()

    def update_labels(self):
        """
        Updates the text in the exercise and solution labels.
        
        Returns
        -------
        None.
        
        """
        self.label_exercise.setText(self.get_exercise_text(
            self.current_chapter(), self.current_problem(), self.current_book()))
        
        self.label_solution.setText(self.get_solution_text(
            self.current_chapter(), self.current_problem(), self.current_book()))
        
        self.update_statusbar()

    def update_statusbar(self):
        """
        Updates the status bar of the main window.

        Returns
        -------
        None.
        
        """
        self.statusbar.showMessage("Viewing Exercise {:0>2d}.{:0>2d} from {}".format(
            self.current_chapter(), self.current_problem(), self.current_book()))
        
    def show_status_message(self, message):
        """
        Update the statusbar with a specific message.

        Parameters
        ----------
        message : string
            The message to show on the statusbar.

        Returns
        -------
        None.

        """
        print(message)
        self.statusbar.showMessage(message)
        

    def update_tables(self):
        """
        Updates the exercise and solution table views to show the variables.

        Returns
        -------
        None.
        
        """
        self.tableView_variables.clearSpans()
        self.tableView_variables.setModel(self.get_variable_model(
            self.current_chapter(), self.current_problem(), self.current_book()))
        self.tableView_variables.resizeColumnsToContents()
        