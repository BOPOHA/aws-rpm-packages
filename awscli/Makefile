# required packages:
# dnf install rpmdevtools rpkg

PROJECTNAME=awscli
PROJECTTMPDIR=/tmp/$(PROJECTNAME)

clean:
	rm -rf $(PROJECTTMPDIR)

rpmprep:
	spectool --get-files --directory $(PROJECTTMPDIR) $(PROJECTNAME).spec
	rpkg srpm --spec $(PROJECTNAME).spec --outdir $(PROJECTTMPDIR)

rpmbuild: rpmprep
	rpmbuild --nocheck --noclean --rebuild $(PROJECTTMPDIR)/$(PROJECTNAME)-*.src.rpm


epel8: rpmprep
	mock --no-clean --dnf --enable-network -r centos-stream+epel-8-x86_64 --resultdir=rpm-results  $(PROJECTTMPDIR)/$(PROJECTNAME)-*.src.rpm

fc38: rpmprep
	mock --no-clean --dnf --enable-network -r fedora-38-x86_64            --resultdir=rpm-results  $(PROJECTTMPDIR)/$(PROJECTNAME)-*.src.rpm
