#!/bin/bash
set -x -u -o pipefail

CURRENT_DEB_VERSION=$( curl -Is https://d20adtppz83p9s.cloudfront.net/GTK/latest/awsvpnclient_amd64.deb | sed -n "s/\r$//;s/^x-amz-meta-version: //p;")
CURRENT_RPM_VERSION=$(rpmspec -q --qf "%{Version}" awsvpnclient.spec)

if [ "$CURRENT_DEB_VERSION" = "$CURRENT_RPM_VERSION" ];then
  echo nothing to do
  exit 0
fi

if [ ! -f /tmp/source.deb ]; then
  # downloading deb https://d20adtppz83p9s.cloudfront.net/GTK/3.1.0/awsvpnclient_amd64.deb
  curl -s https://d20adtppz83p9s.cloudfront.net/GTK/latest/awsvpnclient_amd64.deb -o /tmp/source.deb
fi

rm -rf control/*
ar p /tmp/source.deb control.tar.xz  | tar -xJ  -C  control
ar x /tmp/source.deb data.tar.xz
mv data.tar.xz ~/rpmbuild/SOURCES/data.tar.xz

echo "enable awsvpnclient.service" > ~/rpmbuild/SOURCES/70-awsvpnclient.preset
