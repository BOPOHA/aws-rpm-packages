# AI Notes (awsvpnclient)

Purpose: minimize future context loading by capturing decisions and required state.

## Do Not Touch
- `metadata/` is for tracking DEB contents only. Do not edit it for RPM changes.

## Systemd Integration (RPM)
- Socket activation is not used because `ACVC.GTK.Service` spawns its own dbus-daemon
  and fails if the socket is pre-bound. Do not ship a socket unit.
- Files are provided as RPM Sources and installed into `/etc/systemd/system/`:
  - `awsvpnclient.service.override.conf` -> `/etc/systemd/system/awsvpnclient.service.d/override.conf`

### Override file status
- The drop-in exists for future experiments but is currently empty except for a note.

## Preset Policy
- Preset file: `70-awsvpnclient.preset`
- Must enable service by default:
```
enable awsvpnclient.service
```

## Scriptlet Policy (Fedora/RHEL guidance)
 - Use systemd macros only; no direct `systemctl` calls in scriptlets.
 - Single invocation per scriptlet:
   - `%systemd_post %{name}.service`
   - `%systemd_preun %{name}.service`
   - `%systemd_postun_with_restart %{name}.service`

## Files added in this session
- `awsvpnclient.service.override.conf`

## Spec integration
- `awsvpnclient.spec` includes:
  - `Source2: awsvpnclient.service.override.conf`
  - `%install` installs it into `/etc/systemd/system/...`
  - `%files` lists `/etc/systemd/system/awsvpnclient.service.d/override.conf`

## Known missing file fixed
- The upstream DEB ships `/opt/awsvpnclient/Service/System.IO.Pipelines.dll`.
- RPM packaging must move it out of `Service/` before that directory is removed.
- Spec now includes: `mv ./opt/%{name}/Service/System.IO.Pipelines.dll ./opt/%{name}/`
