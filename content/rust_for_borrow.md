Title: 24 ngày học Rust - ngày 11 for loop borrow
Date: 2023-12-11
Category: frontpage
Tags: rust, adventofcode, for, borrow

## for sẽ move value
Khi lặp qua từng phần tử của v với `for i in v`, v bị move ownership cho vòng for loop, nên ở lần lặp thứ 2 không còn v nữa, Rust compiler báo lỗi. Thấy thêm rằng khi người dùng viết `for i in v` thì code thực sự được chạy là `for i in v.into_iter()`
```rs
fn main() {

    let v = vec![10,20,30,40];
    for i in v {
        println!("{}", i);
    }
    for i in v {
        println!("{}", i);
    }

}
```
Output
```rs
error[E0382]: use of moved value: `v`
 --> src/main.rs:6:14
  |
2 |     let v = vec![10,20,30,40];
  |         - move occurs because `v` has type `Vec<i32>`, which does not implement the `Copy` trait
3 |     for i in v {
  |              - `v` moved due to this implicit call to `.into_iter()`
...
6 |     for i in v {
  |              ^ value used here after move
  |
note: `into_iter` takes ownership of the receiver `self`, which moves `v`
 --> /rustc/84c898d65adf2f39a5a98507f1fe0ce10a2b8dbc/library/core/src/iter/traits/collect.rs:262:18
help: consider iterating over a slice of the `Vec<i32>`'s content to avoid moving into the `for` loop
  |
3 |     for i in &v {
  |              +
```

Fix: để có thể lặp qua v 2 lần, borrow v khi dùng với for:

```rs
    let v = vec![10,20,30,40];
    let mut v2: Vec<i32> = vec![];
    for i in &v {
        v2.push(i);
    }
    for i in &v {
        v2.push(i);
    }
```

Lần này compiler lại báo lỗi, nhưng không phải do v nữa mà ở i:

```rs
 --> src/main.rs:8:17
  |
8 |         v2.push(i);
  |            ---- ^ expected `i32`, found `&{integer}`
  |            |
  |            arguments to this method are incorrect
  |
note: method defined here
 --> /rustc/84c898d65adf2f39a5a98507f1fe0ce10a2b8dbc/library/alloc/src/vec/mod.rs:1836:12
help: consider dereferencing the borrow
  |
8 |         v2.push(*i);
```

khi borrow v thì i cũng là borrow, để thêm i vào vector v2 type Vec<i32>, phải dereferencing i:

```
  v2.push(*i);
```

Trông sẽ không được đẹp mắt, ví dụ khi thêm 1 tuple vào v3:

```rs
    let v = vec![10,20,30,40];
    let mut v3: Vec<(i32, i32)> = vec![];
    for i in &v {
        v3.push((*i, *i));
    }
```

Có thể dereferencing i ngay tại vòng for:

```rs
    for &i in &v {
        v3.push((i, i));
    }
```

## Kết luận
for thực hiện move giá trị, borrow để dùng nhiều lần.

[Ủng hộ tác giả 🍺](https://www.familug.org/p/ung-ho.html)
