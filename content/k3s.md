Title: Tạo và code Python tương tác với Kubernetes trên local dùng k3s
Date: 2023-11-14
Category: frontpage
Tags: kubernetes, python, k3s

Kubernetes vốn mang tiếng phức tạp, lằng nhằng, và không ai phải đối chuyện này... không phản đối nhưng vẫn sinh ra 1 phiên bản Kubernetes nhỏ nhẹ hơn có thể chạy trên cả thiết bị Raspberry Pi tí hon, đó là K3S.

K8S - 5 == K3S

Trang chủ: <https://k3s.io/>

> The certified Kubernetes distribution built for IoT & Edge computing

K3S rất nhẹ, chỉ 1 binary < 80MB, chạy tốn ít tài nguyên:

```sh
root         842  5.8 12.8 1344004 514540 ?      Ssl  14:30   1:25 /usr/local/bin/k3s server
```

Ví dụ chạy trên máy ảo hết 500MB RAM và chiếm 5% CPU.

(đang chạy 2 pod 1 NGINX 1 redis).

Ngoài k3s, có nhiều sản phẩm khác tương tự như minikube, hay microk8s.

## Cài đặt
```
curl -sfL https://get.k3s.io | sh -
# Check for Ready node, takes ~30 seconds
sudo k3s kubectl get node
```

ngay sau khi kết thúc câu lệnh trên, gõ xem cluster đang chạy:

```
# kubectl get nodes
NAME       STATUS   ROLES                  AGE   VERSION
bullseye   Ready    control-plane,master   29m   v1.27.7+k3s2
```

k3s chạy cả master lẫn "worker" node trên cùng 1 máy, và vẫn nhẹ nhàng.

## Tạo namespace
Tạo namespace mới cho quen, thay vì mãi dùng `default`:

```
# kubectl create namespace webdev
# kubectl get namespace
NAME              STATUS   AGE
default           Active   32m
kube-system       Active   32m
kube-public       Active   32m
kube-node-lease   Active   32m
webdev            Active   19m
```

## Tạo alias viết cho ngắn
Thêm vào ~/.bashrc
```sh
alias k=kubectl
```
rồi gõ `source ~/.bashrc`
Từ giờ gõ `k` thay vì `kubectl`

## Tạo deployment, pod

Tạo 1 deploy (deployment) ghi ra file cache.yaml, deploy redis pods

```
k -n webdev create deploy --image=redis cache -o yaml --dry-run=client  > cache.yaml
```

Người dùng k8s thường tạo các resource bằng `kubectl create` bởi không ai nhớ đống YAML thụt ra thụt vào kia có những gì.

Mở file này ra xem nội dung:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  creationTimestamp: null
  labels:
    app: nginx
  name: nginx
spec:
  replicas: 1
  selector:
    matchLabels:
      app: nginx
  strategy: {}
  template:
    metadata:
      creationTimestamp: null
      labels:
        app: nginx
    spec:
      containers:
      - image: nginx
        name: nginx
        resources: {}
status: {}
```
Sửa gì nếu muốn, apply để tạo deployment:

```
# k apply -f cache.yaml
```

chờ một lúc gõ xem pod được tạo

```
# k -n webdev get pod
NAME                   READY   STATUS    RESTARTS   AGE
cache-7cfdc6cc-zgvnm   1/1     Running   0          23m
```

## Code python tương tác với Kubernetes qua thư viện client kubernetes

[Thư viện chính thức](https://kubernetes.io/docs/reference/using-api/client-libraries/) được hỗ trợ: `pip install kubernetes`

Tạo file Kube config tại ~/.kube/config để làm file config mặc định.
Do k3s không có file này, link đến file của k3s:

```
ln -s /etc/rancher/k3s/k3s.yaml ~/.kube/config
```

Bật Python lên và code:

```py
# python3
Python 3.9.2 (default, Feb 28 2021, 17:03:44)
[GCC 10.2.1 20210110] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> from kubernetes import config, client
>>> config.load_config()
>>> core = client.CoreV1Api()
>>> res = core.list_namespaced_pod(namespace="webdev", label_selector="app=cache")
>>> res.items[0].metadata.name
'cache-7cfdc6cc-zgvnm'
>>> res.items[0].spec
{'active_deadline_seconds': None,
 'affinity': None,
 'automount_service_account_token': None,
 'containers': [{'args': None,
 ...
```

Rất ngon lành, rất đơn giản.

## Tham khảo
<https://github.com/kubernetes-client/python/>

## Kết luận
k3s là một giải pháp tuyệt vời để nghịch chơi kubernetes trên máy local!

Hết.

HVN at <http://pymi.vn> and <https://www.familug.org>.

[Ủng hộ tác giả 🍺](https://www.familug.org/p/ung-ho.html)
