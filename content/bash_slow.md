Title: bash chậm tới mức nào?
Date: 2024-09-02
Category: frontpage
Tags: bash, shell, scripting, POSIX

trên những môi trường không có ngôn ngữ nào khác, bash vẫn là lựa chọn duy nhất:

- docker entrypoint (script chạy 1 chương trình phức tạp trong docker)

bash không dùng để viết chương trình cần hiệu năng cao, nhưng liệu bash chậm tới mức nào?

### Tính tổng từ 1 đến 1 triệu

```bash
#1
x=0
for i in {1..1000000} ; do
     x=$((x+i))
done
echo "$x"

#2
x=0
for i in $(seq 1 1000000) ; do
     x=$((x+i))
done
echo "$x"

#3
x=0
for ((i=1;i<=1000000;i++)); do
     x=$((x+i))
done
echo "$x"

#4
x=0
i=1
while [ $i -le 1000000 ]; do
    x=$((x+i))
    i=$((i+1))
done
echo "$x"
```

Trong 4 cách trên,

- cách 1 với {1..1000000} tạo 1 triệu phần tử trong RAM, dùng hết 284MB RAM. (như Python dùng `list(range(1_000_001))`)
- cách 2 với seq 1 1000000 chỉ dùng 3.7MB RAM, nhưng phụ thuộc vào chương trình seq bên ngoài
- cách 3 và 4 tương tự nhau nhưng cách 4 chạy trên tất cả cách loại (POSIX) shell.

Dùng `shellcheck` để biết cách 3 không chạy trên `sh`:

```
$ sudo apt install -y shellcheck
$ shellcheck -s sh slow.sh

In slow.sh line 2:
for i in {1..1000000} ; do
         ^----------^ SC3009 (warning): In POSIX sh, brace expansion is undefined.


In slow.sh line 16:
for ((i=1;i<=1000000;i++)); do
^-^ SC3005 (warning): In POSIX sh, arithmetic for loops are undefined.
                      ^-- SC3018 (warning): In POSIX sh, ++ is undefined.

For more information:
  https://www.shellcheck.net/wiki/SC3005 -- In POSIX sh, arithmetic for loops...
  https://www.shellcheck.net/wiki/SC3009 -- In POSIX sh, brace expansion is u...
  https://www.shellcheck.net/wiki/SC3018 -- In POSIX sh, ++ is undefined.
```

Chạy cách 4 với while:

```sh
$ /usr/bin/time -v bash slow.sh
500000500000	Command being timed: "bash slow.sh"
	User time (seconds): 5.05
	System time (seconds): 0.00
	Percent of CPU this job got: 99%
	Elapsed (wall clock) time (h:mm:ss or m:ss): 0:05.05
	Average shared text size (kbytes): 0
	Average unshared data size (kbytes): 0
	Average stack size (kbytes): 0
	Average total size (kbytes): 0
	Maximum resident set size (kbytes): 3712
	Average resident set size (kbytes): 0
	Major (requiring I/O) page faults: 0
	Minor (reclaiming a frame) page faults: 155
	Voluntary context switches: 1
	Involuntary context switches: 27
	Swaps: 0
	File system inputs: 0
	File system outputs: 0
	Socket messages sent: 0
	Socket messages received: 0
	Signals delivered: 0
	Page size (bytes): 4096
	Exit status: 0
```

Mất 5 giây để tính, trong khi với Python - 1 trong những ngôn ngữ lập trình chậm nhất, chỉ mất 0.08 giây tính cả thời gian bật Python, dùng 9MB RAM. Với Python 1s có thể tính tổng tới 15 triệu, tức bash chậm hơn Python `15*5 = 75` lần.

```
$ /usr/bin/time -v python3 sum.py
500000500000
	Command being timed: "python3 sum.py"
	User time (seconds): 0.08
	System time (seconds): 0.00
	Percent of CPU this job got: 100%
	Elapsed (wall clock) time (h:mm:ss or m:ss): 0:00.08
	Average shared text size (kbytes): 0
	Average unshared data size (kbytes): 0
	Average stack size (kbytes): 0
	Average total size (kbytes): 0
	Maximum resident set size (kbytes): 9088
	Average resident set size (kbytes): 0
	Major (requiring I/O) page faults: 0
	Minor (reclaiming a frame) page faults: 943
	Voluntary context switches: 1
	Involuntary context switches: 0
	Swaps: 0
	File system inputs: 0
	File system outputs: 0
	Socket messages sent: 0
	Socket messages received: 0
	Signals delivered: 0
	Page size (bytes): 4096
	Exit status: 0
```

1 điều đáng chú ý là dùng `dash` - 1 POSIX shell có sẵn trên Ubuntu chạy nhanh hơn và tốn ít RAM hơn bash:

```sh
$ /usr/bin/time -v dash slow.sh
500000500000	Command being timed: "dash slow.sh"
	User time (seconds): 1.76
	System time (seconds): 0.00
	Percent of CPU this job got: 99%
	Elapsed (wall clock) time (h:mm:ss or m:ss): 0:01.76
	Average shared text size (kbytes): 0
	Average unshared data size (kbytes): 0
	Average stack size (kbytes): 0
	Average total size (kbytes): 0
	Maximum resident set size (kbytes): 1536
	Average resident set size (kbytes): 0
	Major (requiring I/O) page faults: 0
	Minor (reclaiming a frame) page faults: 78
	Voluntary context switches: 1
	Involuntary context switches: 45
	Swaps: 0
	File system inputs: 0
	File system outputs: 0
	Socket messages sent: 0
	Socket messages received: 0
	Signals delivered: 0
	Page size (bytes): 4096
	Exit status: 0
```

### Chậm thì sao?
Khi dùng để chạy các chương trình trong container, nếu không hoành thành quá trình trong thời gian giới hạn, container sẽ bị restart để chạy lại từ đầu, và khi chạy lại thì vẫn chậm, vẫn không kịp, tạo thành 1 vòng lặp vô hạn. Mặc dù ví dụ trên bash chạy 5 giây, nhưng khi dùng trong các container với 250m CPU (1/4 CPU), bash sẽ mất ~20s để chạy, trên thực tế, mất gần 50 giây:


```
$ systemd-run --scope --uid=1000 -p CPUQuota=25% /usr/bin/time -v bash slow.sh
==== AUTHENTICATING FOR org.freedesktop.systemd1.manage-units ===
Authentication is required to manage system services or other units.
Authenticating as: username
Password:
==== AUTHENTICATION COMPLETE ===
Running scope as unit: run-u139.scope
500000500000	Command being timed: "bash slow.sh"
	User time (seconds): 12.32
	System time (seconds): 0.00
	Percent of CPU this job got: 25%
	Elapsed (wall clock) time (h:mm:ss or m:ss): 0:49.25
	Average shared text size (kbytes): 0
	Average unshared data size (kbytes): 0
	Average stack size (kbytes): 0
	Average total size (kbytes): 0
	Maximum resident set size (kbytes): 3712
	Average resident set size (kbytes): 0
	Major (requiring I/O) page faults: 0
	Minor (reclaiming a frame) page faults: 152
	Voluntary context switches: 1
	Involuntary context switches: 623
	Swaps: 0
	File system inputs: 0
	File system outputs: 0
	Socket messages sent: 0
	Socket messages received: 0
	Signals delivered: 0
	Page size (bytes): 4096
	Exit status: 0
```

## Kết luận
bash chậm.

Hết.

HVN at <http://pymi.vn> and <https://www.familug.org>.

[Ủng hộ tác giả 🍺](https://www.familug.org/p/ung-ho.html)
