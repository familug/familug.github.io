Title: [TIL] Tên group trong inventory của Ansible là duy nhất
Date: 2025/08/13
Category: frontpage
Tags: til, ansible, inventory
Slug: til-ansible-group-names

Nếu cho 1 file inventory có:

- `host1` trong group `linux`, thuộc về group `zone1`.
- `host3` trong group `linux`, thuộc về group `zone2`.

**Hỏi: `host1` nằm trong những group nào?**

File hosts.yml

```
zone1:
  children:
    linux:
      hosts:
        host1:
    windows:
      hosts:
        host2:

zone2:
  children:
    linux:
      hosts:
        host3:
    windows:
      hosts:
        host4:
```

Dù cấu trúc biểu diễn trong file YAML ở trên trông như `host1` thuộc về `zone1` và không liên quan tới `zone2`, thì kết quả lại đáng ngạc nhiên:

```
$ uvx --from ansible-core ansible -i hosts.yml host1 -m debug -a 'msg={{group_names}}'
Installed 9 packages in 15ms
host1 | SUCCESS => {
    "msg": [
        "linux",
        "zone1",
        "zone2"
    ]
}
```

Giải thích: `host1` trong `linux` group, `linux` group thuộc children của `zone1` group, VÀ `linux` group cũng thuộc children của `zone2` group, nên kết quả: `host1` nằm trong cả group `zone1` lẫn `zone2`.

Thực hiện trên
```
$ uvx --from ansible-core ansible --version
ansible [core 2.19.0]
  ...
  python version = 3.12.8 (main, Jan 14 2025, 22:49:14) [Clang 19.1.6 ]
```
### Kết luận

Quan hệ giữa các group tưởng thẳng, nhưng lại cong.

Hết.

HVN at <https://pymi.vn> and <https://www.familug.org>.

[Ủng hộ tác giả 🍺](https://www.familug.org/p/ung-ho.html)
