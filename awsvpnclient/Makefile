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
	# https://docs.aws.amazon.com/vpn/latest/clientvpn-user/client-vpn-connect-linux.html
	# dists/ubuntu -> 22.04
	curl https://d20adtppz83p9s.cloudfront.net/GTK/latest/debian-repo/dists/ubuntu/main/binary-amd64/Packages -O
	rm -rf metadata && mkdir metadata
	ar p $(PROJECTTMPDIR)/*deb control.tar.zst | tar --zstd -xC metadata/
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
