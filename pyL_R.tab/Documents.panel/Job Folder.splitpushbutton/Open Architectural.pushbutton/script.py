"""Opens Architectural folder of the current project where actual Revit file
(or Central model in case of a Workshared project) located.
"""

from System.Diagnostics import Process
from Autodesk.Revit.DB import ModelPathUtils
from pyrevit import revit

# Set folder separator & destination:
sep = 'Drawings'
target = '\Architectural'

# Checks whether separator in the Revit file path:
def checkSep(sep, fname):
    if sep in fname:
        return True
    else:
        print ("""
                File either not saved or is not located at relevant job folder.
                Check file location manually.
                """)
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
