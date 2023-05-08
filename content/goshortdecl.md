Title: [Go] := đôi khi không gán giá trị
Date: 2023-05-08
Category: frontpage
Tags: go, golang, bashgodaily, pitfall, short declaration, shadow

### Tạo variable (biến) trong Go
Go có 2 cách để khai báo và khởi tạo giá trị cho variable:

```go
var x int // declare
x = 42 // init
```

có thể viết gọn lại

```go
var x int = 42
```

Hoặc cú pháp ngắn "short declaration":

```go
x := 42
```

#### Short declaration rules
Short declaration `:=` ngắn hơn, được ưa chuộng, nhưng cũng kèm theo không ít chú
ý mà ít ai để ý.

```go
package main
import (
    "fmt"
    "os"
)
func main() {
    i, err := os.Open("/etc/passwd")
    i, err := os.Open("/etc/passwd")
    fmt.Printf("i %v err %v\n", i, err)
}
```
Code này không compile với error: `no new variables on left side of :=`, bên trái `:=`
luôn phải có variable mới. Code này compile ok:

```go
func main() {
    i, err := os.Open("/etc/passwd")
    f, err := os.Open("/etc/passwd")
    fmt.Printf("i %v f %v err %v\n", i, f, err)
}
```
ở đây có var `f` mới, còn var `err` cũ được gán cho giá trị mới. Bằng chứng `err` cũ có thể test:

```go
func main() {
	i, _ := os.Open("/etc/passwd")
	var err int = 42
	f, err := os.Open("/etc/passwd")
	fmt.Printf("i %v f %v err %v\n", i, f, err)
}
```
không compile với error: `cannot use os.Open("/etc/passwd") (value of type error) as int value in assignment`,
`err` cũ có kiểu `int`, nên không thể gán giá trị kiểu `error`.

Đoạn code sau [rất phổ biến trong lập trình web](https://github.com/Massad/gin-boilerplate/blob/5ad7e290e6dff18246af84227320034a5215f64a/db/db.go#L19-L32), tạo 1 global var DB client:

```go
var db *gorp.DbMap

//Init ...
func Init() {
	dbinfo := fmt.Sprintf("user=%s password=%s dbname=%s sslmode=disable", os.Getenv("DB_USER"), os.Getenv("DB_PASS"), os.Getenv("DB_NAME"))
	db, err := ConnectDB(dbinfo)
	if err != nil {
		log.Fatal(err)
	}
```

`err` là var mới, còn `db` là var mới hay var cũ được gán giá trị?

Theo những ví dụ trên, có thể mong chờ `db` là var cũ được gán cho giá trị.
Nhưng theo [effective go](https://go.dev/doc/effective_go#redeclaration):

> In a := declaration a variable v may appear even if it has already been declared, provided:
if v is already declared in an outer scope, the declaration will create a new variable.

`db` trong `Init` là var `db` mới, **shadow** (che mất) var `db` bên ngoài, `db` bên ngoài vẫn là `nil`.
Để fix bug này, không dùng `:=` mà viết:

```go
	var err error
	db, err = ConnectDB(dbinfo)
```

### Kết luận
Go vốn dài dòng, mà chỗ ngắn cũng toàn chú ý, **cộng đồng mạng** tạo hẳn 6 luật
để dùng `:=` <https://stackoverflow.com/questions/17891226/difference-between-and-operators-in-go/45654233#45654233>

Go thật đơn giản, ha!

Hết.

HVN at <http://pymi.vn> and <https://www.familug.org>.

[Ủng hộ tác giả 🍺](https://www.familug.org/p/ung-ho.html)
