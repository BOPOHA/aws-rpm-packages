# last build status
[![Copr build status](https://copr.fedorainfracloud.org/coprs/vorona/aws-rpm-packages/package/awsvpnclient/status_image/last_build.png)](https://copr.fedorainfracloud.org/coprs/vorona/aws-rpm-packages/package/awsvpnclient/)

# how to install

```shell
dnf copr enable vorona/aws-rpm-packages -y
dnf install awsvpnclient -y && systemctl start awsvpnclient
```

# known alternatives

- https://gist.github.com/miguelgmalpha/5c9e78d16312d156b0ec1d1c1bb09c1c
- https://github.com/JonathanxD/openaws-vpn-client
- https://github.com/samm-git/aws-vpn-client

# must read

 - https://smallhacks.wordpress.com/2020/07/08/aws-client-vpn-internals/

# where to check latest version

 - https://docs.aws.amazon.com/vpn/latest/clientvpn-user/client-vpn-connect-linux.html
