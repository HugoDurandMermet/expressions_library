import nuke


def getCurrentKnob():
    """ Gives the current knob in focus within the Nuke GUI

        :return: Knob
        :rtype: Nuke Object
    """
    return nuke.thisKnob()


def openAlertDialog(message):
    """ Opens an alert Dialog box on Nuke

        :param message: Alert message
        :type message: str
    """
    nuke.alert(message)