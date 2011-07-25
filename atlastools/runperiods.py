import os
import glob
import re

_RUNFILEPATTERN = re.compile('^(?P<project>[^.]+).(?P<period>[^.]+).runs.list$')
_PERIODPATTERN = re.compile('^period(?P<period>[A-Z])(?P<subperiod>[0-9]+)$')
_runfiles = glob.glob(os.path.join(os.environ['ATLASTOOLS_SYS'], 'dat', '*'))
_runperiods = {}

for f in _runfiles:
    match = re.match(_RUNFILEPATTERN, os.path.basename(f))
    if match:
        project = match.group('project')
        period = match.group('period')
        periodmatch = re.match(_PERIODPATTERN, period)
        if periodmatch:
            periodlabel = periodmatch.group('period')
            subperiod = int(periodmatch.group('subperiod'))
            of = open(f)
            try:
                if not _runperiods.has_key(project):
                    _runperiods[project] = {}
                if not _runperiods[project].has_key(periodlabel):
                    _runperiods[project][periodlabel] = {}
                runs = [int(line) for line in of.readlines()]
                _runperiods[project][periodlabel][subperiod] = runs
            except:
                print "Error: could not parse file %s"% f
            of.close()
        else:
            print "Warning: file %s does not specify a valid run period"% f
    else:
        print "Warning: file %s is not a valid runs list"% f
    
def get_runs(selection = None, project = 'data10_7TeV'):

    runs = []
    if not _runperiods.has_key(project):
        return runs
    if not selection:
        for period,subperiods in _runperiods[project].items():
            for subperiod,runlist in subperiods.items():
                runs += runlist
    else:    
        periodRanges = selection.split(',')
        for periodRange in periodRanges:
            periodRange = periodRange.split('-')
            begin = periodRange[0]
            if len(periodRange) == 1:
                end = begin
            else:
                end = periodRange[1]
            if len(begin) == 1:
                beginPeriod = begin
                beginSubperiod = 1
            else:
                beginPeriod = begin[0]
                beginSubperiod = int(begin[1:])
            if len(end) == 1:
                endPeriod = end
                endSubperiod = -1
            else:
                endPeriod = end[0]
                endSubperiod = int(end[1:])
            record = False
            for period in sorted(_runperiods[project].iterkeys()):
                if period > endPeriod:
                    break
                subperiods = _runperiods[project][period]
                for subperiod in sorted(subperiods.iterkeys()):
                    if not record and period == beginPeriod and subperiod == beginSubperiod:
                        record = True
                    if record:
                        runs += subperiods[subperiod]
                    if period == endPeriod and subperiod == endSubperiod:
                        break
                if period >= endPeriod:
                    break
    # remove duplicates
    runs = list(set(runs))
    # sort
    runs.sort()
    return runs
