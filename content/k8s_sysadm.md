Title: Dùng kubernetes không phức tạp hơn việc thường ngày của sysadmin
Date: 2021-11-14
Category: frontpage
Tags: K8S, kubernetes, container

Bài viết dành cho các sysadmin/DevOps:

- Những người nghe nói đến K8S và các lời chê về sự phức tạp của nó
- Những người định học dùng K8S mà ngại nhiều khái niệm mới.

Những người có kiến thức về các hệ thống trước "thời" Kubernetes (K8S), giúp kết nối các khái niệm, hiểu lý do tại sao K8S lại phức tạp đến thế.

<img src="https://kubernetes.io/images/wheel.svg" width=600>

Để **dùng** K8S, người dùng sẽ gặp phải một loạt các khái niệm:

- pod
- deployment
- rollout
- replicaset
- daemonset
- service
- configmap
- secret
- namespace
- resourcequota
- persistentVolume
- PersistentVolumeClaim

Sau đó các khái niệm ngoài K8S, các tool dùng với K8S như:

- helm/chart
- ...

tất cả các khái niệm này đều không mới, chỉ là các tên mới dành cho hệ thống dùng container, tương đương với các khái niệm/kiến thức khi quản trị một hệ thống server truyền thống (máy ảo/máy vật lý).

### Pod
Pod là đơn vị nhỏ nhất được quản lý trong K8S. Pod là một hoặc nhiều container cùng bật cùng tắt, cùng chung IP, cùng chung ổ cứng. Vì mỗi container thường là một 1 process, nên nếu cần chạy 2 process khác nhau thì cần có 2 container. Trên server Linux truyền thống, nếu cần chạy 1 service (systemd) và muốn chạy 1 script mỗi ngày, người ta có thể dễ dàng dùng cron, cron luôn được cài sẵn, luôn có ở đó. Trong thế giới container, muốn chạy 1 process là cần bật 1 container mới. Một pod có thể chứa 1 container chạy chương trình chính, 1 container chạy cron.

Người mới dùng container (như Docker), sẽ thường hỏi: [làm thế nào để chạy cron trong container](https://stackoverflow.com/questions/37458287/how-to-run-a-cron-job-inside-a-docker-container):

> Trả lời ngắn gọn: bật thêm 1 container chạy crond.

Khi K8S đã có khái niệm cronjob thì không cần chạy container trong pod để chạy cron như nói trên nữa, nhưng pod vẫn có thể chứa các container chạy thứ khác.

Pod thường được config tự restart khi tắt, tương tự tác dụng quan trọng của các hệ thống init như Systemd hay Upstart, SysV.

### Deployment
Một deployment chứa 1 replicaset.
Một replicaset lo việc chạy N pod hay gọi là N replicas.
Khi tạo 1 deployment nginx với replicas=5, nó sẽ tạo ra 5 pods, dễ dàng tăng giảm số replica.

deployment lo chuyện ... deploy. Khi deploy (triển khai) một phiên bản mới của phần mềm, sysadmin sẽ phải lo xử lý bản cũ, làm thế nào để deploy, cho người dùng truy cập vào bản mới bản cũ ra sao, theo các chiến thuật nào: [blue-green, canary, rolling?](https://spinnaker.io/docs/concepts/#deployment-strategies)

Bài toán này luôn tồn tại khi cần deploy một phần mềm, một hệ thống, chưa bao giờ biến mất. Không dùng K8S, sysadmin sẽ phải dùng tool khác, hoặc tự xây dựng theo một mô hình với các tool dùng khi deploy như Jenkins, ansible, bash...

### Daemonset
daemonset liên quan tới "chuyện của kubernetes": khi cần đảm bảo mỗi node của K8S cần có duy nhất 1 pod chạy một chương trình (thường là các "agent" xử lý logging/metrics để các pod trên cùng node gửi log/metric qua "agent" này tới nơi tập trung), daemonset đảm bảo tính duy nhất trên mỗi node và có ở mọi node.

Vấn đề này cũng tồn tại trong hệ thống truyền thống, mọi server đều cần cài logging agent (fluentd/filebeat...) /metric agent (nếu dùng pull model như prometheus, hay push sử dụng statsd).

### PersistentVolume
### PersistentVolumeClaim
Mọi server đều có ổ cứng (trong container gọi là volume), có server cần nhiều ổ cứng. PersistentVolume + PersistentVolumeClaim thực hiện chuyện cấp phát/quản lý ổ cứng (như làm gì volume khi pod đã tắt).

Các doanh nghiệp lớn nếu từng dùng Ceph hay GlusterFS thì dùng Volume là khái niệm tương đương.

### Namespace, resourcequota
Khi có nhiều phòng ban, doanh nghiệp sẽ cần phân chia tài nguyên cho mỗi phòng ban. Namespace giúp phân tách các resource (pod/deploy/service...) theo các namespace khác nhau, và áp dụng quota (giới hạn) khác nhau. Giúp việc phân chia tài nguyên máy tính cho các phòng ban.

### configmap
Sự khác nhau giữa 2 server chạy NGINX là config của chúng. Container thường chỉ chứa chương trình, người dùng sẽ phải cung cấp config mong muốn, file config không được build sẵn trong image của container mà cung cấp qua configmap trước khi chạy - dù là config file hay qua biến  environment.

### secret
Trên server truyền thống, các secret như pasword/token thường được ghi vào config file/set trong environment  variable trước khi service chạy. Việc quản lý các secret này thường: "do sysadmin/devops X biết", "trong trí nhớ của anh" hay thậm chí ghi vào giấy nhớ dán trong phòng sysadmin... một số công ty có thể dùng phần mềm quản lý password rồi chia sẻ cho team như keepass, 1password, Hashicorp Vault...
Trên kubernetes chứa chúng trong "secret".

PS: secret này mặc định không mã hóa (encrypt), chỉ encode base64 nên không có tính bảo mật.

PSS: có thể bật encrypt.

### service
service thực hiện việc cho cả thế giới truy cập vào 1 deployment. Thường sử dụng LoadBalancer trên các hệ thống cloud để chia đều các kết nối cho các pod.

Trên server truyền thống, đó là cài NGINX hay HAProxy, cấu hình IP, VIP (Virtual IP), đảm bảo High Availability (HA) cho dịch vụ vẫn hoạt động khi 1 máy chạy NGINX/HAProxy bị tắt.

### helm/chart
Linux server truyền thống cài phần mềm bằng apt/yum/dnf, cấu hình bằng copy/sửa tay các file config, thì từ 2010 trở đi, bắt đầu phổ biến việc cài đặt + cấu hình bằng 1 Configuration Management tool như Salt/Ansible/Chef/Puppet.

Chức năng chính thường có:

- download hay dùng apt/yum để cài phần mềm
- copy một vài file template rồi điền giá trị vào vị trị
- tạo, cấu hình chmod/chown một vài file, thư mục
- start service (systemd/upstart/sysV)

Trên kubernetes, Helm là công cụ phổ biến nhất để làm chuyện này.

- khai báo container image để K8S tải về
- các config/secret cần để service chạy và điền vào file config qua Go template.
- tạo service/deployment rồi chạy

## Kết luận
Kubernetes có nhiều khái niệm, nhưng không nhiều hơn quản lý server truyền thống, không khó hơn, nhưng tất nhiên việc phải học lại từ đầu những thứ đã biết mà tương đương sẽ không dễ chịu chút nào.

PS: bài này không nói về bên trong K8S, các thành phần để chạy nó hay việc cài đặt vận hành K8S, etcd, kubelet...
Một số có thể phản biện: không hiểu bên trong kubernetes thế nào sao chạy, mặc dù trong thế giới sysadmin truyền thống, số người hiểu về bên trong Linux Kernel, Systemd, NGINX, SaltStack, Ansible, Jenkins cũng không đủ nhiều.

## The end
