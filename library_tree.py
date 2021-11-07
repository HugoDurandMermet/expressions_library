import json
import os
from functools import partial

from PySide2 import (
    QtWidgets,
    QtCore,
    QtGui
)

from common import (
    COLUMNS_SIZES,
    HEADERS_LIST,
)

from expression_form import ExpressionFormWidget
from utils import (
    openAlertDialog,
    getAllNodesAndKnobs
)

fonts = {
    'categories': QtGui.QFont("Helvetica", 14),
    'expressions': QtGui.QFont("Helvetica", 12, QtGui.QFont.Bold),
    'descriptions': QtGui.QFont("Helvetica", 12)
}

data_json_filepath = "{root}/resources/expressions_store.json".format(
    root=os.path.dirname(os.path.realpath(__file__))
)

waves_images_folder = "{root}/resources/waves_images/".format(
    root=os.path.dirname(os.path.realpath(__file__))
)


class LibraryTreeWidget(QtWidgets.QTreeWidget):
    """ The widget that will display all TCL expressions.

        :param QtWidgets.QTreeWidget: Our subclass of QTreeWidget
        :type QtWidgets.QTreeWidget: Pyside2 widget
    """
    def __init__(self, knob):
        """ Class constructor

            :param knob: Knob where the expression will be set
            :type knob: Nuke Object
        """
        QtWidgets.QTreeWidget.__init__(self)
        self.target_knob = knob
        self.nodes_and_knobs = getAllNodesAndKnobs()
        
        self.setColumnCount(len(HEADERS_LIST))

        for key in COLUMNS_SIZES.keys():
            self.setColumnWidth(key, COLUMNS_SIZES[key])

        self.setHeaderLabels(HEADERS_LIST)

        self.expressions_data = {}
        self.all_name_items = []

        self.loadData()
        self.initUI()


    def loadData(self):
        """ Loading all expressions saved in expressions_store.json
        """
        with open(data_json_filepath, "r") as read_file:
            self.expressions_data = json.load(read_file)


    def initUI(self):
        """ Initialising the UI and populating the tree widget
        """
        for category in self.expressions_data.keys():
            category_item = QtWidgets.QTreeWidgetItem(self)

            category_label = QtWidgets.QLabel(category)
            category_label.setObjectName("category_label")

            category_font = fonts['categories']
            category_font.setItalic(True)

            category_label.setFont(category_font)

            self.setItemWidget(category_item, 0, category_label)
            expressions = self.expressions_data[category]


            for name in expressions.keys():
                name_item = QtWidgets.QTreeWidgetItem(category_item)
                name_item.setExpanded(True)

                name_label = QtWidgets.QLabel(str(name))
                name_label.setWordWrap(True)
                name_label.setObjectName("name_label")
                name_label.setFont(QtGui.QFont("Helvetica", 14))
                self.setItemWidget(name_item, 0, name_label)

                expression = expressions[name]

                reference_data = "{name} {expression} {description}".format(
                    name=name,
                    expression=expression["expression"],
                    description=expression["description"]
                )
                name_item.setData(1, QtCore.Qt.ForegroundRole, reference_data)

                self.all_name_items.append(name_item)

                expression_item = QtWidgets.QTreeWidgetItem(name_item)
                expression_label = QtWidgets.QLabel(expression["expression"])
                expression_label.setWordWrap(True)
                expression_label.setObjectName("expression_label")
                expression_label.setFont(fonts['expressions'])
                
                self.setItemWidget(expression_item, 0, expression_label)

                if category == "Waves":
                    picture_path = waves_images_folder + expression["description"]
                    illustration_pixmap = QtGui.QPixmap(picture_path)
                    illustration_pixmap = illustration_pixmap.scaledToWidth(
                        500, QtCore.Qt.SmoothTransformation
                    )
                    
                    illustration_label = QtWidgets.QLabel(self)
                    illustration_label.setPixmap(illustration_pixmap)
                    illustration_label.setScaledContents(True)
                    
                    self.setItemWidget(expression_item, 1, illustration_label)
                else:
                    description_label = QtWidgets.QLabel(expression["description"])
                    description_label.setWordWrap(True)
                    description_label.setObjectName("description_label")
                    description_label.setFont(fonts['descriptions'])
                    
                    self.setItemWidget(expression_item, 1, description_label)

                generate_button = QtWidgets.QPushButton("Generate")
                generate_button.setObjectName("generate_button")

                
                


                if len(expression["example"]) > 1:
                    example_button = QtWidgets.QPushButton("Quick Example")
                    example_button.setObjectName("example_button")
                    example_button.clicked.connect(
                        partial(self.generate_expression, expression["example"])
                    )
                    self.setItemWidget(expression_item, 2, example_button)

                if expression.get("fields"):
                    form_item = QtWidgets.QTreeWidgetItem(name_item)
                    form_widget = ExpressionFormWidget(self, expression)

                    self.setItemWidget(form_item, 1, form_widget)
                    self.setItemWidget(form_item, 2, generate_button)
                    generate_button.clicked.connect(
                        partial(
                            self.generate_expression,
                            expression,
                            form_widget.result
                        )
                    )

                else:
                    generate_button.clicked.connect(
                        partial(self.generate_expression, expression)
                    )
                    self.setItemWidget(expression_item, 2, generate_button)

        self.sortItems(0, QtCore.Qt.AscendingOrder)
        self.setSortingEnabled(True)
        self.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.setFocusPolicy(QtCore.Qt.NoFocus)


    def generate_expression(self, data, form_values=None):
        """ Set a chosen expression in the target knob

            :param data: Original Data from Expression Item
            :type data: dict
            :param form_values: Data from Form Item, defaults to None
            :type form_values: dict, optional
        """
        expression = data['expression']
        field_operations = data['fields']['optional_operations']

        if form_values is not None:

            required_field_values = form_values['required']
            optional_field_values = form_values['optional']

            for required_key in required_field_values.keys():
                this_value = required_field_values[required_key]
                if this_value is None:
                    openAlertDialog("{} field is empty and required".format(
                        required_key
                    ))
                else:
                    expression = expression.replace(required_key, this_value)

            for optional_key in optional_field_values:
                for operation in field_operations:
                    if optional_key in operation:
                        this_operation = operation

                this_value = optional_field_values[optional_key]
                if this_value is None:
                    if this_operation in expression:
                        expression = expression.replace(this_operation, '')
                else:
                    expression = expression.replace(optional_key, this_value)


        self.target_knob.setExpression(expression)
        self.parent().exit_app()


    def search_items(self, terms):
        """ Search items in tree matching searching terms

            :param terms: Text emitted by Search Bar signal
            :type terms: str
        """
        terms_sequence = terms.lower().split()

        for item in self.all_name_items:
            parent_item = item.parent()


            if len(terms) > 0:
                reference_data = item.data(1, QtCore.Qt.ForegroundRole)
                reference_lower = reference_data.lower()

                checker = True

                for term in terms_sequence:
                    if term not in reference_lower:
                        checker = False

                if checker:
                    item.setHidden(False)
                    parent_item.setExpanded(True)

                else:
                    item.setHidden(True)

            else:
                item.setHidden(False)
                parent_item.setExpanded(False)


