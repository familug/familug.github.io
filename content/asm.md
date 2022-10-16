Title: Hello world dùng x64 assembly
Date: 2022-10-16
Category: frontpage
Tags: assembly, asm, gcc, gas, as, ld, elf, xxd, hexdump

Assembly (asm) thường được gọi là ["hợp ngữ cũng có thể được gọi là mã máy tượng trưng"](https://vi.wikipedia.org/wiki/H%E1%BB%A3p_ng%E1%BB%AF), một ngôn ngữ lập trình cấp thấp nhất, thường tương ứng 1 lệnh với 1 lệnh của CPU.
Lập trình assembly ngày nay không còn phổ biến như trước khi có C.

C/Zig/Rust... được dùng để viết code "low level", nhưng khi cần tốc độ tối đa, lập trình nhúng, viết driver, hay thực hiện reverse engineering, binary exploitation, asm là ngôn ngữ được ưa chuộng.

![cpu](https://images.unsplash.com/photo-1591799264318-7e6ef8ddb7ea?ixlib=rb-1.2.1&dl=olivier-collet-JMwCe3w7qKk-unsplash.jpg&w=640&q=80&fm=jpg&crop=entropy&cs=tinysrgb)
Photo by <a href="https://unsplash.com/@ocollet?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText">Olivier Collet</a> on <a href="https://unsplash.com/?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText">Unsplash</a>

- Code Rust ---compile -> binary
- Code C ---compile -> binary
- Code ASM ---compile -> binary

Loạt bài viết này giới thiệu vài chương trình assembly đơn giản, cách compile, chạy, các tool dùng để tìm hiểu file binary.

Assembly đơn giản (giới hạn không nhiều lệnh, luật lệ rõ ràng), nhưng không dễ (mất rất nhiều bước để làm một việc, rất thủ công).

### Hello world
Là một chương trình in ra màn hình dòng chữ "hello world".

Code Python: `print("Hello,world")`

Code C:

```C
#include <stdio.h>
int main(int argc, char *argv[])
{
    puts("Hello, world\n");
    return 0;
}
```

Code asm trong file hello.s - copy từ wikipedia <https://en.wikipedia.org/wiki/GNU_Assembler#Example_program>

```asm
.global	_start

.text
_start:
	mov  $4, %eax   # 4 (code for "write" syscall) -> EAX register
	mov  $1, %ebx   # 1 (file descriptor for stdout) -> EBX (1st argument to syscall)
	mov  $message, %ecx # address of message string -> ECX (2nd argument)
	mov  $len, %edx # len (32 bit address) -> EDX (3rd arg)
	int   $0x80      # interrupt with location 0x80 (128), which invokes the kernel's system call procedure

	mov  $1, %eax   # 1 ("exit") -> EAX
	mov  $0, %ebx   # 0 (with success) -> EBX
	int  $0x80      # see previous
.data
message:
	.ascii  "Hello, PyMivn!\n" # inline ascii string
	len = 15
```

Compile dùng `gcc`

```
$ gcc -c hello.s
$ ls -l
-rw-rw-r--  1 hvn hvn  904 Oct 16 14:11 hello.o
-rw-rw-r--  1 hvn hvn  598 Oct 16 14:11 hello.s
$ file hello.o
hello.o: ELF 64-bit LSB relocatable, x86-64, version 1 (SYSV), not stripped
```

`gcc -c` compile source code hello.s sẽ sinh ra object file hello.o.
GCC sẽ gọi GNU Assembler (gas - lệnh là `as`) để thực hiện compile. Ngoài `as`, trên Linux còn phổ biến `nasm`.

#### ld - linker
`man ld`

> ld combines a number of object and archive files, relocates their data
> and ties up symbol references. Usually the last step in compiling a
> program is to run ld.

`ld` thực hiện link (các) file object, ở đây chỉ có 1 file hello.o, thành file binary cuối cùng chạy đuợc, có tên mặc định là a.out.

```
$ ld hello.o
$ ls -l
-rwxrwxr-x  1 hvn hvn 8920 Oct 16 14:13 a.out
$ file a.out
a.out: ELF 64-bit LSB executable, x86-64, version 1 (SYSV), statically linked, not stripped
$ ./a.out
Hello, PyMivn!
```

#### ELF file
file binary chạy được tên `a.out` trên Linux có format `ELF`.
```
$ whatis elf
elf (5)              - format of Executable and Linking Format (ELF) files
```

Trên MacOS sử dụng format `Mach-O`, trên Windows sử dụng format `Portable Executable (PE)`.

<https://en.wikipedia.org/wiki/Comparison_of_executable_file_formats>.

#### Chi tiết code asm
##### AT&T và Intel syntax
asm có hai nhánh syntax chính, là AT&T và Intel.
Intel phổ biến trên Windows, AT&T phổ biến trên Unix/Linux.
Xem chi tiết so sánh tại <https://en.wikipedia.org/wiki/AT%26T_syntax#Syntax>

##### hello.s
Code asm trong bài này chứa 3 section. `.global`, `.data` và `.text`, sử dụng AT&T syntax.

`.global` sẽ khai báo function nào được chạy, ở đây là `_start`

```asm
.global _start
```

`.data` còn gọi là data segment chứa các global variable & static variable.

```asm
.data
message:
	.ascii  "Hello, PyMivn!\n" # inline ascii string
	len = 15
```

`.text` chứa code của chương trình.  Function `_start`

```asm
.text
_start:
	mov  $4, %eax   # 4 (code for "write" syscall) -> EAX register
	mov  $1, %ebx   # 1 (file descriptor for stdout) -> EBX (1st argument to syscall)
	mov  $message, %ecx # address of message string -> ECX (2nd argument)
	mov  $len, %edx # len (32 bit address) -> EDX (3rd arg)
	int   $0x80      # interrupt with location 0x80 (128), which invokes the kernel's system call procedure

	mov  $1, %eax   # 1 ("exit") -> EAX
	mov  $0, %ebx   # 0 (with success) -> EBX
	int  $0x80      # see previous
```

%eax %ebx %ecx %edx là 4 register (thanh ghi) trong CPU, để chứa các giá trị.

```
mov $4, %eax
```

tương đương với viết code C `eax = 4`. `int $0x80` thực hiện interrupt tại địa chỉ 0x80, tức thực hiện gọi syscall. Dòng `int $0x80` có thể viết thành `syscall`.

Về cơ bản đoạn code trên thực hiện gọi 2 syscall số 4-write và 1-exit

Code giả:
```c
syscall(4, 1, message, len)
syscall(1, 0)
```

hay
```c
write(stdout, message, len)
exit(0)
```

Chạy với lệnh `strace` để xem các syscall đã được dùng:

```
$ strace ./a.out > /dev/null
execve("./a.out", ["./a.out"], 0x7ffd32dba4c0 /* 58 vars */) = 0
strace: [ Process PID=327701 runs in 32 bit mode. ]
write(1, "Hello, PyMivn!\n", 15)        = 15
exit(0)                                 = ?
+++ exited with 0 +++
```

Phiên bản dùng Intel syntax:

```asm
.intel_syntax noprefix
.global	_start

.text
_start:
	mov eax, 0x4
	mov ebx, 0x1
	lea ecx, [message]
	mov edx, 0xf
	int 0x80
	mov eax, 0x1
	mov ebx, 0x0
	int 0x80

.data
message:
	.ascii  "Hello, PyMivn!\n"
```

#### Hex view xxd
xxd in ra mã [hex](https://n.pymi.vn/byt351.html) của từng byte.
```
$ whatis xxd
xxd (1)              - make a hexdump or do the reverse.
```

```
$ xxd a.out | grep -v '0000 0000 0000 0000 0000 0000 0000 0000'
00000000: 7f45 4c46 0201 0100 0000 0000 0000 0000  .ELF............
00000010: 0200 3e00 0100 0000 0010 4000 0000 0000  ..>.......@.....
00000020: 4000 0000 0000 0000 5821 0000 0000 0000  @.......X!......
00000030: 0000 0000 4000 3800 0300 4000 0600 0500  ....@.8...@.....
00000040: 0100 0000 0400 0000 0000 0000 0000 0000  ................
00000050: 0000 4000 0000 0000 0000 4000 0000 0000  ..@.......@.....
00000060: e800 0000 0000 0000 e800 0000 0000 0000  ................
00000070: 0010 0000 0000 0000 0100 0000 0500 0000  ................
00000080: 0010 0000 0000 0000 0010 4000 0000 0000  ..........@.....
00000090: 0010 4000 0000 0000 2200 0000 0000 0000  ..@.....".......
000000a0: 2200 0000 0000 0000 0010 0000 0000 0000  "...............
000000b0: 0100 0000 0600 0000 0020 0000 0000 0000  ......... ......
000000c0: 0020 4000 0000 0000 0020 4000 0000 0000  . @...... @.....
000000d0: 0f00 0000 0000 0000 0f00 0000 0000 0000  ................
000000e0: 0010 0000 0000 0000 0000 0000 0000 0000  ................
00001000: b804 0000 00bb 0100 0000 b900 2040 00ba  ............ @..
00001010: 0f00 0000 cd80 b801 0000 00bb 0000 0000  ................
00001020: cd80 0000 0000 0000 0000 0000 0000 0000  ................
00002000: 4865 6c6c 6f2c 2050 794d 6976 6e21 0a00  Hello, PyMivn!..
00002020: 0000 0000 0000 0000 0000 0000 0300 0100  ................
00002030: 0010 4000 0000 0000 0000 0000 0000 0000  ..@.............
00002040: 0000 0000 0300 0200 0020 4000 0000 0000  ......... @.....
00002050: 0000 0000 0000 0000 0100 0000 0400 f1ff  ................
00002070: 0900 0000 0000 0200 0020 4000 0000 0000  ......... @.....
00002080: 0000 0000 0000 0000 1100 0000 0000 f1ff  ................
00002090: 0f00 0000 0000 0000 0000 0000 0000 0000  ................
000020a0: 1a00 0000 1000 0100 0010 4000 0000 0000  ..........@.....
000020b0: 0000 0000 0000 0000 1500 0000 1000 0200  ................
000020c0: 0f20 4000 0000 0000 0000 0000 0000 0000  . @.............
000020d0: 2100 0000 1000 0200 0f20 4000 0000 0000  !........ @.....
000020e0: 0000 0000 0000 0000 2800 0000 1000 0200  ........(.......
000020f0: 1020 4000 0000 0000 0000 0000 0000 0000  . @.............
00002100: 0068 656c 6c6f 2e6f 006d 6573 7361 6765  .hello.o.message
00002110: 006c 656e 005f 5f62 7373 5f73 7461 7274  .len.__bss_start
00002120: 005f 6564 6174 6100 5f65 6e64 0000 2e73  ._edata._end...s
00002130: 796d 7461 6200 2e73 7472 7461 6200 2e73  ymtab..strtab..s
00002140: 6873 7472 7461 6200 2e74 6578 7400 2e64  hstrtab..text..d
00002150: 6174 6100 0000 0000 0000 0000 0000 0000  ata.............
00002190: 0000 0000 0000 0000 1b00 0000 0100 0000  ................
000021a0: 0600 0000 0000 0000 0010 4000 0000 0000  ..........@.....
000021b0: 0010 0000 0000 0000 2200 0000 0000 0000  ........".......
000021c0: 0000 0000 0000 0000 0100 0000 0000 0000  ................
000021d0: 0000 0000 0000 0000 2100 0000 0100 0000  ........!.......
000021e0: 0300 0000 0000 0000 0020 4000 0000 0000  ......... @.....
000021f0: 0020 0000 0000 0000 0f00 0000 0000 0000  . ..............
00002200: 0000 0000 0000 0000 0100 0000 0000 0000  ................
00002210: 0000 0000 0000 0000 0100 0000 0200 0000  ................
00002230: 1020 0000 0000 0000 f000 0000 0000 0000  . ..............
00002240: 0400 0000 0600 0000 0800 0000 0000 0000  ................
00002250: 1800 0000 0000 0000 0900 0000 0300 0000  ................
00002270: 0021 0000 0000 0000 2d00 0000 0000 0000  .!......-.......
00002280: 0000 0000 0000 0000 0100 0000 0000 0000  ................
00002290: 0000 0000 0000 0000 1100 0000 0300 0000  ................
000022b0: 2d21 0000 0000 0000 2700 0000 0000 0000  -!......'.......
000022c0: 0000 0000 0000 0000 0100 0000 0000 0000  ................
000022d0: 0000 0000 0000 0000                      ........
```

Bài viết thực hiện trên Ubuntu 20.04.

### Tham khảo
Free books:

- <https://en.wikibooks.org/wiki/X86_Assembly>
- <https://pacman128.github.io/static/pcasm-book.pdf>
- <https://mirror.ossplanet.net/nongnu/pgubook/ProgrammingGroundUp-1-0-booksize.pdf>
- <http://www.egr.unlv.edu/~ed/assembly64.pdf>
- [Reverse Engineering for Beginners](https://beginners.re/)
- More at <https://www.linuxlinks.com/excellent-free-books-learn-assembly/>

### Kết luận
Viết helloworld.asm không quá khó.

Happy hacking!
