Title: [TIL] Argo Rollouts có nút bấm restart trên giao diện ArgoCD
Date: 2025-03-10
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


## How it works
> During a restart, the controller iterates through each ReplicaSet to see if all the Pods have a creation timestamp which is newer than the restartAt time. For every pod older than the restartAt timestamp, the Pod will be evicted, allowing the ReplicaSet to replace the pod with a recreated one.

Code:

```go
func (p *RolloutPodRestarter) Reconcile(roCtx *rolloutContext) error {
  ...
	restartedAt := roCtx.rollout.Spec.RestartAt
	needsRestart := 0
	restarted := 0
	for _, pod := range rolloutPods {
		if pod.CreationTimestamp.After(restartedAt.Time) || pod.CreationTimestamp.Equal(restartedAt) {
			continue
		}
		needsRestart += 1
		if canRestart <= 0 {
			continue
		}
		if pod.DeletionTimestamp != nil {
			continue
		}
		newLogCtx := logCtx.WithField("Pod", pod.Name).WithField("CreatedAt", pod.CreationTimestamp.Format(time.RFC3339)).WithField("RestartAt", restartedAt.Format(time.RFC3339))
		newLogCtx.Info("restarting Pod that's older than restartAt Time")
		evictTarget := policy.Eviction{
			ObjectMeta: metav1.ObjectMeta{
				Name:      pod.Name,
				Namespace: pod.Namespace,
			},
		}
		err := p.client.CoreV1().Pods(pod.Namespace).Evict(ctx, &evictTarget)
    ...
```
[github.com/argoproj/argo-rollouts](https://github.com/argoproj/argo-rollouts/blob/933b7b3b1ade0d02e0d4c2fbda2e2ecd369d0612/rollout/restart.go#L62)

### Kết luận
Tính năng nhiều khi có ở đó, nhưng không dễ phát hiện ra, người dùng thường làm theo "bản năng" thay vì đọc doc.

Hết.

HVN at <https://pymi.vn> and <https://www.familug.org>.

[Ủng hộ tác giả 🍺](https://www.familug.org/p/ung-ho.html)
