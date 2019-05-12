#!/bin/bash
#
# Script to set up Travis-CI test VM.
#
# This file is generated by l2tdevtools update-dependencies.py any dependency
# related changes should be made in dependencies.ini.

L2TBINARIES_DEPENDENCIES="";

L2TBINARIES_TEST_DEPENDENCIES="funcsigs mock pbr six";

DPKG_PYTHON2_DEPENDENCIES="";

DPKG_PYTHON2_TEST_DEPENDENCIES="python-coverage python-funcsigs python-mock python-pbr python-setuptools python-six";

DPKG_PYTHON3_DEPENDENCIES="";

DPKG_PYTHON3_TEST_DEPENDENCIES="python3-distutils python3-mock python3-pbr python3-setuptools python3-six";

RPM_PYTHON2_DEPENDENCIES="";

RPM_PYTHON2_TEST_DEPENDENCIES="python2-funcsigs python2-mock python2-pbr python2-setuptools python2-six";

RPM_PYTHON3_DEPENDENCIES="";

RPM_PYTHON3_TEST_DEPENDENCIES="python3-mock python3-pbr python3-setuptools python3-six";

# Exit on error.
set -e;

if test ${TRAVIS_OS_NAME} = "osx";
then
	git clone https://github.com/log2timeline/l2tbinaries.git -b dev;

	mv l2tbinaries ../;

	for PACKAGE in ${L2TBINARIES_DEPENDENCIES};
	do
		echo "Installing: ${PACKAGE}";
		sudo /usr/bin/hdiutil attach ../l2tbinaries/macos/${PACKAGE}-*.dmg;
		sudo /usr/sbin/installer -target / -pkg /Volumes/${PACKAGE}-*.pkg/${PACKAGE}-*.pkg;
		sudo /usr/bin/hdiutil detach /Volumes/${PACKAGE}-*.pkg
	done

	for PACKAGE in ${L2TBINARIES_TEST_DEPENDENCIES};
	do
		echo "Installing: ${PACKAGE}";
		sudo /usr/bin/hdiutil attach ../l2tbinaries/macos/${PACKAGE}-*.dmg;
		sudo /usr/sbin/installer -target / -pkg /Volumes/${PACKAGE}-*.pkg/${PACKAGE}-*.pkg;
		sudo /usr/bin/hdiutil detach /Volumes/${PACKAGE}-*.pkg
	done

elif test -n "${FEDORA_VERSION}";
then
	CONTAINER_NAME="fedora${FEDORA_VERSION}";

	docker pull registry.fedoraproject.org/fedora:${FEDORA_VERSION};

	docker run --name=${CONTAINER_NAME} --detach -i registry.fedoraproject.org/fedora:${FEDORA_VERSION};

	# Install dnf-plugins-core.
	docker exec ${CONTAINER_NAME} dnf install -y dnf-plugins-core;

	# Add additional dnf repositories.
	docker exec ${CONTAINER_NAME} dnf copr -y enable @gift/dev;

	if test -n "${TOXENV}";
	then
		RPM_PACKAGES="python3-tox";

	else
		RPM_PACKAGES="";

		if test ${TARGET} = "pylint";
		then
			RPM_PACKAGES="${RPM_PACKAGES} findutils pylint";
		fi
		if test ${TRAVIS_PYTHON_VERSION} = "2.7";
		then
			RPM_PACKAGES="${RPM_PACKAGES} python2 ${RPM_PYTHON2_DEPENDENCIES} ${RPM_PYTHON2_TEST_DEPENDENCIES}";
		else
			RPM_PACKAGES="${RPM_PACKAGES} python3 ${RPM_PYTHON3_DEPENDENCIES} ${RPM_PYTHON3_TEST_DEPENDENCIES}";
		fi
	fi
	docker exec ${CONTAINER_NAME} dnf install -y ${RPM_PACKAGES};

	docker cp ../dfdatetime ${CONTAINER_NAME}:/

elif test -n "${UBUNTU_VERSION}";
then
	CONTAINER_NAME="ubuntu${UBUNTU_VERSION}";

	docker pull ubuntu:${UBUNTU_VERSION};

	docker run --name=${CONTAINER_NAME} --detach -i ubuntu:${UBUNTU_VERSION};

	# Install add-apt-repository and locale-gen.
	docker exec ${CONTAINER_NAME} apt-get update -q;
	docker exec -e "DEBIAN_FRONTEND=noninteractive" ${CONTAINER_NAME} sh -c "apt-get install -y locales software-properties-common";

	# Add additional apt repositories.
	if test -n "${TOXENV}";
	then
		docker exec ${CONTAINER_NAME} add-apt-repository universe;
		docker exec ${CONTAINER_NAME} add-apt-repository ppa:deadsnakes/ppa -y;

	elif test ${TARGET} = "pylint";
	then
		docker exec ${CONTAINER_NAME} add-apt-repository ppa:gift/pylint3 -y;
	fi
	docker exec ${CONTAINER_NAME} add-apt-repository ppa:gift/dev -y;

	docker exec ${CONTAINER_NAME} apt-get update -q;

	# Set locale to US English and UTF-8.
	docker exec ${CONTAINER_NAME} locale-gen en_US.UTF-8;

	# Install packages.
	if test -n "${TOXENV}";
	then
		DPKG_PACKAGES="build-essential python${TRAVIS_PYTHON_VERSION} python${TRAVIS_PYTHON_VERSION}-dev tox";

	else
		DPKG_PACKAGES="";

		if test "${TARGET}" = "coverage";
		then
			DPKG_PACKAGES="${DPKG_PACKAGES} curl git";

		elif test ${TARGET} = "pylint";
		then
			DPKG_PACKAGES="${DPKG_PACKAGES} python3-distutils pylint";
		fi
		if test ${TRAVIS_PYTHON_VERSION} = "2.7";
		then
			DPKG_PACKAGES="${DPKG_PACKAGES} python ${DPKG_PYTHON2_DEPENDENCIES} ${DPKG_PYTHON2_TEST_DEPENDENCIES}";
		else
			DPKG_PACKAGES="${DPKG_PACKAGES} python3 ${DPKG_PYTHON3_DEPENDENCIES} ${DPKG_PYTHON3_TEST_DEPENDENCIES}";
		fi
	fi
	docker exec -e "DEBIAN_FRONTEND=noninteractive" ${CONTAINER_NAME} sh -c "apt-get install -y ${DPKG_PACKAGES}";

	docker cp ../dfdatetime ${CONTAINER_NAME}:/
fi
