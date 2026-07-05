Title: [clojure] update map với cond->
Date: 2025-03-12
Category: frontpage
Tags: clj, clojure, python
Slug: clj_cond_thread

Kiểu dữ liệu map trong clojure tương tự dict trong Python.
Do Clojure mọi kiểu dữ liệu đều là immutable, nên mọi thao tác với map đều trả về 1 map mới. 
Để update 1 map dựa theo điều kiện sẽ khá phức tạp cho đến khi dùng `cond->` macro.
Ví dụ code Python tương ứng

```py
options = {"max-keys": 100}

if 1 == 1:
    options["next-token"] = "abcd"
if 1 != 1:
    print("won't run")
if 5 > 3:
    options["other-op"] = "hehe"

def call_api(url, options):
    print(url, options)

call_api("https://url", options)
# https://url {'max-keys': 100, 'next-token': 'abcd', 'other-op': 'hehe'}
```

Macro `cond->` nhận vào các cặp điều kiện - function để chạy khi điều kiện đúng, sử dụng để update dict:

```clj
(def init-options {:max-keys 100})
(def options (cond->
                 options
               (= 1 1) (assoc :next-token "abcd")
               (not= 1 1) (prn "won't run")
               (> 5 3) (assoc :other-op "hehe")))

(defn call-api [url options]
  (println "calling " url "with options: " options))

(call-api "https://url" options)
;; calling  https://url with options:  {:max-keys 100, :next-token abcd, :other-op hehe}
```

Đầu vào đầu tiên của `cond->` là giá trị ban đầu `options`, theo sau là các cặp điều kiện:

nếu `(= 1 1)` thì gọi `(assoc optíons :next-token "abcd")` để thêm cặp key-value vào map options, kết quả này lại được gán tiếp làm đầu vào cho function (prn KETQUA "wont'run"), nhưng điều kiện (not= 1 1) là false nên function không được chạy, và tiếp tục...

Toàn bộ phần (cond-> ...) có thể đưa trực tiếp vào trong `(call-api )`:

```clj

(defn call-api [url options]
  (println "calling " url "with options: " options))

(call-api "https://url"
          (cond->
            {:max-keys 100}
            (= 1 1) (assoc :next-token "abcd")
            (not= 1 1) (prn "won't run")
            (> 5 3) (assoc :other-op "hehe")))
```

Code Python liệu có thể viết trong 1 dòng như vậy?

### Ứng dụng
Khi option được gọi sẽ thay đổi theo điều kiện, ví dụ gọi API khi cần paginate sang trang, dùng `cond->` để update options gọi trang tiếp theo.

```clj
(def next-page-token "XYZ")
(call-api "https://url"
          (cond-> 
            init-options 
            (some? next-page-token) (assoc :next-page-token next-page-token)))
```

### Source
Trong REPL

```clj
user=>
(source cond->)
(defmacro cond->
  "Takes an expression and a set of test/form pairs. Threads expr (via ->)
  through each form for which the corresponding test
  expression is true. Note that, unlike cond branching, cond-> threading does
  not short circuit after the first true test expression."
  {:added "1.5"}
  [expr & clauses]
  (assert (even? (count clauses)))
  (let [g (gensym)
        steps (map (fn [[test step]] `(if ~test (-> ~g ~step) ~g))
                   (partition 2 clauses))]
    `(let [~g ~expr
           ~@(interleave (repeat g) (butlast steps))]
       ~(if (empty? steps)
          g
          (last steps)))))
nil

```

### Kết luận
`cond->` macro giúp viết code update kiểu dữ liệu theo các điều kiện một cách sạch đẹp hơn.

Hết.

HVN at <https://pymi.vn> and <https://www.familug.org>.

[Ủng hộ tác giả 🍺](https://www.familug.org/p/ung-ho.html)
