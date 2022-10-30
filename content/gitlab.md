Title: GitLab CE tự host không như GitLab.com
Date: 2022-10-30
Category: frontpage
Tags: gitlab, changes

Một đoạn code đơn giản, đã chạy ít nhất 5 năm trên gitlab.com, khi mang về gitlab CE tự host, dùng cùng gitlab CI runner, chạy CICD job lại fail.

```sh
$ git diff --name-only origin/master...HEAD
...
fatal: ambiguous argument 'origin/master...HEAD': unknown revision or path not in the working tree.
Use '--' to separate paths from revisions, like this:
'git <command> [<revision>...] -- [<file>...]'
...
```

Không có origin/master, kể cả master cũng không có.

![img](https://images.unsplash.com/photo-1572514619891-39295dda66d4?ixlib=rb-4.0.3&dl=abdulaziz-alfawzan-8EOSmlCZfzY-unsplash.jpg&w=640&q=80&fm=jpg&crop=entropy&cs=tinysrgb)

Photo by <a href="https://unsplash.com/@azf93?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText">Abdulaziz Alfawzan</a> on <a href="https://unsplash.com/s/photos/alchemist?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText">Unsplash</a>

Hóa ra bên trên output của GitLab CI job có 1 dòng

```
Fetching changes with git depth set to 20...
```

Config trên `GitLab > CICD Settings` của project, mặc định sau khi cài GitLab CE  15.4.2, giá trị ` Git shallow clone ` là 20.

Trên GitLab.com, giá trị này mặc định là không set (blank).

![gitlab]({static}/gitlab.png)

>  The number of changes to fetch from GitLab when cloning a repository. Lower values can speed up pipeline execution. Set to 0 or blank to fetch all branches and tags for each job

### Kết luận
Code chạy 5 năm, trên cùng 1 chỗ, vẫn fail, vì config từ web thay đổi.

Hết.
