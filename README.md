# Expressions Library

## Disclaimer

The following version was tested on Nuke 12v2.3.

Tests made on Nuke 11 were unsuccessful and resulted in segmentation faults.

## Quick Start

Copy the repo in a folder that will be recognised by your `NUKEPATH` (check within your `init.py`)

Inside your `menu.py`, add the following command:

```
nuke.menu('Animation').addCommand('Expressions Library', 'from expressions_library.dialog import ExpressionsLibraryWidget;el_widget = ExpressionsLibraryWidget();el_widget.show()')
```
And you should be all set to go.

## Instructions

Make a right click on a knob inside Nuke, and when the context menu opens you should see the following option:

![screenshot of context menu](./resources/documentation_images/on_context_menu.png)

Click on it and a dialog will pop up, divided in four main categories for all saved TCL expressions.

![screenshot of dialog opened](./resources/documentation_images/dialog_opened.png)

For each expression, you should find a description, a fields form if the expression receives arguments, and a Generate Button.

![screenshot of dialog on a knob expression](./resources/documentation_images/dialog_on_combobox.png)

If the expression targets a Knob or a Node within Nuke, the usual text form will be traded for two dropdown menus, one listing all Nodes in the current script, the other listing all Knobs for the Node selected in the previous menu.

![screenshot of dialog on waves](./resources/documentation_images/dialog_on_waves.png)

The Waves category is a bit of an outlier:
as depicted in the screenshot, the text description has been swaped for an illustration of the type of animation curve produced by the expression.

![screenshot of dialog on search](./resources/documentation_images/dialog_on_search.png)

Finally the Search Bar on top of the dialog will filter all expressions to find only the ones which descriptions or formulas match the terms typed.
