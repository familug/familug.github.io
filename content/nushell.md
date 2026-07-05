Title: Tìm kiếm công cụ xử lý JSON, YAML xịn nhất: jq, yq, jmes... nushell
Date: 2025-04-16
Category: frontpage
Tags: nushell, jq, yq, jmespath, json, yaml, csv, cli
Slug: nushell

Ngành IT ngày nay ngập tràn JSON và YAML, 2 định dạng này ở khắp mọi nơi. Việc sử dụng các CLI tool truyền thống (ví dụ: grep) không hiệu quả khiến người dùng phải tìm kiếm những công cụ mới. Hàng trăm công cụ được sinh ra để truy cập/xử lý dữ liệu từ 1 JSON object, và cộng đồng khá ưa chuộng `jq`. Nhưng đây đã phải là lựa chọn tốt nhất để "xem và xử lý" JSON, YAML...? Thử các công cụ này để tìm ra giải pháp xịn nhất.

### JMESPath
JMESPath không phổ biến khi xử lý JSON tùy ý, nhưng là cú pháp có sẵn khi dùng `aws cli --query`.
JMESPath cũng có câu lệnh cli là `jp` <https://github.com/jmespath/jp> nhưng ít người biết.
Cú pháp JMESPath <https://jmespath.org/> trông hơi giống `jq` nhưng không phải, và tính năng cũng kém hơn:

```
 aws --region ap-southeast-1 lambda  list-functions --query 'Functions[?LastModified > `2023-01-02`].[FunctionName,LastModified]' --output table
-------------------------------------------------
|                 ListFunctions                 |
+--------------+--------------------------------+
|  myfunction2 |  2023-12-14T13:49:38.000+0000  |
|  pymicloud1  |  2023-12-14T16:20:11.000+0000  |
|  hntop       |  2024-01-08T14:10:58.000+0000  |
+--------------+--------------------------------+
```
khá kỳ lạ khi phải sử dụng backtick `` `2023-01-02` `` để quote JSON value, nếu dùng `"2023-01-02"` sẽ không nhận được gì!

aws cli có [2 kiểu filter: server side và client side](https://docs.aws.amazon.com/cli/latest/userguide/cli-usage-filter.html#cli-usage-filter-server-side). `--query` filter từ kết quả đã nhận được từ AWS, trong khi `--filter` sẽ filter từ phía API của AWS.

Có vấn đề với cả 2 kiểu filter này:

- server filter: chỉ một số service hỗ trợ option này như ec2, rds, và syntax của mỗi cái cũng khác nhau
- client filter: mỗi lần chỉnh sửa nội dung query là 1 lần gọi tới AWS API. Sau 10 lần chỉnh sửa để viết được query đúng thì mất rất nhiều thời gian.

Kết luận: rất khó dùng hàng ngày, trừ khi viết script cần filter trực tiếp lấy ra 1 vài giá trị. Thay vì dùng aws cli --query, có thể output ra JSON rồi dùng các công cụ sau để xử lý.

```
aws --region ap-southeast-1 lambda  list-functions  --output json > functions.json
```
### python với Jupyter notebook
Python hỗ trợ JSON từ stdlib `import json`, mọi biến đổi if else for... đều có thể thực hiện bằng cú pháp ngắn gọn.
Khi làm việc với AWS API, `import boto3` rồi viết code trên Jupyter notebook là một lựa chọn rất hấp dẫn:

- output được lưu trên Jupyter notebook
- code có thể export ra file python để làm script dùng trong hệ thống
- dễ dàng lấy output của function call này làm input cho function call khác, vì đây là lập trình.

### jq
`jq` <https://jqlang.org/tutorial/> là công cụ phổ biến nhất để xem và xử lý JSON trên CLI.

Nhược điểm: không hỗ trợ YAML.

Hiển nhiên là phải học cú pháp của `jq`, điều này là tất yếu vì tất cả các phương án trong bài này đều cần học 1 ngôn ngữ query/lập trình.

Ví dụ sau lấy ra các title có chữ "remote" từ ngày 2025-04-13 trên GitHub API repo `awesome-jobs/vietnam`:

```
curl -o issues.json  https://api.github.com/repos/awesome-jobs/vietnam/issues
cat issues.json | jq '.[] | {created_at,title,html_url} | select(.created_at > "2025-04-13" and (.title | ascii_downcase | test("remote")))'
```

Output:
```
{
  "created_at": "2025-04-16T08:48:11Z",
  "title": "[Remote Fulltime] Frontend Software Engineer - $3000 Gross - Basic English communication",
  "html_url": "https://github.com/awesome-jobs/vietnam/issues/4676"
}
{
  "created_at": "2025-04-14T11:39:43Z",
  "title": "[Remote Fulltime] Mobile Tech Lead - $4000 Gross",
  "html_url": "https://github.com/awesome-jobs/vietnam/issues/4674"
}
```
### yq
<https://github.com/mikefarah/yq>

`yq` giống như `jq` nhưng hỗ trợ cả file YAML.

>  yq is a portable command-line YAML, JSON, XML, CSV, TOML and properties processor

nên có vẻ như nếu đã dùng `jq` thì không có lý do gì để không dùng `yq` cả.

### Nushell
<https://github.com/nushell/nushell>

> A new type of shell.

Nushell là 1 shell mới hiện đại, tương tự các shell truyền thống `bash`, `zsh`,... nhưng output/input của mỗi câu lệnh là data có cấu trúc (structured data) thay vì string.

Đừng để bị đánh lừa bởi chữ `shell` vì Nushell vừa là shell, vừa là 1 ngôn ngữ lập trình functional. Cũng không cần phải dùng Nushell thay zsh/bash nếu không muốn, hãy coi nó như 1 công cụ xử lý dữ liệu trực tiếp.

<center>
![nushell]({static}/images/nushell.png)
</center>

Các command trong Nushell được viết lại hoàn toàn (bằng Rust) để hỗ trợ input/output ra các structured data thay vì string.

Bật trên container `podman run -it --rm ghcr.io/nushell/nushell`

```nu
~> ls /etc/ | sort-by modified | take 5
╭───┬──────────────┬──────┬───────┬──────────────╮
│ # │     name     │ type │ size  │   modified   │
├───┼──────────────┼──────┼───────┼──────────────┤
│ 0 │ /etc/fstab   │ file │  89 B │ 3 months ago │
│ 1 │ /etc/group-  │ file │ 510 B │ 3 months ago │
│ 2 │ /etc/inittab │ file │ 570 B │ 3 months ago │
│ 3 │ /etc/modules │ file │  15 B │ 3 months ago │
│ 4 │ /etc/motd    │ file │ 284 B │ 3 months ago │
╰───┴──────────────┴──────┴───────┴──────────────╯
```

Mỗi dòng ở dây là 1 `record` (như struct/named tuple/data class).
Output của Nushell thường là 1 bảng, dễ dàng truy cập từng cột (như pandas).
Nushell thậm chí có sẵn http client, không cần tới curl, builtin hỗ trợ [JSON, YAML, CSV, sqlite, ...](https://www.nushell.sh/book/loading_data.html#sqlite) ...

Tài liệu: <https://www.nushell.sh/book/>

#### Gửi HTTP GET request, xử lý JSON
```
http get https://api.github.com/repos/awesome-jobs/vietnam/issues |
select created_at title html_url |
where created_at > '2025-04-13' and ( $it.title |  str downcase  ) has 'remote' |
upsert created_at { |it| $it.created_at | str substring 0..9} |
to yaml
# output
- created_at: '2025-04-16'
  title: '[Remote Fulltime] Frontend Software Engineer - $3000 Gross - Basic English communication'
  html_url: https://github.com/awesome-jobs/vietnam/issues/4676
- created_at: '2025-04-14'
  title: '[Remote Fulltime] Mobile Tech Lead - $4000 Gross'
  html_url: https://github.com/awesome-jobs/vietnam/issues/4674
```

hay dùng regex:

```
where created_at > '2025-04-13' and title  =~ '(?i)remote'
```
> =~ or like	regex match / string contains another

#### Tính toán, biến đổi map, filter, reduce
Làm bài ProjectEuler 1, ghi ra file pe1:

```nu
~> 0..999 | filter {|i| $i mod 3 == 0 or $i mod 5 == 0} | reduce {|x,acc| $acc + $x} | save pe1.txt
~> open pe1.txt
233168
```
chú ý có dấu space `$acc + $x`.

#### update YAML file

```nu
~> cat pod.yaml
apiVersion: v1
kind: Pod
metadata:
  name: nginx
spec:
  containers:
  - name: nginx
    image: nginx:1.14.2
    ports:
    - containerPort: 80

~> open pod.yaml | upsert spec.containers.0.image nginx:latest | save pod2.yaml
~> cat pod2.yaml
apiVersion: v1
kind: Pod
metadata:
  name: nginx
spec:
  containers:
  - name: nginx
    image: nginx:latest
    ports:
    - containerPort: 80

```

Nushell rất khác, nên mọi kiến thức về các shell khác không dùng được ở đây, ví dụ `save` để ghi ra file chứ không phải `>`. Cách set biến environment cũng khác.
<https://www.nushell.sh/book/coming_from_bash.html>

Ở đây chỉ bàn tới việc dùng nushell để khám phá, biến đổi JSON/YAML.

Nushell còn có tính năng hỗ trợ viết tool CLI rất đơn giản và mạnh mẽ sẽ khám phá vào bài sau.

### Kết luận

Thời đại mới cần những công cụ mới. Nushell đã mở lối đi riêng trở thành một công cụ (ít người biết) rất mạnh mẽ cho thời đại AI 4.0.

Hết.

HVN at <https://pymi.vn> and <https://www.familug.org>.

[Ủng hộ tác giả 🍺](https://www.familug.org/p/ung-ho.html)
