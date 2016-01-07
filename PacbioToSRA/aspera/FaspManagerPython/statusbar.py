# Modified from http://nbviewer.ipython.org/github/ipython/ipython/blob/3607712653c66d63e0d7f13f073bde8c0f209ba8/docs/examples/notebooks/Animations_and_Progress.ipynb

import uuid
from IPython.display import HTML, Javascript, display

divid=None

def new():
  global divid 
  divid = str(uuid.uuid4())

  pb = HTML(
  """
  <div style="border: 1px solid black; width:500px">
    <div id="%s" style="background-color:blue; width:0%%">&nbsp;</div>
    </div> 
    """ % divid)
  display(pb)

def update( pct ):
  display(Javascript("$('div#%s').width('%i%%')" % (divid, pct)))
