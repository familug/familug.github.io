Title: Tạm biệt Ubuntu, chào Debian
Date: 2022-10-04
Category: frontpage
Tags: debian, linux, ubuntu, server

Ubuntu là distro đầu tiên đưa mình vào thế giới Linux, thế giới không Windows, với phiên bản 8.04.
Nó cũng đi cùng luôn sự nghiệp khi đa phần server đều dùng Ubuntu.

<https://pymi.vn> ra đời năm 2015, chạy trên Ubuntu 14.04, sau 3 lần upgrade

- sang 16.04, thay toàn bộ Upstart init file bằng systemd
- sang 18.04, thay Python2 bằng Python3

thì lần này, mình quyết định chuyển sang dùng Debian.

![debian](https://www.debian.org/Pics/debian-logo-1024x576.png)

Debian không mới, nó là distro mà chính Ubuntu dựa trên, chỉ có một cộng đồng rất lớn,
không có công ty đứng sau.

Lý do vì ở phía server, ngày nay không có gì chỉ chạy trên Ubuntu mà ko chạy
trên Debian cả.

Debian cũng không có [câu chuyện đáng sợ về motd luôn gọi về server của Ubuntu để
chạy quảng cáo](https://blog.bityard.net/articles/2019/August/rabbit-holes-the-secret-to-technical-expertise). Mà nếu để ý, các docker file chính thức đều dùng Debian, điển hình
như [Python bullseye](https://github.com/docker-library/python/tree/master/3.11-rc/bullseye)

Việc sử dụng server debian thì gần như không khác gì Ubuntu, cấu trúc thư mục vẫn vậy,
apt vẫn vậy.

## Không phải toàn màu hồng
- năm 2021, đã từng thử cài debian trên desktop, mà lần bật lên đầu tiên bị lỗi window server (lightdm), nghỉ.
Nếu còn trẻ, rảnh, thì có lẽ sẽ ngồi tìm hiểu tại sao, rồi fix, nhưng khi chỉ muốn có cái máy chạy được thì lại quay về Ubuntu 20.04.
- vì một lý do nào đó, [tải file vagrant box về dùng]({filename}/arch_virtualbox.md) không đăng nhập được bằng tài khoản mặc định?

## Tài liệu
Debian Admin handbook <https://www.debian.org/doc/manuals/debian-handbook/>

### Kết luận
Dùng Debian cho server là một điều hoàn toàn hợp lý.

Happy hacking!
