Title: Thảm họa PyYAML
Date: 2023-06-09
Category: frontpage
Tags: yaml, pyyaml, python

PyYAML, thư viện parse YAML phổ biến bậc nhất của Python, được dùng trong các phần mềm dùng yaml như Ansible, SaltStack, ...

```
> YAML: YAML Ain't Markup Language™
```

Ví dụ [Salt](https://docs.saltproject.io) state:
```yaml
install_network_packages:
  pkg.installed:
    - pkgs:
      - rsync
      - lftp
      - curl
```

### Mặc định nguy hiểm
YAML không phải một ngôn ngữ/format đơn giản như JSON, nó có hàng tá tính năng mà có thể bạn không biết tới. Dùng YAML giống như dùng `pickle` hơn là `json` (có thể chứa object tùy ý).

```py
def double(x):
    return x+x
import sys
yaml.dump(double, sys.stdout)
# !!python/name:__main__.double ''
```

Function mặc định (và siêu phổ biến) để đọc file YAML: `yaml.load`, có thể chạy code Python, và là tác giả của hàng loạt lỗ hổng bảo mật được gắn CVE:

- [CVE-2017-18342](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2017-18342) In PyYAML before 5.1, the yaml.load() API could execute arbitrary code if used with untrusted data. The load() function has been deprecated in version 5.1 and the 'UnsafeLoader' has been introduced for backward compatibility with the function.
- Rất nhiều nữa <https://www.opencve.io/cve?vendor=pyyaml>...

Đến sau 2017, người dùng mới bắt đầu làm quen với function mới `yaml.safe_load`, an toàn hơn.

## Phức tạp, nhiều phiên bản
JSON có... 1 phiên bản duy nhất?!!

YAML có 1.0 1.1 1.2 và còn nữa.
Phiên bản 1.2 có từ 2009, mà PyYAML chỉ hỗ trợ YAML 1.1

```
>   - YAML 1.2:
    - Revision 1.2.2      # Oct 1, 2021 *New*
    - Revision 1.2.1      # Oct 1, 2009
    - Revision 1.2.0      # Jul 21, 2009
  - YAML 1.1
```

Muốn dùng YAML 1.2, phải dùng `ruamel.yaml`

```
  - PyYAML        # YAML 1.1, pure python and libyaml binding
  - ruamel.yaml   # YAML 1.2, update of PyYAML; comments round-trip
```

### PyYAML 6.0+ không tương thích phiên bản cũ
Phiên bản mới nhất 6.0, ra đời năm 2021, không tương thích với code các bản cũ.

6.0

```py
import yaml
yaml.load("key: value", Loader=yaml.CLoader)
```
**CHỮ L ở `Loader=` VIẾT HOA**

5
```py
import yaml
yaml.load("key: value")
```

bản 6 bắt buộc argument Loader phải được set. Tới tháng 6 2023, tài liệu tutorial trang chủ vẫn không update <https://pyyaml.org/wiki/PyYAMLDocumentation>:

```
>>> yaml.load("""
... - Hesperiidae
... - Papilionidae
... - Apatelodidae
... - Epiplemidae
... """)
```

Issue GitHub: <https://github.com/yaml/pyyaml/issues/576>

May thay nếu dùng `yaml.safe_load` thì không đổi, nó sẽ gọi `Loader=yaml.SafeLoader)`

```py
def safe_load(stream):
    """
    Parse the first YAML document in a stream
    and produce the corresponding Python object.

    Resolve only basic YAML tags. This is known
    to be safe for untrusted input.
    """
    return load(stream, SafeLoader)
```

### Tham khảo
- <https://yaml.org/>

### Kết luận
YAML không đơn giản như JSON, nếu không nhất thiết, chớ động vào.

Hết.

HVN at <http://pymi.vn> and <https://www.familug.org>.

[Ủng hộ tác giả 🍺](https://www.familug.org/p/ung-ho.html)
