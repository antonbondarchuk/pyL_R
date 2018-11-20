"""Creates folder structure in the current 'Structural' job folder. 
Copies 'Transmittal.xlsx' from K:\\ drive into working job folder.
Run this tool after job initiated and Revit file saved to relevant destination.
"""

import os
import shutil

from Autodesk.Revit.DB import ModelPathUtils
from pyrevit import revit, forms

# Set folder separator & destination:
sep = 'Drawings'
target = r'\\Structural'

# Transmittal file location:
trans = r'K:\\Revit\\Document Transmittal.xls'

def mkFolder(fpath, folder, subfolder):
    [os.mkdir(fpath + i) for i in folder]
    [os.mkdir(fpath + '\\3_CURRENT' + j) for j in subfolder]

# Checks whether separator in the Revit file path:
def checkSep(sep, fname):
    if sep in fname:
        return True
    else:
        forms.alert("""
                File either not saved or is not located at relevant job folder.
                Check file location.
                """)

destFolder = ['\\1_CIVIL',
        '\\2_ISSUED',
        '\\3_CURRENT',
        '\\4_SKETCHES',
        '\\5_XREF',
        '\\6_MISC']

destSubfolder = ['\\1_CURRENT PDF',
            '\\2_CURRENT CAD',
            '\\3_CURRENT RVT']



# Checks if the file is workshared. Will follow Central model location.
# Otherwise will create job folder from PathName property
if revit.doc.IsWorkshared:
    fname = ModelPathUtils. \
        ConvertModelPathToUserVisiblePath( \
        revit.doc.GetWorksharingCentralModelPath() \
        )
    if checkSep(sep, fname):
        fpath = fname.split(sep)
        strFolder = fpath[0] + sep + target
        try:
            mkFolder(strFolder, destFolder, destSubfolder)
            shutil.copyfile(trans, strFolder + '\\' + revit.doc.Title[:6] + '-TRANS-STR.xls')
            forms.alert('Job folder structure created successfully!')
        except:
            forms.alert('Something went wrong. Create folder structure manually.')
else:
    fname = revit.doc.PathName
    if checkSep(sep, fname):
        fpath = fname.split(sep)
        strFolder = fpath[0] + sep + target
        try:
            mkFolder(strFolder, destFolder, destSubfolder)
            shutil.copyfile(trans, strFolder + '\\' + revit.doc.Title[:6] + '-TRANS-STR.xls')
            forms.alert('Job folder structure created successfully!')
        except:
            forms.alert('Something went wrong. Create folder structure manually.')