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

```shell
/usr/bin/fips-mode-setup --check #--enable

[pid 70401] lstat("/opt/awsvpnclient/System.Private.CoreLib.pdb", 0x7ffc83c555a0) = -1 ENOENT (No such file or directory)

[pid  4709] open("/opt/awsvpnclient/Resources/openvpn/openssl.cnf", O_RDONLY) = 3
[pid  4709] read(3, "config_diagnostics = 1\nopenssl_conf = openssl_init\n\n.include /opt/awsvpnclient/Service/Resources/openvpn/fipsmodule.cnf\n\n[openssl_init]\nproviders = provider_sect\nssl_conf = ssl_module\n\n[ssl_module]\nsystem_default = tls_system_default\n\n[tls_system_default]\nGroups = secp384r1\n\n[provider_sect]\nfips = fips_sect\nbase = base_sect\n\n[base_sect]\nactivate = 1\n", 1024) = 352
[pid  4709] getuid()                    = 0
[pid  4709] geteuid()                   = 0
[pid  4709] getgid()                    = 0
[pid  4709] getegid()                   = 0
[pid  4709] stat("/opt/awsvpnclient/Service/Resources/openvpn/fipsmodule.cnf", 0x7fffe3a3cff0) = -1 ENOENT (No such file or directory)
[pid  4709] brk(0x5635174f9000)         = 0x5635174f9000
[pid  4709] read(3, "", 1024)           = 0
[pid  4709] close(3)                    = 0
[pid  4709] writev(2, [{iov_base="", iov_len=0}, {iov_base="FATAL: Startup failure (dev note: apps_startup()) for /opt/awsvpnclient/Resources/openvpn/openssl\n", iov_len=98}], 2) = 98
[pid  4709] writev(2, [{iov_base="", iov_len=0}, {iov_base="08DD7BB1E57F0000:error:80000002:system library:process_include:No such file or directory:crypto/conf/conf_def.c:822:calling stat(/opt/awsvpnclient/Service/Resources/openvpn/fipsmodule.cnf)\n", iov_len=189}], 2) = 189
[pid  4709] writev(2, [{iov_base="", iov_len=0}, {iov_base="08DD7BB1E57F0000:error:07800069:common libcrypto routines:provider_conf_load:provider section error:crypto/provider_conf.c:218:section=fips_sect not found\n", iov_len=155}], 2) = 155
[pid  4709] writev(2, [{iov_base="", iov_len=0}, {iov_base="08DD7BB1E57F0000:error:0700006D:configuration file routines:module_run:module initialization error:crypto/conf/conf_mod.c:276:module=providers, value=provider_sect retcode=-1      \n", iov_len=181}], 2) = 181
[pid  4709] rt_sigprocmask(SIG_BLOCK, ~[RTMIN RT_1 RT_2], [], 8) = 0
--
[pid  4665] <... futex resumed>)        = 0
[pid  4042] <... waitid resumed>0x7f9e427fbc90, WNOHANG|WEXITED|WNOWAIT, NULL) = -1 ECHILD (No child processes)
[pid  4665] pwrite64(129, "2024-11-16 05:17:22.351 +01:00 [DBG] [TI=17] OpenSSL fips provider not active:\n\n", 80, 786472 <unfinished ...>
[pid  4042] read(71,  <unfinished ...>
[pid  4665] <... pwrite64 resumed>)     = 80
[pid  4665] pwrite64(129, "2024-11-16 05:17:22.351 +01:00 [DBG] [TI=17] UnableToEnforceFipsCode\n", 69, 786552) = 69

```
# known alternatives

- https://gist.github.com/miguelgmalpha/5c9e78d16312d156b0ec1d1c1bb09c1c
- https://github.com/JonathanxD/openaws-vpn-client
- https://github.com/samm-git/aws-vpn-client

# must read

 - https://smallhacks.wordpress.com/2020/07/08/aws-client-vpn-internals/

# where to check latest version

 - https://docs.aws.amazon.com/vpn/latest/clientvpn-user/client-vpn-connect-linux.html
