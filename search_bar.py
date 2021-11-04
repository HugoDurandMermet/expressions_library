from PySide2 import (
    QtWidgets,
)



class SearchBar(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)

        layout = QtWidgets.QHBoxLayout()
        self.setLayout(layout)

        self.line_edit = QtWidgets.QLineEdit()
        self.line_edit.setPlaceholderText("Search expression here...")

        layout.addWidget(self.line_edit)


