Title: CPU chạy thread hay process?
Date: 2023-06-21
Category: frontpage
Tags: ps, top, thread, process, linux, unix, OS, CPU, rust, Python

Hay những câu hỏi liên quan:

- Thread và process khác gì nhau?
- 1 process chạy multithread trên mấy CPU?
- vì sao Rust không nhắc tới multi processing?
- Khi chạy CPU bound, dùng multi process hay multi thread?

bài này sẽ làm cho ra nhẽ.

## Process khác gì thread
Phần khó khăn nhất để trả lời câu hỏi này làm tìm được tài liệu có tính "chuẩn mực"/căn cứ, không phải mấy trang tutorial hay hỏi đáp trên mạng.

Người dùng máy tính thường biết đến khái niệm `process` trước, nó hiển thị mặc định trên các chương trình process manager như `top`, hay `ps`, hay `Monitor` trên Ubuntu, hay cả `Task manager` trên Windows.
Mỗi process được gán cho 1 số ProcessID (PID), biết dùng lệnh `kill -9 PID` để tắt chương trình bị "treo".

Chạy 1 chương trình, hệ điều hành sẽ tạo ra 1 (hay vài) process.

Cho tới khi học lập trình Python, thấy mỗi chương trình chỉ chạy code tuần tự từ trên xuống, nhận ra rằng mỗi 1 process chỉ chạy 1 "luồng" (thread), học thêm thư viện `threading`, biết chạy 2 3 4 thread cùng lúc trong 1 process.

PS: Ở đây dùng khái niệm process và thread của hệ điều hành, một số ngôn ngữ lập trình có khái niệm process của riêng mình, VD: Erlang process không giống như OS process.

Trên hệ điều hành dùng Linux như Ubuntu, gõ `man 7 pthreads`,
`pthread` hay POSIX thread, là "OS thread" trên Linux:

```
A single process can contain multiple threads, all of
which are executing the same program.  These threads share the
same global memory (data and heap segments), but each thread has
its own stack (automatic variables).
```

Các thread trong 1 process dùng chung dữ liệu (share data) và file description, nhưng có stack riêng.

Theo [`man 3 pthreads` trên OpenBSD](https://man.openbsd.org/pthreads.3):

```
A thread is a flow of control within a process. Each thread represents a
minimal amount of state: normally just the CPU state and a signal mask. All
other process state (such as memory, file descriptors) is shared among all of
the threads in the process.

In OpenBSD, threads use a 1-to-1 implementation, where every thread is
independently scheduled by the kernel.
```

Theo [`man 3 pthread` trên FreeBSD](https://man.freebsd.org/cgi/man.cgi?query=pthread)

```
POSIX threads are a set of	functions that support applications with re-
quirements	for multiple flows of control, called threads, within a process.
Multithreading is used to improve the performance of a program.
```

Hai BSD OS đều định nghĩa thread là một `flow of control` trong 1 process.

[Theo Microsoft](https://learn.microsoft.com/en-us/windows/win32/procthread/processes-and-threads), nhà sản xuất hệ điều hành nhiều người dùng nhất trên thế giới: process đơn giản là chương trình đang chạy, còn thread là đơn bị cơ bản mà hệ điều hành sẽ cung cấp cho thời gian của CPU.

### Hệ điều hành sched task (thread) cho CPU

### Kết luận
Có thể nhìn tận mắt thread đang chạy với ps và top.

Hết.

HVN at <http://pymi.vn> and <https://www.familug.org>.

[Ủng hộ tác giả 🍺](https://www.familug.org/p/ung-ho.html)
