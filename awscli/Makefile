# required packages:
# dnf install rpmdevtools rpkg

PROJECTNAME=$(notdir $(CURDIR))
PROJECTTMPDIR=/tmp/$(PROJECTNAME)
RPM_VERSION=$(shell rpmspec -q --qf "%{Version}-%{Release}" ${PROJECTNAME}.spec)
FEDORA_VERSION=$(shell rpm -E %fedora)

clean:
	rm -rf $(PROJECTTMPDIR)

rpmprep:
	spectool --get-files --directory $(PROJECTTMPDIR) $(PROJECTNAME).spec
	rpkg srpm --spec $(PROJECTNAME).spec --outdir $(PROJECTTMPDIR)

rpmbuild: rpmprep
	rpmbuild --nocheck --noclean --rebuild $(PROJECTTMPDIR)/$(PROJECTNAME)-$(RPM_VERSION).src.rpm
	rpm -ql ~/rpmbuild/RPMS/x86_64/$(PROJECTNAME)-$(RPM_VERSION).x86_64.rpm > reference.file.list
	rpmlint -r rpmlint.rc  ~/rpmbuild/RPMS/x86_64/$(PROJECTNAME)-$(RPM_VERSION).x86_64.rpm > rpmlint.result || :
	ls -lah ~/rpmbuild/RPMS/x86_64/$(PROJECTNAME)-$(RPM_VERSION).x86_64.rpm

epel8: rpmprep
	mock --no-clean --dnf --enable-network -r centos-stream+epel-8-x86_64 --resultdir=rpm-results  $(PROJECTTMPDIR)/$(PROJECTNAME)-*.src.rpm

fc: rpmprep
	mock --no-clean --dnf --enable-network -r fedora-$(FEDORA_VERSION)-x86_64            --resultdir=rpm-results  $(PROJECTTMPDIR)/$(PROJECTNAME)-*.src.rpm
