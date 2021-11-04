import nuke


def getCurrentKnob():
    """ Gives the current knob in focus within the Nuke GUI

        :return: Knob
        :rtype: Nuke Object
    """
    return nuke.thisKnob()

