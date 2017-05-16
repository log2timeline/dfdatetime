#!/bin/bash
#
# Script to set up Travis-CI test VM.

COVERALL_DEPENDENCIES="python-coverage python-coveralls python-docopt";

L2TBINARIES_DEPENDENCIES="";

L2TBINARIES_TEST_DEPENDENCIES="funcsigs mock pbr six";

PYTHON2_DEPENDENCIES="";

PYTHON3_DEPENDENCIES="";

PYTHON_TEST_DEPENDENCIES="python-mock";

# Exit on error.
set -e;

if test ${TRAVIS_OS_NAME} = "osx";
then
	git clone https://github.com/log2timeline/l2tdevtools.git;

	mv l2tdevtools ../;
	mkdir dependencies;

	PYTHONPATH=../l2tdevtools ../l2tdevtools/tools/update.py --download-directory=dependencies ${L2TBINARIES_DEPENDENCIES} ${L2TBINARIES_TEST_DEPENDENCIES};

elif test ${TRAVIS_OS_NAME} = "linux" && test ${TRAVIS_PYTHON_VERSION} = "2.7";
then
	sudo add-apt-repository ppa:gift/dev -y;
	sudo apt-get update -q;
	sudo apt-get install -y ${COVERALL_DEPENDENCIES} ${PYTHON2_DEPENDENCIES} ${PYTHON_TEST_DEPENDENCIES};

elif test ${TRAVIS_OS_NAME} = "linux" && test ${TRAVIS_PYTHON_VERSION} = "3.4";
then
	sudo add-apt-repository ppa:gift/dev -y;
	sudo apt-get update -q;
	sudo apt-get install -y ${COVERALL_DEPENDENCIES} ${PYTHON3_DEPENDENCIES} ${PYTHON_TEST_DEPENDENCIES};
fi
