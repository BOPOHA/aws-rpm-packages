This repository is a collection of spec files for building RPM packages for AWS software.

AWS develops applications to work with its services, and usually supports Linux, but does not respect RPM.

Every paranoid person can build a package locally and install it.

For careless people there is Fedora COPR repo.

```shell
dnf copr enable vorona/aws-rpm-packages
```

Packages from the Specs of this repository are built and hosted there.

Supported packages.

| package                              | status                                                                                                                                                                                                                                  |
|--------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| [awscli](awscli)                     | [![Copr build status](https://copr.fedorainfracloud.org/coprs/vorona/aws-rpm-packages/package/awscli/status_image/last_build.png)](https://copr.fedorainfracloud.org/coprs/vorona/aws-rpm-packages/package/awscli/)                     |
| [awsvpnclient](awsvpnclient)         | [![Copr build status](https://copr.fedorainfracloud.org/coprs/vorona/aws-rpm-packages/package/awsvpnclient/status_image/last_build.png)](https://copr.fedorainfracloud.org/coprs/vorona/aws-rpm-packages/package/awsvpnclient/)         |
| [workspacesclient](workspacesclient) | [![Copr build status](https://copr.fedorainfracloud.org/coprs/vorona/aws-rpm-packages/package/workspacesclient/status_image/last_build.png)](https://copr.fedorainfracloud.org/coprs/vorona/aws-rpm-packages/package/workspacesclient/) |
| [workspacesclient-wsp](workspacesclient-wsp) | [![Copr build status](https://copr.fedorainfracloud.org/coprs/vorona/aws-rpm-packages/package/workspacesclient-wsp/status_image/last_build.png)](https://copr.fedorainfracloud.org/coprs/vorona/aws-rpm-packages/package/workspacesclient-wsp/) |
