Title: Tạo giao diện gdb như peda/gef/pwndbg
Date: 2023-01-20
Category: frontpage
Tags: gdb, gef, pwndbg, peda, debugger, python

GDB là một debugger lâu đời có rất nhiều tính năng. Nó giống `vim` editor/emacs nhiều điểm:

- nhiều tính năng nhưng mặc định thì không bật gì, khó dùng
  ![gdb_tui]({static}/images/gdb_tui.png)
- cài thêm các tính năng vào sẽ ngon lành
- việc cấu hình cũng cần phải học, nên có nhiều bản "distro" dùng sẵn.
- sau hàng chục năm config chán chê, người dùng hardcore lại quay về 1 file config đơn giản.

GDB các bản mở rộng dễ dùng/tiện dụng hơn có:

- <https://github.com/pwndbg/pwndbg>
- <https://github.com/longld/peda>
- <https://github.com/hugsy/gef>
- <https://github.com/snare/voltron>

Như vim có

- [spacevim](https://spacevim.org/)
- [spf13-vim](http://vim.spf13.com/)
- ...

Tương tự với emacs.

PS: tham khảo 2 phần trước:

- p1: <https://n.pymi.vn/hgdb.html>
- p2: <https://n.pymi.vn/hgdb-arch.html>

### Tạo giao diện giống pwndbg/gef/peda
![pwndbg](https://github.com/pwndbg/pwndbg/raw/dev/caps/context.png)

3 bản mở rộng này nhìn chung đều có giao diện giống nhau. Màn hình sẽ hiện "context" với 3 phần:

- các register
- disassembly code
- stack

#### gdb lấy thông tin các register
Lệnh gdb `info registers` sẽ hiện thông tin của tất cả các register.

```
$ gdb ./a.out -q
Reading symbols from ./a.out...
(No debugging symbols found in ./a.out)
(gdb) start
Temporary breakpoint 1 at 0x1149
Starting program: /home/hvn/me/news/a.out

Temporary breakpoint 1, 0x0000555555555149 in main ()
(gdb) info registers
rax            0x555555555149      93824992235849
rbx            0x5555555551a0      93824992235936
rcx            0x5555555551a0      93824992235936
rdx            0x7fffffffe548      140737488348488
rsi            0x7fffffffe538      140737488348472
rdi            0x1                 1
rbp            0x0                 0x0
rsp            0x7fffffffe448      0x7fffffffe448
r8             0x0                 0
r9             0x7ffff7fe0d60      140737354009952
r10            0x7                 7
r11            0x2                 2
r12            0x555555555060      93824992235616
r13            0x7fffffffe530      140737488348464
r14            0x0                 0
r15            0x0                 0
rip            0x555555555149      0x555555555149 <main>
eflags         0x246               [ PF ZF IF ]
cs             0x33                51
ss             0x2b                43
ds             0x0                 0
es             0x0                 0
fs             0x0                 0
gs             0x0                 0
(gdb)
```

Để lấy thông tin của 1 register cụ thể, ví dụ rsp, gõ `info register rsp`.

So với pwndbg

```
 RAX  0x555555555149 (main) ◂— endbr64
 RBX  0x5555555551a0 (__libc_csu_init) ◂— endbr64
 RCX  0x5555555551a0 (__libc_csu_init) ◂— endbr64
 RDX  0x7fffffffe488 —▸ 0x7fffffffe80a ◂— 'SSH_AUTH_SOCK=/run/user/1000/keyring/ssh'
 RDI  0x1
 RSI  0x7fffffffe478 —▸ 0x7fffffffe7f2 ◂— '/home/hvn/me/news/a.out'
 R8   0x0
 R9   0x7ffff7fe0d60 (_dl_fini) ◂— endbr64
 R10  0x7
 R11  0x2
 R12  0x555555555060 (_start) ◂— endbr64
 R13  0x7fffffffe470 ◂— 0x1
 R14  0x0
 R15  0x0
 RBP  0x0
 RSP  0x7fffffffe388 —▸ 0x7ffff7dd8083 (__libc_start_main+243) ◂— mov    edi, eax
 RIP  0x555555555149 (main) ◂— endbr64
```

Thứ tự có thay đổi 1 chút và chỉ hiển thị tới RIP.

so với gef:

```
$rax   : 0x0000555555555149  →  <main+0> endbr64
$rbx   : 0x00005555555551a0  →  <__libc_csu_init+0> endbr64
$rcx   : 0x00005555555551a0  →  <__libc_csu_init+0> endbr64
$rdx   : 0x00007fffffffe488  →  0x00007fffffffe80a  →  "SSH_AUTH_SOCK=/run/user/1000/keyring/ssh"
$rsp   : 0x00007fffffffe388  →  0x00007ffff7dd8083  →  <__libc_start_main+243> mov edi, eax
$rbp   : 0x0
$rsi   : 0x00007fffffffe478  →  0x00007fffffffe7f2  →  "/home/hvn/me/news/a.out"
$rdi   : 0x1
$rip   : 0x0000555555555149  →  <main+0> endbr64
$r8    : 0x0
$r9    : 0x00007ffff7fe0d60  →  <_dl_fini+0> endbr64
$r10   : 0x7
$r11   : 0x2
$r12   : 0x0000555555555060  →  <_start+0> endbr64
$r13   : 0x00007fffffffe470  →  0x0000000000000001
$r14   : 0x0
$r15   : 0x0
$eflags: [ZERO carry PARITY adjust sign trap INTERRUPT direction overflow resume virtualx86 identification]
$cs: 0x33 $ss: 0x2b $ds: 0x00 $es: 0x00 $fs: 0x00 $gs: 0x00
```

Hiện đủ các registers.

Cả 2 phiên bản này đều có giá trị thứ 2 là tên function nếu có thể tìm được.

Có thể sử dụng lệnh `x` để thu được kết quả tương tự:

```
(gdb) x $rax
0x555555555149 <main>:	0xfa1e0ff3
(gdb) x $rbx
0x5555555551a0 <__libc_csu_init>:	0xfa1e0ff3
```

dùng `x/i` để "examine instruction" tại đó:

```
(gdb) x/i $rax
=> 0x555555555149 <main>:	endbr64
```

Viết câu lệnh context chạy `info registers` rồi lặp qua các register chạy `x/i` sẽ thu được kết quả như pwndbg/gef.

```py
    def invoke(self, arg, from_tty):
        for line in self.run_command("info registers").splitlines():
            if not line.startswith("r"):
                continue
            register, _address, *contents = line.split()
            r = self.run_command(f"x/i ${register}").strip(" =>\n")
            if '<' in r and '>' in r:
                print("{:<15}{}".format(register, r))
            else:
                print(line)
```

```
(gdb) context
rax            0x555555555149 <main>:	endbr64
rbx            0x5555555551a0 <__libc_csu_init>:	endbr64
rcx            0x5555555551a0 <__libc_csu_init>:	endbr64
rdx            0x7fffffffe548      140737488348488
rsi            0x7fffffffe538      140737488348472
rdi            0x1                 1
rbp            0x0                 0x0
rsp            0x7fffffffe448      0x7fffffffe448
r8             0x0                 0
r9             0x7ffff7fe0d60 <_dl_fini>:	endbr64
r10            0x7                 7
r11            0x2                 2
r12            0x555555555060 <_start>:	endbr64
r13            0x7fffffffe530      140737488348464
r14            0x0                 0
r15            0x0                 0
rip            0x555555555149 <main>:	endbr64
```

#### gdb disassemble code
Hiển thị các instruction tương ứng trước và sau vị trí "hiện tại". Trên kiến trúc x86, đó là register `rip` (register instruction pointer), trên kiến trúc khác có thể là register khác, vậy nên GDB dùng tên chung `pc` (program counter) để thay tương ứng cho từng kiến trúc.

Phần này có tên là DISASM hoặc CODE

```asm
   0x555555555149 <main>       endbr64
   0x55555555514d <main+4>     push   rbp
   0x55555555514e <main+5>     mov    rbp, rsp
   0x555555555151 <main+8>     sub    rsp, 0x20
   0x555555555155 <main+12>    mov    dword ptr [rbp - 0x14], edi
 ► 0x555555555158 <main+15>    mov    qword ptr [rbp - 0x20], rsi
   0x55555555515c <main+19>    mov    dword ptr [rbp - 0xc], 5
   0x555555555163 <main+26>    mov    dword ptr [rbp - 8], 7
   0x55555555516a <main+33>    mov    edx, dword ptr [rbp - 0xc]
   0x55555555516d <main+36>    mov    eax, dword ptr [rbp - 8]
   0x555555555170 <main+39>    add    eax, edx
```

Ta có thể lấy vị trí của `$pc` rồi in ra vài instruction trước và sau `$pc`, sử dụng lệnh `x/10i $pc`.

```asm
(gdb) set disassembly-flavor intel
(gdb) start
Temporary breakpoint 1 at 0x1161
Starting program: /home/hvn/me/news/main

Temporary breakpoint 1, 0x0000555555555161 in main ()
(gdb) x/10i $pc
=> 0x555555555161 <main>:	endbr64
   0x555555555165 <main+4>:	push   rbp
   0x555555555166 <main+5>:	mov    rbp,rsp
   0x555555555169 <main+8>:	sub    rsp,0x20
   0x55555555516d <main+12>:	mov    DWORD PTR [rbp-0x14],edi
   0x555555555170 <main+15>:	mov    QWORD PTR [rbp-0x20],rsi
   0x555555555174 <main+19>:	mov    DWORD PTR [rbp-0xc],0x5
   0x55555555517b <main+26>:	mov    DWORD PTR [rbp-0x8],0x7
   0x555555555182 <main+33>:	mov    edx,DWORD PTR [rbp-0x8]
   0x555555555185 <main+36>:	mov    eax,DWORD PTR [rbp-0xc]
```

Khi binary không chứa `debug_info` (compile -g) như khi dev, không có sourcecode để gdb xem `n`ext - dòng code tiếp theo ứng với địa chỉ nào, ta phải tự đặt breakpoint tại địa chỉ rồi `c`ontinue chạy tiếp:

```asm
(gdb) b *0x555555555182
Breakpoint 2 at 0x555555555182
(gdb) c
Continuing.

Breakpoint 2, 0x0000555555555182 in main ()
(gdb) x/10i $pc
=> 0x555555555182 <main+33>:	mov    edx,DWORD PTR [rbp-0x8]
   0x555555555185 <main+36>:	mov    eax,DWORD PTR [rbp-0xc]
   0x555555555188 <main+39>:	mov    esi,edx
   0x55555555518a <main+41>:	mov    edi,eax
   0x55555555518c <main+43>:	call   0x555555555149 <sum>
   0x555555555191 <main+48>:	mov    DWORD PTR [rbp-0x4],eax
   0x555555555194 <main+51>:	mov    eax,DWORD PTR [rbp-0x4]
   0x555555555197 <main+54>:	mov    esi,eax
   0x555555555199 <main+56>:	lea    rdi,[rip+0xe64]        # 0x555555556004
   0x5555555551a0 <main+63>:	mov    eax,0x0
(gdb)
```

Để in ra trước `$pc`, cần thực hiện 1 chút tính toán để tìm kiếm địa chỉ hợp lệ rồi in ra từ địa chỉ đó thay vì `$pc`, ví dụ ở đây sau khi tính được ra địa chỉ là `$pc-21`, ta có:

```asm
(gdb) x/10i ($pc-21)
   0x55555555516d <main+12>:	mov    DWORD PTR [rbp-0x14],edi
   0x555555555170 <main+15>:	mov    QWORD PTR [rbp-0x20],rsi
   0x555555555174 <main+19>:	mov    DWORD PTR [rbp-0xc],0x5
   0x55555555517b <main+26>:	mov    DWORD PTR [rbp-0x8],0x7
=> 0x555555555182 <main+33>:	mov    edx,DWORD PTR [rbp-0x8]
   0x555555555185 <main+36>:	mov    eax,DWORD PTR [rbp-0xc]
   0x555555555188 <main+39>:	mov    esi,edx
   0x55555555518a <main+41>:	mov    edi,eax
   0x55555555518c <main+43>:	call   0x555555555149 <sum>
   0x555555555191 <main+48>:	mov    DWORD PTR [rbp-0x4],eax
```

Ở đây, để đơn giản sẽ tạm bỏ qua tính toán và chỉ in từ `$pc` trở đi:

Code python để in ra phần DISASM:

```py
        print(self.run_command("x/10i $pc"))
```

#### gdb hiển thị stack
Hiển thị stack là hiển thị giá trị của  các địa chỉ từ `$rsp` (register stack pointer)
tới `$rbp` (register base pointer):

pwndbg:

```asm
00:0000│ rsp 0x7fffffffe358 —▸ 0x555555555191 (main+48) ◂— mov    dword ptr [rbp - 4], eax
01:0008│     0x7fffffffe360 —▸ 0x7fffffffe478 —▸ 0x7fffffffe7f5 ◂— '/home/hvn/me/news/main'
02:0010│     0x7fffffffe368 ◂— 0x155555060
03:0018│     0x7fffffffe370 ◂— 0x5ffffe470
04:0020│     0x7fffffffe378 ◂— 0x7
05:0028│ rbp 0x7fffffffe380 ◂— 0x0
06:0030│     0x7fffffffe388 —▸ 0x7ffff7dd8083 (__libc_start_main+243) ◂— mov    edi, eax
07:0038│     0x7fffffffe390 —▸ 0x7ffff7ffc620 (_rtld_global_ro) ◂— 0x50f4a00000000
```


```
(gdb) print ($rbp-$rsp)
$4 = 40
```

Cách nhau 40 bytes, chia cho 4 được 10 "word" (1 word = 4 bytes)

```
(gdb) x/10w $rsp
0x7fffffffe358:	0x55555191	0x00005555	0xffffe478	0x00007fff
0x7fffffffe368:	0x55555060	0x00000001	0xffffe470	0x00000005
0x7fffffffe378:	0x00000007	0x00000000
```

Code Python:

```py
        word_to_print = int(self.run_command("print ($rbp -$rsp)/4").split()[-1])
        print(self.run_command(f"x/{word_to_print}w $rsp"))
```

### Hiện context sau mỗi câu lệnh gdb
GDB có "hook" để tự chạy mỗi câu lệnh trước/sau một hành động.
`hook-stop` sẽ chạy trước mỗi câu lẹnh.

Thêm code Python:

```py
gdb.execute("""define hook-stop
context
end""")
```

### Kết quả

```asm
(gdb) b *0x555555555182
Breakpoint 2 at 0x555555555182
(gdb) c
Continuing.
rax            0x555555555161 <main>:	endbr64
rbx            0x5555555551c0 <__libc_csu_init>:	endbr64
rcx            0x5555555551c0 <__libc_csu_init>:	endbr64
rdx            0x7fffffffe548      140737488348488
rsi            0x7fffffffe538      140737488348472
rdi            0x1                 1
rbp            0x7fffffffe440      0x7fffffffe440
rsp            0x7fffffffe420      0x7fffffffe420
r8             0x0                 0
r9             0x7ffff7fe0d60 <_dl_fini>:	endbr64
r10            0x7                 7
r11            0x2                 2
r12            0x555555555060 <_start>:	endbr64
r13            0x7fffffffe530      140737488348464
r14            0x0                 0
r15            0x0                 0
rip            0x555555555182 <main+33>:	mov    -0x8(%rbp),%edx
====================DISASM====================
=> 0x555555555182 <main+33>:	mov    -0x8(%rbp),%edx
   0x555555555185 <main+36>:	mov    -0xc(%rbp),%eax
   0x555555555188 <main+39>:	mov    %edx,%esi
   0x55555555518a <main+41>:	mov    %eax,%edi
   0x55555555518c <main+43>:	callq  0x555555555149 <sum>
   0x555555555191 <main+48>:	mov    %eax,-0x4(%rbp)
   0x555555555194 <main+51>:	mov    -0x4(%rbp),%eax
   0x555555555197 <main+54>:	mov    %eax,%esi
   0x555555555199 <main+56>:	lea    0xe64(%rip),%rdi        # 0x555555556004
   0x5555555551a0 <main+63>:	mov    $0x0,%eax

====================STACK====================
0x7fffffffe420:	0xffffe538	0x00007fff	0x55555060	0x00000001
0x7fffffffe430:	0xffffe530	0x00000005	0x00000007	0x00000000

```

Tô màu mè, format đẹp lại là có một phiên bản gdb do chính tay bạn làm ra.

Code at <https://github.com/hvnsweeting/hgdb/blob/v0.1/hgdb.py>

### Kết luận
Python được dùng phổ biến để mở rộng tính năng cho các phần mềm khác ([blender](https://docs.blender.org/api/current/info_overview.html), [calibre](https://manual.calibre-ebook.com/creating_plugins.html), ...)

Với sự có mặt của Python (và Guile), gdb đã cho phép mình tự biến hóa thành những sản phẩm đầy tiện lợi sang xịn mịn nhờ cồng đồng.

Và bạn cũng có thể tự làm agdb bgdb ... hgdb hay ... zgdb cho chính mình.

Hết.

HVN at <https://pymi.vn> and <https://www.familug.org>.

[Ủng hộ tác giả 🍺](https://www.familug.org/p/ung-ho.html)
