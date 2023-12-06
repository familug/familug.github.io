Title: 24 ngày học Rust - ngày 2 set
Date: 2023-12-06
Category: frontpage
Tags: rust, adventofcode

Kiểu set chỉ chứa mỗi phần tử 1 lần duy nhất, loại bỏ các phần tử trùng lặp. Ví dụ sau chỉ thấy có 1 số `1`.

## HashSet - kiểu dữ liệu set
Rust có sẵn kiểu set có tên HashSet, cần phải import từ thư viện "collections"

```rs
use std::collections::HashSet;
pub fn main() {
    let mut s = HashSet::new();
    s.insert(1);
    s.insert(2);
    s.insert(3);
    s.insert(1);
    dbg!(&s);
}

//[src/main.rs:8] &s = {
//    2,
//    1,
//    3,
//}
```

Kiểu set không có thứ tự của các phần tử, kết quả print có thể khác ví dụ trên và khác ở mỗi lần chạy code.

## Tạo set từ vector, iterator

```rs
let cs = "abcddcba".chars();
let s1: HashSet<char> = HashSet::from_iter(cs);
dbg!(s1);

// s1 = {
//    'd',
//    'a',
//    'c',
//    'b',
//}

let v = vec![1, 2, 3, 1];
let s2: HashSet<i64> = HashSet::from_iter(v);
dbg!(s2);

// s2 = {
//    3,
//    1,
//    2,
//}
```

### HashSet có đủ mọi method cho set
Như Python, Rust HashSet có đủ các method

- union (Python |)
- difference (Python -)
- contains (Python >)
- intersection (Python &)
- symmetric_difference (Python ^)

```rs
let s2: HashSet<i64> = HashSet::from_iter(vec![1, 2, 3, 1]);
let s3: HashSet<i64> = HashSet::from_iter(vec![2, 3, 5]);

// pub fn symmetric_difference<'a>(&'a self, other: &'a HashSet<T, S>) -> SymmetricDifference<'a, T, S>
// s2.symmetric_difference(&s3) = [
//    1,
//    5,
//]
```

### Tạo vector từ HashSet

```rs
let v = Vec::from_iter(s3);
dbg!(&v);
// &v = [
//    5,
//    2,
//    3,
//]

```

## Kết luận
Rust tuy gõ type dài hơn một chút, nhưng vẫn có set tiện như Python.
Ngôn ngữ nào không có kiểu set builtin? Go!

[Ủng hộ tác giả 🍺](https://www.familug.org/p/ung-ho.html)
