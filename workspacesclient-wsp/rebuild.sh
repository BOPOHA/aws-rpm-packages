#!/bin/bash
# required packages:
#  dnf install rpmdevtools rpkg
# how to check latest version:
# https://clients.amazonworkspaces.com/linux-install
set -e -u

PROJECTNAME=workspacesclient-wsp
PROJECTTMPDIR=/tmp/${PROJECTNAME}
RPM_VERSION=$(rpmspec -q --qf "%{Version}-%{Release}" ${PROJECTNAME}.spec)
spectool --get-files --directory ${PROJECTTMPDIR} ${PROJECTNAME}.spec
rpkg srpm --spec ${PROJECTNAME}.spec --outdir ${PROJECTTMPDIR}
rpmbuild --nocheck --rebuild ${PROJECTTMPDIR}/${PROJECTNAME}-${RPM_VERSION}.src.rpm
rpmlint  ~/rpmbuild/RPMS/x86_64/${PROJECTNAME}-${RPM_VERSION}.x86_64.rpm
ls -lah ~/rpmbuild/RPMS/x86_64/${PROJECTNAME}-${RPM_VERSION}.x86_64.rpm
