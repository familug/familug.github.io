Title: [Go] any chứa được int nhưng []any không chứa được []int
Date: 2023-05-15
Category: frontpage
Tags: go, golang, pitfall, any, interface

Theo [go tour](https://go.dev/tour/methods/9)
> An interface type is defined as a set of method signatures.
> A value of interface type can hold any value that implements those methods.

Một kiểu interface định nghĩa một bộ các method.
Một giá trị kiểu interface có thể chứa bất kỳ giá trị nào có đủ các method trong interface.

> The interface type that specifies zero methods is known as the empty interface:
> An empty interface may hold values of any type. (Every type implements at least zero methods.)

Một kiểu  interface không chỉ định method nào được gọi là **empty interface**: `interface{}`
Một empty interface có thể chứa giá trị của bất kỳ kiểu nào.

### `any` trong Go là gì
Từ Go phiên bản 1.18 giới thiệu cách viết khác cho `interface{}` là: `any`.

<center>
![any](https://images.unsplash.com/photo-1499334758287-dc8133b315e9?ixlib=rb-4.0.3&q=85&fm=jpg&crop=entropy&cs=srgb&dl=andrew-wulf-59yg_LpcvzQ-unsplash.jpg&w=640)
Photo by <a href="https://unsplash.com/@andreuuuw?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText">Andrew Wulf</a> on <a href="https://unsplash.com/photos/59yg_LpcvzQ?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText">Unsplash</a>
</center>

### function nhận `any`, nhận mọi giá trị

```go
package main

import "fmt"

func doThing(x any) {
	fmt.Print(x)
}

func main() {
	n := 5
	doThing(n)

	s := "hello"
	doThing(s)
}
```

function `doThing` nhận đầu vào kiểu `any`, và nó có thể gọi với mọi giá trị, `n` kiểu `int`, hay `s` kiểu `string`.

Ai viết function nhận vào kiểu `any`? `fmt.Print` là 1 ví dụ.
```go
func Println(a ...any) (n int, err error)
```

### function nhận `[]any` không nhận `[]int`
Dễ suy luận rằng 1 slice của int là `[]int`, thì 1 function nhận `[]any` sẽ nhận `[]int`?
Không! Code sau đây compile với error:

```go
package main

import "fmt"

func doManyThing(xs []any) {
	for _, x := range xs {
		fmt.Printf("%s\n", x)
	}
}

func main() {
	xs := []int{1, 2, 3}
	doManyThing(xs)
}
```

```
./any.go:19:14: cannot use xs (variable of type []int) as []any value in argument to doManyThing
```

Muốn dùng `xs` làm đầu vào cho `doManyThing`, phải convert nó thành `[]any` bằng 1 vòng lặp for:

```
xs := []int{1, 2, 3}
anyxs := make([]interface{}, len(xs))
for i, v := range xs {
    anyxs[i] = v
}

doManyThing(anyxs)
```

Bất ngờ chưa? đây cũng là 1 câu hỏi trong FAQ của Go, tất nhiên, vì có nhiều người hỏi quá: <https://go.dev/doc/faq#convert_slice_of_interface>

```
Q: Can I convert a []T to an []interface{}?

A: Not directly. It is disallowed by the language specification because the two
types do not have the same representation in memory. It is necessary to copy
the elements individually to the destination slice. `
```

Cơ mà... `any` thì lại chứa được `[]int`.

### Kết luận
Go thật bất ngờ.

Hết.

HVN at <http://pymi.vn> and <https://www.familug.org>.

[Ủng hộ tác giả 🍺](https://www.familug.org/p/ung-ho.html)

