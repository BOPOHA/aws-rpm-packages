# required packages:
# dnf install rpmdevtools rpkg
.PHONY: fc rpmbuild srpm spec metadata clean

PROJECTNAME=workspacesclient-wsp
PROJECTTMPDIR=/tmp/$(PROJECTNAME)
RPM_VERSION=$(shell rpmspec -q --qf "%{Version}-%{Release}" ${PROJECTNAME}.spec)

clean:
	rm -rf $(PROJECTTMPDIR)

matadata: srpm
	# https://clients.amazonworkspaces.com/linux-install
	rm -rf metadata && mkdir metadata
	ar p $(PROJECTTMPDIR)/*deb control.tar.xz | tar -xJC metadata/
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
	mock --no-clean --dnf -r fedora-39-x86_64 --resultdir=rpm-results  $(PROJECTTMPDIR)/$(PROJECTNAME)-${RPM_VERSION}.src.rpm
