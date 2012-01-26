from . import _libcleaning

LOOSER,\
LOOSE,\
MEDIUM,\
TIGHT = range(4)

def is_bad(level,
	quality, NegE,
	emf,     hecf,
	time,    fmax,
	eta,     chf ,
    HecQ,    LArQmean ):
    return _libcleaning._is_bad(level,
        quality, NegE,
        emf,     hecf,
        time,    fmax,
        eta,     chf ,
        HecQ,    LArQmean )
