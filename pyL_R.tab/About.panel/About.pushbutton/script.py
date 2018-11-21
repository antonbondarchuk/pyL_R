"""General Info about pyL_R extension and links to contact maintainer.
"""

import sys

from pyrevit import forms
from pyrevit import script


__context__ = 'zerodoc'

__doc__ = 'pyL_R information. Links to github repo, L&R websites ' \
          '& Linked In profile of the pyL_R maintainer.'


class AboutpyL_R(forms.WPFWindow):
    def __init__(self, xaml_file_name):
        forms.WPFWindow.__init__(self, xaml_file_name)

    def opengithubrepopage(self, sender, args):
        script.open_url('https://github.com/antonbondarchuk')
    
    
    def openl_rwebpage(self, sender, args):
        script.open_url('http://www.lar.net.au')

    def openl_rstartpage(self, sender, args):
        script.open_url('http://start.lar.net.au')


    def openlinkedin(self, sender, args):
        script.open_url('https://www.linkedin.com/in/antonbondarchuk/')


    def handleclick(self, sender, args):
        self.Close()

AboutpyL_R('aboutpyL_R.xaml').show_dialog()
