Title: [TIL] Prometheus Alertmanager đôi khi không gửi alertname 
Date: 2025-02-20
Category: frontpage
Tags: til, prometheus, alertmanager
Slug: til_am_title

Template mặc định của Prometheus Alertmanager chỉ hiện các label chung khi group nhiều alert cùng "alertgroup". Việc này có thể khiến notification không chứa "alertname" trong title nếu nó group 2 alert khác alertname.

```go
{{ if gt (len .CommonLabels) (len .GroupLabels) }}({{ with .CommonLabels.Remove .GroupLabels.Names }}{{ .Values | join " " }}{{ end }})
```


Xem [code](https://github.com/prometheus/alertmanager/blob/ff470812937d56c64fd18fe700350b2dd8126df6/template/default.tmpl#L4C1-L4C317)
### Kết luận
Read the code AND the config file.

Hết.

HVN at <https://pymi.vn> and <https://www.familug.org>.

[Ủng hộ tác giả 🍺](https://www.familug.org/p/ung-ho.html)
