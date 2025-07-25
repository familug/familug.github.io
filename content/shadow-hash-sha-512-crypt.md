Title: Tìm hiểu password hashing trong /etc/shadow trên Linux
Date: 2025/07/25
Category: frontpage
Tags: linux, hash, passwd, shadow, mkpasswd, sha512, crypt, python, rust
Slug: shadow-hash-sha-512-crypt

Các hệ điều hành Linux sử dụng file `/etc/passwd` để chứa thông tin các user của hệ thống và `/etc/shadow` để chứa thông tin về password tương ứng của các user này.

Mọi tài khoản đều có thể xem `/etc/passwd`, nhưng file `/etc/shadow` được bảo mật, thường chỉ có root mới xem được:

```
# ls -l /etc/passwd /etc/shadow
-rw-r--r-- 1 root root   3443 Jul 25  18 21:02 /etc/passwd
-rw-r----- 1 root shadow 1855 Jul 25  25 20:52 /etc/shadow
```

Admin không chỉnh sửa trực tiếp nội dung file `/etc/shadow` mà dùng các công cụ quản lý user trên hệ thống như `useradd`, `usermod`, `passwd`.

Ví dụ nội dung 1 file /etc/shadow:

```
# cat /etc/passwd
root:x:0:0:root:/root:/bin/bash
bin:x:1:1:bin:/bin:/sbin/nologin
daemon:x:2:2:daemon:/sbin:/sbin/nologin
ftp:x:14:50:FTP User:/var/ftp:/sbin/nologin
nobody:x:65534:65534:Kernel Overflow User:/:/sbin/nologin
pika:x:1000:1000::/home/pika:/bin/bash

# cat /etc/shadow
root:$6$rounds=100000$iA2WWPgA5yY1mjXj$dHNFwg4Nh5j30Sq6vC/O74wBuuJGdt23pgU3eV//M9wOF1RcqF3lAc/HZ9rpgqcRawFjw0fiMMAqO9SADvSdo0:20294:0:99999:7:::
bin:*:19816:0:99999:7:::
daemon:*:19816:0:99999:7:::
ftp:*:19816:0:99999:7:::
nobody:*:19816:0:99999:7:::
pika:$6$rounds=100000$wYEmXgSx4U3GBF0i$AbEnTG1ag6XlxH9h4nBBaepHe9XWjBK9UxJs.ItnT8UaiLgl30EjwJq.ztKqZC6UrnEIM8p1zC6.d06zBU6gL0:20294:0:99999:7:::
```

Cả 2 file này đều có định dạng theo dòng, mỗi dòng có nhiều "cột" sử dụng dấu `:` để phân cách.
File `/etc/passwd` chứa `login-name:x:uid:gid:username-or-comment:home:shell`.
File `/etc/shadow` chứa `login-name:encrypted-password:last-pw-change:......`

Mỗi dòng của `/etc/shadow` chứa 9 thông tin:

- login name
- password đã được mã hóa
- lần cuối thay đổi password, tính theo số ngày từ 1/1/1970: `$ python3 -c 'import datetime; print((datetime.datetime.now() - datetime.datetime(1970,1,1)).days)' # 20294`
...

xem chi tiết tại `man 5 shadow`.

### Đọc chi tiết password đã được mã hóa

Sử dụng dấu `$` để phân cách các phần:

```
$6$rounds=100000$wYEmXgSx4U3GBF0i$AbEnTG1ag6XlxH9h4nBBaepHe9XWjBK9UxJs.ItnT8UaiLgl30EjwJq.ztKqZC6UrnEIM8p1zC6.d06zBU6gL0
```

- `$6$` là **prefix**, cho biết đây là kết quả của việc sử dụng hashing method **sha512crypt**. Một vài các prefix thường thấy và hashing method tương ứng: `$y$`: **yescrypt** `$7$`: **script** `$2$`: **bcrypt**. Ví dụ trên dùng `AlmaLinux release 9.6` mặc định sử dụng **sha512crypt**, trong khi Debian 12 (bookworm) lại dùng **yescrypt**.
- `rounds=100000`: số vòng lặp khi tính hash, ở đây là `100000`, giá trị càng lớn, tính hash càng lâu. Đây là một trong các biện pháp chống hacker bruteforce password.
- `wYEmXgSx4U3GBF0i`: giá trị salt. Salt trong crypto là giá trị (thường là ngẫu nhiên) được nối thêm vào password trước khi tính hash, nhằm chống lại việc bruteforce password sử dụng bảng hash tính sẵn (rainbow table). Khi sử dụng salt khác nhau, 2 password giống nhau cho ra 2 mã hash khác nhau. User `root` và `pika` đều dùng chung password, nhưng do salt khác nhau nên hash khác nhau.
- Phần còn lại: giá trị hash `AbEnTG1ag6XlxH9h4nBBaepHe9XWjBK9UxJs.ItnT8UaiLgl30EjwJq.ztKqZC6UrnEIM8p1zC6.d06zBU6gL0` biểu diễn ở dạng base-64 biến thể, không chứa dấu `+=` như base64 phổ biến, còn gọi là `B64` (từ khóa: `crypt b64`).

Chi tiết xem `man 5 crypt`:

```
# whatis crypt
crypt (5)            - storage format for hashed passphrases and available hashing methods
crypt (3)            - passphrase hashing
crypt (3posix)       - string encoding function (CRYPT)
```

### Sinh password có thể dùng cho shadow với mkpassword

- Debian/Ubuntu: `sudo apt install whois`
- Fedora/RockyLinux/AlmaLinux: `sudo dnf install mkpasswd`

Mật khẩu chưa mã hóa là: `familug.org`.

Tạo lại encrypted password cho user pika:

```
$ echo -n familug.org | mkpasswd --method=sha-512 --round 100000 --salt wYEmXgSx4U3GBF0i --stdin
$6$rounds=100000$wYEmXgSx4U3GBF0i$AbEnTG1ag6XlxH9h4nBBaepHe9XWjBK9UxJs.ItnT8UaiLgl30EjwJq.ztKqZC6UrnEIM8p1zC6.d06zBU6gL0
```
Tạo lại encrypted password cho user root:

```
$ echo -n familug.org | mkpasswd --method=sha-512 --round 100000 --salt iA2WWPgA5yY1mjXj --stdin
$6$rounds=100000$iA2WWPgA5yY1mjXj$dHNFwg4Nh5j30Sq6vC/O74wBuuJGdt23pgU3eV//M9wOF1RcqF3lAc/HZ9rpgqcRawFjw0fiMMAqO9SADvSdo0
```

Set encrypted password cho user pika:

```
# #-p, --password PASSWORD       use encrypted password for the new password
# usermod pika -p '$6$rounds=100000$iA2WWPgA5yY1mjXj$dHNFwg4Nh5j30Sq6vC/O74wBuuJGdt23pgU3eV//M9wOF1RcqF3lAc/HZ9rpgqcRawFjw0fiMMAqO9SADvSdo0'
# cat /etc/shadow
root:$6$rounds=100000$iA2WWPgA5yY1mjXj$dHNFwg4Nh5j30Sq6vC/O74wBuuJGdt23pgU3eV//M9wOF1RcqF3lAc/HZ9rpgqcRawFjw0fiMMAqO9SADvSdo0:20294:0:99999:7:::
...
pika:$6$rounds=100000$iA2WWPgA5yY1mjXj$dHNFwg4Nh5j30Sq6vC/O74wBuuJGdt23pgU3eV//M9wOF1RcqF3lAc/HZ9rpgqcRawFjw0fiMMAqO9SADvSdo0:20294:0:99999:7:::
```

### Gọi crypt từ Python 3.12

```
$ python3 -c 'import crypt; print(crypt.crypt("familug.org", "$6$rounds=100000$wYEmXgSx4U3GBF0i$"))'
$6$rounds=100000$wYEmXgSx4U3GBF0i$AbEnTG1ag6XlxH9h4nBBaepHe9XWjBK9UxJs.ItnT8UaiLgl30EjwJq.ztKqZC6UrnEIM8p1zC6.d06zBU6gL0
```

Module này đã bị remove từ 3.13.

### Sinh encrypted password sha512crypt với Rust

```toml
# Cargo.toml
[package]
name = "crypt"
version = "0.1.0"
edition = "2021"

[dependencies]
sha-crypt = "0.4.0"
```

```rs
// src/main.rs
fn main() {
    let encrypted = sha_crypt::sha512_crypt_b64(
        "familug.org".as_bytes(),
        "wYEmXgSx4U3GBF0i".as_bytes(),
        &sha_crypt::Sha512Params::new(100000).unwrap(),
    )
    .expect("Failed to get hash");
    println!("{}", encrypted);
}
//  cargo run 2>/dev/null
// AbEnTG1ag6XlxH9h4nBBaepHe9XWjBK9UxJs.ItnT8UaiLgl30EjwJq.ztKqZC6UrnEIM8p1zC6.d06zBU6gL0
```

Xem code [iterate qua các round](https://github.com/RustCrypto/password-hashes/blob/ed2bea299ca13f8cfe0bfee2619334f102404acf/sha-crypt/src/lib.rs#L143-L174)

### Kết luận
`shadow` chứa thông tin về password của các tài khoản trên hệ thống, bao gồm cả password đã mã hóa, nếu sử dụng các `hashing method` yếu/cũ, có thể bị hacker crack shadow password bằng các công cụ chuyên dùng.

Hết.

### Tham khảo
- `man 5 crypt`
- `man 5 passwd`
- `man 5 shadow`

HVN at <https://pymi.vn> and <https://www.familug.org>.

[Ủng hộ tác giả 🍺](https://www.familug.org/p/ung-ho.html)
