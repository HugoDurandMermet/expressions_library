import os

from PySide2 import (
    QtWidgets,
    QtCore
)

from library_tree import LibraryTreeWidget
from search_bar import SearchBar
from utils import getCurrentKnob



qss_filepath = "{root}/style.qss".format(
    root=os.path.dirname(os.path.realpath(__file__))
)


class ExpressionsLibraryWidget(QtWidgets.QDialog):
    """ Main Dialog class.

        :param QtWidgets.QDialog: Our dialog subclass
        :type QtWidgets.QDialog: Pyside2 Widget
    """
    def __init__(self, parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        
        self.setWindowTitle("Expressions Library")
        self.resize(1300, 550)
        self.layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.layout)

        with open(qss_filepath, "r") as f:
            style = f.read()
            self.setStyleSheet(style)

        current_knob = getCurrentKnob()

        search_widget = SearchBar()
        tree_widget = LibraryTreeWidget(knob=current_knob)

        search_widget.line_edit.textChanged.connect(tree_widget.search_items)

        self.layout.addWidget(search_widget)
        self.layout.addWidget(tree_widget)
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)

    def exit_app(self):
        """ Close the dialog
        """
        self.close()


if __name__ == "__main__":
    elWidget = ExpressionsLibraryWidget()
    elWidget.show()