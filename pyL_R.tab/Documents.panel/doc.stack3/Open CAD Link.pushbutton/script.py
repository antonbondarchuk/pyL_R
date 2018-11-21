"""Opens selected CAD link instance with system default AutoCAD version.
Processes only single CAD file link at a time.
"""

import os
from Autodesk.Revit.DB import ExternalFileUtils, ModelPathUtils
from pyrevit import revit, forms

el = revit.get_selection().first

if el != None and el.GetType().FullName == 'Autodesk.Revit.DB.ImportInstance':
    cadLink = revit.doc.GetElement(el.GetTypeId())
    cadRef = ExternalFileUtils.GetExternalFileReference(revit.doc, cadLink.Id)
    fpath = ModelPathUtils.ConvertModelPathToUserVisiblePath(cadRef.GetAbsolutePath())
else:
    forms.alert('One CAD link instance must be selected')

try:
    os.startfile(fpath)
except:
    forms.alert('Oops..Something went wrong.\nOpen CAD link manually')