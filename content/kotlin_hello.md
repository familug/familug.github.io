Title: Hello Kotlin 2024
Date: 2024-07-13
Category: frontpage
Tags: kotlin, JVM, java, CLI, programming

## Kotlin là gì

![kotlin](https://kotlinlang.org/docs/images/kotlin-logo.png)
```
$ apt-cache show kotlin
Package: kotlin
Architecture: all
Version: 1.3.31+~1.0.1+~0.11.12-2
...
Installed-Size: 286240
...
Homepage: https://kotlinlang.org
Description-en: cross-platform, general-purpose programming languagehttps://kotlinlang.org/
 Kotlin is a cross-platform, statically typed, general-purpose programming
 language with type inference. Kotlin is designed to interoperate fully with
 Java, and the JVM version of its standard library  depends on the Java Class
 Library, but type inference allows its syntax to be more concise.
```

Kotlin <https://kotlinlang.org/> là một ngôn ngữ lập trình hiện đại (2011) phát triển bởi JetBrain (IDE: PyCharm, IntelliJ IDEA), chạy trên máy ảo JVM (của Java), tương thích với Java (dùng được thư viện Java), cú pháp ngắn gọn, hỗ trợ functional programming, được Google hỗ trợ là ngôn ngữ chính thức để viết app Android.

### Cài đặt

```
$ sudo apt install -y kotlin
...
Setting up kotlin (1.3.31+~1.0.1+~0.11.12-2) ...
```

### Viết hello world
Viết code vào file main.kt:

```kt
fun main() {
    println("Hello FAMILUG 2024!")
}
```

Build source code thành file MainKt.class

```
$ kotlinc main.kt
$ kotlin MainKt
Hello FAMILUG 2024!
$ find .
.
./META-INF
./META-INF/main.kotlin_module
./MainKt.class
./main.kt

$ file MainKt.class
MainKt.class: compiled Java class data, version 50.0 (Java 1.6)

$ xxd MainKt.class| head -n3
00000000: cafe babe 0000 0032 002b 0100 064d 6169  .......2.+...Mai
00000010: 6e4b 7407 0001 0100 106a 6176 612f 6c61  nKt......java/la
00000020: 6e67 2f4f 626a 6563 7407 0003 0100 046d  ng/Object......m
```

8 bytes đầu đáng yêu của file .class: "cafe babe".

Chạy file MainKt

```
$ /usr/bin/time -v kotlin MainKt
Hello FAMILUG 2024!
	Command being timed: "kotlin MainKt"
	User time (seconds): 0.08
	System time (seconds): 0.02
	Percent of CPU this job got: 116%
	Elapsed (wall clock) time (h:mm:ss or m:ss): 0:00.10
	Average shared text size (kbytes): 0https://github.com/JetBrains/kotlin/releases/tag/v1.3.31
	Average unshared data size (kbytes): 0
	Average stack size (kbytes): 0
	Average total size (kbytes): 0
	Maximum resident set size (kbytes): 37888
	Average resident set size (kbytes): 0
	Major (requiring I/O) page faults: 0
	Minor (reclaiming a frame) page faults: 5296
	Voluntary context switches: 282
	Involuntary context switches: 13
	Swaps: 0
	File system inputs: 0
	File system outputs: 64
	Socket messages sent: 0
	Socket messages received: 0
	Signals delivered: 0
	Page size (bytes): 4096
	Exit status: 0
```

Dùng tới ~37 MiB, gấp 4 lần RAM so với Python, nhưng không sao, năm 2024 thì 40MB RAM không là gì so với Google Chrome hay các IDE cả.

```
$ /usr/bin/time -v /usr/bin/python3.11 -c 'print("Hello FAMILUG!")' |& grep Maximum
	Maximum resident set size (kbytes): 8960
```

## Viết vài chương trình đơn giản

### Viết function tinh tổng 3 số

```kt
fun sum3(a: Int, b: Int, c: Int): Int {
    return a + b + c
}

fun main() {
    println("Hello FAMILUG 2024!")
    val sum = sum3(1,2,3)
    println("Tong cua 1+2+3 la ${sum}")
}
```
Kết quả:
```
$ kotlinc main.kt
$ kotlin MainKt
Hello FAMILUG 2024!
Tong cua 1+2+3 la 6
```

Không khác mấy code Python3
```py
def sum3(a: int, b: int, c: int) -> int:
    return a + b +c

def main():
    print("Hello FAMILUG 2024!")
    sum = sum3(1,2,3)
    print(f"Tong cua 1+2+3 la {sum}")

main()
```

### Giải bài ProjectEuler 1 - tổng các số nhỏ hơn 1000 chia hết cho 3 hoặc 5


```kt
# main.kt
fun pe01(): Int {
    var sum = 0
    for (i in 1..999) {
        if (i % 3 == 0 || i % 5 == 0) {
            sum += i
        }
    }
    return sum
}

fun pe01_functional(): Int {
    return (1..999)
        .filter({it -> it % 3 == 0 || it % 5 == 0}) // hoặc ngắn hơn: .filter({ it % 3 == 0 || it % 5 == 0 })
        .sum()
}


fun main() {
    println(pe01())
    println(pe01() == pe01_functional())
}

```
Kết quả

```
$ kotlinc main.kt
hvn@mini:kotlinplay $ kotlin MainKt
233168
true
```

### Giải bài ProjectEuler 16 - tổng các chữ số của 2 mũ 1000

```kt
# main.kt
import java.math.BigInteger

fun pe16(): Int {
    val p: BigInteger = 2.toBigInteger().pow(1000)
    return p.toString()
            .chars()
            .map({ it - '0'.toInt() })
            .sum()
}

fun main() {
    println("tong cac chu so cua 2**1000 la ${pe16()}".toUpperCase()) // 1366
}
```
Kết quả

```
$ kotlinc main.kt
$ kotlin MainKt
TONG CAC CHU SO CUA 2**1000 LA 1366
```

String functions: <https://kotlinlang.org/api/latest/jvm/stdlib/kotlin/-string/>
Char functions: <https://kotlinlang.org/api/latest/jvm/stdlib/kotlin/-char/>

### Đọc file /etc/passwd và tìm max uid trong các user

```kt
import java.io.File
import java.io.InputStream

fun main() {
    val inputStream: InputStream = File("/etc/passwd").inputStream()
    val lineList = mutableListOf<Int>()

    inputStream.bufferedReader().forEachLine(
        { it -> lineList.add(it.split(":")[2].toInt()) }
    )
    println(lineList.max())
}
```

Kết quả
```
$ kotlinc main.kt
$ kotlin MainKt
65534
```

## Tham khảo
Kotlin tour: <https://kotlinlang.org/docs/kotlin-tour-hello-world.html>

## Tổng kết
Bài này giới thiệu Kotlin và viết các chương trình đơn giản, sử dụng các thư viện standard/thư viện có sẵn của Java, đồng thời dùng bản Kotlin có sẵn trên Ubuntu 22.04 đã khá cũ (1.3.31 từ [2019](https://github.com/JetBrains/kotlin/releases/tag/v1.3.31)) bản hiện tại đã là Kotlin 2.0, build và chạy code trực tiếp với kotlinc trên câu lệnh CLI mà không dùng IDE hay build tool.

Bài viết sau sẽ giới thiệu build tool, sử dụng kotlin bản mới nhất và các thư viện tải từ trên mạng.

## Kết luận
Kotlin ngắn gọn, hiện đại, viết được app di động lẫn code backend/frontend.
Ngon không thể bỏ phi.

Hết.

HVN at <http://pymi.vn> and <https://www.familug.org>.

[Ủng hộ tác giả 🍺](https://www.familug.org/p/ung-ho.html)
