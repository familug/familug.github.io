Title: Post-install setup on OpenBSD 7.4
Date: 2024-02-12
Category: en,
Tags: openbsd, wifi, ifconfig, fw_update

After installing OpenBSD 7.4, here are customizations to make it more usable.

```
$ uname -a
OpenBSD obsd.dev.obsd 7.4 GENERIC.MP#2 amd
```

### Install wireless driver
Run `ifconfig` and see interface names.

```
$ ifconfig | grep flags | grep -o .*:
lo0:
re0:
iwx0:
enc0:
pflog0:
```

In this case, the interface named `iwx0`. Find details about it in `dmesg`:

```
$ dmesg | grep iwx0 
iwx0: could not read firmware iwx-cc-a0-77 (error 2)
```

Download the driver from <http://firmware.openbsd.org/firmware/>, choose the version you using, in this case is 7.4: <http://firmware.openbsd.org/firmware/7.4/iwx-firmware-20230629.tgz>

copy the file to an USB formatted as vfat filesystem so all OSes can read from it.

### Mount USB
Find the partition to mount: run as root

If the device is `sd1`, use `sd1c` as `man disklabel` explained:

> disklabel supports 15 configurable partitions, a through p
> excluding c.  The c partition describes the entire physical
> disk, is automatically created by the kernel, and cannot be
> modified or deleted by disklabel.

```
# disklabel -h /dev/sd1c
# /dev/sd1c:                                                            
type: SCSI                                                              
disk: SCSI disk                                                         
label: DataTraveler 3.0                                                 
duid: 0000000000000000
flags:
bytes/sector: 512
sectors/track: 63
tracks/cylinder: 255
sectors/cylinder: 16065
cylinders: 1884
total sectors: 30277632 # total bytes: 15138816.0K
boundstart: 0
boundend: 30277632 

16 partitions:
#                size           offset  fstype [fsize bsize   cpg]
  c:      15138816.0K                0  unused                    
  i:           480.0K               64   MSDOS                    
  j:        679424.0K             1024   MSDOS    
```

Here the partition we want to mount is `j`.

```
obsd# mount /dev/sd1j /mnt/                                            
obsd# ls /mnt
iwx-firmware-20230629.tgz
```

Run as root: `fw_update /mnt/iwx-firmware-20230629.tgz` to install the driver.


### Turn on wifi
Run as root:

```
# ifconfig iwx0 nwid WIFI_NAME wpakey PASSWORD
# ifconfig iwx0 up
# dhclient iwx0
```

To auto-connect to the wifi on startup, add a file named: `/etc/hostname.iwx0` with content:

```
nwid WIFI_NAME wpakey PASSWORD
inet autoconf
```

Note: change `iwx0` in filename to your real interface name.

### Install packages

```
# pkg_add firefox git tmux redshift
```

### Update firmware

```
# fw_update
```

### Change window manager

Default window manager is fwwm, right click choose cwm.

To set it permanently, write a file at `$HOME/.xsession`

```
# use UTF-8 everywhere
export LANG=en_US.UTF-8

# load Xresources file
xrdb -merge $HOME/.Xresources

xsetroot -solid slategrey &
xterm &
redshift &
exec cwm
```

Read `man cwm` for default key bindings.

### Enable power management to suspend
```
rcctl start apmd
```

Then type `zzz` to suspend.

Append a line to /etc/rc.conf.local

```
apmd_flags=
```
To start apmd with system.

## Conclusion
Hello OpenBSD once again in 2024!
