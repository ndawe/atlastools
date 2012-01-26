from cpython cimport bool

cdef extern from "_cleaning.h":
        
        enum LEVEL:
            LooseMinusBad
            LooseBad
            MediumBad
            TightBad

        bool is_bad(LEVEL criteria,
            double quality, double NegE,
            double emf,     double hecf,
            double time,    double fmax,
            double eta,     double chf ,
            double HecQ,    double LArQmean )

def _is_bad(criteria,
             quality, NegE,
             emf,     hecf,
             time,    fmax,
             eta,     chf ,
             HecQ,    LArQmean ):
    
    return is_bad(criteria,
            quality, NegE,
            emf,     hecf,
            time,    fmax,
            eta,     chf ,
            HecQ,    LArQmean )
