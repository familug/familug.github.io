Title: [TIL] script cài Rust dùng 20 bytes đầu để nhận biết hệ thống
Date: 2025/02/19
Category: frontpage
Tags: til, shell, sh, bash, rust
Slug: til_rustup

Cách cài đặt chính thức đươc khuyên dùng tại trang chủ <https://www.rust-lang.org/tools/install>:

```sh
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
```

nhưng... `curl | sh` thường bị xem là nguy hiểm, do người dùng thường không kiểm tra nội dung sript.
Vậy hãy tải nó về và đọc: 

```
$ curl -Lo rustup.sh https://sh.rustup.rs 
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100 26495  100 26495    0     0   149k      0 --:--:-- --:--:-- --:--:--  149k
```

## Đọc code 


```sh
#!/bin/sh
# shellcheck shell=dash
# shellcheck disable=SC2039  # local is non-POSIX

# This is just a little script that can be downloaded from the internet to
# install rustup. It just does platform detection, downloads the installer
# and runs it.
...

# It runs on Unix shells like {a,ba,da,k,z}sh.
```

đây là 1 file shell code, thậm chí không dùng bash mà dùng dash (POSIX compliant), sử dụng shellcheck để check code theo các best-practice, có thể chạy được với các shell

```sh
$ echo  {a,ba,da,k,z}sh
ash bash dash ksh zsh
```

**It just does platform detection, downloads the installer and runs it.**

nó chỉ nhận biết đây là hệ thống gì để tải bàn cải đặt phù hợp về rồi chạy.
Nhưng làm sao nhận biết được hệ thống đang chạy (windows/linux/macos/arm 32/64 bit?) chỉ với `sh` và coreutils? dùng magic!

Giống như chương trình `file`, đọc vào các byte đầu tiên của file để nhận diện nó.

```sh
get_architecture() {
    local _ostype _cputype _bitness _arch _clibtype
    _ostype="$(uname -s)"
    _cputype="$(uname -m)"
...
```
Chạy thử: 
```sh
$ uname -s
Linux
$ uname -m
x86_64
$ uname -a
Linux hostname 6.8.0-52-generic #53~22.04.1-Ubuntu SMP PREEMPT_DYNAMIC Wed Jan 15 19:18:46 UTC 2 x86_64 x86_64 x86_64 GNU/Linux
```

```sh
get_bitness() {
    need_cmd head
    # Architecture detection without dependencies beyond coreutils.
    # ELF files start out "\x7fELF", and the following byte is
    #   0x01 for 32-bit and
    #   0x02 for 64-bit.
    # The printf builtin on some shells like dash only supports octal
    # escape sequences, so we use those.
    local _current_exe_head
    _current_exe_head=$(head -c 5 /proc/self/exe )
    if [ "$_current_exe_head" = "$(printf '\177ELF\001')" ]; then
        echo 32
    elif [ "$_current_exe_head" = "$(printf '\177ELF\002')" ]; then
        echo 64
    else
        err "unknown platform bitness"
    fi
}
```

đọc vào 5 bytes đầu của chương trình đang chạy (sh) thông qua symlink /proc/self/exe để biết nó thuộc loại nào, nếu byte thứ 5 là 02, đây là 64-bit, nếu là 01 là 32 bit:


```sh
$ head -c 20 /proc/self/exe | xxd
00000000: 7f45 4c46 0201 0100 0000 0000 0000 0000  .ELF............
00000010: 0300 3e00                                ..>.
```
xxd hiển thị mỗi byte bằng 2 ký tự dạng hex, 2 bytes 1 cặp, 7f45 là 2 byte đầu, 4c46 là 2 byte tiếp...
ở máy này byte thứ 5 là 02, vậy đây là 64-bit.

Tương tự, để tìm "endian" là big-endian hay little-endian (Least Significant Bit - LSB), dùng byte thứ 6:
```sh
get_endianness() {
    local cputype=$1
    local suffix_eb=$2
    local suffix_el=$3

    # detect endianness without od/hexdump, like get_bitness() does.
    need_cmd head
    need_cmd tail

    local _current_exe_endianness
    _current_exe_endianness="$(head -c 6 /proc/self/exe | tail -c 1)"
    if [ "$_current_exe_endianness" = "$(printf '\001')" ]; then
        echo "${cputype}${suffix_el}"
    elif [ "$_current_exe_endianness" = "$(printf '\002')" ]; then
        echo "${cputype}${suffix_eb}"
    else
        err "unknown platform endianness"
    fi
}
```
nếu là 01 là little endian, nếu là 02 là bit endian. Ở máy này là 01, tức little endian.

`printf '\002'` in ra giá trị 2 trong hệ octal (8).

```sh
is_host_amd64_elf() {
    need_cmd head
    need_cmd tail
    # ELF e_machine detection without dependencies beyond coreutils.
    # Two-byte field at offset 0x12 indicates the CPU,
    # but we're interested in it being 0x3E to indicate amd64, or not that.
    local _current_exe_machine
    _current_exe_machine=$(head -c 19 /proc/self/exe | tail -c 1)
    [ "$_current_exe_machine" = "$(printf '\076')" ]
}
```
printf '\076' in ra giá trị ở hệ 8 076 ứng với 62 ở hệ 10, và 0x3e ở hệ 16. Máy này có giá trị 3e, nên là amd64_elf.

Thử 1 vòng for từ 1 đến 20 để xem file nhận ra những gì sau mỗi byte:

```sh
$ for i in {1..20}; do echo $i; head -c $i /proc/self/exe > test; file test;  done
1
test: very short file (no magic)
2
test: International EBCDIC text, with no line terminators
3
test: International EBCDIC text, with no line terminators
4
test: ELF
5
test: ELF 64-bit
6
test: ELF 64-bit LSB
7
test: ELF 64-bit LSB
8
test: ELF 64-bit LSB (SYSV)
9
test: ELF 64-bit LSB (SYSV)
10
test: ELF 64-bit LSB (SYSV)
11
test: ELF 64-bit LSB (SYSV)
12
test: ELF 64-bit LSB (SYSV)
13
test: ELF 64-bit LSB (SYSV)
14
test: ELF 64-bit LSB (SYSV)
15
test: ELF 64-bit LSB (SYSV)
16
test: ELF 64-bit LSB (SYSV)
17
test: ELF 64-bit LSB (SYSV)
18
test: ELF 64-bit LSB shared object, (SYSV)
19
test: ELF 64-bit LSB shared object, (SYSV)
20
test: ELF 64-bit LSB shared object, x86-64, (SYSV)
```

Bonus, 4 function `say`, `err`, `check_cmd` và `need_cmd` rất ngắn gọn và hữu ích:

```sh
say() {
    printf 'rustup: %s\n' "$1"
}

err() {
    say "$1" >&2
    exit 1
}

need_cmd() {
    set -x
    if ! check_cmd "$1"; then
        err "need '$1' (command not found)"
    fi
    set +x

}
check_cmd() {
    command -v "$1" > /dev/null 2>&1
}
```
### Kết luận
sh script ở mọi nơi, và cũng có thể sạch đẹp + magic.

Hết.

HVN at <https://pymi.vn> and <https://www.familug.org>.

[Ủng hộ tác giả 🍺](https://www.familug.org/p/ung-ho.html)
