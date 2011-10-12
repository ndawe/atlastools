"""
Pickle your current shell environment for later use.
"""
import cPickle
import sys
import os
import subprocess

DISPLAY = os.getenv("DISPLAY",'')
ATLASTOOLS_ROOT = os.getenv("ATLASTOOLS_CONFIG_ROOT")
if ATLASTOOLS_ROOT is None:
    ATLASTOOLS_ROOT = os.getenv("HOME")
PATH = os.path.join(ATLASTOOLS_ROOT, 'env')

def define(name):
    """
    Define an environment
    """
    if not os.path.exists(PATH):
        os.makedirs(PATH)
    env = {"System":os.environ, "Python":sys.path}
    env_file = open((os.path.join(PATH, "%s.env"))% name,'wb')
    cPickle.dump(env, env_file)
    env_file.close()

def load(name):
    """
    Load a previously pickled environment
    """
    env_filename = (os.path.join(PATH, "%s.env"))% name
    if not os.path.exists(env_filename):
        print "Environment %s is not defined."% name
        return False
    env_file = open(env_filename, 'rb')
    new_env = cPickle.load(env_file)
    env_file.close()
    current_python = subprocess.check_output(["which", "python"])
    os.environ.clear()
    os.environ.update(new_env["System"])
    os.environ["DISPLAY"] = DISPLAY
    new_python = subprocess.check_output(["which", "python"])
    sys.path = new_env["Python"]
    print "Environment %s has been loaded."% name
    return True
