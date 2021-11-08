import re

from PySide2 import (
    QtWidgets,
    QtCore,
    QtGui,
)


class ExpressionFormWidget(QtWidgets.QWidget):
    """ Form for filling up necessary fields in a TCL expression

        :param QtWidgets.QWidget: A subclass of QWidget
        :type QtWidgets.QWidget: PySide2 widget
    """
    def __init__(self, parent, data):
        """ Class constructor

            :param data: Incomming data from the Expression Tree Widget Item
            :type data: dict
        """
        QtWidgets.QWidget.__init__(self, parent=None)

        self.parent = parent
        self.required_fields = data['fields']['required']
        self.optional_fields = data['fields']['optional']

        self.result = {
            'required': {},
            'optional': {}
        }
        self.initUI()

    def initUI(self):
        """ Initialise the UI
        """
        layout = QtWidgets.QVBoxLayout()
        self.setLayout(layout)

        required_group_box = QtWidgets.QGroupBox()
        required_group_box.setTitle("Required Fields")
        required_group_box.setObjectName("required_group")

        required_main_layout = QtWidgets.QVBoxLayout()
        required_group_box.setLayout(required_main_layout)
        layout.addWidget(required_group_box)


        for required_field in self.required_fields:
            required_field_layout = QtWidgets.QHBoxLayout()

            required_field_label = QtWidgets.QLabel(
                "{}*:".format(required_field)
            )
            required_field_label.setObjectName("required_label")
            required_field_label.setFont(QtGui.QFont("Helvetica", 12))

            required_field_layout.addWidget(required_field_label)

            if "knob" in required_field:
                node_combo_box = QtWidgets.QComboBox()
                node_combo_box.setCursor(
                    QtGui.QCursor(QtCore.Qt.PointingHandCursor)
                )
                node_combo_box.addItems(
                    self.parent.nodes_and_knobs.keys()
                )
                node_combo_box.setCurrentIndex(-1)

                knob_combo_box = QtWidgets.QComboBox()
                knob_combo_box.setCursor(
                    QtGui.QCursor(QtCore.Qt.PointingHandCursor)
                )
                knob_combo_box.setEnabled(False)

                node_combo_box.currentTextChanged.connect(
                    lambda text, field=required_field, knob_cb=knob_combo_box:
                        self.onNodeComboBoxSelection(text, field, knob_cb)
                )

                knob_combo_box.currentTextChanged.connect(
                    lambda text, field=required_field:
                        self.onKnobComboBoxSelection(text, field)
                )

                required_field_layout.addWidget(node_combo_box)
                required_field_layout.addWidget(knob_combo_box)

            else:
                required_field_line_edit = QtWidgets.QLineEdit()
                required_field_line_edit.setPlaceholderText(required_field)
                required_field_line_edit.textChanged.connect(self.onLineEditChange)
                required_field_layout.addWidget(required_field_line_edit)

            required_main_layout.addLayout(required_field_layout)

            self.result['required'].update({required_field: None})

        if self.optional_fields:
            optional_group_box = QtWidgets.QGroupBox()
            optional_group_box.setTitle("Optional Fields")
            optional_group_box.setObjectName("optional_group")

            optional_main_layout = QtWidgets.QVBoxLayout()
            optional_group_box.setLayout(optional_main_layout)
            layout.addWidget(optional_group_box)


            for optional_field in self.optional_fields:
                optional_field_layout = QtWidgets.QHBoxLayout()

                optional_field_label = QtWidgets.QLabel(
                    "{}:".format(optional_field)
                )
                optional_field_label.setObjectName("optional_label")
                optional_field_label.setFont(QtGui.QFont("Helvetica", 12))

                optional_field_line_edit = QtWidgets.QLineEdit()
                optional_field_line_edit.textChanged.connect(
                    self.onLineEditChange
                )
                optional_field_line_edit.setPlaceholderText(optional_field)

                optional_field_layout.addWidget(optional_field_label)
                optional_field_layout.addWidget(optional_field_line_edit)

                optional_main_layout.addLayout(optional_field_layout)

                self.result['optional'].update({optional_field: None})


    def onLineEditChange(self, text):
        """ Method called when one of the field line edit is edited

            :param text: Signal from LineEdit
            :type text: str
        """
        emitter = self.sender()
        field = emitter.placeholderText()

        field_type = "required" if field in self.required_fields else "optional"

        self.result[field_type][field] = text if len(text) > 0 else None


    def onNodeComboBoxSelection(self, node_name, field, knob_combobox):
        """ Method called when a Node combobox gets a selection.
            Populates the following Knob combobox

            :param node_name: Name of the Node selected
            :type node_name: str
            :param field: Name of the associated Field
            :type field: str
            :param knob_combobox: The associated Knob QComboBox
            :type knob_combobox: PySide2 widget
        """
        knobs = self.parent.nodes_and_knobs[node_name]
        knob_combobox.addItems(knobs)
        knob_combobox.setCurrentIndex(-1)
        knob_combobox.setEnabled(True)

        self.result["required"][field] = node_name

    def onKnobComboBoxSelection(self, knob_name, field):
        """ Method called when a Knob combobox gets a selection.

            :param knob_name: Name of the Knob selected
            :type knob_name: str
            :param field: Name of the associated Field
            :type field: str
        """
        self.result["required"][field] += "." + knob_name

