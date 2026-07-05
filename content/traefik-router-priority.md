Title: Đọc code Go Traefik xem router ưu tiên match theo độ dài rule
Date: 2025-09-14
Category: frontpage
Tags: traefik, go,
Slug: traefik-router-priority


## Traefik là gì
> Traefik (pronounced traffic) is a modern HTTP reverse proxy and load balancer that makes deploying microservices easy. Traefik integrates with your existing infrastructure components (Docker, Swarm mode, Kubernetes, Consul, Etcd, Rancher v2, Amazon ECS, ...) and configures itself automatically and dynamically. Pointing Traefik at your orchestrator should be the only configuration step you need.

Traefik là một HTTP reverse proxy và load balancer giúp triển khai microservices dễ dàng.
Traefik có tính năng tương tự NGINX, với điểm mạnh lớn nhất là khả năng tích hợp, cấu hình tự động với hệ thống đã chạy như Kubernetes, Docker, ...

Traefik được viết bằng Go, về hiệu năng chưa có gì vượt trội so với NGINX, nhưng có nhiều tính năng hiện đại như: tích hợp HTTPS dễ dàng, hỗ trợ sẵn dashboard, metrics, rate limit,...

## Build Traefik từ source

Tạo file build.sh
```sh
git clone https://github.com/traefik/traefik --depth 1 --branch v3.5
cd traefik
touch webui/static/index.html
make dist
/usr/bin/time -v make binary
./dist/linux/amd64/traefik version
```

Chạy để build với go1.24:
```
bash build.sh
Cloning into 'traefik'...
remote: Enumerating objects: 2215, done.
remote: Counting objects: 100% (2215/2215), done.
remote: Compressing objects: 100% (1713/1713), done.
remote: Total 2215 (delta 654), reused 1107 (delta 427), pack-reused 0 (from 0)
Receiving objects: 100% (2215/2215), 12.89 MiB | 9.15 MiB/s, done.
Resolving deltas: 100% (654/654), done.
fatal: No names found, cannot describe anything.
mkdir -p dist
fatal: No names found, cannot describe anything.
SHA: 27a820950a316451da3d52091cdfac7138e4ee8a cheddar 2025-09-14_04:31:45AM
CGO_ENABLED=0 GOGC= GOOS=linux GOARCH=amd64 go build  -ldflags "-s -w \
    -X github.com/traefik/traefik/v3/pkg/version.Version=27a820950a316451da3d52091cdfac7138e4ee8a \
    -X github.com/traefik/traefik/v3/pkg/version.Codename=cheddar \
    -X github.com/traefik/traefik/v3/pkg/version.BuildDate=2025-09-14_04:31:45AM" \
    -installsuffix nocgo -o "./dist/linux/amd64/traefik" ./cmd/traefik
	Command being timed: "make binary"
	User time (seconds): 5.59
	System time (seconds): 1.02
	Percent of CPU this job got: 150%
	Elapsed (wall clock) time (h:mm:ss or m:ss): 0:04.40
	Maximum resident set size (kbytes): 2106624
    ...
	Exit status: 0
Version:      27a820950a316451da3d52091cdfac7138e4ee8a
Codename:     cheddar
Go version:   go1.24.0
Built:        2025-09-14_04:31:45AM
OS/Arch:      linux/amd64
```

## Sửa code router in ra chi tiết priority

Thêm 1 dòng print
```go
diff --git a/pkg/server/router/router.go b/pkg/server/router/router.go
index 44f6950..12c6589 100644
--- a/pkg/server/router/router.go
+++ b/pkg/server/router/router.go
@@ -142,6 +142,8 @@ func (m *Manager) buildEntryPointHandler(ctx context.Context, entryPointName str
                        routerConfig.Priority = httpmuxer.GetRulePriority(routerConfig.Rule)
                }

+               fmt.Printf("FML priority name: %v rule: '%s' len: %d\n", routerName, routerConfig.Rule, routerConfig.Priority)

                if routerConfig.Priority > maxUserPriority && !strings.HasSuffix(routerName, "@internal") {
                        err = fmt.Errorf("the router priority %d exceeds the max user-defined priority %d", routerConfig.Priority, maxUserPriority)
                        routerConfig.AddError(err, true)

```
rồi build lại.

## Cấu hình Prometheus metrics cho Traefik

```
# traefik.yml
entryPoints:
  web:
    address: :2280
log:
  level: DEBUG
accessLog:
  addInternals: true
metrics:
  addInternals: true
  prometheus:
    manualRouting: true
    entryPoint: web
providers:
  file:
    filename: ./traefik_provider.yml
    watch: true
```

```
# traefik_provider.yml
http:
  routers:
    router1:
      entryPoints:
        - web
      service: prometheus@internal
      rule: PathPrefix(`/metrics`)
      observability:
        accessLogs: true
    regexrouter2:
      entryPoints:
        - web
      service: prometheus@internal
      rule: PathRegexp(`/me.*`)
      observability:
        accessLogs: true
```

Chạy:

```
 ./traefik/dist/linux/amd64/traefik --configfile traefik.yml
2025-09-14T11:40:01+07:00 DBG traefik/cmd/traefik/traefik.go:114 > Static configuration loaded [json] staticConfiguration={"accessLog":{"addInternals":true,"fields":{"defaultMode":"keep","headers":{"defaultMode":"drop"}},"filters":{},"format":"common"},"entryPoints":{"web":{"address":":2280","forwardedHeaders":{},"http":{"maxHeaderBytes":1048576,"sanitizePath":true},"http2":{"maxConcurrentStreams":250},"transport":{"lifeCycle":{"graceTimeOut":"10s"},"respondingTimeouts":{"idleTimeout":"3m0s","readTimeout":"1m0s"}},"udp":{"timeout":"3s"}}},"global":{"checkNewVersion":true},"log":{"format":"common","level":"DEBUG"},"metrics":{"addInternals":true,"prometheus":{"addEntryPointsLabels":true,"addServicesLabels":true,"buckets":[0.1,0.3,1.2,5],"entryPoint":"web","manualRouting":true}},"providers":{"file":{"filename":"./traefik_provider.yml","watch":true},"providersThrottleDuration":"2s"},"serversTransport":{"maxIdleConnsPerHost":200},"tcpServersTransport":{"dialKeepAlive":"15s","dialTimeout":"30s"}}
...
FML priority name: router1@file rule: 'PathPrefix(`/metrics`)' len: 22
...
FML priority name: regexrouter2@file rule: 'PathRegexp(`/me.*`)' len: 19
...
127.0.0.1 - - [14/Sep/2025:04:40:06 +0000] "GET /metrics HTTP/1.1" 200 2065 "-" "-" 1 "router1@file" "-" 1ms
127.0.0.1 - - [14/Sep/2025:04:41:31 +0000] "GET /metrics_but_longer HTTP/1.1" 200 2057 "-" "-" 1 "router1@file" "-" 1ms
```

## Traefik ưu tiên các route có rule dài hơn
Khi truy cập `curl localhost:2280/metrics_but_longer` thấy Traefik log đã match `router1@file`:

- `router1` chứa rule có độ dài 22 ký tự nên được ưu tiên match trước.
- `regexrouter2` chứa rule chỉ có 19 kí tự

> To avoid path overlap, routes are sorted, by default, in descending order using rules length. The priority is directly equal to the length of the rule, and so the longest length has the highest priority. [source](https://github.com/traefik/traefik/blob/v3.5/docs/content/reference/routing-configuration/http/router/rules-and-priority.md#priority-calculation)

Trong code <https://github.com/traefik/traefik/blob/27a820950a316451da3d52091cdfac7138e4ee8a/pkg/muxer/http/mux.go#L73-L88> thực hiện sort các router theo priority:

```go
// AddRoute add a new route to the router.
func (m *Muxer) AddRoute(rule string, syntax string, priority int, handler http.Handler) error {
    matchers, err := m.parser.parse(syntax, rule)
    if err != nil {
        return fmt.Errorf("error while parsing rule %s: %w", rule, err)
    }

    m.routes = append(m.routes, &route{
        handler:  handler,
        matchers: matchers,
        priority: priority,
    })

    sort.Sort(m.routes)

    return nil
}
...
// routes implements sort.Interface.
type routes []*route

// Len implements sort.Interface.
func (r routes) Len() int { return len(r) }

// Swap implements sort.Interface.
func (r routes) Swap(i, j int) { r[i], r[j] = r[j], r[i] }

// Less implements sort.Interface.
func (r routes) Less(i, j int) bool { return r[i].priority > r[j].priority }
```
`Sort` interface sắp xếp theo thứ tự tăng dần:

> Sort sorts data in ascending order as determined by the Less method.
> It makes one call to data.Len to determine n and `O(n*log(n))` calls to
> data.Less and data.Swap. The sort is not guaranteed to be stable.

Nhưng function `Less` ở đây trả về true khi phần tử `r[i].priority > r[j].priority`, tức priority càng cao thì xem như càng đứng trước, vì vậy route có priority cao nhất sẽ đứng đầu.

Khi `ServeHTTP` nhận HTTP request, nó duyệt qua các routes, route có priority cao hơn được duyệt trước:

```
// ServeHTTP forwards the connection to the matching HTTP handler.
// Serves 404 if no handler is found.
func (m *Muxer) ServeHTTP(rw http.ResponseWriter, req *http.Request) {
    ...
    for _, route := range m.routes {
        if route.matchers.match(req) {
            route.handler.ServeHTTP(rw, req)
            return
        }
    }

    m.defaultHandler.ServeHTTP(rw, req)
}
```

Một ngày đẹp trời mà xấu số, người dùng thêm điều kiện kiểm tra Host vào `regexrouter2`:

```
      rule: PathRegexp(`/me.*`) && Host(`localhost`)
```
vô tình khiến route `regexrouter2` có priority là 40 và được match trước:

```
> FML priority name: regexrouter2@file rule: 'PathRegexp(`/me.*`) && Host(`localhost`)' len: 40
...
> 127.0.0.1 - - [14/Sep/2025:08:26:40 +0000] "GET /metrics_but_longer HTTP/1.1" 200 8682 "-" "-" 1 "regexrouter2@file" "-" 0ms
```

### Kết luận
Người dùng nên chỉ định priority cụ thể cho từng route trong config để tránh bất ngờ khi thay đổi config tưởng chừng vô hại lại có thể đảo lộn thứ tự match route:

```
http:
  routers:
    router1:
      entryPoints:
        - web
      service: prometheus@internal
      rule: PathPrefix(`/metrics`)
      priority: 200
    regexrouter2:
      entryPoints:
        - web
      service: prometheus@internal
      rule: PathRegexp(`/me.*`) && Host(`localhost`)
      priority: 100
```

Hết.

HVN at <https://pymi.vn> and <https://www.familug.org>.

[Ủng hộ tác giả 🍺](https://www.familug.org/p/ung-ho.html)
