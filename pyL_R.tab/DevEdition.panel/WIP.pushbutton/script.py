import pyrevit

def pickface():
    picked = pyrevit.ui.Selection.PickObject(ObjectType.Face)
    el = pyrevit.doc.GetElement(picked).GetGeometryObjectFromReference(picked)
    return el

def pickline():
    picked = pyrevit.ui.Selection.PickObject(ObjectType.Element)
    el = pyrevit.doc.GetElement(picked)
    return el.GeometryCurve

def project(line, face):
    ep0 = line.GetEndPoint(0)
    ep1 = line.GetEndPoint(1)
    res = Line.CreateBound( \
    face.Project(ep0).XYZPoint, face.Project(ep1).XYZPoint)
    return res

line = pickline()
face = pickface()

l = db.Collector(of_class='Level').get_first()
bType = db.Collector(of_category='Structural Framing', is_type=True).get_first()

p_line = project(line, face)

with db.Transaction('test'):
    doc.Create.NewFamilyInstance(p_line, bType, l, StructuralType.Beam)