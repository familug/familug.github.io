Title: [TIL] Go map format/print có thứ tự
Date: 2025-03-24
Category: frontpage
Tags: go, golang, map, 
Slug: til_go_map_print_order

Kiểu dữ liệu `map` trong Go không có thứ tự khi duyệt qua:

> A map is an unordered group of elements of one type, called the element type, indexed by a set of unique keys of another type, called the key type. 
<https://go.dev/ref/spec#Map_types>

> When iterating over a map with a range loop, the iteration order is not specified and is not guaranteed to be the same from one iteration to the next. 
<https://go.dev/blog/maps#iteration-order>

```go
package main

func main() {
	m := map[string]string{
		"name":  "FAMILUG",
		"since": "2010",
		"loc":   "Vietnam",
	}

	for k, v := range m {
		println(k, v)
	}
  fmt.Printf("%v\n", m)      
```
Output
```
// lần 1
name FAMILUG
since 2010
loc Vietnam
map[loc:Vietnam name:FAMILUG since:2010]

// lần 2 
since 2010
loc Vietnam
name FAMILUG
map[loc:Vietnam name:FAMILUG since:2010]
```

Vậy `print(m)` kết quả liệu có khác nhau mỗi lần chạy? Từ [Go 1.12 (2018)](https://go.dev/doc/go1.12#fmtpkgfmt) thì không, output print(map) luôn cố định và được sắp xếp theo thứ tự key:

```
fmt¶

Maps are now printed in key-sorted order to ease testing. The ordering rules are:

    When applicable, nil compares low
    ints, floats, and strings order by <
    NaN compares less than non-NaN floats
    bool compares false before true
    Complex compares real, then imaginary
    Pointers compare by machine address
    Channel values compare by machine address
    Structs compare each field in turn
    Arrays compare each element in turn
    Interface values compare first by reflect.Type describing the concrete type and then by concrete value as described in the previous rules.

When printing maps, non-reflexive key values like NaN were previously displayed as <nil>. As of this release, the correct values are printed.
```

[See commit by Rob Pike](https://github.com/golang/go/commit/a440cc0d702e15c19bcc984f7a8f5c10f83726ab#diff-da2756b47399fcd2096dbc973b290baab35dc1d2074a4978671aa3dc90ad8337R757-R758)

### Kết luận

Output print hay format map type được sắp xếp theo key.

Hết.

HVN at <https://pymi.vn> and <https://www.familug.org>.

[Ủng hộ tác giả 🍺](https://www.familug.org/p/ung-ho.html)
