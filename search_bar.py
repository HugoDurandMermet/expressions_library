from PySide2 import (
    QtWidgets,
)



class SearchBar(QtWidgets.QWidget):
    """ Widget acting as our main search bar

        :param QtWidgets.QWidget: Subclass of QWidget
        :type QtWidgets.QWidget: PySide2 widget
    """
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)

        layout = QtWidgets.QHBoxLayout()
        self.setLayout(layout)

        self.line_edit = QtWidgets.QLineEdit()
        self.line_edit.setPlaceholderText("Search expression here...")

        clear_button = QtWidgets.QPushButton("Clear")
        clear_button.clicked.connect(self.clear)

        layout.addWidget(self.line_edit)
        layout.addWidget(clear_button)

    def clear(self):
        """ Reset the search bar
        """
        self.line_edit.setText("")


