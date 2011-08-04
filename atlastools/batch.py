from rootpy.batch import Student

class ATLASStudent(Student):

    def __init__(self, *args, **kwargs):

        super(ATLASStudent, self).__init__(*args, **kwargs)
        self.grl = kwargs.get('grl', None)
        if self.grl:
            print "Using GRL: %s"% self.grl
