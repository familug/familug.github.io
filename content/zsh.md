Title: Máy cá nhân dùng shell nào không còn quan trọng
Date: 2021-06-22
Category: frontpage
Tags: shell, workstation, zsh, bash, shell, opinion

[Cuối năm 2012, mình đã phát hiện ra ZSH](https://www.familug.org/2012/12/zsh-va-bash.html)
lúc nó mới nổi và quyết định...
không dùng với lý do ghi rõ trong bài viết:

> đã, đang và sẽ tiếp tục dùng bash, bởi nó có 1 điều mà zsh không thể vượt
> qua: bash "ở khắp mọi nơi".

![xonsh](https://xon.sh/_static/landing2/images/conch_ascii.png)

Điều này vẫn đúng, ZSH không thể vượt qua tính ubiquitos (ở khắp mọi nơi) của
bash, nhưng

> Cú pháp script của bash và zsh không khác nhau nhiều. Nếu đã biết bash thì
> học zsh không có gì khó cả.

điều này không quan trọng và chưa từng quan trọng.

Việc "học" dùng ZSH là chuyện cấu hình và làm quen với 1 số câu lệnh/tính năng
khác của nó như auto-complete cực xịn, etc...
nhưng không liên quan gì tới chuyện viết script. Bởi N lý do:

- gần như không ai viết zsh script cả, người người vẫn viết bash
- khi phải viết bash, tôi viết [(POSIX) shell code](https://pubs.opengroup.org/onlinepubs/9699919799/utilities/V3_chap02.html), chạy với /bin/sh chứ không
phải bash - lý do: sh ở khắp mọi nơi
- khi cần chạy bash script, bash vẫn luôn ở đó
- /bin/sh trên Ubuntu còn gọi là `dash`
```sh
$ ls -l /bin/sh
lrwxrwxrwx 1 root root 4 Jan 17 16:11 /bin/sh -> dash
$ whatis dash
dash (1)             - command interpreter (shell)
```
- từ khi Docker/[K8S](https://www.familug.org/search/label/Kubernetes) trở nên
phổ biến, bash không còn "ở khắp mọi nơi nữa", hiếm
có docker image nào cài bash, nhưng `sh` thì ở khắp mọi nơi
- nếu phải [dùng tới Array](https://stackoverflow.com/a/35385978/807703),
tôi viết Python script ngay lập tức.

Vậy nên cứ thoải mái đổi shell nào tùy thích, chuyện viết script chẳng hề liên
quan, các tính năng dùng để viết script không phải các tính năng của shell dùng
tương tác hàng ngày.

Ngày càng có nhiều shell hấp dẫn khác để lựa chọn:

- [zsh](https://zsh.sourceforge.io/)
- [fish](https://fishshell.com/)
- [nushell](https://www.nushell.sh/)
- [xonsh](https://xon.sh/) - a Python shell
- [janetsh](https://janet-shell.org/) - a Janet shell

## Bonus
Để viết shell code tránh các lỗi nho nhỏ, cài `shellcheck` rồi check file code
như check Python pep8.

```sh
sudo apt-get install -y shellcheck
```

## Hết
