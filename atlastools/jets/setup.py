import numpy
from numpy.distutils.misc_util import Configuration


def configuration(parent_package="", top_path=None):
    config = Configuration("cleaning", parent_package, top_path)
    config.add_extension("_cleaning",
                         sources=["_cleaning.c"],
                         include_dirs=[numpy.get_include()])
    return config

if __name__ == "__main__":
    from numpy.distutils.core import setup
    setup(**configuration().todict())
