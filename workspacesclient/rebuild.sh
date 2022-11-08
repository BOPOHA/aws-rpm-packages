#!/bin/bash
# https://clients.amazonworkspaces.com/linux-install
# curl https://d3nt0h4h6pmmc4.cloudfront.net/ubuntu/dists/focal/main/binary-amd64/Packages -O
set -e -u

PROJECTNAME=workspacesclient
PROJECTTMPDIR=/tmp/${PROJECTNAME}
RPM_VERSION=$(rpmspec -q --qf "%{Version}-%{Release}" ${PROJECTNAME}.spec)
spectool --get-files --directory ${PROJECTTMPDIR} ${PROJECTNAME}.spec
rpkg srpm --spec ${PROJECTNAME}.spec --outdir ${PROJECTTMPDIR}
rpmbuild --nocheck --rebuild ${PROJECTTMPDIR}/${PROJECTNAME}-${RPM_VERSION}.src.rpm
# rpmlint  ~/rpmbuild/RPMS/x86_64/${PROJECTNAME}-${RPM_VERSION}.x86_64.rpm
ls -lah ~/rpmbuild/RPMS/x86_64/${PROJECTNAME}-${RPM_VERSION}.x86_64.rpm
