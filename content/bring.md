Title: Ta mang gì theo sau 1 công việc
Date: 2024-04-01
Category: frontpage
Tags: career, life, thought

Trong ngành IT, chuyện một người làm 1 công ty suốt cả sự nghiệp (~30-40 năm) gần như là không có.
Đa số làm một công việc nhiều thì 4 năm, còn nhìn chung thì 2, 3 năm là đã thay đổi.

Lý do thì không bàn tới, bởi bài viết này muốn hỏi xem "nếu chuyển việc, bạn mang theo những gì (từ công việc cũ)?"

Hãy thử dành 5 phút để tự trả lời, trước khi đọc tiếp.

![bring memory]({static}/images/bring.jpeg)

### Mang theo "kinh nghiệm"
Kinh nghiệm là thứ mơ hồ nhất mà bạn có thể mang theo, vậy thử hỏi, kinh nghiệm đó **CỤ THỂ** là những gì?

- kinh nghiệm không được đúc kết sau quá trình làm việc, không được ghi lại thành dạng văn bản: nên dù có định mang theo thì sau có khi lúc cần lại quên mất. Không có mấy người viết blog để ghi lại kinh nghiệm.
- kinh nghiệm rất phụ thuộc vào hoàn cảnh cụ thể, kinh nghiệm chỗ này **nhiều khi** không phù hợp với chỗ khác. Ví dụ: tôi có kinh nghiệm làm AWS cloud, mang sang công ty dùng Google Cloud rõ ràng là không dùng được nhiều.
- kinh nghiệm có hạn sử dụng, best practice 3 năm trước có thể không còn đúng với năm nay: kinh nghiệm code JQuery có thể không còn nhiều tác dụng khi code ReactJS, 3 năm trước JavaScript/Python không dùng type, còn giờ type ở mọi nơi. 10 năm trước các tool DevOps đều bằng Python, giờ đây đa phần là Go.
- kinh nghiệm không đơn giản là tính bằng "năm": 5 năm làm đi làm lại 1 việc không đổi và kinh nghiệm 5 năm làm nhiều việc khác nhau từ dễ đến khó.


### Mang theo (open source) code
Code là thứ tài sản gần như duy nhất của dân IT. Nếu bạn đã build thành công 1 hệ thống ở công ty A, nhiều khả năng người ta muốn bạn dựng 1 hệ thống tương tự ở công ty B. Nhưng nếu code không mang đi được có nghĩa là  phải làm hết tất cả lại từ đầu, có thể nhanh hơn, thay vì 3 năm, giờ còn 1.5 năm?!!!

Các công ty sẽ coi code như tài sản và có quy định sở hữu code đó vậy làm sao "mang đi được"?
Câu trả lời không hề đơn giản, và tất nhiên không phải là đi ... hack. 
Một điều khác cần chú ý, rằng không phải code nào cũng là bí mật công ty. Ví dụ một công ty làm về đặt xe thì code hệ thống logging hay monitoring hay tool quản lý cloud không phải là bí mật.

#### Open source là 1 giải pháp
Uber không public code hệ thống đặt xe của họ, nhưng rất nhiều các hệ thống khác được public tại [https://github.com/orgs/uber/repositories](https://github.com/orgs/uber/repositories).

Nếu làm ở Uber và làm dự án [https://github.com/uber/cadence](https://github.com/uber/cadence), khi sang một công ty khác, bạn tải cadence về và tiếp tục phát triển/ mở rộng. Không có gì mất đi, kinh nghiệm được bê nguyên đi và phát triển thêm!
Dù sao thì trường hợp này là lý tưởng hiếm hoi, bởi không phải công ty nào cũng có chương trình phát triển open source software như Uber, Facebook, Netflix...

Thế nhưng, bạn có thể phát triển 1 thư viện đủ "generic", dùng được cho nhiều trường hợp, có ích cho nhiều người, và là 1 người dùng của chính thư viện đó.
Các công ty có thể cấm mang code công ty public lên mạng, nhưng lại không có mấy công ty cấm "thêm 1 dependency 1 thư viện trên github" về?!!!

Hãy thêm 1 dòng trong [52000 dòng](https://github.com/facebook/create-react-app/blob/0a827f69ab0d2ee3871ba9b71350031d8a81b7ae/package-lock.json) dependencies của create-react-app...

## Kết luận
Vậy bạn sẽ mang gì đi khi chuyển sang công việc mới? 
Nếu là kinh nghiệm, hãy viết blog và chia sẻ ngay thôi.

Hết.

HVN at <http://pymi.vn> and <https://www.familug.org>.

[Ủng hộ tác giả 🍺](https://www.familug.org/p/ung-ho.html)
