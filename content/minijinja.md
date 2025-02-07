Title: Những bất ngờ khi dùng Rust minijinja của tác giả Jinja2
Date: 2025-02-07
Category: frontpage
Tags: rust, jinja2, minijinja, askama
Slug: minijinja

Khi dùng Rust, người dùng thường có cảm giác an toàn: nếu nó compile, nó sẽ chạy đúng.
Điều này không viết ở đâu trong tài liệu cả, và chỉ là ảo tưởng của người dùng (hello AI hallucination).

minijinja <https://github.com/mitsuhiko/minijinja/> là thư viện giống jinja2 của tác giả mitsuhiko, viết cho Rust.
Dùng minijinja có syntax giống như Jinja2, đỡ phải học thêm gi mới, thế nhưng, vẫn có những bất ngờ.

Code:

```rs
// cargo add minijinja serde --features serde/derive
use minijinja::{Environment, context};
use serde::Serialize;

mod models {
    use serde::Serialize;
    #[derive(Debug, Serialize)]
    pub struct Profile {
        email: String,
    }

    pub fn new() -> Profile {
        Profile{email: "info@debian.com".to_string()}
    } }

#[derive(Debug, Serialize)]
struct User {
    name: String,
    address: String
}
fn main() {
    let mut env = Environment::new();
    let user = User{name: "Pikachu".to_string(), address: "Japan".to_string()};
    let profile = models::new();
    env.add_template("hello.txt", "Hello {{ user.name }} from address {{ user.addres }} email {{ profile.email }} !").unwrap();
    let template = env.get_template("hello.txt").unwrap();
    println!("{}", template.render(context! { user, profile }).unwrap());
}
```

Kết quả:

```
$ cargo run

Hello Pikachu from address  email info@debian.com !
```

### Không phát hiện được typo trong tên field
Trước hết, address trong output bị bỏ trống. Lý do trong template gõ nhầm field `addres` thay vì `address`, người dùng có thể mong đợi chương trình sẽ compile fail nhưng ở đây lại thành công lặng lẽ và output empty string.

Giải pháp: dùng thư viện hỗ trợ check ở compile time như [askama](https://github.com/rinja-rs/askama) có hỗ trợ `Benefit from the safety provided by Rust's type system`.


```rs
use askama::Template; // bring trait in scope

#[derive(Template)] // this will generate the code...
#[template(path = "hello.html")] // using the template in this path, relative
                                 // to the `templates` dir in the crate root
struct HelloTemplate<'a> { // the name of the struct can be anything
    user: &'a User, // the field name should match the variable name
                   // in your template
}


#[derive(Debug)]
struct User {
    name: String,
    address: String
}
fn main() {
    let user = User{name: "Pikachu".to_string(), address: "Japan".to_string()};

    let hello = HelloTemplate { user: &user }; // instantiate your struct
    println!("{}", hello.render().unwrap()); // then render it.
}
```

```html
// templates/hello.html
"Hello {{ user.name }} from address {{ user.addres }} !"
```
Báo lỗi như sau khi build:
```
error[E0609]: no field `addres` on type `&'a User`
```

### Truy cập được nội dung private field trong struct

Bất ngờ thứ 2 field email, dù không phải public, vẫn truy cập được từ mod khác, do sử dụng `derive(Serialize)`, có thể sẽ có ngày có người lộ password field.

Giải pháp: dùng skip để bỏ skip các field không mong muốn <https://serde.rs/attr-skip-serializing.html>


### Kết luận

Không phải cứ dùng Rust là sẽ an toàn, hãy dùng biện pháp an toàn khi cần thiết.

Hết.

HVN at <https://pymi.vn> and <https://www.familug.org>.

[Ủng hộ tác giả 🍺](https://www.familug.org/p/ung-ho.html)
