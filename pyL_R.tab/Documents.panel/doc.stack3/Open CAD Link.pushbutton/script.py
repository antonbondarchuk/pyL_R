"""Opens selected CAD link instance in AutoCAD 2018.
Processes only single CAD file link at a time.
"""
import os
from Autodesk.Revit.DB import ExternalFileUtils, ModelPathUtils
from pyrevit import revit, forms

# autoCADpath = 'C:\\Program Files\\Autodesk\\AutoCAD 2018\\acad.exe'
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
    pass