Title: Using virtual machine via vmd on OpenBSD 6.8
Date: 2021-02-20 16:00:00
Category: en,
Tags: openbsd, vmm, alpine, debian

OpenBSD 6.8 comes with the vmm(4) hypervisor and vmd(8) daemon.
Instead of installing VirtualBox or look for kvm on OpenBSD, everything
is already there, a built-in virtualization solution.

### Check wiki FAQ first
https://www.openbsd.org/faq/faq16.html

it lists all features, not ready features, prequisites, basic commands.

## Distro
Sure run OpenBSD guest on OpenBSD host is "should just work", it's fully tested.
But for Linux based OS, the options are not much:

It's a real coincidence, someone asked the question two days ago on Reddit:
https://www.reddit.com/r/openbsd/comments/llscql/most_easiest_linux_distro_to_install_in_vmd/

Thanks to the answers there, I tried many but success only some:

- AlpineLinux: use "Virtual" edition https://alpinelinux.org/downloads/
  "it just works", just boot on and run `setup-alpine`
- Debian: I used `debian-10.8.0-amd64-netinst.iso `,
  after start, type Tab, then enter ` console=ttyS0,115200 ` then enter,
  the text-based-curse-like UI would work.

And these failed:

- Ubuntu: `ubuntu-20.04.2-live-server-amd64.iso`, failed.
- NixOS: failed at phase 2/3 of systemd.
- ArchLinux: failed with error `ACPI BIOS Error (bug): A valid RSDP was not found (20200925/tbxfroot-210)`

Most of these default to use Video, thus must add boot parameter:

> type Tab, then enter ` console=ttyS0,115200 ` then enter,

https://help.ubuntu.com/lts/installation-guide/amd64/ch05s03.html

### Network
Setup `pf` and `sysctl net.inet.ip.forwarding=1`
as metioned in [FAQ, `NAT for the VMs`](http://www.openbsd.org/faq/faq16.html#VMMnet)

After installed, can ssh from OpenBSD host to guest via, change to your IP get from
output of `ip ad` after installed:

```
ssh root@100.64.1.3 -v
```

Note that password login seems always fail even put correct password
(or maybe Linux-based OS disabled them by default). Copy your pubkey
to `/root/.ssh/authorized_keys` then ssh would work.

### Commands

Two major important commands:

#### Create image

```
vmctl create -s 10G image.qcow2
```

#### Start VM

```
vmctl start \
  -i 1 \ # 1 interface
  -L \ # create interface
  -c \ # auto connect console after started
  -m 1G \ # 1G memory
  -r file.iso \ # path to ISO file (CD)
  -d image.qcow2 \ # image created above
  myvm # name of VM
```

```
vmctl status
vmctl stop ID
```

The start command would start and give the name temporary, after installed,
create a file at `/etc/vm.conf` with config like:

```
vm "alpine" {
	disable  # disable auto start when boot
	memory 1G
	disk "/root/linux.qcow2"
    local interface
}
```

### Result
VMs installed successfully run smoothly on vmd, low CPU usage (compare to
VirtualBox on MacOS).

Have fun.
