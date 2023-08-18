Title: [Go] nil không là duy nhất, cap(map) = ?
Date: 2023-08-18
Category: frontpage
Tags: go, golang, nil

Trong Python, `None` là giá trị duy nhất thể hiện sự "không có gì", sự "null", thì trong Go, nil lại là nhiều thứ khác nhau.

## Go nil có kiểu
Mỗi giá trị `nil` có kiểu cụ thể.

```go
package main

func main() {
	var s []int
	var m map[string]int

	println(s == nil)
	println(m == nil)
	// println(x == y) // Compile error: ./nil.go:9:15: invalid operation: s == m (mismatched types []int and map[string]int)
}
```
s và m đều bằng `nil`, nhưng không bằng nhau.

## nil map không phải là vô dụng
```go
var m map[string]int
```
Khi 1 map chưa được khởi tạo, nó có giá trị là `nil`.
Map là kiểu **reference**, như pointer hay slices. `nil` map vẫn đọc giá trị bình thường (giá trị là **zero** value của kiểu int tức 0):

```go
var m map[string]int
v := m["password"]
println(m)// 0x0
println(v)// 0
```

`nil` map không thêm được giá trị.

```go
var m map[string]int
m["age"] = 8
```
Panic với nội dung
```
panic: assignment to entry in nil map

goroutine 1 [running]:
main.main()
	/home/hvn/me/familug.github.io/content/nil.go:5 +0x2e

panic: assignment to entry in nil map
```

`nil` map giống như empty map khi read, nhưng khác khi write.

```go
var m map[string]int
fmt.Printf("nil: %v\n", m)
// nil: map[]

var e = map[string]int{}
fmt.Printf("empty: %v\n", e)
// empty: map[]
```
### cap(map) bằng mấy?
Các kiểu **reference** trong Go phải allocation để cấp phát bộ nhớ sử dụng `new` hoặc `make`. Dùng make để alloc map hay slice.

>  It creates slices, maps, and channels only, and it returns an initialized (not zeroed) value of type T (not *T). The reason for the distinction is that these three types represent, under the covers, references to data structures that must be initialized before use. A slice, for example, is a three-item descriptor containing a pointer to the data (inside an array), the length, and the capacity, and until those items are initialized, the slice is nil. For slices, maps, and channels, make initializes the internal data structure and prepares the value for use.
<https://go.dev/doc/effective_go#allocation_make>

Một slice chứa 3 thông tin: pointer tới array phía dưới, length và capacity.

> A slice is a descriptor of an array segment. It consists of a pointer to the array, the length of the segment, and its capacity (the maximum length of the segment).
<https://go.dev/blog/slices-intro>

```go
var nilSlice []int
fmt.Printf("%v len %d cap %d\n", nilSlice, len(nilSlice), cap(nilSlice))
// [] len 0 cap 0

var s = make([]int, 0)
fmt.Printf("%v len %d cap %d\n", s, len(s), cap(s))
// [] len 0 cap 0

var a = make([]int, 2, 10)
fmt.Printf("%v len %d cap %d\n", a, len(a), cap(a))
// [0 0] len 2 cap 10
```

Và dùng make với map:

```go
var m = make(map[string]int)
fmt.Printf("%v len %d cap ?\n", m, len(m))
```

cap(m) bằng mấy?

`fmt.Printf("%v len %d cap %d\n", m, len(m), cap(m))`
> ./nil.go:7:49: invalid argument: m (variable of type map[string]int) for cap

Không dùng được `cap` với map. Tại sao?  vì nó như thế và sẽ không thay đổi.

Sau 12+ năm dùng Go, tác giả Russ Cox đã đề xuất thêm cap(map), nhưng đã bị từ chối <https://github.com/golang/go/issues/52157>.

## Tham khảo
- <https://go.dev/blog/maps>

## Kết luận
Go thật đơn giản, và đầy bất ngờ.

Hết.

HVN at <http://pymi.vn> and <https://www.familug.org>.

[Ủng hộ tác giả 🍺](https://www.familug.org/p/ung-ho.html)
