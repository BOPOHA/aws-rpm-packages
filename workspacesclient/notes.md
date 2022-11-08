# double check that there no new deletes files

```shell
cd /tmp/workspacesclient/
dpkg -c workspacesclient_*deb | sed "s#^.* \./#/#" | sort > /tmp/deb.list
rpm -ql ~/rpmbuild/RPMS/x86_64/workspacesclient-*.x86_64.rpm  | sort > /tmp/rpm.list
diff /tmp/rpm.list /tmp/deb.list
```
```txt
> /opt/workspacesclient/createdump
> /opt/workspacesclient/libcoreclrtraceptprovider.so
> /opt/workspacesclient/libdbgshim.so
> /opt/workspacesclient/libmscordaccore.so
> /opt/workspacesclient/libmscordbi.so
> /opt/workspacesclient/System.IO.Compression.Native.a
> /opt/workspacesclient/System.Native.a
> /opt/workspacesclient/System.Net.Http.Native.a
> /opt/workspacesclient/System.Net.Http.Native.so
> /opt/workspacesclient/System.Net.Security.Native.a
> /opt/workspacesclient/System.Net.Security.Native.so
> /opt/workspacesclient/System.Security.Cryptography.Native.OpenSsl.a
> /opt/workspacesclient/WorkSpacesClient.Binding.Gtk.PCoIP.pdb
> /opt/workspacesclient/WorkSpacesClient.Common.pdb
> /opt/workspacesclient/WorkSpacesClient.Common.Protocol.pdb
> /opt/workspacesclient/workspacesclient.deps.json
> /opt/workspacesclient/workspacesclient.pdb
> /opt/workspacesclient/workspacesclient.runtimeconfig.json
```

# tail logs
```shell
tail ~/.local/share/Amazon\ Web\ Services/Amazon\ WorkSpaces/logs/{,pcoip/}* -n 0 -f 
```
