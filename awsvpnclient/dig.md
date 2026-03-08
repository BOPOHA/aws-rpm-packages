# Debug / Trace Helper (awsvpnclient)

## Coredumps / GUI binary
```shell
strace -ff -tt -T -s 4096 -o /tmp/awsvpnclient.strace /opt/awsvpnclient/AWSVPNClient
coredumpctl info
coredumpctl gdb /opt/awsvpnclient/AWSVPNClient
```

## Service diagnostics (ACVC.GTK.Service)

### Quick status and logs
```shell
systemctl status awsvpnclient
journalctl -u awsvpnclient --no-pager -n 200
systemctl show awsvpnclient -p ExecStart -p Environment -p Restart -p RestartSec -p Result
```

### Trace DBus and socket activity (basic)
```shell
strace -f -s 256 -o /tmp/awsvpnclient.strace \
  -e trace=socket,connect,bind,listen,accept,accept4,getsockname,getpeername,getsockopt,setsockopt \
  /opt/awsvpnclient/ACVC.GTK.Service
grep -E "bind|connect|socket|listen|accept" /tmp/awsvpnclient.strace | grep -E "awsvpnclient|dbus|abstract"
```

### Trace DBus handshake and timeouts (I/O heavy)
```shell
strace -f -ttT -s 256 -o /tmp/awsvpnclient.strace.io \
  -e trace=sendto,recvfrom,sendmsg,recvmsg,read,write,poll,ppoll,select,epoll_wait,connect,getsockopt \
  /opt/awsvpnclient/ACVC.GTK.Service
grep -E "sendmsg|recvmsg|sendto|recvfrom|poll|ppoll|epoll_wait|connect" /tmp/awsvpnclient.strace.io \
  | grep -E "awsvpnclient|AF_UNIX"
```

### Verify the private D-Bus bus
```shell
dbus-send --address=unix:abstract=awsvpnclient --print-reply \
  --dest=org.freedesktop.DBus /org/freedesktop/DBus org.freedesktop.DBus.Hello
dbus-send --address=unix:abstract=awsvpnclient --print-reply \
  --dest=org.freedesktop.DBus / org.freedesktop.DBus.Peer.Ping
```

### Full process triage (one shot)
```shell
systemctl status awsvpnclient
systemctl show awsvpnclient -p ExecStart -p Environment -p Result -p ExecMainStatus -p ExecMainCode
journalctl -u awsvpnclient --no-pager -n 200
ss -xl | grep awsvpnclient
```

# Postmortems
## Important finding (March 8, 2026)

### Root cause of timeout
The `System.TimeoutException: Timeout waiting for D-Bus daemon to be ready` was not a systemd
or D-Bus configuration issue. The service was starting `dbus-daemon`, binding
`unix:abstract=awsvpnclient`, and successfully connecting to that socket. Strace showed repeated
successful `connect()` calls to the correct abstract socket.

The actual cause was a missing managed dependency:
`/opt/awsvpnclient/Service/System.IO.Pipelines.dll` from the upstream DEB package.
Without it, the service fails during startup and times out while waiting for D-Bus readiness.

### Packaging fix
The RPM spec must move `System.IO.Pipelines.dll` out of `Service/` before that directory is removed:
```
mv ./opt/%{name}/Service/System.IO.Pipelines.dll ./opt/%{name}/
```

The upstream DEB file list confirms the path:
`/opt/awsvpnclient/Service/System.IO.Pipelines.dll`
