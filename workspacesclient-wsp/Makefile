# required packages:
# dnf install rpmdevtools rpkg rpmlint
.PHONY: fc rpmbuild srpm spec metadata clean
.DEFAULT_GOAL := all

PROJECTNAME=$(notdir $(CURDIR))
PROJECTTMPDIR=/tmp/$(PROJECTNAME)
RPM_VERSION=$(shell rpmspec -q --qf "%{Version}-%{Release}" ${PROJECTNAME}.spec)
FEDORA_VERSION=$(shell rpm -E %fedora)

clean:
	rm -rf $(PROJECTTMPDIR)

metadata: srpm
	# https://clients.amazonworkspaces.com/linux-install
	rm -rf metadata && mkdir metadata
	ar p $(PROJECTTMPDIR)/new_*deb control.tar.xz | tar -xJC metadata/
	(cd $(PROJECTTMPDIR) && sha256sum *.deb) > checksums.sha256

spec:
	rpkg spec --spec $(PROJECTNAME).spec -p

srpm:
	spectool --get-files --directory $(PROJECTTMPDIR) $(PROJECTNAME).spec
	rpkg srpm --spec $(PROJECTNAME).spec --outdir $(PROJECTTMPDIR)

rpmbuild: srpm
	rpmbuild --nocheck --rebuild $(PROJECTTMPDIR)/$(PROJECTNAME)-$(RPM_VERSION).src.rpm
	rpm -ql ~/rpmbuild/RPMS/x86_64/$(PROJECTNAME)-$(RPM_VERSION).x86_64.rpm > reference.file.list
	rpmlint -r rpmlint.rc  ~/rpmbuild/RPMS/x86_64/$(PROJECTNAME)-$(RPM_VERSION).x86_64.rpm > rpmlint.result || :
	ls -lah ~/rpmbuild/RPMS/x86_64/$(PROJECTNAME)-$(RPM_VERSION).x86_64.rpm

fc: srpm
	mock --no-clean --dnf -r fedora-$(FEDORA_VERSION)-x86_64 --resultdir=rpm-results  $(PROJECTTMPDIR)/$(PROJECTNAME)-${RPM_VERSION}.src.rpm

all: clean metadata spec rpmbuild
