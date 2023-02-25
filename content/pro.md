Title: [ProTips] làm IT chuyên nghiệp
Date: 2023-02-25
Category: frontpage
Tags: công việc, work, tips

Đi làm thì cơ bản cứ "chăm chỉ cố gắng" là sẽ thành công thôi, phải không?
Không!

Sau chục năm đi làm thuê cho các tập đoàn quốc tế lớn nhỏ (lên tới 1000+ người), sống sót qua các đợt layoff hàng ngàn người, leo lên đến chức ˜kỹ sư trưởng˜ (tech) lead, có rút ra một ít kinh nghiệm mau xướng như này.

### Dùng riêng máy tính cá nhân, không dùng máy công ty
Máy (laptop) công ty chỉ dùng cho duy nhất một mục đích: làm việc công ty. Kể cả đọc báo mạng lá cải cũng không!

Điều này có cực nhiều lợi ích:

- Nhỡ 1 ngày bị layoff, chỉ việc mang máy tính đi trả, không mất bất cứ thứ gì của cá nhân.
- Không lo nhầm lẫn các tài khoản cá nhân và công ty, không push nhầm code công ty lên public github
- Máy công ty thường được IT giới hạn các phần mềm, có chỗ còn không cho cắm USB
- Máy công ty cài sẵn nhiều thứ, cách tốt nhất là nghĩ máy này có keylog và tự chụp màn hình gửi đi (dù có thể ko phải thế). Tức bạn xem Facebook youtube đọc báo bao nhiêu lâu, công ty đều biết.

### Dùng riêng tài khoản cho công việc
Công ty nào cũng có và cấp riêng email, nhưng nhiều người vẫn dùng tài khoản github cá nhân (và các loại dịch vụ khác) cho công việc. Điều này tạo ra không ít rắc rối khi push nhầm, hay lúc chuyển việc. Vậy nên tốt nhất là tạo tài khoản riêng. Nếu tài khoản cá nhân là hvn thì tài khoản công ty là hvn-pymi hay hvn-familug hoặc chả liên quan như ho-ten-congty.

### Viết 1 trang brag trong công ty
Brag là 1 trang để khoe bạn đã làm được gì trong công ty. Đôi chỗ gọi là internal resume, để ở chế độ public để toàn công ty thấy. Có thể là 1 page trong wiki như Confluence hay Google Doc đều được.

Tài liệu này giúp:

- người khác (gồm cả quản lý các cấp) biết bạn đã cống hiến những gì
- tiện cho việc viết Performance Review hay promotion
- bạn không quên mình đã làm gì trong quý, năm nay/năm ngoái

Tham khảo <https://jvns.ca/blog/brag-documents/>

### Luôn bắt đầu công việc bằng 1 trang wiki hay Google doc
1 trang không cần quá nhiều chữ trình bày dự án (internal) này làm gì, tại sao, các phương án và lựa chọn. Không nhất thiết phải formal như <https://blog.pragmaticengineer.com/rfcs-and-design-docs/>, nhưng phục vụ việc sharing trong công ty nếu cần thiết.

Viết 1 trang doc cũng giúp người viết có được cái nhìn tổng quát hơn về vấn đề, thay vì chỉ code sẽ bị tập trung vào "low level".

### Làm thì tới chốn, phải có giao diện
Dù ghét frontend đến đâu, yêu dòng lệnh đến nhường nào, thì kết quả của 1 công việc, nếu không dễ dàng để "cấp trên" thấy, bạn sẽ ... không được thấy, thì không được thưởng, nên không được thăng chức.

5 mức độ hoàn thành công việc ứng với 5 mức lương tăng dần:

- SSH vào server, gõ 1 câu lệnh, xong việc
- Như trên, nhưng viết thêm tài liệu, tạo thành SoP (standard of procedure - hay có chỗ gọi là Runbook) xử lý vấn đề
- Viết 1 "automation" job, như Jenkins job hay GitHub workflow hay câu lệnh chat Slack để người dùng (thường là đồng nghiệp cùng team) chỉ việc nhập vào 1 vài input, ví dụ gõ 1 lệnh là sẽ tạo tài khoản cho user dev XYZ - đa phần, kể cả senior, dừng lại ở đây, vì Jenkins hay các tech-tool rất thân thuộc với họ.
- Tạo 1 trang web để người dùng (user dev XYZ) tự vào bấm vài nút hoặc nhập input và tự phục vụ (hay 1 chatbot), không cần tới mình cung cấp, hoặc cùng lắm mình chỉ cần bấm nút "cho phép". Một trang web có giao diện và tính năng do mình quyết định. Jenkins hay GitHub action chỉ có output là text đên trên nền trắng không màu.
- Viết báo cáo, lập bảng excel, vẽ đồ thị, tự động gửi mail báo cáo hàng tuần... tất nhiên không phải công việc nào cũng áp dụng, nhưng 1 devops biết Excel (hay pandas), vẽ đồ thị tổng hợp kết quả (hay metric Grafana) sẽ khác hẳn với 1 sysadmin chỉ copy paste output toàn text.

### Hạn chế chuyển việc nội bộ
Chuyển công ty thì thường được tăng lương, chứ chuyển việc nội bộ xin sang team khác thường là thảm họa. Vì team mới, mình lại là người mới, sếp mới cũng không biết tới, cũng chưa có gì nhiều. Kết quả review performance sẽ ít đẹp, ít thưởng.

Hết.

HVN at <http://pymi.vn> and <https://www.familug.org>.

[Ủng hộ tác giả 🍺](https://www.familug.org/p/ung-ho.html)
