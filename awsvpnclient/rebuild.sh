#!/bin/bash
# required packages:
#  dnf install rpmdevtools rpkg
# how to check latest version:
# https://docs.aws.amazon.com/vpn/latest/clientvpn-user/client-vpn-connect-linux.html
# curl https://d20adtppz83p9s.cloudfront.net/GTK/latest/debian-repo/dists/ubuntu-20.04/main/binary-amd64/Packages -O
set -e -u
PROJECTNAME=awsvpnclient
PROJECTTMPDIR=/tmp/${PROJECTNAME}
RPM_VERSION=$(rpmspec -q --qf "%{Version}-%{Release}" ${PROJECTNAME}.spec)
spectool --get-files --directory ${PROJECTTMPDIR} ${PROJECTNAME}.spec
rpkg srpm --spec ${PROJECTNAME}.spec --outdir ${PROJECTTMPDIR}
rpmbuild --nocheck --rebuild ${PROJECTTMPDIR}/${PROJECTNAME}-${RPM_VERSION}.src.rpm
# rpmlint  ~/rpmbuild/RPMS/x86_64/${PROJECTNAME}-${RPM_VERSION}.x86_64.rpm
ls -lah ~/rpmbuild/RPMS/x86_64/${PROJECTNAME}-${RPM_VERSION}.x86_64.rpm
