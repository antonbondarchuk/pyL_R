"""Isolates Structural elements by their Structural Material in current view.
"""

from Autodesk.Revit.DB import FilteredElementCollector
from Autodesk.Revit.DB.Structure import (StructuralMaterialTypeFilter,
                                        StructuralMaterialType)
from pyrevit import revit, forms
from pyrevit import forms


options = sorted(['Steel',
                'Concrete',
                'Wood',
                'Other',
                'PrecastConcrete',
                'Generic',
                'Aluminum'])

selected_switch = \
forms.CommandSwitchWindow.show(options,
                        message='Isolate only elements of Structural Material:')



try:
    strMatType = 'StructuralMaterialType.' + selected_switch
    matfilter = StructuralMaterialTypeFilter(eval(strMatType))
    
    if selected_switch:
        isolateElems = FilteredElementCollector(revit.doc). \
                        WherePasses(matfilter). \
                        ToElementIds()
    with revit.Transaction('Isolate in view'):
        revit.doc.ActiveView.IsolateElementsTemporary(isolateElems)
except:
    forms.alert('Oops..Something went wrong.\nIsolate elements manually.')