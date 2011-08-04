from rootpy.tree.filtering import EventFilter
from goodruns.grl import GRL

class GRLFilter(EventFilter):

    def __init__(self, grl, **kwargs):

        super(GRLFilter, self).__init__(**kwargs)
        
        if isinstance(grl, GRL):
            self.grl = grl
        else:
            self.grl = GRL(grl)

    def passes(self, event):

        return (event.RunNumber[0], event.lbn[0]) in self.grl
