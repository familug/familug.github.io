Title: CPU chạy thread hay process?
Date: 2023-06-26
Category: frontpage
Tags: ps, top, thread, process, linux, unix, OS, CPU, rust, Python

Hay những câu hỏi liên quan:

- Thread và process khác gì nhau?
- 1 process chạy multithreading trên mấy CPU?
- Vì sao Java, Rust không nhắc tới multiprocessing?
- Khi chạy CPU bound, dùng multi-process hay multi-threaded?

bài này sẽ làm cho ra nhẽ.

Việc khó khăn nhất khi trả lời các câu hỏi này là tìm được các tài liệu có tính "chuẩn mực"/căn cứ, không phải mấy trang tutorial, wikipedia hay hỏi đáp trên mạng.

## Process là gì, thread là gì

Người dùng máy tính thường biết đến khái niệm `process` trước, nó hiển thị mặc định trên các chương trình process manager như `top`, hay `ps`, hay `Monitor` trên Ubuntu, hay cả `Task manager` trên Windows.
Mỗi process được gán cho 1 số ProcessID (PID), dùng lệnh `kill -9 PID` để tắt chương trình bị "treo".
Khi chạy 1 chương trình, hệ điều hành sẽ tạo ra 1 (hay vài) process.

Cho tới khi học lập trình Python, thấy mỗi chương trình chỉ chạy code tuần tự từ trên xuống, nhận ra rằng mỗi 1 process chỉ chạy 1 "luồng" (thread), học thêm thư viện `threading`, biết tạo 2 3 4 thread chạy "cùng lúc" trong 1 process.

Ở đây dùng khái niệm process và thread của hệ điều hành (OS), một số ngôn ngữ lập trình có khái niệm process của riêng mình, VD: Erlang process không giống như OS process.

Trên hệ điều hành dùng Linux như Ubuntu, gõ `man 7 pthreads`,
`pthread` hay POSIX thread, là "OS thread" trên Linux:

> A single process can contain multiple threads, all of
> which are executing the same program.  These threads share the
> same global memory (data and heap segments), but each thread has
> its own stack (automatic variables).

Các thread trong 1 process dùng chung dữ liệu (share data) và file description, nhưng có stack riêng.

Theo [`man 3 pthreads` trên OpenBSD](https://man.openbsd.org/pthreads.3):

> A thread is a flow of control within a process. Each thread represents a
> minimal amount of state: normally just the CPU state and a signal mask. All
> other process state (such as memory, file descriptors) is shared among all of
> the threads in the process.
>
> In OpenBSD, threads use a 1-to-1 implementation, where every thread is
> independently scheduled by the kernel.

Theo [`man 3 pthread` trên FreeBSD](https://man.freebsd.org/cgi/man.cgi?query=pthread)

> POSIX threads are a set of	functions that support applications with re-
> quirements	for multiple flows of control, called threads, within a process.
> Multithreading is used to improve the performance of a program.

Hai BSD OS đều định nghĩa thread là một `flow of control` trong 1 process.

[Theo Microsoft](https://learn.microsoft.com/en-us/windows/win32/procthread/processes-and-threads), nhà sản xuất hệ điều hành nhiều người dùng nhất trên thế giới định nghĩa: 1 process đơn giản là 1 chương trình đang chạy.
Hay [chi tiết hơn](https://learn.microsoft.com/en-gb/windows/win32/procthread/about-processes-and-threads): **một process cung cấp các tài nguyên để chạy 1 chương trình (code, file description, memory, ... và ít nhất 1 thread)**, một process bắt đầu với 1 thread, thường được gọi là primary/main thread.

Còn **thread là đơn vị mà được hệ điều hành cung cấp cho thời gian dùng CPU**.

### So sánh process và thread
Khái niệm process có trước, mãi sau này mới có khái niệm (nhiều) thread.
Mặc dù khi có 1 process thì nó luôn luôn chạy 1 thread.
Trong 1 process có thể có nhiều thread, trong 1 thread không thể có nhiều process.

Nhưng thực ra phần lớn người ta muốn hỏi:
### So sánh multi thread và multi process
Multi thread giống như multi process, ngoại trừ 1 việc: các thread share chung memory còn process thì không.

## Multitasking - đa nhiệm
Máy tính ngày nay CPU 4 lõi, 8 lõi (core)... luôn chạy nhiều chương trình cùng lúc. Máy tính ngày xưa khi chỉ có 1 CPU 1 core cũng vậy, chạy được nhiều chương trình "cùng lúc" nhờ CPU chuyển liên tục chạy các chương trình khác nhau, việc chuyển đổi rất nhanh này khiến người dùng có cảm giác là chạy cùng lúc. Ví dụ chạy 4 process A B C D:

```
A B C D A B D C B A C D...
```
chuyện này không thay đổi kể cả với máy tính nhiều core do số chương trình chạy luôn lớn hơn số core nhiều lần. Ví dụ:

```
$ grep -c processor /proc/cpuinfo
4
$ ps -ef | wc -l
287
```

PS: bạn đọc sau khi đọc xong bài và tham khảo [xem thread bằng top]({filename}/thread.md) sẽ chạy `ps -eLf`
## Một process chạy multithreading trên mấy CPU core?

### CPU Scheduler
Việc sắp xếp các chương trình chạy thế nào (dùng CPU thế nào) do một bộ phận của kernel có tên "scheduler" thực hiện.

Tham khảo tại `man 7 sched`
```
$ whatis sched
sched (7)            - overview of CPU scheduling
```

Trong tài liệu viết:

```
Scheduling policies
   The scheduler is the kernel component that decides which runnable thread
   will be executed by the CPU next.  Each thread has an associated
   scheduling policy and a  static scheduling  priority, sched_priority.  The
   scheduler makes  its  decisions  based  on knowledge  of  the  scheduling
   policy and static priority of all threads on the sys‐ tem.
...
API summary
   Linux provides the following system  calls for  controlling the CPU
   scheduling behavior, policy,  and  priority  of  processes (or, more
   precisely, threads).
```
## CPU chạy thread hay process?

Linux kernel scheduler sắp xếp lịch chạy cho các thread (hay gọi là task).
Trong `man 1 taskset` viết:

```
-a, --all-tasks
  Set or retrieve the CPU affinity of all the tasks (threads) for a given PID.
```

Đọc thêm về Linux CPU scheduler tại <https://opensource.com/article/19/2/fair-scheduling-linux>.

Với 10 process, mỗi process chỉ có 1 thread, sẽ là 10 thread cần chạy, kernel sẽ sched (xếp lịch) việc chạy 10 task này cho N CPU.
Tương tự 1 process, chạy 10 thread, kernel cũng sẽ sched việc chạy 10 task này cho N CPU (N > 0).

What?!
### Python multi-threaded vs multi-process
Dòng thứ 2 trong tài liệu thư viện [`threading` của Python](https://docs.python.org/3/library/threading.html#module-threading) viết

> CPython implementation detail: In CPython, due to the Global Interpreter
> Lock, only one thread can execute Python code at once (even though certain
> performance-oriented libraries might overcome this limitation). If
> you want your application to make better use of the computational resources
> of multi-core machines, you are advised to use multiprocessing or
> concurrent.futures.ProcessPoolExecutor. However, threading is still an
> appropriate model if you want to run multiple I/O-bound tasks simultaneously.

Python là một trong số ít ngôn ngữ mà nhiều thread không chạy được trên nhiều CPU core cùng lúc do giới hạn của [Global Interpreter Lock - GIL](https://docs.python.org/3/glossary.html#term-global-interpreter-lock) trong CPython/PyPy.
Giới hạn này **KHÔNG** tồn tại trong các bản Python khác như Jython (trên JVM) và IronPython (trên .NET).
Vì GIL, CPython chỉ có thể **chạy trên CPU** 1 thread 1 lúc, nên muốn chạy nhiều thread/process trên nhiều CPU core cùng lúc, Python có thư viện [multiprocessing](https://docs.python.org/3/library/multiprocessing.html).

> multiprocessing is a package that supports spawning processes using an API
> similar to the threading module. The multiprocessing package offers both
> local and remote concurrency, effectively side-stepping the Global
> Interpreter Lock by using subprocesses instead of threads. Due to this, the
> multiprocessing module allows the programmer to fully leverage multiple
> processors on a given machine.

Tránh nhầm lẫn rằng python `threading` thực sự chạy các thread cùng lúc trên nhiều CPU core, việc các thread có vẻ chạy cùng lúc trong Python chỉ là multitasking, chạy chuyển đổi giữa các thread.

### Java multithreading
Java hỗ trợ multithreading với các thread chạy cùng lúc như mong đợi, và nhiều thread này hoàn toàn có thể được chạy trên nhiều CPU core.

Vì multithreading chạy rất ngon lành, nên ít có lý do gì để sinh ra khái niệm "multiprocessing" như Python.
Ngoài ra, bật 1 Java process là chạy 1 máy ảo JVM nặng nề, khởi động chậm (so với bật 1 process CPython interpreter 0.1s 8MB RAM) nên việc này rất ít thấy trong thực tế.

PS: Python `threading` API [dựa trên API của Java](https://docs.python.org/2/library/threading.html)

### Rust multithreading
Tương tự Java, không tồn tại thư viện "multiprocessing" trong Rust.

> In most current operating systems, an executed program’s code is run in a
> process, and the operating system will manage multiple processes at once.
> Within a program, you can also have independent parts that run
> simultaneously. The features that run these independent parts are called
> threads. For example, a web server could have multiple threads so that it
> could respond to more than one request at the same time.

<https://doc.rust-lang.org/book/ch16-01-threads.html>

### Go multithreading, multiprocessing
Go không dùng khái niệm process hay thread của hệ điều hành mà dùng khái niệm Goroutine, tương tự thread, nhưng do Go runtime quản lý thay vì OS kernel.

> A goroutine is a lightweight thread managed by the Go runtime.
> Goroutines run in the same address space, so access to shared memory must be synchronized.

<https://go.dev/tour/concurrency/1>

Các goroutine cũng có thể được nhiều CPU core chạy cùng lúc

> GOMAXPROCS sets the maximum number of CPUs that can be executing simultaneously and returns the previous setting.

## Khi chạy CPU bound, dùng multi process hay multi thread?
- CPU bound là chương trình dành phần lớn thời gian dùng CPU xử lý, khác với
- IO bound là chương trình dành phần lớn thời gian đọc ghi file/network.

Câu hỏi này có thể là trap, cần hỏi lại dùng ngôn ngữ gì, trừ khi hỏi cụ thể tới Python thì trả lời dùng multiprocessing.
Trong các ngôn ngữ khác như Rust/Java, multithreading là câu trả lời, vì không có thư viện multi-process mà chạy.
Hay Go chỉ có goroutine chứ không có lựa chọn khác.

Khi nói chung chung, multi-process có ưu điểm là sự tách biệt giữa các process, một process bị crash sẽ không ảnh hưởng tới process khác, nhược điểm là việc giao tiếp giữa các process để chia sẻ data sẽ phức tạp.
Nhiều chương trình dùng mô hình này như:

- postgresql
- nginx master-workers

Multi-threaded giúp dễ dàng truy cập bộ nhớ chung, nhưng có thể gặp trường hợp 1 thread crash khiến cả chương trình tắt ngóm, nhược điểm là dễ xảy ra race-condition: N thread tranh nhau truy cập cùng 1 tài nguyên.

Không có câu trả lời dễ dàng, vì đây là trường hợp của PostgreSQL, sau vài chục năm chạy multi-process, nay đang khám phá option multi-threaded.

[Let's make PostgreSQL multi-threaded](https://www.postgresql.org/message-id/flat/31cc6df9-53fe-3cd9-af5b-ac0d801163f4%40iki.fi)

### Tham khảo

- OSTEP: <https://pages.cs.wisc.edu/~remzi/OSTEP/threads-intro.pdf>
- <https://www.postgresql.org/message-id/flat/31cc6df9-53fe-3cd9-af5b-ac0d801163f4%40iki.fi>
- <https://pages.cs.wisc.edu/~remzi/OSTEP/threads-intro.pdf>
- <https://opensource.com/article/19/2/fair-scheduling-linux>
- <https://man.openbsd.org/pthreads.3>
- <https://man.freebsd.org/cgi/man.cgi?query=pthread>
- <https://learn.microsoft.com/en-us/windows/win32/procthread/processes-and-threads>
- <https://learn.microsoft.com/en-gb/windows/win32/procthread/about-processes-and-threads>
- <https://go.dev/tour/concurrency/1>
- <https://docs.python.org/3/library/multiprocessing.html>
- <https://docs.python.org/3/glossary.html#term-global-interpreter-lock>
- <https://docs.python.org/2/library/threading.html>
- <https://doc.rust-lang.org/book/ch16-01-threads.html>

### Kết luận
Thread là đơn vị task được kernel sched chạy trên nhiều CPU, process là 1 chương trình đang chạy.

Hết.

HVN at <http://pymi.vn> and <https://www.familug.org>.

[Ủng hộ tác giả 🍺](https://www.familug.org/p/ung-ho.html)
