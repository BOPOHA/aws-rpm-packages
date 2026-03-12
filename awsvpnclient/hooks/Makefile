CC ?= gcc
CFLAGS ?= -fPIC
LDFLAGS ?= -shared -ldl

all: clean

hook0.so: clean
	$(CC) $(CFLAGS) -shared ../hook0.c -o hook.so -ldl

hook8.so: clean
	$(CC) $(CFLAGS) -shared hook8.c -o hook.so -ldl

clean:
	rm -f hook.so

.PHONY: all clean

findings:
	ilspycmd /opt/awsvpnclient/AWSVPNClient.Core.dll -o /tmp/awsvpn-src
	grep "processesByName.Length\|IsExclusiveAppInstance\|active users"  /tmp/awsvpn-src/AWSVPNClient.Core.decompiled.cs  -nC15 > findings.txt
