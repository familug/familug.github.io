Title: 24 ngày học Rust - ngày 1 String
Date: 2023-12-02
Category: frontpage
Tags: rust, adventofcode

Loạt bài viết giới thiệu các khái niệm trong Rust.
Không quá chi tiết, đa phần ngắn gọn, mục tiêu trong 24 ngày.

PS: Là note khi giải <https://adventofcode.com>

## Cài đặt & chạy code
Tham khảo <https://pp.pymi.vn/article/aoc2021/>

Bài viết sử dụng [Rust 2021](https://doc.rust-lang.org/edition-guide/rust-2021/index.html).

## String, &str
Rust có 2 kiểu string thường dùng là str và String.

### str - string slice
`str` còn được gọi là **string slice**, thường được dùng ở dạng "borrowed" `&str`.
Kiểu của các string khi viết trực tiếp vào code (literal string) là `&str`.
`str` dùng double quote `"` để bao quanh nội dung:

```rust
let s: &str = "Hello, world!";
```

### String
`String` là một UTF-8 string có thể thay đổi.

> A UTF-8–encoded, growable string.

`String` làm chủ sở hữu giá trị của nó nên còn gọi là **owned string** - trái với `&str` là **borrowed** (đi mượn).

```rust
let s: String = String::from("Hello, world!");
dbg!(s);
// [src/main.rs:6] s = "Hello, world!"
```
Thêm (append) vào String với `push(char)` hay `push_str(&str)`.

```rust
let mut res: String = String::from("Hello, world!");
res.push('\t');
res.push_str("How are you?");
// [src/main.rs:10] res = "Hello, world!\tHow are you?"
```

### String vs &str
`String` và `&str` có nhiều method giống nhau: `starts_with`, `ends_with`, `split`, `replace`, `is_digit`...

Sự khác biệt chủ yếu ở mục đích sử dụng:

- Dùng `String` khi tạo string mới hay nội dung string thay đổi.
- Dùng `&str` khi nội dung string cố định, không mới.

Method `replace` cho thấy sự khác biệt này:

```rs
pub fn replace<'a, P>(&'a self, from: P, to: &str) -> String
where
    P: Pattern<'a>,
```

`"a b c a".replace("a", "d")` trả về 1 `String`. Có thể hiểu rằng do Rust cần cấp phát bộ nhớ để tạo ra 1 String có nội dung mới, nên đây là kiểu `String` thay vì `&str`.

Đọc nội dùng 1 file cũng trả về String:

```rs
let contents = std::fs::read_to_string("/etc/passwd").unwrap();
```

```rs
pub fn read_to_string<P>(path: P) -> io::Result<String>
where
    P: AsRef<Path>,
```

Dùng `"abc".to_string()` để biến `&str` thành `String`, ngược lại `String::from("abc").as_str()` để biến `String` thành `&str`.

### Split
`"a-b-c".split("-")` trả về một `Split` struct, hay full name `std::str::Split` chứ không phải 1 vector `Vec<&str>`.

```rs
pub fn split<'a, P>(&'a self, pat: P) -> Split<'a, P>
where
    P: Pattern<'a>,
```
`Split` implement `Iterator` trait (hay nói như Python: list là 1 iterable, có method `__iter__`)

nên có thể duyệt qua từng phần tử của kết quả, mỗi phần tử là 1 `&str` cho dù `s` là `&str` hay `String`:
```rust
let sp: std::str::Split<&str>  = "bacadae".split("a");
for p in sp {
  dbg!(p);
}
let s = String::from("bacadae");
for p in s.split("a") {
  dbg!(p);
}
//[src/main.rs:16] p = "b"
//[src/main.rs:16] p = "c"
//[src/main.rs:16] p = "d"
//[src/main.rs:16] p = "e"
```

`filter` method trả về 1 `Filter`
```rust
let s = String::from("bacadae");
// Filter<Split<&str>, |&&str| -> bool>
let ps = s.split("a").filter(|&s| s > "c");
for r in ps {
  dbg!(r); // r là &str
}
// [src/main.rs:17] r = "d"
// [src/main.rs:17] r = "e"
```

Để thu được `Vec<&str>` dùng `collect()`:
```rust
let s = "  a  b\tc\nd    ";
// pub fn split_whitespace(&self) -> SplitWhitespace<'_>
let parts: Vec<&str> = s.split_whitespace().collect();
dbg!(parts);
// [src/main.rs:19] parts = [
//     "a",
//     "b",
//     "c",
//     "d",
// ]
```
## char - character

char là một ký tự, hay chính xác hơn là 1 Unicode scalar value, dùng single quote `'` để bao quanh 2 bên char.

```rust
let c: char = '\u{1b0}'; // ư
let c2 = 'a';
```

Biến vector char thành String với `collect`:

```rust
let v = vec!['a', 'b', 'c'];
let s: String = v.iter().collect();
```

## Kết luận
Khi nội dung string được tạo mới, hoặc thay đổi, dùng `String`, khi nội dung cố định, không mới, dùng `&str`.

[Ủng hộ tác giả 🍺](https://www.familug.org/p/ung-ho.html)
