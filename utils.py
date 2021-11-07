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
    

def getAllNodesAndKnobs():
    """ Get all nodes and knobs from current node graph

        :param result: Data with all nodes and their knobs
        :type result: dict
    """
    result = {}
    nodes = nuke.allNodes()

    for node in nodes:
        node_name = node['name'].value()
        knobs = node.knobs().keys()
        result.update({node_name: knobs})
        
    return result