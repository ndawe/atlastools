from rootpy.tree.filtering import EventFilter
from goodruns import GRL

class GRLFilter(EventFilter):

    def __init__(self, grl, **kwargs):

        super(GRLFilter, self).__init__(**kwargs)
        
        if isinstance(grl, GRL):
            self.grl = grl
        else:
            self.grl = GRL(grl)

    def passes(self, event):

        if not self.grl:
            return True
        return (event.RunNumber, event.lbn) in self.grl
