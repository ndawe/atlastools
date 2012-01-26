from ._cleaning import is_bad as _is_bad

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
    return _is_bad(level,
        quality, NegE,
        emf,     hecf,
        time,    fmax,
        eta,     chf ,
        HecQ,    LArQmean )
