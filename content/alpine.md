Title: Cài đặt và chạy máy ảo Alpine Linux 3.13
Date: 2021-02-20
Category: frontpage
Tags: alpine, linux, virtual-machine

Alpine linux là 1 linux distro bỗng chợt phổ biến nhờ Docker.
Lý do chính Alpine Linux được dùng là vì nó nhẹ (về dung lượng), nên thích hợp
cho việc build docker image, [tạo docker image có size nhỏ hơn so với các
distro phổ biến như Ubuntu, Debian...](https://www.familug.org/2020/11/kien-truc-docker-phong-van-best-practice.html).

![alpine]({static}/images/alpinelinux-logo.svg)

Nhưng nó vốn là một Linux distro như mọi distro khác, vậy nên dùng để tạo máy ảo
là chuyện hoàn toàn bình thường.

Bài viết này giới thiệu cách tạo 1 môi trường dev Python trên máy ảo chạy Alpine Linux:

Tải file iso tối ưu cho virtual machine từ trang https://alpinelinux.org/downloads/
Ví dụ ở đây tải URL sau - bản mới nhất tại thời điểm viết bài - 3.13

https://dl-cdn.alpinelinux.org/alpine/v3.13/releases/x86_64/alpine-virt-3.13.2-x86_64.iso

File ISO này chỉ nặng có 41 MB:

```
$ ls -lh /home/hvn/Downloads/alpine*.iso
-rw-r--r--  1 hvn  hvn  41.0M Feb 20 10:16 /home/hvn/Downloads/alpine-virt-3.13.2-x86_64.iso
```

Tạo máy ảo, chọn đĩa ISO này và bật máy ảo lên, bộ cài đặt bằng dòng lệnh của Alpine rất đơn giản, chỉ cần gõ alpine-setup rồi enter liên tục cho tới khi chọn ổ đĩa ảo (vda) , cho đến khi xong.

```
Welcome to Alpine Linux 3.13
Kernel 5.10.16-0-virt on an x86_64 (/dev/ttyS0)

localhost login: root
Welcome to Alpine!

The Alpine Wiki contains a large amount of how-to guides and general
information about administrating Alpine systems.
See <http://wiki.alpinelinux.org/>.

You can setup the system with the command: setup-alpine

You may change this message by editing /etc/motd.

localhost:~# setup-alpine
Available keyboard layouts:
af     be     cn     fi     hu     it     lk     mm     pl     sy     uz
al     bg     cz     fo     id     jp     lt     mt     pt     th     vn
am     br     de     fr     ie     ke     lv     my     ro     tj
ara    brai   dk     gb     il     kg     ma     ng     rs     tm
at     by     dz     ge     in     kr     md     nl     ru     tr
az     ca     ee     gh     iq     kz     me     no     se     tw
ba     ch     epo    gr     ir     la     mk     ph     si     ua
bd     cm     es     hr     is     latam  ml     pk     sk     us
Select keyboard layout: [none]
Enter system hostname (short form, e.g. 'foo') [localhost]
Available interfaces are: eth0.
Enter '?' for help on bridges, bonding and vlans.
Which one do you want to initialize? (or '?' or 'done') [eth0]
Ip address for eth0? (or 'dhcp', 'none', '?') [dhcp]
Do you want to do any manual network configuration? (y/n) [n]
udhcpc: started, v1.32.1
udhcpc: sending discover
udhcpc: sending select for 100.64.1.3
udhcpc: lease of 100.64.1.3 obtained, lease time 4294967295
Changing password for root
New password:
Bad password: too many similar characters
Retype password:
passwd: password for root changed by root
Which timezone are you in? ('?' for list) [UTC]
 * Starting busybox acpid ...
 [ ok ]
 * Starting busybox crond ...
 [ ok ]
HTTP/FTP proxy URL? (e.g. 'http://proxy:8080', or 'none') [none]
Which NTP client to run? ('busybox', 'openntpd', 'chrony' or 'none') [chrony]
 * service chronyd added to runlevel default
 * Caching service dependencies ...
 [ ok ]
 * Starting chronyd ...

 [ ok ]

Available mirrors:
1) dl-cdn.alpinelinux.org
2) uk.alpinelinux.org
3) dl-2.alpinelinux.org
4) dl-4.alpinelinux.org
5) dl-5.alpinelinux.org
6) mirror.yandex.ru
7) mirrors.gigenet.com
8) mirror1.hs-esslingen.de
9) mirror.leaseweb.com
10) mirror.fit.cvut.cz
11) alpine.mirror.far.fi
12) alpine.mirror.wearetriple.com
13) mirror.clarkson.edu
14) linorg.usp.br
15) ftp.yzu.edu.tw
16) mirror.aarnet.edu.au
17) speglar.siminn.is
18) mirrors.dotsrc.org
19) ftp.halifax.rwth-aachen.de
20) mirrors.tuna.tsinghua.edu.cn
21) mirrors.ustc.edu.cn
22) mirrors.xjtu.edu.cn
23) mirrors.nju.edu.cn
24) mirror.lzu.edu.cn
25) ftp.acc.umu.se
26) mirror.xtom.com.hk
27) mirror.csclub.uwaterloo.ca
28) alpinelinux.mirror.iweb.com
29) pkg.adfinis.com
30) mirror.ps.kz
31) mirror.rise.ph
32) mirror.operationtulip.com
33) mirrors.ircam.fr
34) alpine.42.fr
35) mirror.math.princeton.edu
36) mirrors.sjtug.sjtu.edu.cn
37) ftp.icm.edu.pl
38) mirror.ungleich.ch
39) alpine.mirror.vexxhost.ca
40) sjc.edge.kernel.org
41) ewr.edge.kernel.org
42) ams.edge.kernel.org
43) download.nus.edu.sg
44) alpine.yourlabs.org
45) mirror.pit.teraswitch.com
46) mirror.reenigne.net
47) quantum-mirror.hu
48) tux.rainside.sk
49) alpine.cs.nctu.edu.tw
50) mirror.ihost.md
51) mirror.ette.biz
52) mirror.lagoon.nc
53) alpinelinux.c3sl.ufpr.br
54) foobar.turbo.net.id
55) alpine.ccns.ncku.edu.tw

r) Add random from the above list
f) Detect and add fastest mirror from above list
e) Edit /etc/apk/repositories with text editor

Enter mirror number (1-55) or URL to add (or r/f/e/done) [1] Added mirror dl-cdn.alpinelinux.org
Updating repository indexes... done.
Which SSH server? ('openssh', 'dropbear' or 'none') [openssh]
 * service sshd added to runlevel default
 * Caching service dependencies ...
 [ ok ]
ssh-keygen: generating new host keys: RSA DSA ECDSA ED25519
 * Starting sshd ...
 [ ok ]
Available disks are:
  vda	(10.7 GB 0x0b5d )
Which disk(s) would you like to use? (or '?' for help or 'none') [none] vda
The following disk is selected:
  vda	(10.7 GB 0x0b5d )
How would you like to use it? ('sys', 'data', 'lvm' or '?' for help) [?]

You can select between 'sys', 'data', 'lvm', 'lvmsys' or 'lvmdata'.

sys:
  This mode is a traditional disk install. The following partitions will be
  created on the disk: /boot, / (filesystem root) and swap.

  This mode may be used for development boxes, desktops, virtual servers, etc.

data:
  This mode uses your disk(s) for data storage, not for the operating system.
  The system itself will run from tmpfs (RAM).

  Use this mode if you only want to use the disk(s) for a mailspool, databases,
  logs, etc.

lvm:
  Enable logical volume manager and ask again for 'sys' or 'data'.

lvmsys:
  Same as 'sys' but use logical volume manager for partitioning.

lvmdata:
  Same as 'data' but use logical volume manager for partitioning.

The following disk is selected:
  vda	(10.7 GB 0x0b5d )
How would you like to use it? ('sys', 'data', 'lvm' or '?' for help) [?] sys
WARNING: The following disk(s) will be erased:
  vda	(10.7 GB 0x0b5d )
WARNING: Erase the above disk(s) and continue? (y/n) [n] y
Creating file systems...
Installing system on /dev/vda3:
/mnt/boot is device /dev/vda1
100% ████████████████████████████████████████████==> initramfs: creating /boot/initramfs-virt
/boot is device /dev/vda1

Installation is complete. Please reboot.

# halt
```

Cài xong, reboot lại, dùng lệnh apk để cài các gói cần thiết để code Python

```
localhost:~# apk add tmux vim git python3
(1/6) Installing libbz2 (1.0.8-r1)
(2/6) Installing libffi (3.3-r2)
(3/6) Installing gdbm (1.19-r0)
(4/6) Installing readline (8.1.0-r0)
(5/6) Installing sqlite-libs (3.34.1-r0)
(6/6) Installing python3 (3.8.7-r1)
Executing busybox-1.32.1-r3.trigger
OK: 179 MiB in 72 packages
localhost:~# python3 -m this
The Zen of Python, by Tim Peters

Beautiful is better than ugly.
Explicit is better than implicit.
Simple is better than complex.
Complex is better than complicated.
Flat is better than nested.
Sparse is better than dense.
Readability counts.
Special cases aren't special enough to break the rules.
Although practicality beats purity.
Errors should never pass silently.
Unless explicitly silenced.
In the face of ambiguity, refuse the temptation to guess.
There should be one-- and preferably only one --obvious way to do it.
Although that way may not be obvious at first unless you're Dutch.
Now is better than never.
Although never is often better than *right* now.
If the implementation is hard to explain, it's a bad idea.
If the implementation is easy to explain, it may be a good idea.
Namespaces are one honking great idea -- let's do more of those!
```


### Kết luận
Cài đặt máy ảo Alpine Linux là một việc đơn giản, nhanh chóng.

Happy hacking!
