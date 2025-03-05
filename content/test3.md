Title: Luôn test ít nhất 3 case
Date: 2025/03/05
Category: frontpage
Tags: test, testing,
Slug: test3

Khi viết 1 tool hay viết code, một câu hỏi có thể nảy sinh là: test bao nhiêu trường hợp cho đủ?
Câu trả lời luôn nhận được là: càng nhiều càng tốt!

![a peace can]({static}/images/can.jpg)

Nhưng test ít nhất là bao nhiêu? 1 2 3 4? bài viết này xin đưa ra 1 con số kèm theo lý do: 3.

Giả sử đang viết 1 tool cli kiểm tra syntax của file yaml/json. Tạm gọi là `checker`. `checker` nhận vào argument là các file cần check.

### 3 case chụm lại nên hòn đá to
Tại sao lại là 3? vì 3 gồm những trường hợp sau:

- 0
- 1

0 và 1 phân biệt giữa không và có.

- 1
- 2 trở lên 

1 và 2 (trở lên) phân biệt giữa ít và nhiều. Tool hỗ trợ nhận 1 file đầu vào HẦU HẾT chưa chắc nhận 2 (vd: --config).

Ngoài ra, có thể thêm test case thứ 4 khi bài toán có số N là max thì hãy test N.

#### 0 - trường hợp luôn đặc biệt
`checker` nhận 0 đầu vào: chương trình sẽ làm gì? fail với yêu cầu phải có đầu vào? hay test tất cả các file trong thư mục hiện tại (thường chọn cách này)

#### 1 khác với nhiều 
Trong tiếng Anh, 1 bottle không có `s`, nhiều bottles thì có `s`. Khi test các file cần thử 2 file trở lên để tránh việc:

- `checker file1` : trường hợp 1 input, chạy ok
- `checker 'file1 file2'`: lẽ ra là 2 argument thì đây lại là 1 string. Cần sửa thành `checker file1 file2`.

#### 99 bottles of beer on the wall
Bài toán phổ biến trong lập trình: 99 chai bia trong két cũng cần test đủ với các trường hợp:

- nhiều chai
- chỉ còn 1 chai
- hết bia 

Xem đề và 1500 loại code ở <http://www.99-bottles-of-beer.net/lyrics.html>

### Kết luận
Dù viết code hay viết tool, luôn test tối thiểu 3 case mà nhiều hơn thì là 4:

- 0
- 1
- random.choice(2 -> N-1)
- N

Happy testing.

Hết.

HVN at <https://pymi.vn> and <https://www.familug.org>.

[Ủng hộ tác giả 🍺](https://www.familug.org/p/ung-ho.html)
