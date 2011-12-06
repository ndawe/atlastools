from rootpy.batch import Student, Supervisor


class ATLASSupervisor(Supervisor): pass


class ATLASStudent(Student):

    def __init__(self, *args, **kwargs):

        super(ATLASStudent, self).__init__(*args, **kwargs)
        self.grl = kwargs.get('grl', None)
        self.events = kwargs.get('events', -1)
        if self.grl:
            print "Using GRL: %s"% self.grl
