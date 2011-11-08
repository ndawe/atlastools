#!/bin/bash
# Author: Noel Dawe

function print_help() {
    echo "Usage : $0 [clean|local|build-root-python|build-packages|worker]"
    exit
}

if [[ $# -eq 0 ]]
then
    print_help
fi

BASE=${PWD}

packages='rootpy goodruns atlastools'

repo='http://linuxsoft.cern.ch/cern/slc5X/updates/x86_64/RPMS/'
GIT_USER=ndawe

PYTHON_VERS_MAJOR=2.7
PYTHON_VERS=2.7.2
ROOT_VERS=5.30.00

use_precompiled_python=true
use_precompiled_root=true

function download_from_github() {
    PACKAGE=${1}
    if [[ ! -e ${PACKAGE}.tar.gz ]]
    then
        if ! wget --no-check-certificate -O ${PACKAGE}.tar.gz https://github.com/${GIT_USER}/${PACKAGE}/tarball/master
        then
            echo "Failed to download package ${PACKAGE} from github"
            exit 1
        fi
    fi
}

function install_python_package() {
    cd ${BASE}
    PACKAGE=${1}
    if [[ ! -e ${PACKAGE} ]]
    then
        if tar -pzxf ${PACKAGE}.tar.gz
        then
            rm -f ${PACKAGE}.tar.gz
            mv ${GIT_USER}-${PACKAGE}-* ${PACKAGE}
            if [[ -d ${PACKAGE} ]]
            then
                echo "Installing ${PACKAGE}..."
                cd ${PACKAGE}
                #echo ">>> lib dirs: ${PYTHON_LIB}:${BASE}/rpmroot/usr/lib64"
                #echo ">>> include dirs: ${RPM_INCLUDE}"
                #python setup.py build_ext --library-dirs="${PYTHON_LIB}:${BASE}/rpmroot/usr/lib64" --include-dirs="${RPM_INCLUDE}"
                #python setup.py build -e "/usr/bin/env python"
                #python setup.py setopt --command build_ext --option library-dirs --set-value ${PYTHON_LIB}
                if ! python setup.py install --user
                then
                    echo "Failed to install package ${PACKAGE}"
                    exit 1
                fi
                cd ..
            fi
        else
            exit 1
        fi
    fi
}

function install_rpm() {
    cd ${BASE}
    if [[ ! -e rpmroot ]]
    then
        mkdir rpmroot
    fi
    echo "Installing ${2}..."
    cd rpmroot
    if ! wget ${1}${2}
    then
        echo "Failed to download ${1}${2}"
        exit 1
    fi
    rpm2cpio ${2} | cpio -idmv
    rm -rf ${2}
    cd ${BASE}
    export RPM_INCLUDE=${BASE}/rpmroot/usr/include/${3}${RPM_INCLUDE:+:$RPM_INCLUDE}
}

function setup_rpm() {
    export RPM_INCLUDE=${BASE}/rpmroot/usr/include${RPM_INCLUDE:+:$RPM_INCLUDE}
    export LD_LIBRARY_PATH=${BASE}/rpmroot/usr/lib64${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}
    export PATH=${BASE}/rpmroot/usr/bin${PATH:+:$PATH}
}

function setup_root() {
    source ${BASE}/root/bin/thisroot.sh
}

function setup_python() {
    export PYTHONPATH=${BASE}/python/lib/python${PYTHON_VERS_MAJOR}/site-packages${PYTHONPATH:+:$PYTHONPATH}
    export LD_LIBRARY_PATH=${BASE}/python/lib${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}
}

case "${1}" in
clean)

    echo "Cleaning up..."
    rm -rf cython
    rm -rf lxml
    rm -rf yaml
    rm -rf python
    rm -rf root
    rm -rf rpmroot
    
    for package in ${packages}
    do
        rm -rf ${package}
        rm -f ${package}.tar.gz
    done
    ;;

local)

    for package in ${packages}
    do
        download_from_github ${package}
    done
    ;;

build-root-python)

    # install python and ROOT

    if [[ ! -e python ]]
    then
        if $use_precompiled_python
        then
            if ! wget http://hep.phys.sfu.ca/~endw/grid/python.tar.gz
            then
                echo "Failed to download Python"
                exit 1
            fi
            tar -zxf python.tar.gz
            rm -rf python.tar.gz
        else
            if ! wget http://www.python.org/ftp/python/${PYTHON_VERS}/Python-${PYTHON_VERS}.tar.bz2
            then
                echo "Failed to download Python"
                exit 1
            fi
            tar -xjf Python-${PYTHON_VERS}.tar.bz2
            cd Python-${PYTHON_VERS}
            ./configure --enable-shared --prefix=${BASE}/python
            make -j
            make install
            cd ..
            rm -rf Python-${PYTHON_VERS}
            rm -rf Python-${PYTHON_VERS}.tar.bz2
        fi
    fi

    setup_python

    if [[ ! -e root ]]
    then
        if ${use_precompiled_root}
        then
            if ! wget http://hep.phys.sfu.ca/~endw/grid/root.tar.gz
            then
                echo "Failed to download ROOT"
                exit 1
            fi
            tar -zxf root.tar.gz
            rm -rf root.tar.gz
        else
            if ! wget ftp://root.cern.ch/root/root_v${ROOT_VERS}.source.tar.gz
            then
                echo "Failed to download ROOT"
                exit 1
            fi
            gzip -dc root_v${ROOT_VERS}.source.tar.gz | tar -xf -
            rm -rf root_v${ROOT_VERS}.source.tar.gz
            cd root
            ./configure --with-python-libdir=${BASE}/python/lib --with-python-incdir=${BASE}/python/include/python${PYTHON_VERS_MAJOR} \
                        --with-dcap-libdir=/atlas/software/ATLASLocalRootBase/x86_64/gLite/current/d-cache/dcap/lib64 \
                        --with-dcap-incdir=/atlas/software/ATLASLocalRootBase/x86_64/gLite/current/d-cache/dcap/include
            make -j
            cd ..
        fi
    fi
    
    setup_root
    ;;

build-packages)
    
    python_version=`python -c "import distutils.sysconfig; print distutils.sysconfig.get_python_version()"`
    PYTHON_LIB=`python -c "import distutils.sysconfig; import os; print os.path.dirname(distutils.sysconfig.get_python_lib(standard_lib=True))"`
    echo "Python version "${python_version}
    echo "Python lib located in "${PYTHON_LIB}

    if [[ ! -e user-python ]]
    then
        echo "Creating user python area"
        mkdir -p user-python/lib/python${python_version}/site-packages/
        mkdir user-python/bin
    fi
    export PYTHONUSERBASE=${BASE}/user-python
    export PATH=${PYTHONUSERBASE}/bin${PATH:+:$PATH}

    for package in ${packages}
    do
        install_python_package ${package}
    done
    ;;

worker)
    
    if [[ -e python ]]
    then
        setup_python
    fi
    if [[ -e root ]]
    then
        setup_root
    fi
    export PYTHONUSERBASE=${BASE}/user-python
    export PATH=${PYTHONUSERBASE}/bin${PATH:+:$PATH}
    export ROOTPY_GRIDMODE=true
    ;;

*)
    
    print_help
    ;;
esac
