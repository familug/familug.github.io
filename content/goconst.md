Title: [Go] Đôi khi 0.1 + 0.1 + 0.1 == 0.3
Date: 2023-01-31
Category: frontpage
Tags: go, golang, bashgodaily, pitfall, const, float

Trong cuộc sống, những thứ đúng là đúng, sai là sai thật dễ dàng, còn những thứ đôi khi thế này, đôi khi thế nọ, thì tùy.

Như các học viên của <https://pymi.vn> đều biết [vì sao 0.1 + 0.1 + 0.1 != 0.3](https://pymi.vn/blog/why-not-float/) trong Python và hầu hết các ngôn ngữ khác, thì với Go, thực hiện 1 phép tính cộng đơn giản theo 2 cách khác nhau, cho ra 2 kết quả khác nhau.

![go nowhere const]({static}/images/go_nowhere.webp)

### Cách giống các ngôn ngữ khác

```go
func main() {
	x := 0.1
	fmt.Printf("%v + %v + %v == 0.3? %t\n", x, x, x, x+x+x == 0.3)
	fmt.Printf("%f\n", x+x+x)
	fmt.Printf("%.17f\n", x+x+x)
}

```

Kết quả giống như Python và các ngôn ngữ khác, 0.1 + 0.1 + 0.1 != 0.3 do kết quả vế trái là `0.30000000000000004`

```
0.1 + 0.1 + 0.1 == 0.3? false
0.300000
0.30000000000000004
```

<https://go.dev/play/p/eDe3szlFyi7>

### Cách của riêng Go
Nếu viết khác đi một chút, sử dụng từ khóa `const`, hay viết trực tiếp mà không gán cho biến `x`, kết quả lại là đúng:


```go
func main() {
	const x = 0.1
	fmt.Printf("%v + %v + %v == 0.3? %t\n", x, x, x, x+x+x == 0.3)

	fmt.Printf("%v + %v + %v == 0.3? %t\n", 0.1, 0.1, 0.1, 0.1+0.1+0.1 == 0.3)
	fmt.Printf("%.30f\n", 0.1+0.1+0.1)
	fmt.Printf("%.30f\n", 0.3)
}
```

Kết quả:

```
0.1 + 0.1 + 0.1 == 0.3? true
0.1 + 0.1 + 0.1 == 0.3? true
0.299999999999999988897769753748
0.299999999999999988897769753748
```

<https://go.dev/play/p/IPuQD9aLlV8>

Vậy rốt cuộc là sao?

#### Go const
Từ khóa `const` trong Go khác với trong các ngôn ngữ khác, không phải mỗi chuyện nó immutable (không thay đổi), mà cách tính toán giá trị cũng không như "thường".

Cách viết `0.1+0.1+0.1` cũng là const trong Go, gọi chính xác là `const expression`.

Sự khác biệt to lớn này khiến các tác giả Go phải viết một bài blog để giải thích `const` khác các ngôn ngữ thế nào <https://go.dev/blog/constants>.

Trích blog nói trên:

> First, a quick definition. In Go, const is a keyword introducing a name for a scalar value such as 2 or 3.14159 or "scrumptious". Such values, named or otherwise, are called constants in Go. Constants can also be created by expressions built from constants, such as 2+3 or 2+3i or math.Pi/2 or ("go"+"pher").

Khi viết 0.1 trong Go, giá trị này **không có kiểu** (have no type), hay còn gọi là `untyped constant`. Nhưng nó có **kiểu mặc định** (default type) KHI CẦN. Hoặc cũng có thể đổi sang một kiểu khác. Trong Go có 2 kiểu float là float32 và float64.

```go
	const x = 0.1
	fmt.Printf("%T\n", x) // float64
	var y float32 = 0.2
	fmt.Printf("%T\n", x+y) // float32
	z := 0.1
	fmt.Printf("%T\n", z+y) // Compile error: invalid operation: z + y (mismatched types float64 and float32)

```

`x` có default type là `float64`, khi cộng với giá trị `y` kiểu `float32`, `x` lúc này có kiểu `float32` mà không cần phải đổi kiểu.

- Chú ý, `const x = 0.1` (untyped) khác với `z := 0.1` (biến z kiểu float64).
- Chú ý, `const x float32 = 0.1` đã có kiểu float32, khác với untyped const.

#### Tính toán const expression
Trong bài blog:

> Numeric constants live in an arbitrary-precision numeric space; they are just regular numbers.

```go
    const Huge = 1e1000
    fmt.Println(Huge / 1e999)
```
in ra 10.

Các const được tính toán bởi Go compiler - khi build, chứ không tính KHI CHẠY, sử dụng kiểu dữ liệu có độ chính xác cao hơn so với float64

Trong Go spec <https://go.dev/ref/spec#Constants>

> Numeric constants represent exact values of arbitrary precision and do not overflow.

```
>  Implementation restriction: Although numeric constants have arbitrary precision in the language, a compiler may implement them using an internal representation with limited precision. That said, every implementation must:

    Represent integer constants with at least 256 bits.
    Represent floating-point constants, including the parts of a complex constant, with a mantissa of at least 256 bits and a signed binary exponent of at least 16 bits.
    ```

Vậy khi tính toán 0.1+0.1+0.1 với 256 bits (so với float64 chỉ có 64 bit), độ chính xác cao hơn 4 lần, kết quả cho 0.1+0.1+0.1 bằng với giá trị biểu diễn 0.3 (xem ở trên, vẫn không bằng 0.3 về mặt tóan học).

### Kết luận
Kiểu float64 trong Go vẫn tuân theo [IEEE754](https://en.wikipedia.org/wiki/IEEE_754), nên kết luận về kiểu float vẫn giống như Python. Điều khác biệt chỉ là một số trường hợp nhỏ xảy ra khi sử dụng const.

Go thật đơn giản, ha!

Hết.

HVN at <http://pymi.vn> and <https://www.familug.org>.

[Ủng hộ tác giả 🍺](https://www.familug.org/p/ung-ho.html)


Đáp án: t.names = append(t.names, "python") sẽ gán giá trị mới cho t.names, do dùng value receiver nên không thấy thay đổi gì.
Nếu thay đổi phần tử của slice, ví dụ t.names[0] = "Python" thì kết quả có thay đổi.
Tương tự, nếu viết t.ages = map[string]int{} sẽ thấy map ages không thay đổi. Xem code tại <https://go.dev/play/p/yCn-mKVpPSo>

