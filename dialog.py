import os

from PySide2 import (
    QtWidgets,
    QtCore
)

from library_tree import LibraryTreeWidget
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
            _style = f.read()
            self.setStyleSheet(_style)

        current_knob = getCurrentKnob()

        tree_widget = LibraryTreeWidget(knob=current_knob)

        self.layout.addWidget(tree_widget)
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)


if __name__ == "__main__":
    elWidget = ExpressionsLibraryWidget()
    elWidget.show()