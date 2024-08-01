Title: Rust không import
Date: 2024-08-01
Category: frontpage
Tags: rust, use, import

Mọi ngôn ngữ lập trình hiện đại đều có cơ chế để dùng lại code. C có `#include<stdio.h>` thì Python, Go, Java có `import`. Rust không như thế, không có import, không cần import.

## Rust dùng thư viện bằng path đầy đủ
Không cần import. Ví dụ sử dụng các function trong thư viện `std::fs`:

```rust
fn main() {
    std::fs::create_dir_all("a/b/c/d").unwrap();
    std::fs::write("a/file", "Hello").expect("Cannot write file");

    let rd = std::fs::read_dir("a").unwrap();
    for i in rd {
        let i = i.unwrap();
        if i.path().is_dir() {
            println!("Directory {}", i.file_name().to_string_lossy());
        } else if i.path().is_file() {
            println!("File {}", i.file_name().to_string_lossy());
        }
    }
}
```

### Rust crate, module

`std::fs::create_dir_all` là **full path** tới function `create_dir_all`.

`std` là 1 crate /kreɪt/ - đơn vị 1 "library" trong Rust. Xem các crates tại <https://crates.io/>

`fs` là 1 module - thường tương ứng với 1 file hay 1 thư mục, xem các module trong crate `std` tại <https://doc.rust-lang.org/std/index.html>

Code tạo thư mục a chứa thư mục b chứa thư mục c chứa thư mục d, tương tự lệnh `mkdir -p a/b/c/d` trên Linux.
Sau đó ghi ra 1 file text tên "file" trong thư mục "a" dòng chữ "Hello". Liệt kê các file trong thư mục "a" và in ra màn hình đâu là thư mục đâu là file.

Output:

```
File file
Directory b
```

Rust có thể gọi function `create_dir_all` trong `fs` trong `std` mà không cần import.

Nhưng gõ `std::fs::create_dir_all` dài, nên Rust có `use` dùng để tạo "shortcut".

```rust
use std::fs::create_dir_all;
// use std::fs::{create_dir_all, write}; viết ngắn gọn thay vì viết use cho từng function.
// use std::fs::{*}; tất cả
fn main() {
    create_dir_all("a/b/c/d").unwrap();
}
```

tương tự Python `from math import sqrt; sqrt(4)`.
hay `from math import *; sqrt(4)`

Nếu viết `use std::fs` thì sẽ chỉ cần gõ `fs::create_dir_all` là đủ.
Đây là "best practice" để vừa gõ ngắn hơn, vừa biết `create_dir_all` thuộc về `fs`.

```rust
use std::fs;

fn main() {
    fs::create_dir_all("a/b/c/d").unwrap();
    fs::write("a/file", "Hello").expect("Cannot write file");

    let rd = fs::read_dir("a").unwrap();
    for i in rd {
        let i = i.unwrap();
        if i.path().is_dir() {
            println!("Directory {}", i.file_name().to_string_lossy());
        } else if i.path().is_file() {
            println!("File {}", i.file_name().to_string_lossy());
        }
    }
}
```


## Kết luận
Rust không import, chỉ use để tạo shortcut.

Hết

## Tham khảo
- The Rust Programming Language <https://web.archive.org/web/20240718162636/https://doc.rust-lang.org/stable/book/ch07-04-bringing-paths-into-scope-with-the-use-keyword.html>

[Ủng hộ tác giả 🍺](https://www.familug.org/p/ung-ho.html)
