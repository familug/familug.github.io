Title: Ansible không ưu tiên CLI option --user cao bằng inventory 
Date: 2025/11/01
Category: frontpage
Tags: ansible, inventory
Slug: ansible-remote-user-option

99% các chương trình có giao diện dòng lệnh CLI đều ưu tiên option được người dùng chỉ định mức ưu tiên cao nhất. Ansible đặc biệt, vì nó nằm trong 1% còn lại.

Mặc định, ansible sử dụng user của người dùng gõ lệnh `$USER` để ssh vào máy cần quản lý. Người dùng có thể thay đổi giá trị này với option `--user REMOTE_USER`. Nhưng khi trong inventory có chỉ định `ansible_user` thì khác:

```yml
all:
  hosts:
    vm1:
      ansible_host: 127.0.0.1
      ansible_user: inventory_user
```

Chạy:

```
$ ansible-playbook -i inventory.yml order.yml --user cli_user

PLAY [all] **************************************************************************

TASK [Gathering Facts] **************************************************************
[ERROR]: Task failed: Failed to connect to the host via ssh: inventory_user@127.0.0.1: Permission denied (publickey,password).
fatal: [vm1]: UNREACHABLE! => {"changed": false, "msg": "Task failed: Failed to connect to the host via ssh: inventory_user@127.0.0.1: Permission denied (publickey,password).", "unreachable": true}

PLAY RECAP **************************************************************************
vm1                        : ok=0    changed=0    unreachable=1    failed=0    skipped=0    rescued=0    ignored=0   
```

ansible sử dụng user `inventory_user` cấu hình trong file inventory.yml để kết nối tới máy vm1 chứ không dùng `cli_user` và thất bại:

> Failed to connect to the host via ssh: inventory_user@127.0.0.1: Permission denied.

Đừng cảm thấy cô đơn, vì bạn không phải người duy nhất: [ansible -u does not take precedence over ansible_ssh_user from inventory #4622](https://github.com/ansible/ansible/issues/4622)

### Ansible set CLI option ở mức ưu tiên thấp nhất

> Some behavioral parameters that you can set in variables you can also set in Ansible configuration, as command-line options, and using playbook keywords. For example, you can define the user that Ansible uses to connect to remote devices as a variable with ansible_user, in a configuration file with DEFAULT_REMOTE_USER, as a command-line option with -u, and with the playbook keyword remote_user. If you define the same parameter in a variable and by another method, the variable overrides the other setting. This approach allows host-specific settings to override more general settings. For examples and more details on the precedence of these various settings, see Controlling how Ansible behaves: precedence rules.

`ansible_user` là 1 variable, nó tuân theo [luật ưu tiên](https://github.com/ansible/ansible-documentation/blob/307434dd188f5a4d7631d205e7c741f3a2a8964b/docs/docsite/rst/playbook_guide/playbooks_variables.rst?plain=1#L403):

> Ansible does apply variable precedence, and you might have a use for it. Here is the order of precedence from least to greatest (the last listed variables override all other variables):

> #. Command-line values (for example, ``-u my_user``, these are not variables)
> ...
> #. Inventory file or script host vars [2]_

tức command-line value có mức ưu tiên thấp nhất.

> When you type something directly at the command line, you may feel that your hand-crafted values should override all others, but Ansible does not work that way. Command-line options have low precedence - they override configuration only. They do not override playbook keywords, variables from inventory or variables from playbooks.
[source](https://github.com/ansible/ansible-documentation/blob/307434dd188f5a4d7631d205e7c741f3a2a8964b/docs/docsite/rst/reference_appendices/general_precedence.rst?plain=1#L47C1-L47C332)

### Giải pháp
>   #. Extra vars (for example, ``-e "user=my_user"``)(always win precedence) [source](https://github.com/ansible/ansible-documentation/blob/307434dd188f5a4d7631d205e7c741f3a2a8964b/docs/docsite/rst/playbook_guide/playbooks_variables.rst?plain=1#L429)

extra vars được gán qua option -e có độ ưu tiên cao nhất, thay vì -u cli_user, hãy dùng `-e ansible_user=cli_user`.

### Kết luận
Ansible rất thành công so với các đối thủ lừng lẫy một thời của nó: Salt, Puppet, Chef. Người thành công thường có lối đi riêng ???!!!

Hết.

HVN at <https://pymi.vn> and <https://www.familug.org>.

[Ủng hộ tác giả 🍺](https://www.familug.org/p/ung-ho.html)
