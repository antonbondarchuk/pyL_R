import sys
import os

from pyrevit import UI
from pyrevit import forms

sys.path.insert(0, 'C:\\Python27\Lib\site-packages')
from PyPDF2 import PdfFileMerger

__context__='zerodoc'
__doc__='Combines pdf files using PyPDF2. The tool will ask for a folder '\
        'where pdf files located.\n\n'\
        

merger = PdfFileMerger(strict=False)

basefolder = forms.pick_folder()
destination = basefolder + '\\'

filecount = 0

filenames = os.listdir(basefolder)

if '_Combined.pdf' in os.listdir(basefolder):
    os.remove('_Combined.pdf')

for f in filenames:
    if f.endswith('.pdf') and not ('TRANS' in f):
        try:
            op = open(destination+f, 'rb')
            merger.append(op)
            filecount += 1
        except:
            pass

outPDF = destination + '_Combined.pdf'
output = open(outPDF, 'wb')
merger.write(output)
output.close()

forms.alert('{0} FILES COMBINED'.format(filecount))
