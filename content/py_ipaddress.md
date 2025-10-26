Title: [Python] Tính số IP trong mạng
Date: 2025/10/26
Category: frontpage
Tags: python, network, subnet, ipv4
Slug: py_ipaddress

Python từ 3.3 có sẵn thư viện `ipaddress` rất tiện lợi để tính toán IP trong network.

### Thư viện ipaddress

```py
$ podman run -it python:3.10-alpine
...
Python 3.10.19 (main, Oct  9 2025, 22:43:20) [GCC 14.2.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import ipaddress
>>> print(ipaddress.__doc__)
A fast, lightweight IPv4/IPv6 manipulation library in Python.

This library is used to create/poke/manipulate IPv4 and IPv6 addresses
and networks.


>>> ipaddress.
ipaddress.AddressValueError(        ipaddress.IPv4Network(              ipaddress.collapse_addresses(       ipaddress.ip_network(
ipaddress.IPV4LENGTH                ipaddress.IPv6Address(              ipaddress.functools                 ipaddress.summarize_address_range(
ipaddress.IPV6LENGTH                ipaddress.IPv6Interface(            ipaddress.get_mixed_type_key(       ipaddress.v4_int_to_packed(
ipaddress.IPv4Address(              ipaddress.IPv6Network(              ipaddress.ip_address(               ipaddress.v6_int_to_packed(
ipaddress.IPv4Interface(            ipaddress.NetmaskValueError(        ipaddress.ip_interface(
>>> print(ipaddress.IPv4Network.__doc__)
This class represents and manipulates 32-bit IPv4 network + addresses..

    Attributes: [examples for IPv4Network('192.0.2.0/27')]
        .network_address: IPv4Address('192.0.2.0')
        .hostmask: IPv4Address('0.0.0.31')
        .broadcast_address: IPv4Address('192.0.2.32')
        .netmask: IPv4Address('255.255.255.224')
        .prefixlen: 27
```

Thử tạo 1 network với địa chỉ `10.10.1.241/29`:

```py
>>> ipaddress.ip_network("10.10.1.241/29", strict=False)
IPv4Network('10.10.1.240/29')
```
set strict=False vì địa chỉ đầu vào vốn không phải địa chỉ network hợp lệ, Python sẽ tự tính giá trị chính xác là `10.10.1.240`.
Còn `10.10.1.241` là 1 host trong network này.

```py
>>> ip = ipaddress.ip_network("10.10.1.241/29", strict=False)
>>> ip.
ip.address_exclude(   ip.hostmask           ip.is_multicast       ip.netmask            ip.reverse_pointer    ip.version
ip.broadcast_address  ip.hosts()            ip.is_private         ip.network_address    ip.subnet_of(         ip.with_hostmask
ip.compare_networks(  ip.is_global          ip.is_reserved        ip.num_addresses      ip.subnets(           ip.with_netmask
ip.compressed         ip.is_link_local      ip.is_unspecified     ip.overlaps(          ip.supernet(          ip.with_prefixlen
ip.exploded           ip.is_loopback        ip.max_prefixlen      ip.prefixlen          ip.supernet_of(
>>> ip.network_address
IPv4Address('10.10.1.240')
>>> ip.broadcast_address
IPv4Address('10.10.1.247')
>>> ip.netmask
IPv4Address('255.255.255.248')
>>> ip.num_addresses
8
>>> ip.prefixlen
29
```

ip object có các attribute:

- Số IP trong network: `8 == 2**(32-29) == 2**3`
- địa chỉ đầu tiên là địa chỉ network: `10.10.1.240`
- địa chỉ cuối là địa chỉ broadcast: `10.10.1.247`
- các địa chỉ còn lại từ 241 tới 246 có thể cấp cho các host.

```py
>>> type(ip)
<class 'ipaddress.IPv4Network'>
>>> ip
IPv4Network('10.10.1.240/29')
>>> ipaddress.IPv4
ipaddress.IPv4Address(    ipaddress.IPv4Interface(  ipaddress.IPv4Network(
>>> ipaddress.IPv4Address("10.10.1.242") in ip
True
>>> ipaddress.IPv4Address("10.10.1.249") in ip
False
```

### Tính tất cả các network /29 trong 10.10.1.0/24

```py
>>> nip = ipaddress.ip_network("10.10.1.0/24")
>>> for n in nip.subnets(new_prefix=29):
...     print(n)
...
10.10.1.0/29
10.10.1.8/29
10.10.1.16/29
10.10.1.24/29
10.10.1.32/29
10.10.1.40/29
10.10.1.48/29
10.10.1.56/29
10.10.1.64/29
10.10.1.72/29
10.10.1.80/29
10.10.1.88/29
10.10.1.96/29
10.10.1.104/29
10.10.1.112/29
10.10.1.120/29
10.10.1.128/29
10.10.1.136/29
10.10.1.144/29
10.10.1.152/29
10.10.1.160/29
10.10.1.168/29
10.10.1.176/29
10.10.1.184/29
10.10.1.192/29
10.10.1.200/29
10.10.1.208/29
10.10.1.216/29
10.10.1.224/29
10.10.1.232/29
10.10.1.240/29
10.10.1.248/29
```

### Kết luận
`ipaddress` có sẵn trong stdlib và rất tiện lợi.

Hết.


HVN at <https://pymi.vn> and <https://www.familug.org>.

[Ủng hộ tác giả 🍺](https://www.familug.org/p/ung-ho.html)
