Title: Ansible role luôn chạy trước task
Date: 2025/10/31
Category: frontpage
Tags: ansible, sysadmin,
Slug: ansible-order-role-task

Ansible là công cụ tự động hóa "đơn giản", "dễ dùng". Trong một ansible play, có thể dùng tasks, hoặc roles, hoặc cả hai.
Thứ tự chạy của chúng có chút **bất ngờ**.


### Thứ tự role và task khi trong cùng play

Playbook `order.yml`

```yml
- hosts: all
  tasks:
    - name: task1
      debug:
        msg: "This is task1"
  roles:
    - role: pika
```

Role pika: `roles/pika/tasks/main.yml`:

```yml
- name: task in role
  debug:
    msg: this is task in a role
```

Output:

```
$ uvx --from 'ansible-core>2.19' ansible-playbook -K -i localhost, order.yml 
BECOME password: 

PLAY [all] **************************************************************************
...
TASK [pika : task in role] **********************************************************
ok: [localhost] => {
    "msg": "this is task in a role"
}

TASK [task1] ************************************************************************
ok: [localhost] => {
    "msg": "This is task1"
}

PLAY RECAP **************************************************************************
localhost                  : ok=3    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
```

Thấy role chạy trước task, mặc dù trong `order.yml` tasks viết trước roles. Lý do bởi thứ tự này được quy định trong [tài liệu](https://github.com/ansible/ansible-documentation/blob/307434dd188f5a4d7631d205e7c741f3a2a8964b/docs/docsite/rst/playbook_guide/playbooks_reuse_roles.rst?plain=1#L159-L167):

> When you use the ``roles`` option at the play level, Ansible treats the roles as static imports and processes them during playbook parsing. Ansible executes each play in this order:
> ...
> - Each role listed in ``roles:``, in the order listed. Any role dependencies defined in the role's ``meta/main.yml`` run first, subject to tag filtering and conditionals. See :ref:`role_dependencies` for more details.
> - Any ``tasks`` defined in the play.

Một giải pháp để tasks chạy trước role là include role vào 1 task tiếp theo:

```
- hosts: all
  tasks:
    - name: task1
      debug:
        msg: "This is task1"
    - name: task run role
      include_role:
        name: pika
```

Output:

```
TASK [task1] ************************************************************************
ok: [localhost] => {
    "msg": "This is task1"
}

TASK [task run role] ****************************************************************
included: pika for localhost

TASK [pika : task in role] **********************************************************
ok: [localhost] => {
    "msg": "this is task in a role"
}
```

### Kết luận

Bình thường Ansible chạy từ trên xuống dưới, ngoại trừ các trường hợp ngoại lệ, như khi `tasks` gặp `roles`.

Hết.

HVN at <https://pymi.vn> and <https://www.familug.org>.

[Ủng hộ tác giả 🍺](https://www.familug.org/p/ung-ho.html)
