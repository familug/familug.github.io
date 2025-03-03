Title: [TIL] Go http server không set status header sau khi write
Date: 2025/03/04
Category: frontpage
Tags: til, go, http, header
Slug: go_header

Cộng đồng Go ưa chuộng cách làm web không dùng framework, chủ yếu chỉ dùng stdlib như net/http.
Uư điểm này giúp web app Go bớt đi nhiều dependency, bù lại, nhiều thứ phải tự làm/low level.

Ví dụ sau đúng cho cả gorilla/mux lẫn net/http:

```go
package main

import (
	"fmt"
	"html"
	"log"
	"net/http"
)

func main() {

	http.HandleFunc("/bar", func(w http.ResponseWriter, r *http.Request) {
		fmt.Fprintf(w, "Hello, %q", html.EscapeString(r.URL.Path))

		http.Error(w, http.StatusText(http.StatusBadRequest), http.StatusBadRequest)
	})

	log.Fatal(http.ListenAndServe(":8080", nil))
}
```

Output khi truy cập `/bar`:

```
  2025/03/04 06:57:11 http: superfluous response.WriteHeader call from main.main.func1 (main.go:15)
````

Do dòng trên đã viết "Hello" vào response, nó đã tự set HTTP status code 200.
Dòng http.Error set status code 400 nhưng không có tác dụng gì.
Trong go doc [ResponseWriter viết](https://pkg.go.dev/net/http#ResponseWriter):

```
// WriteHeader sends an HTTP response header with the provided
// status code.
//
// If WriteHeader is not called explicitly, the first call to Write
// will trigger an implicit WriteHeader(http.StatusOK).
// Thus explicit calls to WriteHeader are mainly used to
// send error codes or 1xx informational responses.
//
// The provided code must be a valid HTTP 1xx-5xx status code.
// Any number of 1xx headers may be written, followed by at most
// one 2xx-5xx header. 1xx headers are sent immediately, but 2xx-5xx
// headers may be buffered. Use the Flusher interface to send
// buffered data. The header map is cleared when 2xx-5xx headers are
// sent, but not with 1xx headers.
//
// The server will automatically send a 100 (Continue) header
// on the first read from the request body if the request has
// an "Expect: 100-continue" header.
```

hay trong Gorilla/mux viết:

> Middlewares should write to ResponseWriter if they are going to terminate the request, and they should not write to ResponseWriter if they are not going to terminate it.
[source](https://github.com/gorilla/mux/tree/v1.8.1?tab=readme-ov-file#middleware)


### Kết luận
Happy bug fixing.


Hết.

HVN at <https://pymi.vn> and <https://www.familug.org>.

[Ủng hộ tác giả 🍺](https://www.familug.org/p/ung-ho.html)
