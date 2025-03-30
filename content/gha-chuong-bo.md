Title: Điều gì tệ hơn "mất bò mới lo làm chuồng"
Date: 2025/03/30
Category: frontpage
Tags: github action, gha, security
Slug: gha-chuong-bo

Nửa tháng sau khi [GitHub action tj-actions/changed-file bị hack]({filename}/github-action-pinning.md), thế giới có gì thay đổi? 

Xưa các cụ có câu "mất bò mới lo làm chuồng", nhằm phê phán việc không quan tâm đến chuồng của con bò. Nhưng điều tệ hơn là gì? 

### mất bò xong vẫn không làm chuồng 
Trong ngành IT (hay việc gì cũng thế), thất bại là chỗ người ta rút kinh nhiệm để tiến bộ hơn, phát triển hơn hôm qua. Thôi thì qua đã mất bò thì làm chuồng để mai không mất nữa.
Nhưng như mọi "kinh nghiệm", nó không được học qua "chuyện kể"/"lời khuyên" mà chỉ thực sự thấm nếu đã phải trả giá. Internet vẫn tiếp tục dùng GitHub action không pinning tới SHA1 commit hash...

Blog FAMILUG do 1 phút lười biếng cũng dùng GHA `nelsonjchen/gh-pages-pelican-action@master`, để rồi hôm nay trả giá 30 phút [gỡ bỏ GHA](https://github.com/familug/familug.github.io/commit/e64e5b345379595003cd665efb70067a8a9333cf) này.
GHA build blog FAMILUG giờ chỉ còn dùng action chính thức của GitHub. Mà nếu GitHub bị hack... thì mọi lo lắng khác đều không có nghĩa lý gì khi blog familug.github.io chạy trên GitHub page.

Thêm 1 điều **thú vị** rằng: GHA  <https://github.com/nelsonjchen/gh-pages-pelican-action> cũng đã chuyển sang chế độ "archived" mà người dùng không hề hay biết:

>  This repository was archived by the owner on Mar 23, 2025. It is now read-only. 

### Kết luận
Cuối cùng cũng đã làm chuồng.

Hết.

HVN at <https://pymi.vn> and <https://www.familug.org>.

[Ủng hộ tác giả 🍺](https://www.familug.org/p/ung-ho.html)
