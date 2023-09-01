Title: Truy cập website chỉ với TCP socket - Python, Perl, Bash
Date: 2023-08-31
Category: frontpage
Tags: python, perl, bash, http

Thời đại ngày nay khi mọi ngôn ngữ lập trình đều có sẵn hay dễ dàng cài thư viện HTTP client, HTTP dần trở thành "hộp đen" ít người thọc vào táy máy. Chỉ có 1 TCP socket, liệu có kết nối HTTP được không? let's do it

CHÚ Ý: HTTP, không phải HTTPS

## HTTP/1.1 protocol
Truy cập: HTTP/1.0 hay HTTP/1.1 là protocol (giao thức) dùng text, chỉ cần gửi các string đi là nhận được response.

Cấu trúc 1 HTTP/1.x request:

CRLF là Carriage Return and Line Feed `\r\n`

### HTTP request format
```
Method Request-URI HTTP-Version CRLF
headers CRLF
message-body
```

Chạy HTTP server có sẵn ở python3

```
$ python3 -m http.server
Serving HTTP on 0.0.0.0 port 8000 (http://0.0.0.0:8000/) ...
127.0.0.1 - - [31/Aug/2023 19:06:49] "GET / HTTP/1.1" 200 -
```

### Gửi HTTP request bằng lệnh nc (netcat)

```
$ nc localhost 8000
GET / HTTP/1.1
header1=value

HTTP/1.0 200 OK
Server: SimpleHTTP/0.6 Python/3.11.3
Date: Thu, 31 Aug 2023 12:06:49 GMT
Content-type: text/html; charset=utf-8
Content-Length: 6504
...
```

### Gửi HTTP request bằng Python3 socket
Python3

```py
import socket
# tạo 1 TCP socket (SOCK_STREAM)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Kết nối tới địa chỉ 127.0.0.1 port 8000
sock.connect(("127.0.0.1", 8000))
# Gửi HTTP request
sock.send(b"GET / HTTP/1.1\r\nheader=1\r\nbody\r\n\r\n")
# Nhận 1024 bytes kết quả, in 2 dòng đầu
print(sock.recv(1024).splitlines()[:2])
# [b'HTTP/1.0 200 OK', b'Server: SimpleHTTP/0.6 Python/3.11.3']
sock.close()
```

### Gửi HTTP request bằng Perl
but why?

Khi thế giới đều chạy trên server, Python có ở mọi nơi, gần như mọi hệ điều hành UNIX/Linux thì khi thế giới chạy container (docker, K8S), Python không còn có ưu điểm này nữa. Container cắt giảm tối đa các phần mềm cài trên đó, thường không có Python, nhưng bất ngờ thay nhiều khi vẫn có perl hay bash.

```perl
# perl http.pl
use IO::Socket;
my $sock = new IO::Socket::INET (
                                 PeerAddr => '127.0.0.1',
                                 PeerPort => '8000',
                                 Proto => 'tcp',
                                );
die "Could not create socket: $!\n" unless $sock;
print $sock "GET / HTTP/1.1\r\n";
print $sock "Host: any.domain.org\r\n\r\n";
print while <$sock>;
close($sock);
```

### Gửi HTTP request bằng bash
Khi không có perl, thì bash cũng được. CHÚ Ý: bash chứ không phải zsh hay dash.

Một tính năng có từ lâu, ít được biết tới, phụ thuộc vào option khi compile bash mà có hay không:

> --enable-net-redirections
>   This enables the special handling of filenames of the form /dev/tcp/host/port and /dev/udp/host/port when used in redirections (see Redirections).

```bash
$ exec 3<>/dev/tcp/127.0.0.1/8000
$ echo -e "GET / HTTP/1.1\r\n\r\n" >&3
$ cat <&3
Server: SimpleHTTP/0.6 Python/3.11.3
Date: Fri, 01 Sep 2023 02:54:38 GMT
Content-type: text/html; charset=utf-8
...
```
Xem thêm <https://www.xmodulo.com/tcp-udp-socket-bash-shell.html>

> /dev/tcp/host/port
>   If host is a valid hostname or Internet address, and port is an integer port number or service name, Bash attempts to open the corresponding TCP socket.

## Tham khảo
- <https://www.gnu.org/software/bash/manual/bash.html#Redirections>

## Kết luận
HTTP 1 thật đơn giản, không như HTTP/2.
Khi chỉ cần gửi HTTP request trong container, ai cần đến `curl` nữa?

Hết.

HVN at <http://pymi.vn> and <https://www.familug.org>.

[Ủng hộ tác giả 🍺](https://www.familug.org/p/ung-ho.html)
