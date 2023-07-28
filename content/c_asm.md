Title: Viết "Hello World" bằng C, đọc và chạy Assembly x86-64 (phần 1)
Date: 2023-07-28
Category: frontpage
Tags: assembly, asm, gcc, gdb, x86-64

Điều đầu tiên và quan trọng nhất khi đọc về C hay assembly là: không được sợ. Code có thể lạ hay dài, nhưng không hề khó, mà thường đơn giản.

- không yêu cầu biết C
- không yêu cầu biết assembly
- biết code đơn giản 1 ngôn ngữ bất kỳ

đọc xong là biết.

Bài viết liên quan hơi ngược lại với bài [viết hello word bằng x86-64 assembly]({filename}/asm.md), viết thì khó hơn đọc, bởi viết cần nghĩ đủ thứ, lên kế hoạch viết gì tiếp, đặt tên ra sao, còn đọc thì chỉ cần đi theo.
### Cài đặt gcc gdb
Trên Ubuntu

```
sudo apt update && sudo apt install -y gcc gdb
```

## Viết Hello World bằng C
Hơn "hello world" 1 chút, sẽ viết 1 function nhận vào 8 đầu vào và tính tổng.

```c
#include <stdio.h>

int sum(int a, int b, int c, int d, int e, int f, int g, int h) {
    float s = a + b + c + d + e + f + g + h;
    return s;
}

int main() {
    puts("Hello world!");
    int s = sum(1,2,3,4,5,6,7,8);
    return s*2;
}
```

Dòng include như import trong Python để C có thể gọi function `puts`. Còn lại, code trên tương đương code Python3 sau:

```py
def sum(a: int, b: int, c: int, d: int, e: int, f: int, g: int, h: int) -> int:
    s = a + b + c + d + e + f + g + h
    return s

def main() -> int:
    print("Hello world!")
    s: int = sum(1,2,3,4,5,6,7,8)
    return s*2
```

### Compile & link code thành binary bằng gcc
```
$ gcc --help
Usage: gcc [options] file...
...
  --help={common

$ gcc --help=common | grep debug
  --debug                     Same as -g.
```

```
$ gcc -g hello.c
$ file a.out
a.out: ELF 64-bit LSB pie executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, BuildID[sha1]=80dbc7d0bdab643730e858ec44e97fcd92dacb7b, for GNU/Linux 4.4.0, with debug_info, not stripped
```

Chạy code

```
$ ./a.out
Hello world!
$ echo $?
72
```
Vì main return `(1+2+3+4+5+6+7+8)*2` ta được kết quả 72.

### Các lệnh gdb cơ bản

- `info` hiển thị các thông tin, gõ `info` sẽ hiện các lệnh con như `info functions`

```asm
File hello.c:
8:	int main();
3:	int sum(int, int, int, int, int, int, int, int);

Non-debugging symbols:
0x0000000000001000  _init
0x0000000000001030  puts@plt
0x0000000000001040  _start
0x00000000000011dc  _fini
```

- Code assembly có 2 syntax, gdb mặc định là AT&T `att` , hoặc phổ biến (cả trên Windows) là `intel`. Lệnh `set disassembly-flavor intel` để chọn intel syntax.
```
(gdb) set disassembly-flavor intel
```

- `disas` hay `disassemble` in ra code assembly của function tương ứng.
Gõ `help disas` để hiện thêm chi tiết các option

```
(gdb) help disas
With a /s modifier, source lines are included (if available).
In this mode, the output is displayed in PC address order, and
file names and contents for all relevant source files are displayed.
...
```

Gõ `help disas /s main` để hiện code C kèm asm:

```
(gdb) disas /s main
Dump of assembler code for function main:
hello.c:
8	int main() {
   0x000000000000118f <+0>:	push   rbp
   0x0000000000001190 <+1>:	mov    rbp,rsp
   0x0000000000001193 <+4>:	sub    rsp,0x10

9	    puts("Hello world!");
   0x0000000000001197 <+8>:	lea    rax,[rip+0xe66]        # 0x2004
   0x000000000000119e <+15>:	mov    rdi,rax
   0x00000000000011a1 <+18>:	call   0x1030 <puts@plt>

10	    int s = sum(1,2,3,4,5,6,7,8);
   0x00000000000011a6 <+23>:	push   0x8
   0x00000000000011a8 <+25>:	push   0x7
   0x00000000000011aa <+27>:	mov    r9d,0x6
   0x00000000000011b0 <+33>:	mov    r8d,0x5
   0x00000000000011b6 <+39>:	mov    ecx,0x4
   0x00000000000011bb <+44>:	mov    edx,0x3
   0x00000000000011c0 <+49>:	mov    esi,0x2
   0x00000000000011c5 <+54>:	mov    edi,0x1
   0x00000000000011ca <+59>:	call   0x1139 <sum>
   0x00000000000011cf <+64>:	add    rsp,0x10
   0x00000000000011d3 <+68>:	mov    DWORD PTR [rbp-0x4],eax

11	    return s;
   0x00000000000011d6 <+71>:	mov    eax,DWORD PTR [rbp-0x4]

12	}
   0x00000000000011d9 <+74>:	leave
   0x00000000000011da <+75>:	ret
End of assembler dump.
```

### Giải thích code assembly trong hello world
Code assembly tuy dài nhưng đơn giản, chỉ dùng vài
instruction (câu lệnh) như:

- mov
- call
- lea
- push
- add
- sub
- leave
- ret

#### Các register trong assembly x86-64
asm x86-64 có 16 register (thanh ghi) thường dùng sau

- rbp: stack-frame base pointer
- rsp: (top of) stack pointer
- rax: accumulator - thường chứa kết quả của các phép tính
- rbx
- rcx
- rdx
- rdi
- rsi

và các register chỉ có trong x86-64 (64 bits), không có trong x86 (32 bits):

- r8d
- r9d
- ...
- r15d

chúng như các "biến" với tên cố định trên CPU để chứa các giá trị.

- rip: instruction pointer là register đặc biệt, trỏ tới instruction tiếp theo được chạy.

Các register đều có kích thước 64 bits, ở dạng 32 bits, tên của chúng thay chữ `r` bằng chữ `e`: eip, esp, ebp, eax, ebx, ecx, edx, edi, esi.

### rbp - base pointer register và stack
```
8	int main() {
   0x000000000000118f <+0>:	push   rbp
   0x0000000000001190 <+1>:	mov    rbp,rsp
   0x0000000000001193 <+4>:	sub    rsp,0x10
```

Khi vào 1 function, dòng đầu tiên luôn là `push rbp` để lưu giá trị hiện tại của `rbp` vào stack.
Stack là 1 vùng bộ nhớ liên tục, thường được chia thành các frames.
Mỗi function khi chạy có 1 stack-frame để lưu các thông tin của function đang chạy (biến local, parameter để gọi function khác ...). Stack giống như chồng sách, xếp vào trước sẽ ở dưới, lấy ra sau cùng.
`rbp` khi ở địa chỉ 0x00118f chứa "base pointer" của function `_start`, function gọi `main` (lập trình viên C phải viết chương trình chạy từ `main` vì `_start` chỉ gọi `main`).
`rbp` sẽ được dùng trong main để lưu "base pointer" của `main`, nên sẽ đè mất `rbp` của `_start`, do vậy phải push `rbp` vào stack. Tương ứng với nó, cuối function sẽ có instruction `leave`, thực chất là `pop` stack để lấy ra `rbp` đã lưu.

```
12	}
   0x00000000000011db <+76>:	leave
   0x00000000000011dc <+77>:	ret
```

#### Cú pháp asm instruction
Hầu hết ở 1 trong các dạng

```
instruction
instruction register
instruction register value
instruction register [memory]
```

Hai dòng tiếp theo khi bắt đầu main

```asm
   0x0000000000001190 <+1>:	mov    rbp,rsp
   0x0000000000001193 <+4>:	sub    rsp,0x10
```

`mov` thực hiện lấy giá trị của `rsp` ghi vào `rbp`, hay dễ hiểu hơn, như viết `rbp = rsp` trong C, Python.
#TODO why sub?

#### Hiển thị hello world!
```asm
9	    puts("Hello world!");
   0x0000000000001197 <+8>:	lea    rax,[rip+0xe66]        # 0x2004
   0x000000000000119e <+15>:	mov    rdi,rax
   0x00000000000011a1 <+18>:	call   0x1030 <puts@plt>
```
Gồm 3 bước:

- tính vị tri của string "Hello world!" trong file binary.  `lea` Load effective address tính địa chỉ rồi gán cho rax: `rax = rip + 0xe66`, ở đây tính địa chỉ, không đọc nội dung.
- gán `rdi` cho giá trị này `rdi = rax`
- `call` gọi function ở vị trí `0x1030`, tức function `puts` với 1 argument được chứa trong `rdi`. Và bắt buộc phải là `rdi`, lý do bởi "call convention".

#### Call convention
Định nghĩa trong [System V AMD64 ABI](https://gitlab.com/x86-psABIs/x86-64-ABI/-/jobs/artifacts/master/raw/x86-64-ABI/abi.pdf?job=build), mục 3.2.3 Parameter passing:

> 2. If the class is INTEGER, the next available register of the sequence %rdi, %rsi, %rdx, %rcx, %r8 and %r9 is used

- Lần lượt, rsi, rdi, rdx, rcx, r8, r9 chứa các argument 1-6
- argument thứ 7 trở đi được push vào stack. Đây là lý do các function C thường không dùng hơn 6 argument để tối ưu tốc độ, các register luôn nhanh hơn push vào stack.
- thứ tự các câu lệnh gán argument thực hiện từ phải qua trái (từ 8 đến 1): push 8, push 7, r9d=6, r8d=5, ecx=4, edx=3, rsi=2, rdi=1.
- gọi call 0x1139, 0x1139 là địa chỉ của function sum.

```asm
10	    int s = sum(1,2,3,4,5,6,7,8);
   0x00000000000011a6 <+23>:	push   0x8
   0x00000000000011a8 <+25>:	push   0x7
   0x00000000000011aa <+27>:	mov    r9d,0x6
   0x00000000000011b0 <+33>:	mov    r8d,0x5
   0x00000000000011b6 <+39>:	mov    ecx,0x4
   0x00000000000011bb <+44>:	mov    edx,0x3
   0x00000000000011c0 <+49>:	mov    esi,0x2
   0x00000000000011c5 <+54>:	mov    edi,0x1
   0x00000000000011ca <+59>:	call   0x1139 <sum>
   0x00000000000011cf <+64>:	add    rsp,0x10
   0x00000000000011d3 <+68>:	mov    DWORD PTR [rbp-0x4],eax
```
- kết quả của function sum tự được chứa trong register eax. `mov` gán giá trị return của sum vào địa chỉ rbp-0x4.


```asm
11	    return s*2;
   0x00000000000011d6 <+71>:	mov    eax,DWORD PTR [rbp-0x4]
   0x00000000000011d9 <+74>:	add    eax,eax
```
giá trị được gán vào eax rồi thực hiện `*2` bằng cách cộng eax với eax qua `add eax,eax`. Kết quả của phép tính này tự được chứa trong eax, là giá trị main trả về.

#### Các kiểu dữ liệu trong asm - data type
Chapter 4.1 vol 1 Intel SDM viết:

> A byte is eight bits, a word is 2 bytes (16 bits), a doubleword is 4 bytes (32 bits), a quadword is 8 bytes (64 bits), and a double quadword is 16 bytes (128 bits).

doubleword trong asm được ký hiệu là DWORD, quadword ký hiệu là QWORD.

### Đọc assembly function sum

```asm
(gdb) disas /s sum
Dump of assembler code for function sum:
hello.c:
3	int sum(int a, int b, int c, int d, int e, int f, int g, int h) {
   0x0000000000001139 <+0>:	push   rbp
   0x000000000000113a <+1>:	mov    rbp,rsp
   0x000000000000113d <+4>:	mov    DWORD PTR [rbp-0x14],edi
   0x0000000000001140 <+7>:	mov    DWORD PTR [rbp-0x18],esi
   0x0000000000001143 <+10>:	mov    DWORD PTR [rbp-0x1c],edx
   0x0000000000001146 <+13>:	mov    DWORD PTR [rbp-0x20],ecx
   0x0000000000001149 <+16>:	mov    DWORD PTR [rbp-0x24],r8d
   0x000000000000114d <+20>:	mov    DWORD PTR [rbp-0x28],r9d
```
gán lần lượt trái qua phải (1-6) các register cho các địa chỉ dưới (nhỏ hơn) rbp. Chú ý chỉ là 6, 2 phần tử 7 8 trong stack chưa được xử lý.

```asm
4	    float s = a + b + c + d + e + f + g + h;
   0x0000000000001151 <+24>:	mov    edx,DWORD PTR [rbp-0x14]
   0x0000000000001154 <+27>:	mov    eax,DWORD PTR [rbp-0x18]
   0x0000000000001157 <+30>:	add    edx,eax
   0x0000000000001159 <+32>:	mov    eax,DWORD PTR [rbp-0x1c]
   0x000000000000115c <+35>:	add    edx,eax
   0x000000000000115e <+37>:	mov    eax,DWORD PTR [rbp-0x20]
   0x0000000000001161 <+40>:	add    edx,eax
   0x0000000000001163 <+42>:	mov    eax,DWORD PTR [rbp-0x24]
   0x0000000000001166 <+45>:	add    edx,eax
   0x0000000000001168 <+47>:	mov    eax,DWORD PTR [rbp-0x28]
   0x000000000000116b <+50>:	add    edx,eax
### 7
   0x000000000000116d <+52>:	mov    eax,DWORD PTR [rbp+0x10]
   0x0000000000001170 <+55>:	add    edx,eax
### 8
   0x0000000000001172 <+57>:	mov    eax,DWORD PTR [rbp+0x18]
   0x0000000000001175 <+60>:	add    eax,edx
   0x0000000000001177 <+62>:	pxor   xmm0,xmm0
   0x000000000000117b <+66>:	cvtsi2ss xmm0,eax
   0x000000000000117f <+70>:	movss  DWORD PTR [rbp-0x4],xmm0

5	    return s;
   0x0000000000001184 <+75>:	movss  xmm0,DWORD PTR [rbp-0x4]
   0x0000000000001189 <+80>:	cvttss2si eax,xmm0

6	}
   0x000000000000118d <+84>:	pop    rbp
   0x000000000000118e <+85>:	ret
```
Thực hiện cộng rồi trả về kết quả. Truy cập argument 7 8 qua địa chỉ trên (lớn hơn) rbp: rbp+0x10 và rbp+0x18.
Những câu lệnh movss (move scalar single precision floating-point) hay cvttss2si `Convert_Integer_To_Single_Precision_Floating_Point` thực hiện trên register xmm0, register chuyên dụng để tính toán float được sử dụng ở đây dù không có số float nào.

Thực hiện trên

```
$ gcc --version
gcc (GCC) 13.1.1 20230429
Copyright (C) 2023 Free Software Foundation, Inc.
This is free software; see the source for copying conditions.  There is NO
warranty; not even for MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.

$ gdb --version
GNU gdb (GDB) 13.1
Copyright (C) 2023 Free Software Foundation, Inc.
License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>
This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.
$ uname -a
Linux zb 6.1.38-1-MANJARO #1 SMP PREEMPT_DYNAMIC Wed Jul  5 23:49:30 UTC 2023 x86_64 GNU/Linux
```

## Tham khảo
- [Intel SDM](https://www.intel.com/content/www/us/en/developer/articles/technical/intel-sdm.html)
- [System V AMD64 ABI](https://gitlab.com/x86-psABIs/x86-64-ABI/-/jobs/artifacts/master/raw/x86-64-ABI/abi.pdf?job=build)
- <https://www.timdbg.com/posts/fakers-guide-to-assembly/>

## Kết luận
Assembly đơn giản, dễ đọc, khó viết.

Phần sau sẽ chạy qua từng dòng code với gdb để xem khi chạy các giá trị được lưu trữ và tính toán thế nào.

Hết.

HVN at <http://pymi.vn> and <https://www.familug.org>.

[Ủng hộ tác giả 🍺](https://www.familug.org/p/ung-ho.html)
