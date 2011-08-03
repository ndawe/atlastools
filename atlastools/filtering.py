from rootpy.tree.filtering import *
from goodruns.grl import GRL

class GRLFilter(EventFilter):

    def __init__(self, grl = None, **kwargs):

        super(GRLFilter, self).__init__(self, **kwargs)
        if isinstance(grl, GRL):
            self.grl = grl
        else:
            self.grl = GRL(grl)

    def passes(self, event):

        return (event.RunNumber[0], event.lbn[0]) in self.grl
