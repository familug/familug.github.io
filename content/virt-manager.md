Title: virt-manager error: Failed to start network default error: Unable to create bridge virbr0: Package not installed
Date: 2023-07-24
Category: frontpage
Tags: archlinux, manjaro, virsh, virt-manager, vm, en


```
$ sudo virsh net-start default
error: Failed to start network default error: Unable to create bridge virbr0: Package not installed
```

Or turn on the VM using virt-manager:

```
Error starting domain: Requested operation is not valid: network 'default' is not active
```

### Solution
Enable libvirtd to start with the system.

```
systemctl enable libvirtd
reboot
```

HVN at <http://pymi.vn> and <https://www.familug.org>.

[Ủng hộ tác giả 🍺](https://www.familug.org/p/ung-ho.html)
