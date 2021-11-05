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
    def __init__(self, data):
        """ Class constructor

            :param data: Incomming data from the Expression Tree Widget Item
            :type data: dict
        """
        QtWidgets.QWidget.__init__(self)
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

            required_field_line_edit = QtWidgets.QLineEdit()
            required_field_line_edit.setPlaceholderText(required_field)
            required_field_line_edit.textChanged.connect(self.onLineEditChange)

            required_field_layout.addWidget(required_field_label)
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
        key = emitter.placeholderText()

        field_type = "required" if key in self.required_fields else "optional"

        self.result[field_type][key] = text if len(text) > 0 else None

