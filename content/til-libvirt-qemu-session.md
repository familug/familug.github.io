Title: [TIL] Libvirt QEMU://session has limited network funtions
Date: 2025/04/06
Category: frontpage
Tags: en, libvirt,
Slug: til-libvirt-qemu-session

https://wiki.libvirt.org/FAQ.html#what-is-the-difference-between-qemu-system-and-qemu-session-which-one-should-i-use

> What is the difference between qemu:///system and qemu:///session? Which one should I use?
> 
> All 'system' URIs (be it qemu, lxc, uml, ...) connect to the libvirtd daemon running as root which is launched at system startup. Virtual machines created and run using 'system' are usually launched as root, unless configured otherwise (for example in /etc/libvirt/qemu.conf).
> 
> All 'session' URIs launch a libvirtd instance as your local user, and all VMs are run with local user permissions.
> 
> You will definitely want to use qemu:///system if your VMs are acting as servers. VM autostart on host boot only works for 'system', and the root libvirtd instance has necessary permissions to use proper networkings via bridges or virtual networks. qemu:///system is generally what tools like virt-manager default to.
> 
> qemu:///session has a serious drawback: since the libvirtd instance does not have sufficient privileges, the only out of the box network option is qemu's usermode networking, which has nonobvious limitations, so its usage is discouraged. More info on qemu networking options: http://people.gnome.org/~markmc/qemu-networking.html
> 
> The benefit of qemu:///session is that permission issues vanish: disk images can easily be stored in $HOME, serial PTYs are owned by the user, etc.


### Kết luận

use system to able to SSH into the VM.



Hết.

HVN at <https://pymi.vn> and <https://www.familug.org>.

[Ủng hộ tác giả 🍺](https://www.familug.org/p/ung-ho.html)
