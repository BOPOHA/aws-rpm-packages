# last build status
[![Copr build status](https://copr.fedorainfracloud.org/coprs/vorona/aws-rpm-packages/package/awsvpnclient/status_image/last_build.png)](https://copr.fedorainfracloud.org/coprs/vorona/aws-rpm-packages/package/awsvpnclient/)

# how to install

```shell
dnf copr enable vorona/aws-rpm-packages -y
dnf install awsvpnclient -y && systemctl start awsvpnclient
```

# logs
```shell
tail -f -n0 ~/.config/AWSVPNClient/logs/aws_vpn_client_*.log /var/log/aws-vpn-client/$USER/gtk_service_aws_client_vpn_connect_*.log

2024-11-16 02:28:41.155 +01:00 [DBG] [TI=5] Start method called with config file and management port password file contents.
2024-11-16 02:28:41.188 +01:00 [ERR] [TI=5] OvpnResourcesChecksumValidationFailed acvc-openvpn calculated[30784947455af7472e3b2274ded8da95a0e6eaae870c03635c4ca98f54686f2d] expected[9b6e72f18f9526b87eb6f0461c3fb3fd4a63ae5a1225c88430fb67425afdf7df]

ACVC.Core.OpenVpn.OvpnResourcesChecksumValidationFailedException: Ovpn resources checksum validation failed.
   at ACVC.Core.OpenVpn.OvpnGtkProcessManager.Start(String openVpnConfigPath, String managementPortPasswordFile, Int32 timeoutMilliseconds)
   at ACVC.Core.OpenVpn.OvpnConnectionManager.Connect(OvpnConnectionProfile configProfile, GetCredentialsCallback getCredentialsCallback, Int32 timeout)

```
# known alternatives

- https://gist.github.com/miguelgmalpha/5c9e78d16312d156b0ec1d1c1bb09c1c
- https://github.com/JonathanxD/openaws-vpn-client
- https://github.com/samm-git/aws-vpn-client

# must read

 - https://smallhacks.wordpress.com/2020/07/08/aws-client-vpn-internals/

# where to check latest version

 - https://docs.aws.amazon.com/vpn/latest/clientvpn-user/client-vpn-connect-linux.html
