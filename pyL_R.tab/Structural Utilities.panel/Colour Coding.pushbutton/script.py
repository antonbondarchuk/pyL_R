"""Visual audit tool that does the following:
- Creates new '_ColourCode' 3D view & applies '_ColourCode' template to this view (Manage view template visibility graphics to filter certain structural categories if needed);
- Randomly overrides surface pattern for structural elements in the _ColourCode view based on their respective family type (intentionally works for Structural Framing, Structural Column & Structural Foundations categories only);
- Creates '_ColourCodeLegend' Drafting View to explain colour coding palette.

"""

from random import randint
from System.Collections.Generic import List
from Autodesk.Revit.DB import (ElementId, CurveLoop, Line, XYZ, FilledRegion,
                    ElementTypeGroup, TextNoteOptions, TextNote,
                    View3D, ViewFamily, ViewDrafting,
                    Color, OverrideGraphicSettings,
                    ElementTransformUtils)

from pyrevit import revit, forms
from rpw import db


def grouped(instance, symbol):
    """Groups element family types to list of elements visible in active view
    that share same family type.
    Returns dict().

    symbol:     FamilySymbol    - Family type () of group
    instance:   list    - Elements of FamilyInstance type that will be grouped                      based on FamilySymbol (key)
    """

    res = {}
    for key in symbol:
        for val in instance:
            if val.Symbol.Id == key.Id:
                res.setdefault(key.Id, []).append(val.Id)
    return res

def randcolour(t):
    """Returns list of tuples of random rgb values to pass into colouring function. Number of tuples equals len of list (t).

     """

    res = []
    for i in range(len(t)):
        r=randint(0,256)
        g=randint(0,256)
        b=randint(0,256)
        res.append((r, g, b))
    return res

def colouring(group, pattern, vw):
    """Randomly overrides surface pattern for elements in provided view
    based on their respective FamilySymbol. Commits Transaction.

    Returns list of tuples (rgb, FamilySymbol) where:
        rgb    - tuple of int values for RGB colour representation (e.g. (0,0,0)       for Black)

    group:  dict() of FamilySymbol:[FamilyInstances] pairs.
    """
    
    rgb = randcolour(group.values())
    res = zip(rgb, group.values())
    for color, elem in res:
        with db.Transaction('Graphic _ColourCoding Overrides'):
            ogs = OverrideGraphicSettings(). \
                SetProjectionFillColor(Color(color[0], color[1], color[2]))
            ogs.SetProjectionFillPatternId(pattern[0])
            map(lambda x: vw.SetElementOverrides(x, ogs), elem)

    return zip(rgb, group.keys())

# Creates '_ColourCode' 3D view & new '_ColourCodeLegend' drafing view:
threeDFamId = db.Collector(of_class="ViewFamilyType", \
                where=lambda x: x.ViewFamily == ViewFamily.ThreeDimensional). \
                get_element_ids()

with db.Transaction('Create 3D View'):
    nThreeDv = View3D.CreateIsometric(revit.doc, threeDFamId[0])
    nThreeDv.Name = '_ColourCode'

# Applies template to the new view:
vwTemplate = db.Collector(of_class='View', \
                where=lambda x: x.IsTemplate and x.Name == '_ColourCode'). \
                get_element_ids()

with db.Transaction('Set 3D View Template'):
    try:
        nThreeDv.ViewTemplateId = vwTemplate[0]
    except:
        forms.alert('Check if _ColourCoding view tempate exists in the current Revit project', title='pyRevitSTR')

draftFamId = db.Collector(of_class="ViewFamilyType", \
                where=lambda x: x.ViewFamily == ViewFamily.Drafting). \
                get_element_ids()

with db.Transaction('Create Drafting View'):
    nDraftV = ViewDrafting.Create(revit.doc, draftFamId[0])
    nDraftV.Name = '_ColourCodeLegend'
    nDraftV.Scale = 1


# Collects columns, str framing and foundations in active view
cols = db.Collector(view=nThreeDv, of_category='Structural Columns')
colSyms = db.Collector(of_class='FamilySymbol', \
                        of_category='Structural Columns', \
                        is_type=True)

fr = db.Collector(view=nThreeDv, of_category='Structural Framing')
frSyms = db.Collector(of_class='FamilySymbol', \
                        of_category='Structural Framing', \
                        is_type=True)

fnd = db.Collector(view=nThreeDv, of_category='OST_Structural Foundation')
fndSyms = db.Collector(of_class='FamilySymbol', \
                        of_category='OST_Structural Foundation', \
                        is_type=True)

columns = grouped(cols, colSyms)
framing = grouped(fr, frSyms)
foundations = grouped(fnd, fndSyms)

# Solid fill pattern
ptn = db.Collector(of_class='FillPatternElement', \
                    where=lambda x: x.GetFillPattern().IsSolidFill). \
                    get_element_ids()

colColour = colouring(columns, ptn, nThreeDv)
frColour = colouring(framing, ptn, nThreeDv)
foundColour = colouring(foundations, ptn, nThreeDv)
totalColour = [i for sublist in [colColour + frColour + foundColour] for i in sublist]

ptn = db.Collector(of_class='FilledRegionType', is_type=True).get_elements()
solid = [i for i in ptn if i.name == 'Solid_Black']
solid = solid[0]

rgnloc = [XYZ(0.0,0.0,0.0),
		XYZ(0.0,0.025,0.0),
		XYZ(0.049,0.025,0.0),
		XYZ(0.049,0.0,0.0),
		XYZ(0.0,0.0,0.0)]

loop = CurveLoop()
for i in range(4):
    line = Line.CreateBound(rgnloc[i], rgnloc[i+1])
    loop.Append(line)

loops = CurveLoop()
loops = [loop]

with db.Transaction('Filled Region'):
	rgn = FilledRegion.Create(revit.doc, \
    solid.Id, \
    nDraftV.Id, \
    loops)

txtloc = XYZ(0.082,0.018,0.0)
defaultTxtTypeId = revit.doc.GetDefaultElementTypeId(ElementTypeGroup.TextNoteType)
opt = TextNoteOptions(defaultTxtTypeId)

with db.Transaction('Text Note'):
    txtNote = TextNote.Create(revit.doc, \
    nDraftV.Id, \
    txtloc, \
    'FamilySymbol name goes here', \
    opt)

txtRgnOptionOverride = [(rgn.Id, txtNote.Id)]

copyElems = List[ElementId]([i.Id for i in [rgn, txtNote]])

descrRange = [i*-0.032 for i in range(len(colColour)+len(frColour)+len(foundColour))]
descrRange = descrRange[1:]

with db.Transaction('Copy Elements'):
    for i in descrRange:
        descr = ElementTransformUtils. \
                CopyElements(revit.doc, copyElems, XYZ(0.0,i,0.0))
        txtRgnOptionOverride.append(tuple(descr))

for i, j in zip(totalColour, txtRgnOptionOverride):
    with db.Transaction('Description Legend'):
        ogs = OverrideGraphicSettings(). \
            SetProjectionFillColor(Color(i[0][0], i[0][1], i[0][2]))
        nDraftV.SetElementOverrides(j[0], ogs)
        fSymName = revit.doc.GetElement(i[1]).LookupParameter('Type Name').AsString()
        revit.doc.GetElement(j[1]).Text = \
            revit.doc.GetElement(i[1]).Category.Name + \
            '--' + \
            fSymName + \
            '--' + \
            revit.doc.GetElement(i[1]).LookupParameter('Type Mark').AsString()
