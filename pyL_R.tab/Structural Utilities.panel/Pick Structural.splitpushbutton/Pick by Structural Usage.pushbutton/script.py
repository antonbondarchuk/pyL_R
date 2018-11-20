"""Activates selection tool that picks specific structural usage of
Structural Framing elements (e.g. Girders, Joists, Bracing, etc.)

"""

from pyrevit.framework import List
from pyrevit import revit, DB, UI
from pyrevit import forms


selection = revit.get_selection()

class PickByCategorySelectionFilter(UI.Selection.ISelectionFilter):
    def __init__(self, catname, str_usage):
        self.category = catname
        self.strusage = str_usage

    # standard API override function
    def AllowElement(self, element):
        if self.category in element.Category.Name:
            if self.strusage in element.StructuralUsage.ToString():
                return True
            else:
                return False

    # standard API override function
    def AllowReference(self, refer, point):
        return False


def pickbycategory(catname, str_usage):
    try:
        msfilter = PickByCategorySelectionFilter(catname, str_usage)
        selection_list = revit.pick_rectangle(pick_filter=msfilter)
        filtered_list = []
        for el in selection_list:
            filtered_list.append(el.Id)
        selection.set_to(filtered_list)
    except Exception:
        pass

options = sorted(['Girder',
                'Joist',
                'Purlin',
                'Other',
                'Brace',
                'HorizontalBracing',
                'KickerBracing',
                'TrussChord',
                'TrussWeb'])

selected_switch = \
forms.CommandSwitchWindow.show(options,
                               message='Pick only elements of type:')

if selected_switch:
    pickbycategory('Structural Framing', selected_switch)
