Title: Docker image alpine/curl không phải alpine
Date: 2024-08-02
Category: frontpage
Tags: alpine, curl, docker, container,

Nếu cần chạy 1 câu lệnh curl (hay http client khác để truy cập web API) trên container, dùng image nào nhẹ nhất?

## alpine rồi cài curl

[`alpine`]({filename}/alpine.md) vốn phổ biến trong giới container vì nhẹ, nhưng không có sẵn curl, phải cài:

```
$ podman run -it alpine sh -c 'apk add curl>/dev/null; curl https://www.openbsd.org/robots.txt'
User-agent: *
Disallow: /cgi-bin/
Disallow: /donations.html
```

## alpine/curl KHÔNG PHẢI alpine
Google alpine curl xem image alpine nào cài sẵn curl? thấy ngay kết quả top `alpine/curl`, và dùng có vẻ thành công:

```
$ podman run -it docker.io/alpine/curl sh -c 'curl https://www.openbsd.org/robots.txt'
Trying to pull docker.io/alpine/curl:latest...
Getting image source signatures
Copying blob 9f444ea7cf45 done
Copying blob 299588fda28b done
Copying blob c6a83fedfae6 done
Copying config d4f2de61cf done
Writing manifest to image destination
Storing signatures
User-agent: *
Disallow: /cgi-bin/
Disallow: /donations.html
```

**NHƯNG** `alpine` này là tên của 1 người dùng, không phải của hệ điều hành `alpine`. Nhờ cách đặt tên thông minh này mà tác giả đã khiến hàng trăm triệu lượt tải `alpine/git`

- alpine user Bill Wang: <https://hub.docker.com/u/alpine>
- alpine linux OS (Docker official image): <https://hub.docker.com/_/alpine>

## busybox wget
busybox rất nhỏ, và có sẵn wget, wget khác curl <https://daniel.haxx.se/docs/curl-vs-wget.html> nhưng đủ tính năng để truy cập 1 HTTP API:

Option `-O FILE		Save to FILE ('-' for stdout)`  và `-q		Quiet`

```
$ podman run -it busybox wget -qO- https://www.openbsd.org/robots.txt                 [0]
wget: note: TLS certificate validation not implemented
User-agent: *
Disallow: /cgi-bin/
Disallow: /donations.html
```

## So sánh kích thước image
```
$ podman images
REPOSITORY                              TAG         IMAGE ID      CREATED        SIZE
docker.io/alpine/curl                   latest      d4f2de61cfdf  5 days ago     13.7 MB
docker.io/library/alpine                latest      a606584aa9aa  5 weeks ago    8.09 MB
docker.io/library/busybox               latest      65ad0d468eb1  14 months ago  4.5 MB
```

busybox nhỏ nhất.

## Kết luận
Tránh bị "bất ngờ" vì `alpine/curl` hay `alpine/git` không đến từ `alpine`.

[Ủng hộ tác giả 🍺](https://www.familug.org/p/ung-ho.html)
