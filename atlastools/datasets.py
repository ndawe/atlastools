import glob
import os
import sys
import re
import yaml
from atlastools import runperiods
from rootpy.data.dataset import Fileset

mcpattern = re.compile("^(optimized.)?group(?P<year>[0-9]{2}).(?P<group>[^.]+).mc(?P<prodyear>[0-9]{2})[_]?(?P<energy>[0-9]{1,2})(TeV)?.(?P<run>[0-9]+).(?P<name>).(?P<tag>[^.]+).(?P<suffix>.+)$")
#datapattern = re.compile("^group(?P<year>[0-9]+).(?P<group>[^.]+).(?P<run>[0-9]+).(?P<stream>[^.]+).(?P<tag>[^.]+).(?P<version>[0-9\-]+)(?:.(?P<grl>GRL))?.D3PD.(?:(?P<edition>[0-9]+).)?(?P<suffix>.+)?$")
datapattern = re.compile("^(\w+).(?P<name>[a-zA-Z_\-0-9]+).(?P<run>[0-9]+).*$")

DATA,MC = range(2)
BACKGROUND,SIGNAL = range(2)
TAU,MUON,ELEC,JET = range(4)

classes = {
    'BACKGROUND': BACKGROUND,
    'SIGNAL'    : SIGNAL
}

types = {
    'DATA': DATA,
    'MC'  : MC
}

labels = {
    'TAU' : TAU,
    'MUON': MUON,
    'ELEC': ELEC,
    'JET' : JET
}

if not os.environ.has_key('DATAROOT'):
    sys.exit("DATAROOT not defined!")
dataroot = os.environ['DATAROOT']

def get_sample(name, runs = None, periods = None):

    base = os.path.join(dataroot,name)
    if not os.path.isdir(base):
        print "Sample %s not found at %s"%(name,base)
        return None
    metafile = os.path.join(base,'meta.yml')
    if not os.path.isfile(metafile):
        print "Metadata %s not found!"%metafile
        return None
    try:
        metafile = open(metafile)
        meta = yaml.load(metafile)
        metafile.close()
        datatype = meta['type'].upper()
        classname = meta['class'].upper()
        if type(meta['weight']) is str:
            weight = float(eval(meta['weight']))
        else:
            weight = float(meta['weight'])
        treename = meta['tree']
        labelname = meta['label']
    except:
        print "Could not parse metadata!"
        return None 
    if not classes.has_key(classname):
        print "Class %s is not defined!"%classname
        if len(classes) > 0:
            print "Use one of these:"
            for key in classes.keys():
                print key
        else:
            print "No classes have been defined!"
        return None
    classtype = classes[classname]
    if not types.has_key(datatype):
        print "Datatype %s is not defined!"%datatype
        if len(types) > 0:
            print "Use one of these:"
            for key in types.keys():
                print key
        else:
            print "No datatypes have been defined!"
    datatype = types[datatype]
    if not labels.has_key(labelname):
        print "Label %s is not defined!"%labelname
        if len(labels) > 0:
            print "Use one of these:"
            for key in labels.keys():
                print key
        else:
            print "No labels have been defined!"
    labeltype = labels[labelname]
    dirs = glob.glob(os.path.join(base,'*'))
    actualdirs = []
    for dir in dirs:
        if os.path.isdir(dir):
            actualdirs.append(dir)
    files = []
    samplename = name
    if datatype == types['DATA']:
        # check for duplicate runnumbers and take last edition
        selected_runs = []
        if runs != None:
            selected_runs = runs
        elif periods != None:
            selected_runs = runperiods.get_runs(periods)
        runnumbers = {}
        versions = {}
        for dir in actualdirs:
            datasetname = os.path.basename(dir)
            match = re.match(datapattern,datasetname)
            if not match:
                print "Warning: directory %s is not a valid dataset name!"%datasetname
            else:
                
                #versions[match.group('version')] = None
                runnumber = int(match.group('run'))
                if selected_runs:
                    if runnumber not in selected_runs:
                        continue
                """
                edition = 0
                if match.group('edition'):
                    edition = int(match.group('edition'))
                if runnumbers.has_key(runnumber):
                    print "Warning: multiple editions of dataset %s exist!"%datasetname
                    if edition > runnumbers[runnumber]['edition']:
                        runnumbers[runnumber] = {'edition':edition, 'dir':dir}
                else:
                    runnumbers[runnumber] = {'edition':edition, 'dir':dir}
                """
                files += glob.glob(os.path.join(dir,'*root*'))
        """
        if len(versions) > 1:
            print "Warning: multiple versions of TauD3PDMaker used:"
            for key in versions.keys():
                print key
        """
    else:
        for dir in actualdirs:
            #datasetname = os.path.basename(dir)
            #match = re.match(mcpattern,datasetname)
            """
            if not match:
                print "Warning: directory %s is not a valid dataset name!"%datasetname
            else:
            """
            files += glob.glob(os.path.join(dir,'*root*'))
    return Fileset(
            name = samplename,
            title = labeltype,
            datatype = datatype,
            classtype = classtype,
            treename = treename,
            weight = weight,
            files = files,
            meta = None,
            properties = None
        )
