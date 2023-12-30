# required packages:
# dnf install rpmdevtools rpkg
.PHONY: epel7

PROJECTNAME=workspacesclient
PROJECTTMPDIR=/tmp/$(PROJECTNAME)
RPM_VERSION=$(shell rpmspec -q --qf "%{Version}-%{Release}" ${PROJECTNAME}.spec)

clean:
	rm -rf $(PROJECTTMPDIR)

check:
	# https://clients.amazonworkspaces.com/linux-install
	curl https://d3nt0h4h6pmmc4.cloudfront.net/ubuntu/dists/focal/main/binary-amd64/Packages -O

spec:
	rpkg spec --spec $(PROJECTNAME).spec -p

srpm:
	spectool --get-files --directory $(PROJECTTMPDIR) $(PROJECTNAME).spec
	rpkg srpm --spec $(PROJECTNAME).spec --outdir $(PROJECTTMPDIR)

rpmbuild: srpm
	rpmbuild --nocheck --rebuild $(PROJECTTMPDIR)/$(PROJECTNAME)-$(RPM_VERSION).src.rpm
	rpm -ql ~/rpmbuild/RPMS/x86_64/$(PROJECTNAME)-$(RPM_VERSION).x86_64.rpm > reference.file.list
	ls -lah ~/rpmbuild/RPMS/x86_64/$(PROJECTNAME)-$(RPM_VERSION).x86_64.rpm
	rpmlint -r rpmlint.rc  ~/rpmbuild/RPMS/x86_64/$(PROJECTNAME)-$(RPM_VERSION).x86_64.rpm > rpmlint.result

fc: srpm
	mock --no-clean --dnf -r fedora-39-x86_64 --resultdir=rpm-results  $(PROJECTTMPDIR)/$(PROJECTNAME)-${RPM_VERSION}.src.rpm

