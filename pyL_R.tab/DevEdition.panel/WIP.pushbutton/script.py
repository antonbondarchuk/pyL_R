import clr
clr.AddReference("Microsoft.Office.Interop.Excel")
from Microsoft.Office.Interop import Excel

from System import Array
import itertools

from Autodesk.Revit.DB import ModelPathUtils
from pyrevit import revit, forms
from rpw import db

if revit.doc.IsWorkshared:
    wrshared = revit.doc.GetWorksharingCentralModelPath()
    model_path = ModelPathUtils.ConvertModelPathToUserVisiblePath(wrshared)
else:
    model_path = revit.doc.PathName

docLoc = model_path.split(revit.doc.Title)
docNum = revit.doc.ProjectInformation.Number

sh = db.Collector(of_class='ViewSheet', is_not_type=True, \
                where=lambda x: x.Name == 'Starting View'). \
                get_first()

try:
    ex = Excel.ApplicationClass()
    ex.Visible = True
    wb = ex.Workbooks.Open(docLoc[0] + docNum + '-TRANS-STR.xls')
except:
    ex.Visible = False
    forms.alert('Oops.. Something went wrong.\nCheck if {0} Excel transmittal file exists or has correct file name'.format(revit.doc.Title))

wk = wb.ActiveSheet

# Fills up General Info part
wk.Range["C3"] = docNum
wk.Range["C4"] = revit.doc.ProjectInformation.Name
wk.Range["C5"] = revit.doc.ProjectInformation.ClientName
wk.Range["C6"] = '1 OF 1'
wk.Range["C7"] = sh.LookupParameter('Client Representative').AsString()

# Drawings numbers and Drawing Names:
drNums = [el.SheetNumber \
        for el in db.Collector(of_class='ViewSheet', \
        is_not_type=True, \
        where=lambda x: x.IsPlaceholder==False and \
        x.LookupParameter("Appears In Sheet List").AsInteger()==1)]

drNames = [el.ViewName \
        for el in db.Collector(of_class='ViewSheet', \
        is_not_type=True, \
        where=lambda x: x.IsPlaceholder==False and \
        x.LookupParameter("Appears In Sheet List").AsInteger()==1)]

drgs = zip(drNums, drNames)
drgs.sort()

# Initialises 2D Array of SheetNumbers & SheetNames and fills up Excel workbook:
arr = Array.CreateInstance(str, len(drNums), 2)

for i in range(0, len(drNums)):
    arr[i, 0] = drgs[i][0]
    arr[i, 1] = drgs[i][1]

wk.Range["B14", "C41"].Value2 = arr
