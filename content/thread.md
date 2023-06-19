Title: ps và top hiển thị số thread
Date: 2023-06-19
Category: frontpage
Tags: ps, top, thread, python, linux, unix, cli

Người dùng Linux hẳn đều biết dùng lệnh `ps -ef` hay `top` để xem các "chương trình" đang chạy.
Chương trình trên Linux thường ám chỉ 1 (vài) process đang chạy, mỗi process được gắn số ProcessID (PID).

Một process có thể chạy nhiều OS thread, để xem số lượng thread (NLWP) hay thread ID (LWP), thêm option `-L`

### Xem thread với `ps`

```
$ ps -efL | grep python3
# Dòng này được thêm vào cho dễ hiểu
UID          PID    PPID     LWP  C NLWP STIME TTY          TIME CMD
--------------------------------------------------------------------------------
hvn         3818    1585    3818  0    2 21:28 pts/0    00:00:00 python3 main.py
hvn         3818    1585    3819  0    2 21:28 pts/0    00:00:00 python3 main.py
```

PID là 3818, 2 thread ID lần lượt là 3818 và 3819.

Code Python3

```py
import time
from threading import Thread

class MyThread(Thread):
    def run(self):
        while True:
            time.sleep(2)
            print("running")

t = MyThread()
t.start()

t.join()
```

### Xem thread với `top`
Trong `top`, bấm chữ `H` (hoa) để hiển thị thread, cột PID lúc này sẽ hiển thị threadID.

```
$ top -Hbn1 | grep python3
    PID USER      PR  NI    VIRT    RES    SHR S  %CPU  %MEM     TIME+ COMMAND
   3979 hvn       20   0   87912  10232   4900 S   0.0   0.1   0:00.05 python3
   3980 hvn       20   0   87912  10232   4900 S   0.0   0.1   0:00.00 python3
$ ps -efL | grep python3
UID          PID    PPID     LWP  C NLWP STIME TTY          TIME CMD
hvn         3979    1585    3979  0    2 21:35 pts/0    00:00:00 python3 main.py
hvn         3979    1585    3980  0    2 21:35 pts/0    00:00:00 python3 main.py
```

### Tham khảo
- man top
```
      -H  :Threads-mode operation Instructs top to display individual threads.
      Without this command-line option a summation of all threads  in  each
      process  is shown.  Later this can be changed with the `H' interactive
      command.
```
- man ps
```
       -f     Do full-format listing.  This option can be combined with many
       other UNIX-style options to add additional columns.  It also causes the
       command arguments to be printed.  When used with -L, the NLWP (number of
               threads) and LWP (thread ID) columns will be added.  See the c
       option, the format keyword args, and the format keyword comm.
```

### Kết luận
Có thể nhìn tận mắt thread đang chạy với ps và top.

Hết.

HVN at <http://pymi.vn> and <https://www.familug.org>.

[Ủng hộ tác giả 🍺](https://www.familug.org/p/ung-ho.html)
