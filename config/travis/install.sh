#!/bin/bash
#
# Script to set up Travis-CI test VM.

COVERALL_DEPENDENCIES="python-coverage python-coveralls python-docopt";

L2TBINARIES_DEPENDENCIES="";

L2TBINARIES_TEST_DEPENDENCIES="funcsigs mock pbr six";

PYTHON2_DEPENDENCIES="";

PYTHON2_TEST_DEPENDENCIES="python-mock python-tox";

# Exit on error.
set -e;

if test ${TRAVIS_OS_NAME} = "osx";
then
	git clone https://github.com/log2timeline/l2tbinaries.git -b dev;

	mv l2tbinaries ../;

	for PACKAGE in L2TBINARIES_DEPENDENCIES;
	do
		sudo /usr/sbin/installer -target / -pkg ../l2tbinaries/macos/${PACKAGE}-*.dmg;
	done

	for PACKAGE in L2TBINARIES_TEST_DEPENDENCIES;
	do
		sudo /usr/sbin/installer -target / -pkg ../l2tbinaries/macos/${PACKAGE}-*.dmg;
	done

elif test ${TRAVIS_OS_NAME} = "linux";
then
	sudo rm -f /etc/apt/sources.list.d/travis_ci_zeromq3-source.list;

	sudo add-apt-repository ppa:gift/dev -y;
	sudo apt-get update -q;
	# Only install the Python 2 dependencies.
	# Also see: https://docs.travis-ci.com/user/languages/python/#Travis-CI-Uses-Isolated-virtualenvs
	sudo apt-get install -y ${COVERALL_DEPENDENCIES} ${PYTHON2_DEPENDENCIES} ${PYTHON2_TEST_DEPENDENCIES};
fi
