"""Opens Structural folder of the current project where actual Revit file
(or Central model if Workshared) located.
"""

from System.Diagnostics import Process
from Autodesk.Revit.DB import ModelPathUtils
from pyrevit import revit, forms

# Set folder separator & destination:
sep = 'Drawings'
target = '\Structural'

# Checks whether separator in the Revit file path:
def checkSep(sep, fname):
    if sep in fname:
        return True
    else:
        forms.alert('Oops..Something went wrong.\nFile either not saved or is not located at relevant job folder.\nCheck file location manually.')
        
# Checks if the file is workshared. Will follow Central model location.
# Otherwise opens single file folder location
if revit.doc.IsWorkshared:
    mdPath = revit.doc.GetWorksharingCentralModelPath()
    fname = ModelPathUtils.ConvertModelPathToUserVisiblePath(mdPath)
    if checkSep(sep, fname):
        fpath = fname.split(sep)
        strFolder = fpath[0] + sep + target
        Process.Start(strFolder)
else:
    fname = revit.doc.PathName
    if checkSep(sep, fname):
        fpath = fname.split(sep)
        strFolder = fpath[0] + sep + target
        Process.Start(strFolder)
