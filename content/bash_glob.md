Title: Đọc code bash xem vì sao echo * không hiện tên file ẩn
Date: 2024-09-10
Category: frontpage
Tags: bash, C, shell, POSIX, readcode, glob, clang, lldb

### glob là gì

```
$ whatis glob
glob (7)             - globbing pathnames
```

Gõ [`man 7 glob`](https://man7.org/linux/man-pages/man7/glob.7.html) có viết:


```
NAME
       glob - globbing pathnames

DESCRIPTION
       Long ago, in UNIX V6, there was a program /etc/glob that would expand wildcard patterns.  Soon afterward this became a shell built-in.
```

`glob` là khái niệm để "match" (chọn) filename sử dụng "pattern", gần giống với Regular Expression. Ví dụ trên shell gõ `ls *.py` sẽ hiện tên các file có đuôi `.py`.

Điểm khác biệt so với Regular Expression: glob chỉ dùng để match filename, và các ký tự đặc biệt trong glob có ý nghĩa khác so với Regular Expression (ví dụ `*` có nghĩa khác).

### Wildcard pattern là gì
Một string là 1 wildcard pattern nếu chứa `?` `*` hoặc `[`, glob là việc biến wildcard pattern thành list các filename "match" pattern.

```
   A '?' (not between brackets) matches any single character.
   A '*' (not between brackets) matches any string, including the empty string.
```

Ví dụ

```
$ touch error.c error.h
$ echo er??r.c
error.c
$ echo error.*
error.c  error.h
```

Một điểm đáng chú ý là `*` không match các filename bắt đầu bằng dấu `.` - hay còn gọi là **file ẩn** (hidden file) trên các hệ điều hành UNIX/Linux. Muốn chọn cả các file bắt đầu bằng `.`, phải dùng `.*`.

```
$ touch error.c error.h
$ touch .flag
$ echo *
error.c error.h
$ echo .*
.flag
```

### Đọc code bash xem tại sao glob `echo *` không hiện filename bắt đầu bằng dấu `.`
Tải code bash 5.1 về
```
$ wget https://ftp.gnu.org/gnu/bash/bash-5.1.16.tar.gz
--2024-09-10 21:59:27--  https://ftp.gnu.org/gnu/bash/bash-5.1.16.tar.gz
Resolving ftp.gnu.org (ftp.gnu.org)... 209.51.188.20, 2001:470:142:3::b
Connecting to ftp.gnu.org (ftp.gnu.org)|209.51.188.20|:443... connected.
HTTP request sent, awaiting response... 200 OK
Length: 10522932 (10M) [application/x-gzip]
Saving to: ‘bash-5.1.16.tar.gz’

bash-5.1.16.tar.gz           100%[============================================>]  10,04M  3,52MB/s    in 2,8s

2024-09-10 21:59:31 (3,52 MB/s) - ‘bash-5.1.16.tar.gz’ saved [10522932/10522932]

$ tar xf bash-5.1.16.tar.gz
$ cd bash-5.1.16

```

Tìm từ khóa glob

```
$ find . -name '*.c' | xargs grep -l glob
...
./lib/glob/gmisc.c
./lib/glob/smatch.c
./lib/glob/xmbsrtowcs.c
./lib/glob/strmatch.c
./lib/glob/glob_loop.c
./lib/glob/sm_loop.c
./lib/glob/glob.c
...
```
Thấy có riêng 1 thư mục tên `lib/glob`.

```C
$ head glob.c
/* glob.c -- file-name wildcard pattern matching for Bash.
...
/* To whomever it may concern: I have never seen the code which most
   Unix programs use to perform this function.  I wrote this from scratch
   based on specifications for the pattern matching.  --RMS.  */
```
Viết bởi [RMS - Richard Stallman](https://en.wikipedia.org/wiki/Richard_Stallman) tác giả của GNU.

Trong file này chỉ có 10 function:
```c
static int
extglob_skipname (pat, dname, flags)
--
static int
skipname (pat, dname, flags)
--
static int
wskipname (pat, dname, flags)
--
static int
wextglob_skipname (pat, dname, flags)
--
static int
mbskipname (pat, dname, flags)
--
static void
wdequote_pathname (pathname)
--
static void
dequote_pathname (pathname)
--
static int
glob_testdir (dir, flags)
--
static struct globval *
finddirs (pat, sdir, flags, ep, np)
--
static char **
glob_dir_to_array (dir, array, flags)
```

nhìn tên đoán `skipname` có vẻ là thứ cần tìm:

```C
/* Return 1 if DNAME should be skipped according to PAT.  Mostly concerned
   with matching leading `.'. */
static int
skipname (pat, dname, flags)
     char *pat;
     char *dname;
     int flags;
{
#if EXTENDED_GLOB
  if (extglob_pattern_p (pat))      /* XXX */
    return (extglob_skipname (pat, dname, flags));
#endif

  if (glob_always_skip_dot_and_dotdot && DOT_OR_DOTDOT (dname))
    return 1;

  /* If a leading dot need not be explicitly matched, and the pattern
     doesn't start with a `.', don't match `.' or `..' */
  if (noglob_dot_filenames == 0 && pat[0] != '.' &&
    (pat[0] != '\\' || pat[1] != '.') &&
    DOT_OR_DOTDOT (dname))
    return 1;

  /* If a dot must be explicitly matched, check to see if they do. */
  else if (noglob_dot_filenames && dname[0] == '.' && pat[0] != '.' &&
    (pat[0] != '\\' || pat[1] != '.'))
    return 1;

  return 0;
}
```
Comment rất rõ ràng:

> Return 1 if DNAME should be skipped according to PAT.  Mostly concerned with matching leading `.`

Xem trong các điều kiện return 1 trong function trên, thấy

```C
  else if (noglob_dot_filenames && dname[0] == '.' && pat[0] != '.' &&
    (pat[0] != '\\' || pat[1] != '.'))
    return 1;
```

nếu `noglob_dot_filenames` và filename tại index 0 có giá trị là . `dname[0] == '.'` và kí tự đầu tiên trong pattern không phải . `pat[0] != '.'` thì return 1 - tức bỏ qua file này.

`noglob_dot_filenames` là 1 global var:

```c
/* Global variable which controls whether or not * matches .*.
   Non-zero means don't match .*.  */
int noglob_dot_filenames = 1;
```

### Chạy debugger lldb xem code chạy
Thay vì các bài trước sửa code, thêm print, build lại, bài này dùng C debugger LLDB để debug và in ra.

Clang là C compiler hiện đại, có debugger tương ứng là LLDB, combo hiện đại này xuất hiện trên MacOS và các hệ điều hành BSD khác. Combo khác hay dùng là gcc và gdb.

```
$ sudo apt install -y clang lldb
...

```

```
$ CC=clang ./configure
$ make -j `nproc`
...
make -j `nproc`  28,47s user 3,28s system 364% cpu 8,716 total
$ file ./bash
./bash: ELF 64-bit LSB pie executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, BuildID[sha1]=cbc1d1b6f48f5881c417e988c2253f29d1a5900d, for GNU/Linux 3.2.0, with debug_info, not stripped
```
Mất 8s trên máy AMD Ryzen 3 4300U.

#### Các lệnh cơ bản của LLDB

- `b skipname` : tạo breakpoint tại function `skipname`
- `process launch -- -c 'echo *'` chạy chương trình với argument `-c 'echo *'`
- `bt` - in ra backtrace, hiển thị call-stack - tức function nào gọi function nào.
- `n` chạy đến dòng code tiếp theo
- `c` chạy đến breakpoint tiếp theo
- `frame var` in ra các variable trong frame hiện tại
- `finish` kết thúc function và in ra return value.

gõ lệnh xong gõ enter để chạy.

#### dùng lldb chạy chương trình bash với argument `-c 'echo *'`
```c
$ mkdir test
$ cd test
$ touch main.py lib.py .flag
$ lldb ../bash
Traceback (most recent call last):
(lldb) target create "../bash"
Current executable set to '/home/me/bash-5.1.16/bash' (x86_64).

(lldb) b skipname
Breakpoint 1: where = bash`skipname + 22 at glob.c:268:7, address = 0x00000000000b0fe6
(lldb) launch process -- -c 'echo *'
error: 'launch' is not a valid command.
(lldb) process launch -- -c 'echo *'
Process 17373 launched: '/home/me/bash-5.1.16/bash' (x86_64)
Process 17373 stopped
* thread #1, name = 'bash', stop reason = breakpoint 1.1
    frame #0: 0x0000555555604fe6 bash`skipname(pat="*", dname=".", flags=<unavailable>) at glob.c:268:7
   265 	     int flags;
   266 	{
   267 	#if EXTENDED_GLOB
-> 268 	  if (extglob_pattern_p (pat))		/* XXX */
   269 	    return (extglob_skipname (pat, dname, flags));
   270 	#endif
   271
(lldb) bt
* thread #1, name = 'bash', stop reason = breakpoint 1.1
  * frame #0: 0x0000555555604fe6 bash`skipname(pat="*", dname=".", flags=<unavailable>) at glob.c:268:7
    frame #1: 0x0000555555604d68 bash`mbskipname(pat=<unavailable>, dname=<unavailable>, flags=<unavailable>) at glob.c:386:13 [artificial]
    frame #2: 0x00005555556040cf bash`glob_vector(pat="*", dir=".", flags=256) at glob.c:812:26
    frame #3: 0x00005555556053e0 bash`glob_filename(pathname=<unavailable>, flags=0) at glob.c:1492:22
    frame #4: 0x00005555555d09fc bash`shell_glob_filename(pathname=<unavailable>, qflags=8) at pathexp.c:470:13
    frame #5: 0x00005555555c2b46 bash`expand_word_list_internal [inlined] glob_expand_word_list(tlist=0x00005555556acc90, eflags=<unavailable>) at subst.c:11409:17
    frame #6: 0x00005555555c2aca bash`expand_word_list_internal(list=<unavailable>, eflags=31) at subst.c:12022:13
    frame #7: 0x00005555555c2135 bash`expand_words(list=<unavailable>) at subst.c:11357:11 [artificial]
    frame #8: 0x000055555559aa00 bash`execute_simple_command(simple_command=0x00005555556ac850, pipe_in=-1, pipe_out=-1, async=0, fds_to_close=0x00005555556ac910) at execute_cmd.c:4381:15
    frame #9: 0x0000555555599638 bash`execute_command_internal(command=0x00005555556ac810, asynchronous=0, pipe_in=-1, pipe_out=-1, fds_to_close=0x00005555556ac910) at execute_cmd.c:846:4
    frame #10: 0x00005555555f0f87 bash`parse_and_execute(string="echo *", from_file="-c", flags=20) at evalstring.c:489:17
    frame #11: 0x0000555555585f60 bash`run_one_command(command="echo *") at shell.c:1440:12
    frame #12: 0x00005555555854f3 bash`main(argc=3, argv=0x00007fffffffe6c8, env=<unavailable>) at shell.c:741:7
    frame #13: 0x00007ffff7c29d90 libc.so.6`__libc_start_call_main(main=(bash`main at shell.c:368), argc=3, argv=0x00007fffffffe6c8) at libc_start_call_main.h:58:16
    frame #14: 0x00007ffff7c29e40 libc.so.6`__libc_start_main_impl(main=(bash`main at shell.c:368), argc=3, argv=0x00007fffffffe6c8, init=0x00007ffff7ffd040, fini=<unavailable>, rtld_fini=<unavailable>, stack_end=0x00007fffffffe6b8) at libc-start.c:392:3
    frame #15: 0x0000555555583de5 bash`_start + 37
(lldb) n
(lldb) frame var
(char *) pat = <variable not available>

(char *) dname = 0x00005555556af053 "."
(int) flags = <no location, value may have been optimized out>
(lldb) c
Process 17373 resuming
Process 17373 stopped
* thread #1, name = 'bash', stop reason = breakpoint 1.1
    frame #0: 0x0000555555604fe6 bash`skipname(pat="*", dname=".flag", flags=<unavailable>) at glob.c:268:7
   265 	     int flags;
   266 	{
   267 	#if EXTENDED_GLOB
-> 268 	  if (extglob_pattern_p (pat))		/* XXX */
   269 	    return (extglob_skipname (pat, dname, flags));
   270 	#endif
   271

(lldb) frame var
(char *) pat = <variable not available>

(char *) dname = 0x00005555556af06b ".flag"
(int) flags = <no location, value may have been optimized out>
```

Tới đây ta có filename đang được xét là `.flag`,và `pat="*"`
```
    frame #0: 0x0000555555604fe6 bash`skipname(pat="*", dname=".flag", flags=<unavailable>) at glob.c:268:7
```

bấm `n` cho tới khi thấy
```c
(lldb)  n
Process 17373 stopped
* thread #1, name = 'bash', stop reason = step over
    frame #0: 0x0000555555605180 bash`skipname(pat=<unavailable>, dname=".flag", flags=<unavailable>) at glob.c:283:45
   280 	    return 1;
   281
   282 	  /* If a dot must be explicitly matched, check to see if they do. */
-> 283 	  else if (noglob_dot_filenames && dname[0] == '.' && pat[0] != '.' &&
   284 		(pat[0] != '\\' || pat[1] != '.'))
   285 	    return 1;
   286
(lldb)
Process 17373 stopped
* thread #1, name = 'bash', stop reason = step over
    frame #0: 0x00005555556051e3 bash`skipname(pat=<unavailable>, dname=".flag", flags=<unavailable>) at glob.c:288:1
   285 	    return 1;
   286
   287 	  return 0;
-> 288 	}
   289
(lldb) finish
* thread #1, name = 'bash', stop reason = step out
Stepped out past: frame #1: 0x0000555555604d68 bash`mbskipname(pat=<no value available>, dname=<no value available>, flags=<no summary available>) at glob.c:386:13 [artificial]

Return value: (int) $13 = 1
```
thấy sau khi `finish` function trả về `1` tức skip file `.flag`.

Làm tương tự, thấy trả về `0` với `lib.py`:

```c
(lldb) c
Process 17373 resuming
Process 17373 stopped
* thread #1, name = 'bash', stop reason = breakpoint 8.1
    frame #0: 0x0000555555604fe6 bash`skipname(pat="*", dname="lib.py", flags=<unavailable>) at glob.c:268:7
   265 	     int flags;
   266 	{
   267 	#if EXTENDED_GLOB
-> 268 	  if (extglob_pattern_p (pat))		/* XXX */
   269 	    return (extglob_skipname (pat, dname, flags));
   270 	#endif
   271
(lldb) finish
Process 17373 stopped
* thread #1, name = 'bash', stop reason = step out
Stepped out past: frame #1: 0x0000555555604d68 bash`mbskipname(pat=<no value available>, dname=<no value available>, flags=<no summary available>) at glob.c:386:13 [artificial]

Return value: (int) $14 = 0
```

### Tham khảo
`man 7 glob`

## Kết luận
glob không match file ẩn có tên bắt đầu bằng `.`.
Đọc code C khó quá thì chạy debugger LLDB.

Written using
```
$ bash --version
GNU bash, version 5.1.16(1)-release (x86_64-pc-linux-gnu)
```
Hết.

HVN at <http://pymi.vn> and <https://www.familug.org>.

[Ủng hộ đồng bào bị ảnh hưởng bởi cơn bão số 3.](https://tuoitre.vn/ban-doc-tuoi-tre-lien-tuc-dong-gop-gui-den-nguoi-dan-mien-bac-20240910182204886.htm)

> Báo Tuổi Trẻ, Ngân hàng Công thương chi nhánh 3, TP.HCM. Số tài khoản: 113000006100 (Việt Nam đồng). Nội dung: Ủng hộ đồng bào bị ảnh hưởng bởi cơn bão số 3.

![yagi]({static}/images/yagi.webp)
