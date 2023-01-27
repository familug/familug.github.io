Title: Go value receiver method vẫn thay đổi được giá trị?!
Date: 2023-01-27
Category: frontpage
Tags: go, golang, bashgodaily, pitfall, map,

Bài viết đầu tiên của nhiều bài viết sẽ bán than về "Go" - ngôn ngữ lập trình
non trẻ (since 2010) nhưng khá hot trên toàn cầu.

### Go is simple
Go thường được nhìn nhận là "đơn giản", không phủ nhận việc làm xong gotour <https://go.dev/tour/> khiến người học có thể bắt đầu viết code go, sau 1 tháng có thể tham gia code production (và viết bug).

Có hẳn cuốn sách giá cả triệu đồng bán rất chạy về những mistake khi dùng
ngôn ngữ đơn giản này [100 Go Mistakes and How to Avoid
Them](https://www.manning.com/books/100-go-mistakes-and-how-to-avoid-them).

Không dùng thì thôi, sao phải chê, thích chiến à?

Có một sự thật đi làm khá lâu mới nhận ra, rằng 99.99% **BẠN** không phải người quyết định công ty/dự án dùng cái gì. Những người/thứ quyết định sẽ là:

- công nghệ có sẵn của công ty
- công nghệ quen thuộc của team
- bên trên chỉ xuống (CTO/architect...)
- khách hàng yêu cầu

vậy nên thích hay không vẫn phải dùng. Mà dùng không sướng thì phê bình thôi.
![map bug]({static}/images/go_map_bug.webp)

### Go pointer receiver vs value receiver
Go receiver có 2 loại là pointer và value.

Trích từ Go tour <https://go.dev/tour/methods/4>

> Methods with pointer receivers can modify the value to which the receiver points (as Scale does here). Since methods often need to modify their receiver, pointer receivers are more common than value receivers.

và [Choosing a value or pointer receiver](https://go.dev/tour/methods/8)

> There are two reasons to use a pointer receiver.
> The first is so that the method can modify the value that its receiver points to.
> The second is to avoid copying the value on each method call. This can be more efficient if the receiver is a large struct, for example.

Theo hướng dẫn này, người học Go sẽ hiểu rằng khi viết

```go
func (t *type) name(args)
```

thì có thể thay đổi t

và

```go
func (t type) name(args)
```

thì không thể thay đổi t.

Ngoài ra, trong Go tour không còn chỗ nào ghi thêm gì nữa.

Thử ví dụ sau, đừng ôm đầu kêu đau:

```go
package main

import (
    "fmt"
)

type toy struct {
    names []string
    ages  map[string]int
}

func (t *toy) change() {
    t.names = append(t.names, "python")
    t.ages["python"] = 32
}
func (t toy) mayNotChange() {
    t.names = append(t.names, "python")
    t.ages["python"] = 32
}

func main() {
    t := toy{ages: map[string]int{"golang": 12}}
    fmt.Printf("%v\n", t)
    t.change()
    fmt.Printf("%v\n", t)
    t2 := toy{ages: map[string]int{"golang": 12}}
    fmt.Printf("%v\n", t2)
    t2.mayNotChange()
    fmt.Printf("%v\n", t2)
}
```

chạy online trên <https://go.dev/play/p/N781b6vT-GF>

Theo tài liệu Go tour, change nhận 1 pointer receiver nên sẽ thay đổi toy t và kết quả không có gì bất ngờ khi map giờ chứa thêm golang 12.

Nhưng trong mayNotChange, trong khi slice t.names không đổi thì map t.ages vẫn bị thay đổi dù cho đã dùng value receiver.

```go
{[] map[golang:12]}
{[python] map[golang:12 python:32]}
====================================
{[] map[golang:12]}
{[] map[golang:12 python:32]}
```

### Golang map là reference
Trong [Effective Go](https://go.dev/doc/effective_go#maps) có viết

> Like slices, maps hold references to an underlying data structure. If you pass a map to a function that changes the contents of the map, the changes will be visible in the caller.

map refers tới cấu trúc dữ liệu bên dưới, thay đổi map sẽ thay đổi cấu trúc dữ liệu đó, còn bản thân map là 1 reference, không thay đổi, đúng như value receiver cam kết.

Bài tập cho bạn đọc: slice cũng là reference, sao map thay đổi còn slice thì không khi dùng value receiver?

Thêm 1 ít tài liệu về 3 kiểu references: slice, map, channel <https://go.dev/doc/effective_go#allocation_make>

> Back to allocation. The built-in function make(T, args) serves a purpose different from new(T). It creates slices, maps, and channels only, and it returns an initialized (not zeroed) value of type T (not *T). The reason for the distinction is that these three types represent, under the covers, references to data structures that must be initialized before use.

### Kết luận
Golang map là kiểu reference, có thể thay đổi giá trị nó refer tới bên trong 1 value receiver method.

Go thật đơn giản, ha!

Hết.

HVN at http://pymi.vn and https://www.familug.org.

[Ủng hộ tác giả 🍺](https://www.familug.org/p/ung-ho.html)
