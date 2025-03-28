Title: Rust tuple, array, slice và compile time size 
Date: 2025/03/27
Category: frontpage
Tags: a,b,c
Slug: rust_array

Hay làm thế nào để "stack overflow" trong Rust.

Tuple và array là 2 kiểu dữ liệu [*primitive*](https://doc.rust-lang.org/std/#primitives) [**compound**](https://github.com/rust-lang/book/blob/45f05367360f033f89235eacbbb54e8d73ce6b70/src/ch03-02-data-types.md?plain=1#L202) trong Rust.

> Compound types can group multiple values into one type.
Compound type có thể gộp nhiều giá trị vào 1 kiểu.

Xem code online và làm theo tại [playground](https://play.rust-lang.org/?version=stable&mode=debug&edition=2024&gist=1bcfb8548e81190f625e424dfd999e06).

### Tuple 
Tuple là 1 cách để gộp nhiều giá trị có kiểu khác nhau vào 1 kiểu compound (kiểu gộp?).
Các phần tử của tuple nằm trong cặp `()`, phân cách nhau bằng dấu phẩy `,`.
Tuple hỗ trợ phép *destructuring*, để tách 1 tuple thành nhiều phần (tương tự Python unpacking). 
Truy cập từng phần tử theo thứ tự bằng cú pháp `T.0 T.1 T.2`...

```rs
fn main() {
    let tup = ("Pika", 42); // type (&str, i32)
    let (name, number) = tup;
    println!("Name: {name}: number {number}");
    println!("Name: {}", tup.0);
}
// Name: Pika: number 42
// Name: Pika
```
Tuple không chứa phần tử nào gọi là 1 unit `()`. Các biểu thức không trả về gì sẽ tự động return unit `()`.

### Array
> An array is a fixed-size sequence of N elements of type T. The array type is written as [T; N].
Array là một cách khác đểu gộp nhiều giá trị **cùng kiểu** thành 1 kiểu. Kiểu của array ký hiệu `[T; N]` với T là kiểu của phần tử, và N là số phần tử.
Cú pháp sử dụng dấu `;` ở đây rất lạ mắt, vì dấu `;` vốn thưởng chỉ dùng để kết thúc 1 biểu thức (thường thấy cuối mỗi dòng).
Đồng thời, dấu `;` cũng dùng trong cú pháp để tạo array chứa N lần 1 giá trị (ở ví dụ sau là 6 lần số 3)
```rs
fn main() {
    let a1: [i32; 5] = [2,3,5,8,13];
    let a2 = [3;6];
    println!("a1: {a1:?}");
    println!("a2: {a2:?}");
    println!("a2 first: {}", a2[0]);      
}
// a1: [2, 3, 5, 8, 13]
// a2: [3, 3, 3, 3, 3, 3]
// a2 first: 3
```
Rust compiler có thể phát hiện các trường hợp out of bounds (OOB) đơn giản khi sử dụng index là các số / phép toán đơn giản + - * /
Compile output
```rs
    error: this operation will panic at runtime
  --> main.rs:12:29
   |
12 |     println!("a1 some: {}", a1[4+2-1]);
   |                             ^^^^^^^^^ index out of bounds: the length is 5 but the index is 5
```
nhưng không thể phát hiện khi index là các phép tính phức tạp như lũy thừa, hay gọi function, chương trình sẽ panic (runtime error) và tắt.

```rs
    // như trên 
    println!("a2 some: {}", a2[4usize.pow(2)]);                                                               
```
Run output
```rs
$ RUST_BACKTRACE=1 ./main
...
thread 'main' panicked at main.rs:13:29:
index out of bounds: the len is 6 but the index is 16
stack backtrace:
   0: rust_begin_unwind
             at /rustc/eeb90cda1969383f56a2637cbd3037bdf598841c/library/std/src/panicking.rs:665:5
   1: core::panicking::panic_fmt
             at /rustc/eeb90cda1969383f56a2637cbd3037bdf598841c/library/core/src/panicking.rs:74:14
   2: core::panicking::panic_bounds_check
             at /rustc/eeb90cda1969383f56a2637cbd3037bdf598841c/library/core/src/panicking.rs:276:5
   3: main::main
```

Để lấy 1 tập con của array, thử dùng cú pháp :

```rs
14 |     a1[2..4];
   |     ^^^^^^^^ the size of `[i32]` cannot be statically determined
```
Thấy có `[i32]` *gần giống*  như kiểu của array, nhưng không có số lượng phần tử. Vì vậy kích thước của a1[2..4] không thể biết được khi compile, nên không compile được.
Có thể cho rằng Rust dễ dàng tính toán được số phần tử là 4-2 = 2, nhưng việc tính toán này không khả thi nếu các số này là `a..b` với giá trị được tính toán sử dụng các phép toán phức tạp, vậy nên tốt nhất là không compile.

### Stack
tuple và array là 2 kiểu **primitive** và chúng được chứa trong stack của chương trình nên cần có kích thước (size) cố định, không đổi, biết lúc compile (statically determined).
Các kiểu khác như vector, map, set được chứa trên heap nên có kích thước tùy ý, thay đổi được lúc chạy (runtime).
#### Stack overflow in Rust
Stack của chương trình trên Linux có kích thước mặc định là:
```
$ ulimit --stack-size
8192
```
8192KB hay 8MB. 

```rs
let aso = [1i64;1024*1000];  // OK
```
Một giá trị kiểu i64 có kích thước là 64bits == 8 bytes, tạo 1 array với 1048576 (1024*1024) phần tử sẽ dẫn tới stack overflow:
```rs
16 |     let aso = [1i64;1024*1024];
   |
thread 'main' has overflowed its stack
fatal runtime error: stack overflow
```


### Slice
> Slices let you reference a contiguous sequence of elements in a collection rather than the whole collection. A slice is a kind of reference, so it does not have ownership.

Slice refer (trỏ - tương tự pointer/con trỏ) tới 1 chuỗi các phần tử trong 1 tập hợp hay vì cả tập hợp. Nó chứa:

- địa chỉ của phần tử đầu tiên (trên máy 64bit có kích thước là 64bits == 8bytes)
- kích thước của slice (kiểu usize, trên máy 64bit có kích thước là 64bits == 8bytes)

nên kiểu slice có kích thước biết khi compile.

> In Rust, a slice on a 64-bit system typically has a size of 16 bytes

Trên máy 64-bit, 1 slice có kích thước 16 bytes.

Cú pháp: `&a1[2..4]`, kiểu `&[i32]`

```rs
    let s: &[i32] = &a1[2..4];
    println!("{:?}", s);
    // [5, 8]
```

### Kết luận
- Tuple để chứa các giá trị khác loại/kiểu, truy cập bằng `T.index`.
- Array có kiểu `[T;N]` với dấu `;` kì lạ, chỉ hỗ trợ check OOB đơn giản và hoàn toàn có thể bị Stack Overflow.
- Slice luôn biết trước size vì chỉ chứa 2 thông tin.

### Tham khảo 
<https://github.com/rust-lang/book/blob/async-2024/src/ch03-02-data-types.md>

Hết.

HVN at <https://pymi.vn> and <https://www.familug.org>.

[Ủng hộ tác giả 🍺](https://www.familug.org/p/ung-ho.html)
