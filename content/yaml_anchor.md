Title: YAML không phải JSON
Date: 2023-07-17
Category: frontpage
Tags: YAML, anchor, alias, merge, JSON,

### YAML dễ dùng để viết file cấu hình
YAML là định dạng file phổ biến `.yaml` hay `.yml`, thường dùng để viết file cấu hình cho phần mềm như Kubernetes, Ansible, SaltStack, Elasticsearch, ...
Phổ biến tới mức ngày nay có hẳn nghề: ["YAML engineer"](https://www.google.com/search?hl=en&q=yaml%20engineer).

YAML được ưa chuộng để viết file cấu hình thay vì dùng JSON do các nhược điểm của JSON:

- Khó sửa: thiếu/thừa dấu `,` hay nhầm dấu `"` với `'` là hỏng ngay
- Không hỗ trợ comment #ahuhu

Cú pháp YAML cơ bản khá dễ dàng tương đương với JSON, tên gọi khác nhau do JSON (JavaScript Object Notation) dùng tên của JavaScript:

**object** này chứa **name** `tags` với **value** là 1 **array**
```json
{"my name": "FAMILUG",
 "age": 13,
 "tags": ["Python", "Linux"]}
```

**mapping** này chứa **key** `tags` với **value** là 1 **sequence**
```yaml
my name: FAMILUG
age: 13
tags:
  - Python
  - Linux
```

Dừng lại ở đó, đủ dùng 10 năm.

### YAML có nhiều tính năng
JSON chỉ dùng để biểu diễn dữ liệu, viết 1 là 1, viết 2 là 2, YAML có nhiều tính năng bất ngờ... như merge 2 mappings.

#### YAML anchor và YAML alias
Hai từ tiếng Anh này khá dễ đọc sai, phiên âm:

- anchor `/ˈæŋ.kɚ/`
- alias `/ˈeɪ.li.əs/`

<http://yaml.org/spec/1.2.0/#id2565016>

Anchor `&NAME` để ký hiệu vị trí của 1 giá trị, `*NAME` để chỉ tới (refer) nội dung của anchor. Khái niệm này tương tự con trỏ (pointer) trong các ngôn ngữ như C, C++, Go, Rust,...

`NAME` có thể là bất kỳ kí tự gì ngoài `[]{},`:

```py
from ruamel.yaml import YAML
yaml = YAML(typ='safe')

yaml.load(
    """first name: &F-n python
    second: *F-n"""
)
# {'first name': 'python', 'second': 'python'}
```

Ví dụ này dùng tên `F-n` làm anchor name.

#### YAML merge
[YAML Merge](https://yaml.org/type/merge.html) `<<` là một tính năng optional của bản 1.1, có thư viện có thể hỗ trợ, có thư viện thì không.

> Specify one or more mappings to be merged with the current one.

```yaml
yaml.load("""
d1: &head
  name: FAMILUG
  age: 18
d2: &body
  name: PyMi
  color: WhitePink
d3:
  <<: [*head, *body]
  """
)
```
Kết quả

```py
{'d1': {'name': 'FAMILUG', 'age': 18},
 'd2': {'name': 'PyMi', 'color': 'WhitePink'},
 'd3': {'name': 'FAMILUG', 'color': 'WhitePink', 'age': 18}}
```

đáng chú ý rằng khác với Python dict update, value sau sẽ đè lên value trước nếu cùng key, thì YAML ngược lại, giá trị xuất hiện trước sẽ được dùng: name được lấy ở phần tử d1 FAMILUG chứ không phải từ d2.

### Dùng trong thực tế
[dockercompose file](https://docs.docker.com/compose/compose-file/10-fragments/):
```docker
volumes:
db-data: &default-volume
driver: default
metrics: *default-volume

services:
first:
  image: my-image:latest
  environment: &env
    FOO: BAR
    ZOT: QUIX
second:
  image: another-image:latest
  environment:
    <<: *env
    YET_ANOTHER: VARIABLE
```

[GitLabCI](https://docs.gitlab.com/ee/ci/yaml/yaml_optimization.html#anchors):

```yaml
.default_scripts: &default_scripts
- ./default-script1.sh
- ./default-script2.sh

job1:
script:
  - *default_scripts
  - ./job-script.sh
```

Helm <https://helm.sh/docs/chart_template_guide/yaml_techniques/>

K8S kustomize <https://github.com/kubernetes-sigs/kustomize/issues/3675>

## Tham khảo
- [Thảm họa PyYAML]({filename}/pyyaml.md)
- <http://yaml.org/spec/1.2.0/>
- <https://www.json.org/json-en.html>
- <https://yaml.readthedocs.io/en/latest/basicuse.html>

## Kết luận
YAML, không phải MarkUp Language, càng không phải là JSON.

Hết.

HVN at <http://pymi.vn> and <https://www.familug.org>.

[Ủng hộ tác giả 🍺](https://www.familug.org/p/ung-ho.html)
