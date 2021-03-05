Title: Máy làm việc có nên cùng hệ điều hành với server?
Date: 2021-03-01 01:02:03
Category: frontpage
Tags: sysadmin, workstation, opinion

Trước đây khi mới học dùng Linux/làm sysadmin, mình từng nghĩ việc "nếu làm
Ubuntu sysadmin thì máy bàn/ máy cá nhân phải dùng Ubuntu", để có kinh nghiệm
khi dùng hàng ngày ứng dụng cho công việc.


![Photo by <a href="https://unsplash.com/@xps?utm_source=unsplash&amp;utm_medium=referral&amp;utm_content=creditCopyText">XPS</a> on <a href="https://unsplash.com/@xps?utm_source=unsplash&amp;utm_medium=referral&amp;utm_content=creditCopyText">Unsplash</a>]({static}/images/xps.jpg)

Sau gần 8 năm đi làm (since 2013), kết luận hiện tại mình đưa ra là: không
cần thiết.

## Kiến thức đi làm khác với kiến thức dùng hàng ngày
Thứ công nghệ khiến mình bị shock nhất trong những năm đầu làm sysadmin,
đó là OpenLDAP. Bạn sẽ không bao giờ hiểu được nó là thứ gì và tại sao lại cần,
cho đến khi đi làm môi trường doanh nghiệp, khi công ty có hàng trăm hay hàng
nghìn nhân viên. Bạn sẽ không bao giờ chơi với OpenLDAP ở nhà cả, chẳng
có lý do gì làm vậy.
Ngắn gọn: OpenLDAP/ActiveDirectory hay các hệ thống "directory" thường dùng lưu
trữ
thông tin về các cá nhân, và nó hoạt động như 1 database tối ưu cho việc truy
cập, người dùng có thể dùng 1 tài khoản để đăng nhập vào nhiều chương trình
như email, dịch vụ nội bộ a,b,c... lý do là LDAP đã quá phổ biến và các
ngôn ngữ lập trình đều có sẵn thư viện giúp việc này chỉ mất < 1 ngày để làm.

Vậy nên cả ngày dùng Ubuntu, cũng chẳng giúp ích gì cho dùng OpenLDAP.

Vài thứ kiến thức / công nghệ khác mà dùng máy cá nhân giống máy server không
giúp ích gì:

- Kiến thức setup BIOS, Grub, format ổ cứng... khi server dùng cloud.
- Kiến thức về kết nối các thiết bị phần cứng: loa phím chuột
- Cấu hình wifi
- cấu hình giao diện đồ họa (DE, WM, X.org)

Vài thứ kiến thức / công nghệ mà chỉ dùng khi đi làm, còn máy cá nhân không
dùng bao giờ:

- Terraform, Kubernetes
- Databases, NGINX, Jenkins, ELK, Prometheus,...
- SaltStack, Ansible (có thể dùng nhưng rất giới hạn).

## Những kiến thức hữu dụng cả ở máy cá nhân/làm việc và công việc
Thành thạo sử dụng các câu lệnh UNIX, vừa giúp các công việc hàng ngày, vừa
hữu dụng khi đi làm:

- cd
- cp
- find
- grep
- ls
- mkdir
- mv
- ps
- top
- vi

.., xem thêm tại [đây](https://www.familug.org/2014/11/cmd-linux-utilities-co-gi-can-thiet.html).

các chương trình này đều tuân theo chuẩn "POSIX" và tương tự nhau trên các
hệ điều hành: Ubuntu, Fedora, ArchLinux,... OSX/MacOS, OpenBSD, FreeBSD,
hay cả Windows Subsystem for Linux (WSL).

- git/GitHub/GitLab
- tmux
- cài máy ảo (KVM/VirtualBox) hay dùng container (docker) để có môi trường
  giống server khi cần thiết.
- kiến thức network: ping, netstat, DNS, iptable, tcpdumb...
- kiến thức lập trình
- đọc log

Những thứ "căn bản" này, lại là thứ hữu ích.

## Kết luận
Kinh nghiệm với một công nghệ nào đó, có giá trị ở một mức độ nhất định.
Người dùng máy bàn Ubuntu 10 năm, giỏi cấu hình giao diện đẹp lóng lánh,
cũng khó chắc mà đủ kiến thức và kinh nghiệm Kubernetes, hay OpenLDAP để đi làm.

Chuyện server chạy Ubuntu còn máy làm việc/cá nhân dùng MacOS, Windows (WSL),
hay ArchLinux, OpenBSD đều hoàn toàn bình thường, OK. Thậm chí, các lập trình
viên sang chảnh giờ đều dùng MacOS trong khi code đều chạy trên một Linux server
nào đó như Ubuntu.

Xông lên và khám phá những thứ mới, những hệ điều hành mới, dùng 1 workstation
OS giống máy server sẽ không giúp bạn quá nhiều. Nếu đã plan sau 5 năm trở
thành senior DevOps, 2 năm đầu hãy dùng Ubuntu, rồi mỗi năm sau đó chuyển qua
1 OS mới, càng khác biệt càng tốt: Fedora, ArchLinux, FreeBSD/OpenBSD...
kinh nghiệm thu được sẽ nhiều hơn là 5 năm làm đi làm lại 1 vài task trên
Ubuntu.
