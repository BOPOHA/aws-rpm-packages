#!/bin/bash
set -e -u
PROJECTNAME=awsvpnclient
PROJECTTMPDIR=/tmp/${PROJECTNAME}
RPM_VERSION=$(rpmspec -q --qf "%{Version}-%{Release}" awsvpnclient.spec)
spectool --get-files --directory ${PROJECTTMPDIR} ${PROJECTNAME}.spec
rpkg srpm --spec ${PROJECTNAME}.spec --outdir ${PROJECTTMPDIR}
rpmbuild --nocheck --rebuild ${PROJECTTMPDIR}/${PROJECTNAME}-${RPM_VERSION}.src.rpm
# rpmlint  ~/rpmbuild/RPMS/x86_64/awsvpnclient-${RPM_VERSION}.x86_64.rpm
ls -lah ~/rpmbuild/RPMS/x86_64/awsvpnclient-${RPM_VERSION}.x86_64.rpm
