Title: Cài VPN với WireGuard trên Debian 11 / Ubuntu 22.04
Date: 2022-11-22
Category: frontpage
Tags: vpn, wireguard, privacy

Tự cài VPN có dễ không? xưa khó lắm nay khác xưa nhiều rồi.

![wireguard]({static}/images/wireguard.png)

## VPN là gì
Virtual Private Network (VPN) là tên một công nghệ cho phép mở rộng mạng nội bộ (private network) qua internet, nhờ đó có thể giúp kết nối mạng an toàn và riêng tư hơn.

Ví dụ khi vào một quán cafe và kết nối tới pymi.vn:

Máy bạn --> Wifi quán cafe --> nhà cung cấp mạng (ví dụ FPT) --> pymi.vn. Trên 3 con đường kết nối đó có thể rình rập nhiều nguy hiểm:

- hacker ngồi quán cafe và nghe trộm kết nối mạng rồi tấn công tạo trang giả mạo để đánh cắp tài khoản của bạn
- mọi kết nối đi qua nhà mạng FPT **có thể** được ghi lại, cũng **có thể** bị can thiệp.
- trang pymi.vn có IP của bạn có thể truy ra vị trí bạn truy cập.
- rất nhiều nữa.

Sử dụng VPN, mô hình thay đổi thành

Máy bạn --> wifi quán cafe --> nhà cung cấp mạng --> VPN --> pymi.vn

- hacker ngồi quán cafe chỉ có thể biết bạn truy cập tới IP của VPN
- nhà cung cấp mạng chỉ có thể biết bạn truy cập tới IP của VPN
- trang pymi.vn chỉ có IP của VPN server nên chỉ biết vị trí của server, không phải vị trí nhà bạn.

Vài nhược điểm:

- do thông qua thêm 1 hop (điểm) nên kết nối có thể chậm hơn một chút.
- do phải dùng thêm 1 phần mềm nên trên máy di động sẽ tốn thêm chút pin
- vì các website sẽ thấy IP của VPN server nên biết bạn đang dùng VPN và có thể sẽ chặn, ví dụ một vài sàn crypto (không phải tất cả).

Chú ý: VPN không giúp bạn trở nên "ẩn danh như hacker" trên mạng.

Cài đặt VPN vốn không phải chuyện đơn giản, vậy nên các nhà cung cấp VPN luôn ăn nên làm ra, và ngày càng nhiều:

- 1.1.1.1 của Cloudflare
- [Mozilla VPN](https://www.mozilla.org/en-US/products/vpn/more/what-is-a-vpn/)
- ProtonVPN
- search ra cả đống

Người tự cài VPN server, thường có 2 lựa chọn:

- IPSec: rất rất phức tạp
- OpenVPN: đơn giản hơn, rất phổ biến, nhưng vẫn khá phức tạp

Cho đến khoảng 2020, khi xuất hiện 1 phần mềm siêu mới, rất xịn với tên [WireGuard](https://www.wireguard.com/), cài đặt cũng dễ dàng, đã làm việc setup VPN đơn giản hơn bao giờ hết.

Về chất lượng/độ bảo mật thì đủ tin cậy khi:

- wireguard được merge code vào [Linux kernel 5.6](https://github.com/torvalds/linux/commit/bd2463ac7d7ec51d432f23bf0e893fb371a908cd)
- wireguard được [merge](https://lists.zx2c4.com/pipermail/wireguard/2020-June/005588.html) code vào [OpenBSD - hệ điều hành nổi tiếng về bảo mật (sản sinh ra OpenSSH)](/tags.html#openbsd-ref).

PS: mọi câu lệnh trong bài này đều chạy với user root.
## Cài đặt wireguard
Server dùng Debian 11 hay Ubuntu 22.04

```
sudo apt install wireguard unbound
```

## Mô hình
Để setup VPN gồm 2 bước:
- setup kết nối từ máy mình (gọi là peer) tới server (gọi là endpoint)
- config server để cho phép VPN kết nối ra ngoài internet

## Cấu hình peer <-> server
Wireguard có 2 câu lệnh, hoạt động khác nhau:

- wg
- wg-quick

ở đây sẽ dùng wg-quick để bật tắt VPN vì đơn giản hơn.

### server
Sinh private & public key:

```
# touch /etc/wireguard/private
# chmod 400 /etc/wireguard/private
# wg genkey > /etc/wireguard/private
# wg pubkey < /etc/wireguard/private > /etc/wireguard/public
```

Viết file config /etc/wireguard/wg0.conf , tên file wg0.conf sẽ dùng cho network interface tên là wg0.
Gõ man wg-quick rồi copy config mẫu.

```
[Interface]
Address = 10.10.0.1/16
PrivateKey = THAY_NOIDUNG_PRIVATE_KEY_VAO_DAY
ListenPort = 51820

[Peer]
PublicKey = THAY_NOIDUNG_PUBKEY_PEER1_VAO_DAY
AllowedIPs = 10.10.0.2/32

# [Peer]
# PublicKey = THAY_NOIDUNG_PUBKEY_PEER2_VAO_DAY
# AllowedIPs = 10.10.0.3/32
```
Address là địa chỉ IP gán cho interface của server, ví dụ này chọn private network : 10.10.0.1/16, các peer khác sẽ có IP tùy ý trong 10.10.0.2 -> 10.10.xx.yy

Gõ `ip ad | grep inet` để lấy public IP của server, dùng để config peer.

### Peer
Trên máy peer, làm tương tự các bước sinh private/public key rồi gõ config vào /etc/wireguard/wg0.conf

```
[Interface]
Address = 10.10.0.2/32
PrivateKey = PRIVATE_KEY_CUA_PEER

[Peer]
PublicKey = PUBLIC_KEY_CUA_SERVER
Endpoint = PUBLIC_IP_CUA_SERVER:51820
AllowedIPs = 0.0.0.0/0
```
rồi bật:

```
sudo wg-quick up wg0
```

### server
Copy public key của peer điền vào phần `[peer]` `THAY_NOIDUNG_PUBKEY_PEER1_VAO_DAY` trên server /etc/wireguard/wg0.conf.

Sau đó bật wireguard: `sudo wg-quick up wg0`

Gõ wg để xem public key và trạng thái kết nối của các peer.

Tới đây nếu kết nối thành công, khi gõ wg ở server sẽ thấy:

```
# wg
interface: wg0
  public key: serverpubkey
  private key: (hidden)
  listening port: 51820

peer: pXXXvEXXXX=
  endpoint: XXXX:57226
  allowed ips: 10.10.0.2/32
  latest handshake: 23 hours, 14 minutes, 44 seconds ago
  transfer: 512.48 KiB received, 824.25 KiB sent

# ip ad
...
4: wg0: <POINTOPOINT,NOARP,UP,LOWER_UP> mtu 1420 qdisc noqueue state UNKNOWN group default qlen 1000
    link/none
    inet 10.10.0.1/16 scope global wg0
       valid_lft forever preferred_lft forever
```

Ở peer có thể ping server: ping 10.10.0.1

Trên cả 2 máy (ở đây peer ví dụ là 1 máy Ubuntu), gõ
```
systemctl enable wg-quick@wg0
```
để tự bật VPN khi bật máy.

## Config để kết nối internet qua VPN
Sau các bước trên, mới chỉ kết nối tới VPN, chứ chưa kết nối ra internet được.

Để kết nối ra internet, phía server phải config cho phép "forward" các network packet, và phải config firewall để đổi IP source của máy peer thành của VPN.

Mở file /etc/sysctl.d/99-sysctl.conf
```
# Uncomment the next line to enable packet forwarding for IPv4
net.ipv4.ip_forward=1
# Uncomment the next line to enable packet forwarding for IPv6
net.ipv6.conf.all.forwarding=1
```
Rồi gõ `sysctl -p`

Tạo /etc/rc.local
```
#!/bin/sh
iptables -t nat -A POSTROUTING -s 10.10.0.0/16 -o $THAY_DEFAULT_INTERFACE -j MASQUERADE
```

với `$THAY_DEFAULT_INTERFACE` là interface mặc định xuất hiện ở output:

```
ip route | grep default
```

VD: `default via 4.3.2.1 dev eth1 proto dhcp src 4.3.2.1 metric 100` -> eth1

Rồi `chmod a+x /etc/rc.local; /etc/rc.local`

Tới đây mọi thứ đã xong có thể truy cập internet qua VPN, reboot lại server để thực hiện bài test khi server mất điện trong tương lai bật lên vẫn chạy ngon lành cành mít.

### Kiểm tra DNS leak
Khi kết nối tới VPN, người dùng không mong muốn người khác biết mình truy cập trang nào, nhưng nếu config DNS không đúng sẽ bị lộ thông tin (DNS leak).
Truy cập vào trang <https://www.dnsleaktest.com/> để test xem có bị rò rỉ DNS không. Nếu server ở nước ngoài, kết quả cũng hiện ở nước ngoài là ok.

PS: wireguard có phần mềm trên Android, iOS, Windows, MacOS và tất nhiên Linux như Debian Ubuntu.

### Kết luận
Tổng cộng thao tác

- server: 1 config 1 rc 1 sysctl là 3 file, mỗi file 2-4 dòng, gõ 2 câu lệnh
- peer: 1 config 1 rc, 2 câu lệnh

Setup VPN chưa bao giờ dễ dàng đến thế!

## Tham khảo
- <https://www.wireguard.com/quickstart/>
- <https://ubuntu.com/server/docs/wireguard-vpn-defaultgw>

Happy safe surfing.

Hết.

HVN at http://pymi.vn and https://www.familug.org.

[Ủng hộ tác giả 🍺](https://www.familug.org/p/ung-ho.html)
