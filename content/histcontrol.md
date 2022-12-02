Title: Vài khoảng trắng không xóa đi lịch sử
Date: 2022-12-02
Category: frontpage
Tags: bash, ubuntu, histcontrol, security

Người dùng Ubuntu có một bí kíp để khiến cho câu lệnh vừa gõ trong bash không hiện trong lệnh "history": thêm dấu space trước khi gõ lệnh:
```
$ docker run -it ubuntu:22.04                                                                                 [0]
root@19b65c7de3f6:/# echo you see me
you see me
root@19b65c7de3f6:/#  echo you do not see my password is hunter42
you do not see my password is hunter42
root@19b65c7de3f6:/# history
    1  echo you see me
    2  history
root@19b65c7de3f6:/# echo $HISTCONTROL
ignoredups:ignorespace
```

Bí kíp này ... chỉ có ở trên Ubuntu bash.

![golden bridge](https://images.unsplash.com/photo-1588411393236-d2524cca1196?ixlib=rb-4.0.3&dl=ling-tang-rsD_jv_A8Yo-unsplash.jpg&w=640&q=80&fm=jpg&crop=entropy&cs=tinysrgb)

Photo by <a href="https://unsplash.com/@linglivestolaugh?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText">Ling Tang</a> on <a href="https://unsplash.com/s/photos/vietnam?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText">Unsplash</a>


### HISTCONTROL
Trong bash, biến môi trường HISTCONTROL dùng để config shell sẽ lưu cái gì vào "history".
Mặc định trên Ubuntu từ xưa tới nay có giá trị:

```
ignoredups:ignorespace
```

Nhưng điều này không đúng trên Debian cũng như nhiều hệ điều hành khác như [MacOS](https://unix.stackexchange.com/questions/115917/why-is-bash-not-storing-commands-that-start-with-spaces?noredirect=1&lq=1), cũng không đúng trên zsh (HIST_IGNORE_SPACE).

```
$ docker run -it debian:bullseye-slim                                                                         [0]
root@5a7ecd7dd69e:/#  echo you see mypassword
you see mypassword
root@5a7ecd7dd69e:/# history
    1   echo you see mypassword
    2  history
```

Vậy nên nếu đang dùng server khác Ubuntu mà hồn nhiên gõ mật khẩu vào câu lệnh, bắt đầu bằng dấu space, thì vẫn lưu trong history như thường. Pwned!


HISTCONTROL

>    A colon-separated list of values controlling how commands are saved on the history list. If the list of values includes ‘ignorespace’, lines which begin with a space character are not saved in the history list. A value of ‘ignoredups’ causes lines which match the previous history entry to not be saved. A value of ‘ignoreboth’ is shorthand for ‘ignorespace’ and ‘ignoredups’. A value of ‘erasedups’ causes all previous lines matching the current line to be removed from the history list before that line is saved. Any value not in the above list is ignored. If HISTCONTROL is unset, or does not include a valid value, all lines read by the shell parser are saved on the history list, subject to the value of HISTIGNORE. The second and subsequent lines of a multi-line compound command are not tested, and are added to the history regardless of the value of HISTCONTROL.

<https://www.gnu.org/software/bash/manual/bash.html>
### Kết luận
Không gõ password trong câu lệnh dưới mọi hình thức!

## Tham khảo
Happy ~enter~ leak password in commandline.

Hết.

HVN at http://pymi.vn and https://www.familug.org.

[Ủng hộ tác giả 🍺](https://www.familug.org/p/ung-ho.html)
