Title: Máy không có IPv6, ai query DNS record AAAA?
Date: 2023-12-10
Category: frontpage
Tags: DNS, IPV6, tcpdump, getaddrinfo, gethostbyname

Đa phần các máy tính vào cuối 2023 đều đã sử dụng IPv6, đặc biệt là các Linux server. Nhưng khi đã tắt IPv6, disable qua sysctl:

```sh
# sysctl -w net.ipv6.conf.all.disable_ipv6=1
```

bật tcpdump vẫn thấy các ứng dụng query AAAA record (lấy địa chỉ IPv6 tương ứng với domain), tại sao?

## Thí nghiệm

Mở 1 cửa sổ chạy tcpdump port 53:

```
root@box:~# tcpdump port 53
tcpdump: verbose output suppressed, use -v[v]... for full protocol decode
listening on eth0, link-type EN10MB (Ethernet), snapshot length 262144 bytes
...

```

Mở cửa sổ khác, bật Python3, import socket và gọi các function để lấy địa chỉ IP từ tên miền:

```py
>>> import socket
>>> socket.gethostbyname("pymi.vn")
'104.21.61.168'
>>> socket.gethostbyname("pymi.vn")
'172.67.212.45'
>>> socket.getaddrinfo("familug.org")
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: getaddrinfo() missing 1 required positional argument: 'port'
>>> socket.getaddrinfo("familug.org", 443)
[(<AddressFamily.AF_INET: 2>, <SocketKind.SOCK_STREAM: 1>, 6, '', ('216.239.32.21', 443)), (<AddressFamily.AF_INET: 2>, <SocketKind.SOCK_DGRAM: 2>, 17, '', ('216.239.32.21', 443)), (<AddressFamily.AF_INET: 2>, <SocketKind.SOCK_RAW: 3>, 0, '', ('216.239.32.21', 443))]
>>>
```

Đoạn code trên sử dụng `gethostbyname`, một function cổ điển để lấy IP, tương ứng với function trên C, xem `man 3 gethostbyname`.

Kết quả tcpdump sẽ chỉ có IPv4:

```sh
12:21:25.019583 IP box.41423 > 192.168.122.1.domain: 57705+ A? pymi.vn. (25)
12:21:25.020054 IP 192.168.122.1.domain > box.41423: 57705 2/0/0 A 172.67.212.45, A 104.21.61.168 (57)
```

Còn khi query familug.org, sử dụng function `getaddrinfo` kèm them port 443, kết quả

```sh
12:21:39.722169 IP box.49228 > 192.168.122.1.domain: 29210+ A? familug.org. (29)
12:21:39.722208 IP box.49228 > 192.168.122.1.domain: 23059+ AAAA? familug.org. (29)
12:21:39.889210 IP 192.168.122.1.domain > box.49228: 29210 1/0/0 A 216.239.32.21 (45)
12:21:39.896108 IP 192.168.122.1.domain > box.49228: 23059 0/1/0 (90)
```

thấy có query id 23059 `AAAA? familug.org.` và kết quả 0/1/0.

`gethostbyname` đã rất cũ và hiện nay được coi là **obsoleted** (lỗi thời), các ứng dụng hiện đại đều được khuyên dùng `getaddrinfo`.

> The obsolescent h_errno external integer, and the obsolescent gethostbyaddr() and gethostbyname() functions are removed, along with the HOST_NOT_FOUND, NO_DATA, NO_RECOVERY, and TRY_AGAIN macros.
<https://pubs.opengroup.org/onlinepubs/9699919799/>

Vậy nên dù máy không có IPv6, ứng dụng vẫn gọi `getaddrinfo`, function này vẫn sẽ lấy địa chỉ IPv6 của domain tương ứng.

Và có vẻ như không thể dễ dàng disable tính năng nay, tức các ứng dụng sẽ luôn query IPv6 dù muốn hay không.

## Kết luận
AAAA là DNS record IPv6, `getaddrinfo` luôn lấy cả 4 và 6... để được điểm 10.

## Tham khảo
- [How to disable AAAA lookups?](https://serverfault.com/questions/632665/how-to-disable-aaaa-lookups)
- man 3 gethostbyname
- man 3 getaddrinfo

[Ủng hộ tác giả 🍺](https://www.familug.org/p/ung-ho.html)
