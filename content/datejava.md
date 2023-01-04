Title: ElasticSearch/Java format thời gian không giống Python
Date: 2023-01-02
Category: frontpage
Tags: java, elasticsearch, ES, ELK, Python, datetime, Go

Hầu hết các ngôn ngữ lập trình đều có sẵn thư viện để format thời gian, vì dù cho mỗi người một nghề - người làm web, sysadmin, kẻ làm data, scientist nhưng đâu ai thoát khỏi được thời gian?

Cứ tưởng các ngôn ngữ lập trình format sẽ giống nhau, học 1 lần là dùng được mãi, ai ngờ!

![time](https://images.unsplash.com/photo-1501139083538-0139583c060f?ixlib=rb-4.0.3&dl=aron-visuals-BXOXnQ26B7o-unsplash.jpg&w=640&q=80&fm=jpg&crop=entropy&cs=tinysrgb)
Photo by <a href="https://unsplash.com/@aronvisuals?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText">Aron Visuals</a> on <a href="https://unsplash.com/photos/BXOXnQ26B7o?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText">Unsplash</a>

### Linux date, C, C++
Lấy làm mốc chuẩn, chương trình `date` trên UNIX/Linux dùng Ymd HMS cho ngày tháng năm giờ phút giây
```
$ date +"%Y/%m/%d %H:%M:%S"
2023/01/04 20:16:48
$ date --version
date (GNU coreutils) 8.30
Copyright (C) 2018 Free Software Foundation, Inc.
License GPLv3+: GNU GPL version 3 or later <https://gnu.org/licenses/gpl.html>.
This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.

Written by David MacKenzie.
```

Có vẻ như bắt nguồn từ function `strftime` trong `time.h` của C <https://en.cppreference.com/w/c/chrono/strftime>, dễ hiểu C++ và Python cũng kế thừa và phát huy từ đó. Xem ví dụ tại <https://strftime.org/>

```py
>>> import datetime
>>> datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
'2023/01/04 20:27:21'
```

### Java format time
Java (và thế nên [ElasticSearch](https://www.elastic.co/guide/en/elasticsearch/reference/8.5/mapping-date-format.html#built-in-date-formats) - 1 chương trình viết bằng Java), sử dụng format khác. Ở đây sẽ dùng `lein repl` để chạy code Clojure, gọi thư viện Java cho tiện (cài lein: sudo apt install lein).

```clj
$ lein repl                                                                                                                                            [0]
nREPL server started on port 32771 on host 127.0.0.1 - nrepl://127.0.0.1:32771
REPL-y 0.4.3, nREPL
Clojure 1.10.1
OpenJDK 64-Bit Server VM 11.0.17+8-post-Ubuntu-1ubuntu220.04
...
user=> (.format (java.text.SimpleDateFormat. "yyyy/MM/dd HH:mm:ss") (new java.util.Date))
"2023/01/04 20:33:12"
```

- Java   dùng y thường cho năm, M hoa cho tháng   , m thường cho phút, s thường cho giây.
- Python dùng Y hoa cho năm,    m thường cho tháng, M hoa    cho phút, S hoa    cho giây.

### Go lang - một mình một kiểu

Ra đời tận những năm 2000, Go quyết định format 1 mình 1 kiểu không giống ai trên đời:

```go
package main

import (
	"fmt"
	"time"
)

func main() {
	t := time.Now()
	fmt.Printf("%s\n", t.Format("2006/01/02 15:04:05"))
}
```

<https://pkg.go.dev/time#pkg-constants>


### Kết luận
Vì đúng sai chỉ là do góc nhìn, nên các công nhân phải chịu làm dâu trăm họ để có tiền mua cơm.

Hết.

HVN at <https://pymi.vn> and <https://www.familug.org>.

[Ủng hộ tác giả 🍺](https://www.familug.org/p/ung-ho.html)
