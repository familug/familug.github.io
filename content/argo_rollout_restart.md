Title: [TIL] Argo Rollouts có nút bấm restart trên giao diện ArgoCD
Date: 2025/03/10
Category: frontpage
Tags: argo, k8s, kubernetes,
Slug: argo_rollout_restart

## Argo CD là gì
> Argo CD is a declarative, GitOps continuous delivery tool for Kubernetes. <https://argoproj.github.io/cd/>
 
Argo CD và FluxCD là 2 lựa chọn phổ biến để thực hiện "Continuous Delivery" (CD) trên Kubernetes. 
Argo CD có giao diện nên thường được ưa chuộng hơn.


## Argo Rollouts là gì
> Argo Rollouts is a Kubernetes controller and set of CRDs which provide advanced deployment capabilities such as blue-green, canary, canary analysis, experimentation, and progressive delivery features to Kubernetes. <https://argoproj.github.io/argo-rollouts/>

Kubernetes Deployment mặc định hỗ trợ strategy deploy RollingUpdate, nhưng chiến thuật này có nhiều hạn chế. Argo Rollouts hỗ trợ nhiều chiến thuật deploy như blue-green, canary với nhiều tính năng phức tạp hơn.

## Restart rollout
Khi cần restart các pod trong 1 rollout, các cách làm:

- xóa từng pod đi để replicaset sẽ tạo lại pod mới (không khả thi với số lượng pod lớn, bấm mỏi tay)
- xóa replicaset đi để rollout tạo lại replicaset mới 
- restart rollout: đây là 1 tính năng của Argo Rollouts, nó thậm chí có cả 1 nút bấm trong menu của rollout object trên giao diện Argo UI. <https://argoproj.github.io/argo-rollouts/features/restart/#how-it-works>

### Kết luận
Tính năng nhiều khi có ở đó, nhưng không dễ phát hiện ra, người dùng thường làm theo "bản năng" thay vì đọc doc.

Hết.

HVN at <https://pymi.vn> and <https://www.familug.org>.

[Ủng hộ tác giả 🍺](https://www.familug.org/p/ung-ho.html)
