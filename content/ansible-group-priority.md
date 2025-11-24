Title: Đọc code Python xem Ansible group priority thay đổi thứ tự gộp group vars
Date: 2025/11/24
Category: frontpage
Tags: ansible, devops, python
Slug: ansible-group-priority

Ansible group dùng để nhóm các máy lại thành từng nhóm trong kho inventory.
Khi một máy nằm trong nhiều group, các group vars sẽ được gộp lại, theo thứ tự children sẽ ghi đè parent, group **sau** sẽ ghi đè group **trước**.
Sau và trước mặc định dựa theo tên group theo thứ tự bảng chữ cái.
Trong Ansible inventory có thể cấu hình group priority cho group, khi không set có giá trị mặc định là `1`, giá trị priority có kiểu int, có thể là số âm.

```py
#  lib/ansible/inventory/group.py 
class Group:
    """A group of ansible hosts."""

    def __init__(self, name: str) -> None:
        name = helpers.remove_trust(name)

        self.depth: int = 0
        self.name: str = to_safe_group_name(name)
        self.hosts: list[Host] = []
        self._hosts: set[str] | None = None
        self.vars: dict[str, t.Any] = {}
        self.child_groups: list[Group] = []
        self.parent_groups: list[Group] = []
        self._hosts_cache: list[Host] | None = None
        self.priority: int = 1
...
    def set_variable(self, key: str, value: t.Any) -> None:
        ...
        if key == 'ansible_group_priority':
            self.set_priority(int(value))
        else:
            if key in self.vars and isinstance(self.vars[key], MutableMapping) and isinstance(value, Mapping):
                self.vars = combine_vars(self.vars, {key: value})
            else:
                self.vars[key] = value
```
Xem [online GitHub](https://github.com/ansible/ansible/blob/d0473c98ba03fd4cf65af6fe30d4d870ffa5d98c/lib/ansible/inventory/group.py#L68-L85).

Khi gộp var của các groups, Ansible sắp xếp theo thứ tự tăng dần theo:

- depth: mỗi cấp children tăng depth lên 1
- group priority
- group name

rồi cho var sau ghi đè lên var trước:

```py
#  lib/ansible/inventory/helpers.py 
def sort_groups(groups):
    return sorted(groups, key=lambda g: (g.depth, g.priority, g.name))

def get_group_vars(groups):
    """
    Combine all the group vars from a list of inventory groups.

    :param groups: list of ansible.inventory.group.Group objects
    :rtype: dict
    """
    results = {}
    for group in sort_groups(groups):
        results = combine_vars(results, group.get_vars())

    return results
```
Xem [online GitHub](https://github.com/ansible/ansible/blob/d0473c98ba03fd4cf65af6fe30d4d870ffa5d98c/lib/ansible/inventory/helpers.py#L25-L40).

Nếu file inventory.yml viết:

```yml
db:
  ansible_group_priority: 20
  hosts:
    vm1:

webserver:
  hosts:
    vm1:
```

Thì var `user: abcdb` trong `group_vars/db` sẽ được dùng thay vì var `user: webuser` ghi trong `group_vars/webserver`.

### Kết luận
`ansible_group_priority` chỉ được nhắc tới 1 lần duy nhất trong tài liệu nhưng là tính năng rất quan trọng khi cần sắp xếp thứ tự ưu tiên group vars.

Hết.

HVN at <https://pymi.vn> and <https://www.familug.org>.

[Ủng hộ tác giả 🍺](https://www.familug.org/p/ung-ho.html)
